# -*- coding: utf-8 -*-

import test_helper

import unittest
import json

from audio_knigi_service import AudioKnigiService

class AudioKnigiServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = AudioKnigiService()

    def test_get_audiobooks(self):
        result = self.service.get_audiobooks()

        print(json.dumps(result, indent=4))

    def test_pagination(self):
        result = self.service.get_audiobooks(page=1)

        pagination = result['pagination']

        self.assertEqual(pagination['has_next'], True)
        self.assertEqual(pagination['has_previous'], False)
        self.assertEqual(pagination['page'], 1)

        result = self.service.get_audiobooks(page=2)

        pagination = result['pagination']

        self.assertEqual(pagination['has_next'], True)
        self.assertEqual(pagination['has_previous'], True)
        self.assertEqual(pagination['page'], 2)

    def test_get_audiobook(self):
        path = "http://audioknigi.club/alekseev-gleb-povesti-i-rasskazy"

        result = self.service.get_audiobook(path)

        print(json.dumps(result, indent=4))

if __name__ == '__main__':
    unittest.main()
