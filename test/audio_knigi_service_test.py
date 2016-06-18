# -*- coding: utf-8 -*-

import test_helper

import unittest
import json

from audio_knigi_service import AudioKnigiService

class AudioKnigiServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = AudioKnigiService()

    def test_get_new_books(self):
        result = self.service.get_new_books()

        print(json.dumps(result, indent=4))

    def test_get_best_books_by_week(self):
        result = self.service.get_best_books(period='7')

        print(json.dumps(result, indent=4))

    def test_get_best_books_by_month(self):
        result = self.service.get_best_books(period='30')

        print(json.dumps(result, indent=4))

    def test_get_best_books_by_all(self):
        result = self.service.get_best_books(period='all')

        print(json.dumps(result, indent=4))

    def test_get_author_books(self):
        result = self.service.get_authors()

        path = result['items'][0]['path']

        result = self.service.get_books(path)

        print(json.dumps(result, indent=4))

    def test_get_performer_books(self):
        result = self.service.get_performers()

        path = result['items'][0]['path']

        result = self.service.get_books(path)

        print(json.dumps(result, indent=4))

    def test_get_authors(self):
        result = self.service.get_authors()

        print(json.dumps(result, indent=4))

    def test_get_performers(self):
        result = self.service.get_performers()

        print(json.dumps(result, indent=4))

    def test_get_genres(self):
        result = self.service.get_genres(page=1)

        print(json.dumps(result, indent=4))

        result = self.service.get_genres(page=2)

        print(json.dumps(result, indent=4))

    def test_pagination(self):
        result = self.service.get_new_books(page=1)

        print(json.dumps(result, indent=4))

        pagination = result['pagination']

        self.assertEqual(pagination['has_next'], True)
        self.assertEqual(pagination['has_previous'], False)
        self.assertEqual(pagination['page'], 1)

        result = self.service.get_new_books(page=2)

        print(json.dumps(result, indent=4))

        pagination = result['pagination']

        self.assertEqual(pagination['has_next'], True)
        self.assertEqual(pagination['has_previous'], True)
        self.assertEqual(pagination['page'], 2)

    def test_get_audio_tracks(self):
        path = "http://audioknigi.club/alekseev-gleb-povesti-i-rasskazy"

        result = self.service.get_audio_tracks(path)

        print(json.dumps(result, indent=4))

if __name__ == '__main__':
    unittest.main()
