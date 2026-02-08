from github import Github, GithubException
from devmate.config import settings



def _client():
    if not settings.GITHUB_TOKEN:
        raise RuntimeError("GITHUB_TOKEN not set")
    return Github(settings.GITHUB_TOKEN)


def list_open_prs(repo: str):
    gh = _client()
    try:
        repo_obj = gh.get_repo(repo)
        prs = repo_obj.get_pulls(state="open")
        return [
            {
                "number": pr.number,
                "title": pr.title,
                "author": pr.user.login,
                "url": pr.html_url,
            }
            for pr in prs
        ]
    except GithubException as e:
        return {
            "error": f"GitHub error {e.status}: {e.data.get('message')}"
        }


def get_pr(repo: str, pr_number: int):
    gh = _client()
    repo = gh.get_repo(repo)
    pr = repo.get_pull(pr_number)

    return {
        "number": pr.number,
        "title": pr.title,
        "body": pr.body,
        "author": pr.user.login,
    }


def get_pr_comments(repo: str, pr_number: int):
    gh = _client()
    repo = gh.get_repo(repo)
    pr = repo.get_pull(pr_number)

    comments = pr.get_review_comments()
    return [
        {
            "path": c.path,
            "body": c.body,
            "author": c.user.login,
        }
        for c in comments
    ]



def list_pr_review_comments(repo: str, pr_number: int):
    gh = _client()
    try:
        repo_obj = gh.get_repo(repo)
        pr = repo_obj.get_pull(pr_number)
        comments = pr.get_review_comments()

        return [
            {
                "id": c.id,
                "path": c.path,
                "line": c.line,
                "body": c.body,
            }
            for c in comments
        ]
    except GithubException as e:
        return {"error": f"GitHub error {e.status}: {e.data.get('message')}"}
