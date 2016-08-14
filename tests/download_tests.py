import os
import responses
import unittest
import re

from esridump.dumper import EsriDumper

class TestEsriDownload(unittest.TestCase):
    def setUp(self):
        self.responses = responses.RequestsMock()
        self.responses.start()

        self.fake_url = 'http://example.com'

    def tearDown(self):
        self.responses.stop()
        self.responses.reset()

    def add_fixture_response(self, url_re, file, method='POST'):
        with open(os.path.join('tests/fixtures', file), 'r') as f:
            self.responses.add(
                method=method,
                url=re.compile(url_re),
                body=f.read(),
                match_querystring=True,
            )

    def test_object_id_enumeration(self):
        self.add_fixture_response(
            '.*/\?f=json.*',
            'us-ca-carson/us-ca-carson-metadata.json',
            method='GET',
        )
        self.add_fixture_response(
            '.*returnCountOnly=true.*',
            'us-ca-carson/us-ca-carson-count-only.json',
            method='GET',
        )
        self.add_fixture_response(
            '.*returnIdsOnly=true.*',
            'us-ca-carson/us-ca-carson-ids-only.json',
            method='GET',
        )
        self.add_fixture_response(
            '.*query.*',
            'us-ca-carson/us-ca-carson-0.json',
            method='POST',
        )

        dump = EsriDumper(self.fake_url)
        data = dump.get_all()

        self.assertEqual(5, len(data))

    def test_statistics_pagination(self):
        self.add_fixture_response(
            '.*/\?f=json.*',
            'us-ms-madison/us-ms-madison-metadata.json',
            method='GET',
        )
        self.add_fixture_response(
            '.*returnCountOnly=true.*',
            'us-ms-madison/us-ms-madison-count-only.json',
            method='GET',
        )
        self.add_fixture_response(
            '.*outStatistics=.*',
            'us-ms-madison/us-ms-madison-outStatistics.json',
            method='GET',
        )
        self.add_fixture_response(
            '.*query.*',
            'us-ms-madison/us-ms-madison-0.json',
            method='POST',
        )

        dump = EsriDumper(self.fake_url)
        data = dump.get_all()

        self.assertEqual(1, len(data))

    def test_advanced_query_pagination(self):
        self.add_fixture_response(
            '.*/\?f=json.*',
            'us-esri-test/us-esri-test-metadata.json',
            method='GET',
        )
        self.add_fixture_response(
            '.*returnCountOnly=true.*',
            'us-esri-test/us-esri-test-count-only.json',
            method='GET',
        )
        self.add_fixture_response(
            '.*query.*',
            'us-esri-test/us-esri-test-0.json',
            method='POST',
        )

        dump = EsriDumper(self.fake_url)
        data = dump.get_all()

        self.assertEqual(838, len(data))

    def test_advanced_query_pagination_incorrect_outfield_name(self):
        self.add_fixture_response(
            '.*/\?f=json.*',
            'us-ca-tuolumne/us-ca-tuolumne-metadata.json',
            method='GET',
        )
        self.add_fixture_response(
            '.*returnCountOnly=true.*',
            'us-ca-tuolumne/us-ca-tuolumne-count-only.json',
            method='GET',
        )
        self.add_fixture_response(
            '.*outStatistics=.*',
            'us-ca-tuolumne/us-ca-tuolumne-statistics.json',
            method='GET',
        )
        self.add_fixture_response(
            '.*query.*',
            'us-ca-tuolumne/us-ca-tuolumne-0.json',
            method='POST',
        )

        dump = EsriDumper(self.fake_url)
        data = dump.get_all()

        self.assertEqual(15, len(data))

