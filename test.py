# test_manual.py (put at root, delete after testing)
from domains.github.client import create_issue, get_repo_activity

# Test read (safe, no side effects)
activity = get_repo_activity("Annoymous-VE96/MCP-Center")
print(activity)

# Test write (creates a REAL issue — use a test repo!)
issue = create_issue("Annoymous-VE96/MCP-Center", "Test issue", "Testing the MCP tool by Sandipan and Niloy")
print(issue)