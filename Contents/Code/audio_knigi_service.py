# -*- coding: utf-8 -*-

from http_service import HttpService

class AudioKnigiService(HttpService):
    URL = 'http://audioknigi.club'

    def available(self):
        return True

    def get_page_path(self, path, page=1):
        if page == 1:
            new_path = path
        else:
            new_path = '/index/page' + str(page) + '/'

        return new_path

    def get_audiobooks(self, page=1, per_page=12):
        data = []

        page_path = self.get_page_path('/', page)

        document = self.fetch_document(self.URL)

        items = document.xpath('//article')

        for item in items:
            name = item.find('header/h3/a').text
            href = item.find('header/h3/a').get('href')
            thumb = item.find('img').get('src')
            description = item.find('div[@class="topic-content text"]').text.strip()

            data.append({'name': name, 'path': href, 'thumb': thumb, 'description': description})

        pagination = self.extract_pagination_data(page_path, page=page, per_page=per_page)

        return {'books': data, 'pagination': pagination}

    def extract_pagination_data(self, path, page, per_page):
        page = int(page)
        per_page = int(per_page)

        document = self.fetch_document(self.URL + path)

        pages = 1

        pagination_root = document.xpath('//div[@class="paging"]')

        if pagination_root:
            pagination_block = pagination_root[0]

            items = pagination_block.xpath('ul/li')

            last_link = items[len(items) - 2].find('a').get('href')

            index = last_link.find('/index/page')

            pages = int(last_link[index+11:len(last_link)-1]) / per_page

        return {
            "page": page,
            "pages": pages,
            "has_previous": page > 1,
            "has_next": page < pages,
        }

    def get_audiobook(self, url):
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
            new_url = "http://audioknigi.club/rest/bid/" + book_id

            return self.to_json(self.http_request(new_url).read())

