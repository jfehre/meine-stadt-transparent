from unittest import mock

from django.test import TestCase

from mainapp.tests.live.helper import MockMainappSearch


class TestRSS(TestCase):
    fixtures = ["initdata"]

    def test_paper_feed(self):
        response = self.client.get("/paper/feed/").content.decode()
        self.assertIn("<rss", response)
        self.assertIn("Latest papers", response)
        self.assertIn(
            '&lt;a href="/file/5/"&gt;Some obligatory cat content.&lt;/a&gt;', response
        )
        self.assertIn("Frank Underwood", response)

    @mock.patch(
        "mainapp.functions.search_tools.MainappSearch.execute",
        new=MockMainappSearch.execute,
    )
    def test_search_results(self):
        response = self.client.get("/search/query/complexity/feed/").content.decode()
        self.assertIn("<rss", response)
        self.assertIn("The latest search results", response)
        self.assertIn("File: Title", response)
        self.assertNotIn("Frank Underwood", response)