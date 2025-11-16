#!/usr/bin/env python3
"""Module for testing client.GithubOrgClient
"""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests the GithubOrgClient class methods.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: MagicMock) -> None:
        """Tests that GithubOrgClient.org returns the correct value
           and that get_json is called once with the expected argument.
        """
        client = GithubOrgClient(org_name)
        client.org()
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self) -> None:
        """Tests that GithubOrgClient._public_repos_url returns the expected
           URL based on the mocked `org` property.
        """
        # Define a mock payload for the `org` property
        expected_url = "https://api.github.com/orgs/holbertonschool/repos"
        payload = {"repos_url": expected_url}

        # Patch `GithubOrgClient.org` property using a context manager
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("holbertonschool")
            # Test that the result of _public_repos_url is the expected one
            self.assertEqual(client._public_repos_url, expected_url)
            # Ensure the org property was accessed once
            mock_org.assert_called_once()

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_repos_payload(self, mock_public_repos_url: PropertyMock,
                           mock_get_json: MagicMock) -> None:
        """Tests that GithubOrgClient.repos_payload returns the expected
           JSON payload and that dependencies were called once.
        """
        # Define mock return values
        mock_public_repos_url.return_value = "https://mock-repos-url.com"
        mock_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = mock_payload

        client = GithubOrgClient("mockorg")
        result = client.repos_payload

        # Test that the result is what's expected from the mocked get_json
        self.assertEqual(result, mock_payload)

        # Test that the mocked property and get_json were called once
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("https://mock-repos-url.com")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": None}, "my_license", False),
        ({"license": {"key": "my_license"}, "name": "repo"}, "my_license", True),
    ])
    def test_has_license(self, repo: dict, license_key: str, expected: bool) -> None:
        """Tests the static method GithubOrgClient.has_license.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url: PropertyMock,
                          mock_get_json: MagicMock) -> None:
        """Tests GithubOrgClient.public_repos without license filtering.
        """
        # Mock return values for get_json (which is called by repos_payload)
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]
        mock_get_json.return_value = repos_payload

        # Mock _public_repos_url property (used by repos_payload)
        mock_public_repos_url.return_value = "https://mock-repos-url.com"

        client = GithubOrgClient("mockorg")
        expected_repos = ["repo1", "repo2", "repo3"]
        self.assertEqual(client.public_repos(), expected_repos)

        # Test that the mocked property and get_json were called once
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos_with_license(self, mock_public_repos_url: PropertyMock,
                                        mock_get_json: MagicMock) -> None:
        """Tests GithubOrgClient.public_repos with license filtering.
        """
        # Mock return values for get_json (which is called by repos_payload)
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
            {"name": "repo4", "license": None}
        ]
        mock_get_json.return_value = repos_payload

        # Mock _public_repos_url property (used by repos_payload)
        mock_public_repos_url.return_value = "https://mock-repos-url.com"

        client = GithubOrgClient("mockorg")
        # Test filtering for "mit" license
        expected_repos_mit = ["repo1", "repo3"]
        self.assertEqual(client.public_repos(license="mit"), expected_repos_mit)

        # Test filtering for "apache-2.0" license
        expected_repos_apache = ["repo2"]
        self.assertEqual(client.public_repos(license="apache-2.0"), expected_repos_apache)

        # Test that the mocked property and get_json were called once each
        # (It's called once in total for repos_payload due to memoization)
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Set up class method to mock external requests.get.
        """
        # Define the URLs we expect to be called
        org_url = "https://api.github.com/orgs/google"
        repos_url = cls.org_payload["repos_url"]

        # Define the side effect function for requests.get
        def side_effect(url):
            if url == org_url:
                mock_response = MagicMock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            elif url == repos_url:
                mock_response = MagicMock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response
            return None # Should not happen

        # Start the patcher for requests.get
        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class method to stop the patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Tests GithubOrgClient.public_repos without license filtering (integration).
        """
        client = GithubOrgClient("google")
        # The client uses the mocked responses set up in setUpClass
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.mock_get.assert_called()

    def test_public_repos_with_license(self) -> None:
        """Tests GithubOrgClient.public_repos with license filtering (integration).
        """
        client = GithubOrgClient("google")
        # The client uses the mocked responses set up in setUpClass
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
        self.mock_get.assert_called()