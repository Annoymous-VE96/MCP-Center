"""
mcp_chat_client.py

REUSABLE TEMPLATE — works with ANY MCP server and ANY set of tools.
Nothing here is hardcoded to GitHub/Discord/etc. — tools are discovered
live from your server at startup.

WHAT IT DOES, IN ORDER:
  1. Launch your MCP server, ask it "what tools do you have?"
  2. Convert those tool definitions into the format Groq's API understands.
  3. Loop: you type something -> Groq decides if a tool is needed
     -> if yes, the REAL tool runs via MCP -> result goes back to Groq
     -> Groq replies in plain English.

WHAT YOU'LL SEE PRINTED, PER TURN:
  [TOOL CALL]   <tool name>      <- which tool Groq picked
  [ARGS]        {...}            <- what arguments it extracted from your prompt
  [RAW RESULT]  {...}            <- the actual data your tool function returned
  [ASSISTANT]   <text>           <- Groq's final natural-language reply

Run (from project root):
    python clients/mcp_chat_client.py
"""

import asyncio
import json
import os
import pathlib

from dotenv import load_dotenv
load_dotenv()

from groq import Groq
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ============================================================
# CONFIG — the only section you'd ever need to touch
# ============================================================
GROQ_MODEL = "llama-3.3-70b-versatile"
SERVER_SCRIPT = str(pathlib.Path(__file__).parent.parent / "server.py")
SYSTEM_PROMPT = "You are a helpful ops assistant talk with the user. Use the available tools when needed."


# ============================================================
# MCP <-> Groq translation (generic — do not need to edit)
# ============================================================

def mcp_tools_to_groq_format(mcp_tools: list) -> list[dict]:
    """Convert MCP tool definitions into Groq's expected JSON schema list."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.inputSchema,
            },
        }
        for tool in mcp_tools
    ]


async def execute_tool_call(session: ClientSession, tool_name: str, tool_args: dict) -> str:
    """Run a tool call against the live MCP server and return its result as text."""
    result = await session.call_tool(tool_name, arguments=tool_args)
    return "".join(block.text for block in result.content if hasattr(block, "text"))


def ask_groq(client: Groq, messages: list, tools: list):
    """One call to Groq with the current conversation + tool definitions."""
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    return response.choices[0].message


# ============================================================
# Chat loop
# ============================================================

async def run_chat():
    groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
    server_params = StdioServerParameters(command="python", args=[SERVER_SCRIPT])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            mcp_tools = (await session.list_tools()).tools
            groq_tools = mcp_tools_to_groq_format(mcp_tools)

            print(f"[READY] {len(groq_tools)} tools loaded: {[t.name for t in mcp_tools]}")
            print("[READY] Type your request, or 'exit' to quit.\n")

            messages = [{"role": "system", "content": SYSTEM_PROMPT}]

            while True:
                user_input = input("You: ").strip()
                if user_input.lower() in ("exit", "quit"):
                    break

                messages.append({"role": "user", "content": user_input})
                reply = ask_groq(groq_client, messages, groq_tools)

                # --- Case 1: no tool needed, plain answer ---
                if not reply.tool_calls:
                    print(f"[ASSISTANT] {reply.content}\n")
                    messages.append({"role": "assistant", "content": reply.content})
                    continue

                # --- Case 2: one or more tool calls requested ---
                messages.append({
                    "role": "assistant",
                    "content": reply.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                        }
                        for tc in reply.tool_calls
                    ],
                })

                for tc in reply.tool_calls:
                    tool_name = tc.function.name
                    tool_args = json.loads(tc.function.arguments)

                    print(f"[TOOL CALL]  {tool_name}")
                    print(f"[ARGS]       {tool_args}")

                    result_text = await execute_tool_call(session, tool_name, tool_args)
                    print(f"[RAW RESULT] {result_text}")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result_text,
                    })

                # Feed tool result(s) back to Groq for the final natural-language reply
                final_reply = ask_groq(groq_client, messages, groq_tools)
                print(f"[ASSISTANT]  {final_reply.content}\n")
                messages.append({"role": "assistant", "content": final_reply.content})


if __name__ == "__main__":
    asyncio.run(run_chat())