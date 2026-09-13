import requests

def analyze_github(username: str) -> dict:
    if not username:
        return {"summary": ""}

    try:
        user = requests.get(
            f"https://api.github.com/users/{username}",
            timeout=8
        ).json()

        repos = requests.get(
            f"https://api.github.com/users/{username}/repos?per_page=30&sort=updated",
            timeout=8
        ).json()

        if not isinstance(repos, list):
            repos = []

        languages = []
        repo_names = []

        for repo in repos:
            if repo.get("name"):
                repo_names.append(repo["name"])
            if repo.get("language"):
                languages.append(repo["language"])

        unique_languages = sorted(set(languages))
        summary = (
            f"GitHub profile: {user.get('public_repos', 0)} public repositories. "
            f"Main detected languages: {', '.join(unique_languages) or 'not available'}. "
            f"Recent repositories: {', '.join(repo_names[:8]) or 'none'}."
        )

        return {"summary": summary}

    except Exception:
        return {"summary": "GitHub analysis unavailable."}
