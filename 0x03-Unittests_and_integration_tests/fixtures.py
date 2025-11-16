#!/usr/bin/env python3
"""
Fixture module for integration tests.
Contains payload samples used for mocking GitHub API.
"""

org_payload = {
    "login": "google",
    "id": 1342004,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjEzNDIwMDQ=",
    "url": "https://api.github.com/orgs/google",
    "repos_url": "https://api.github.com/orgs/google/repos",
    "events_url": "https://api.github.com/orgs/google/events",
    "hooks_url": "https://api.github.com/orgs/google/hooks",
    "issues_url": "https://api.github.com/orgs/google/issues",
    "members_url": "https://api.github.com/orgs/google/members{/member}",
    "public_members_url": "https://api.github.com/orgs/google/public_members{/member}",
    "avatar_url": "https://avatars.githubusercontent.com/u/1342004?v=4",
    "description": "Google Open Source",
}

repos_payload = [
    {
        "id": 1,
        "name": "repo1",
        "private": False,
        "license": {"key": "apache-2.0"},
    },
    {
        "id": 2,
        "name": "repo2",
        "private": False,
        "license": {"key": "other"},
    },
    {
        "id": 3,
        "name": "repo3",
        "private": False,
        "license": None,
    },
]

expected_repos = ["repo1", "repo2", "repo3"]

apache2_repos = ["repo1"]
