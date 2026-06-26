from domains.github.client import create_issue, get_repo_activity
from domains.github.schemas import (
    CreateIssueInput, CreateIssueOutput,
    RepoActivityInput, RepoActivityItem,
)
from shared.db import log_activity

def create_github_issue_tool(input: CreateIssueInput) -> CreateIssueOutput:
    """
    Creates a github issue inside a designated repo
    input: repo name, title, description
    output: issue number, url of the created issue
    """
    data = create_issue(input.repo, input.title, input.body)
    log_activity('github', 'created a issue')
    return CreateIssueOutput(
        issue_number=data["number"],
        url=data["html_url"]

    )

def get_repo_activity_tool(input: RepoActivityInput) -> list[RepoActivityItem]:
    """
    Gets the current activity inside a particular repo like commit, pull requests etc.
    input: repo name, per_page(activities per page), page(number of pages/activity sets)
    output: list of(activity type, creator of it, created at)
    """
    data = get_repo_activity(input.repo, input.per_page, input.page)
    return [
        RepoActivityItem(**item)
        for item in data
    ]