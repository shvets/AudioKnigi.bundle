# -*- coding: utf-8 -*-

from http_service import HttpService

# http://audioknigi.club/index/views/?period=7
# http://audioknigi.club/index/views/?period=30
# http://audioknigi.club/index/views/?period=all
# POST http://audioknigi.club/authors/ajax-search/
# topic_author_text:Б
# isPrefix:1
# security_ls_key:592d84b7ba51106f38c5861139e8e420
# http://audioknigi.club/search/books/?q=%D0%BF%D1%80%D0%B0%D1%82%D1%87%D0%B5%D1%82%D1%82
# q:пратчетт

class AudioKnigiService(HttpService):
    URL = 'http://audioknigi.club'

    def available(self):
        return True

    def get_page_path(self, path, page=1):
        return path + "page" + str(page) + "/"

    def get_new_books(self, page=1):
        return self.get_books(url=self.URL+'/index/', page=page)

    def get_books(self, url, page=1):
        data = []

        page_path = self.get_page_path(url + '/', page)

        document = self.fetch_document(page_path, encoding='utf-8')

        items = document.xpath('//article')

        for item in items:
            name = item.find('header/h3/a').text
            href = item.find('header/h3/a').get('href')
            thumb = item.find('img').get('src')
            description = item.find('div[@class="topic-content text"]').text.strip()

            data.append({'name': name, 'path': href, 'thumb': thumb, 'description': description})

        pagination = self.extract_pagination_data(document, page=page)

        return {'items': data, 'pagination': pagination}

    def get_best_books(self, page=1):
        data = []

        page_path = self.get_page_path('/', page)

        document = self.fetch_document(self.URL + page_path, encoding='utf-8')

        items = document.xpath('//article')

        for item in items:
            name = item.find('header/h3/a').text
            href = item.find('header/h3/a').get('href')
            thumb = item.find('img').get('src')
            description = item.find('div[@class="topic-content text"]').text.strip()

            data.append({'name': name, 'path': href, 'thumb': thumb, 'description': description})

        pagination = self.extract_pagination_data(document, page=page)

        return {'items': data, 'pagination': pagination}

    def get_authors(self, page=1):
        data = []

        page_path = self.get_page_path('/authors/', page)

        document = self.fetch_document(self.URL + page_path, encoding='utf-8')

        items = document.xpath('//td[@class="cell-name"]')

        for item in items:
            link = item.find('h4/a')
            name = link.text
            href = link.get('href')

            data.append({'name': name, 'path': href})

        pagination = self.extract_pagination_data(document, page=page)

        return {'items': data, 'pagination': pagination}

    def get_performers(self, page=1):
        data = []

        page_path = self.get_page_path('/performers/', page)

        document = self.fetch_document(self.URL + page_path, encoding='utf-8')

        items = document.xpath('//td[@class="cell-name"]')

        for item in items:
            link = item.find('h4/a')
            name = link.text
            href = link.get('href')

            data.append({'name': name, 'path': href})

        pagination = self.extract_pagination_data(document, page=page)

        return {'items': data, 'pagination': pagination}

    def get_genres(self, page=1):
        data = []

        page_path = self.get_page_path('/sections/', page)

        document = self.fetch_document(self.URL + page_path, encoding='utf-8')

        items = document.xpath('//td[@class="cell-name"]')

        for item in items:
            link = item.find('a')
            name = item.find('h4/a').text
            href = link.get('href')
            thumb = link.find('img').get('src')

            data.append({'name': name, 'path': href, 'thumb': thumb})

        pagination = self.extract_pagination_data(document, page=page)

        return {'items': data, 'pagination': pagination}

    def extract_pagination_data(self, document, page):
        page = int(page)

        pages = 1

        pagination_root = document.xpath('//div[@class="paging"]')

        if pagination_root:
            pagination_block = pagination_root[0]

            items = pagination_block.xpath('ul/li')

            last_link = items[len(items) - 2].find('a')

            if not last_link:
                last_link = items[len(items) - 3].find('a')

                pages = int(last_link.text)
            else:
                href = last_link.get('href')

                pattern = path + 'page'

                index1 = href.find(pattern)
                index2 = href.find('/?')

                # len(last_link)-1]

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
            new_url = "http://audioknigi.club/rest/bid/" + book_id

            return self.to_json(self.http_request(new_url).read())

