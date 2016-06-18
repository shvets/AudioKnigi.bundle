# -*- coding: utf-8 -*-

import urllib

from http_service import HttpService

# POST http://audioknigi.club/authors/ajax-search/
# topic_author_text:Б
# isPrefix:1
# security_ls_key:592d84b7ba51106f38c5861139e8e420

class AudioKnigiService(HttpService):
    URL = 'http://audioknigi.club'

    def available(self):
        return True

    def get_page_path(self, path, page=1):
        return path + "page" + str(page) + "/"

    def get_new_books(self, page=1):
        return self.get_books(path='/index/', page=page)

    def get_best_books(self, period, page=1):
        return self.get_books(path='/index/views/', period=period, page=page)

    def get_books(self, path, period=None, page=1):
        data = []

        page_path = self.get_page_path(path + '/', page)

        if period:
            page_path = page_path + "?period=" + period

        document = self.fetch_document(self.URL + page_path, encoding='utf-8')

        items = document.xpath('//article')

        for item in items:
            name = item.find('header/h3/a').text
            href = item.find('header/h3/a').get('href')
            thumb = item.find('img').get('src')
            description = item.find('div[@class="topic-content text"]').text.strip()

            data.append({'name': name, 'path': href, 'thumb': thumb, 'description': description})

        pagination = self.extract_pagination_data(document, path=path, page=page)

        return {'items': data, 'pagination': pagination}

    def get_authors(self, page=1):
        return self.get_collection('/authors/', page=page)

    def get_performers(self, page=1):
        return self.get_collection('/performers/', page=page)

    def get_collection(self, path, page=1):
        data = []

        page_path = self.get_page_path(path, page)

        document = self.fetch_document(self.URL + page_path, encoding='utf-8')

        items = document.xpath('//td[@class="cell-name"]')

        for item in items:
            link = item.find('h4/a')
            name = link.text
            href = link.get('href')[len(self.URL):] + '/'

            data.append({'name': name, 'path': href})

        pagination = self.extract_pagination_data(document, path=path, page=page)

        return {'items': data, 'pagination': pagination}

    def get_genres(self, page=1):
        data = []

        path = '/sections/'

        page_path = self.get_page_path(path, page)

        document = self.fetch_document(self.URL + page_path, encoding='utf-8')

        items = document.xpath('//td[@class="cell-name"]')

        for item in items:
            link = item.find('a')
            name = item.find('h4/a').text
            href = link.get('href')
            thumb = link.find('img').get('src')

            data.append({'name': name, 'path': href, 'thumb': thumb})

        pagination = self.extract_pagination_data(document, path=path, page=page)

        return {'items': data, 'pagination': pagination}

    def extract_pagination_data(self, document, path, page):
        page = int(page)

        pages = 1

        pagination_root = document.xpath('//div[@class="paging"]')

        if pagination_root:
            pagination_block = pagination_root[0]

            items = pagination_block.xpath('ul/li')

            last_link = items[len(items) - 2].find('a')

            if last_link is None:
                last_link = items[len(items) - 3].find('a')

                pages = int(last_link.text)
            else:
                href = last_link.get('href')

                pattern = urllib.unquote(path).decode('utf-8') + 'page'

                index1 = href.find(pattern)
                index2 = href.find('/?')

                if index2 == -1:
                    index2 = len(href)-1

                pages = int(href[index1+len(pattern):index2])

        return {
            "page": page,
            "pages": pages,
            "has_previous": page > 1,
            "has_next": page < pages,
        }

    def get_audio_tracks(self, url):
        book_id = None

        document = self.fetch_document(url)

        scripts = document.xpath('//script[@type="text/javascript"]')

        for script in scripts:
            script_body = script.text_content()

            index = script_body.find('$(document).audioPlayer')

            if index >= 0:
                book_id = script_body[28:script_body.find(',')]
                break

        if book_id:
            new_url = self.URL + "/rest/bid/" + book_id

            return self.to_json(self.http_request(new_url).read())

    def search(self, query, page=1):
        path = '/search/books/'

        url = self.URL + path

        content = self.http_request(url, data={'q': query}).read()

        document = self.to_document(content, encoding='utf-8')

        data = []

        items = document.xpath('//article')

        for item in items:
            name = item.find('header/h3/a').text
            href = item.find('header/h3/a').get('href')
            thumb = item.find('img').get('src')
            description = item.find('div[@class="topic-content text"]').text.strip()

            data.append({'name': name, 'path': href, 'thumb': thumb, 'description': description})

        pagination = self.extract_pagination_data(document, path=path, page=page)

        return {'items': data, 'pagination': pagination}