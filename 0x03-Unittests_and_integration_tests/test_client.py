#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient methods"""


@parameterized.expand([
    ("google",),
    ("abc",)
])
@patch("client.get_json")  # must patch where it's used
def test_org(self, org_name, mock_get_json):
    expected_payload = {"login": org_name}
    mock_get_json.return_value = expected_payload

    client = GithubOrgClient(org_name)
    result = client.org  # access property, no parentheses

    self.assertEqual(result, expected_payload)
    mock_get_json.assert_called_once_with(
        f"https://api.github.com/orgs/{org_name}"
    )


if __name__ == "__main__":
    unittest.main()
