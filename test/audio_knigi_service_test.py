# -*- coding: utf-8 -*-

import test_helper

import unittest
import json

from audio_knigi_service import AudioKnigiService

class AudioKnigiServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = AudioKnigiService()

    def test_get_authors_letters(self):
        result = self.service.get_authors_letters()

        print(json.dumps(result, indent=4))

    def test_get_performers_letters(self):
        result = self.service.get_performers_letters()

        print(json.dumps(result, indent=4))

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

    def test_get_genre(self):
        genres = self.service.get_genres(page=1)

        path = genres['items'][0]['path']

        result = self.service.get_genre(path=path)

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

    def test_search(self):
        query = 'пратчетт'

        result = self.service.search(query)

        print(json.dumps(result, indent=4))

    # def test_search_by_letter(self):
    #     letter = 'Б'
    #
    #     result = self.service.search_by_letter(letter)
    #
    #     print(json.dumps(result, indent=4))

    def test_generate_authors_list(self):
        result = self.service.generate_authors_list('authors.json')

        print(json.dumps(result, indent=4))

    def test_grouping(self):
        authors = None

        with open("../Contents/authors.json", 'r') as file:
            authors = json.load(file)

        authors = self.service.group_items_by_letter(authors)

        print(json.dumps(authors, indent=4))

    # def test_songdetails(self):
    #     #file = "/Users/alex/01_Vyzhit za bortom.mp3"
    #     #file = "/Users/alex/01.mp3"
    #     url = "http://get.sweetbook.net/b/40239/tNwhpJACpgfIYnXlBL8nMSTTrZa_bO8IJdteJ85W1OI,/01 - \u041c\u0430\u0440\u0438\u044f \u0413\u0430\u043c\u0438\u043b\u044c\u0442\u043e\u043d (\u0427\u0438\u0442\u0430\u0435\u0442 \u0415\u0433\u043e\u0440 \u0421\u0435\u0440\u043e\u0432)/01.mp3"
    #     #
    #     # file = self.service.http_request(url)
    #
    #     #
    #     # id3info = ID3(file)
    #     #
    #     # print id3info
    #
    #     # import songdetails
    #     #
    #     # song = songdetails.scan(file)
    #     #
    #     # if song is not None:
    #     #     print song.duration
    #
    #     import id3reader
    #
    #     # Construct a reader from a file or filename.
    #     id3r = id3reader.Reader(file)
    #
    #     # Ask the reader for ID3 values:
    #     print id3r.getValue('TLEN')
    #
    #     print float(id3r.getValue('TLEN')) / 60 / 1000

if __name__ == '__main__':
    unittest.main()
