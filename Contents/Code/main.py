# -*- coding: utf-8 -*-

import urllib
import json

import history
import pagination
import common_routes
from media_info import MediaInfo
from flow_builder import FlowBuilder

authors_file_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'authors.json'))
authors = json.loads(Core.storage.load(authors_file_name))
authors = service.group_items_by_letter(authors)

performers_file_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'performers.json'))
performers = json.loads(Core.storage.load(performers_file_name))
performers = service.group_items_by_letter(performers)

@route(PREFIX + '/new_books')
def HandleNewBooks(title, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_new_books(page=page)

    for item in response['items']:
        name = item['name']
        id = item['path']
        thumb = item['thumb']
        description = item['description']

        new_params = {
            'type': 'tracks',
            'id': id,
            'name': name,
            'thumb': thumb,
            # 'artist': author,
            'content': description,
            # 'rating': rating
        }
        oc.add(DirectoryObject(
            key=Callback(HandleTracks, **new_params),
            title=unicode(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleNewBooks, title=title)

    return oc

@route(PREFIX + '/best_books')
def HandleBestBooks(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    oc.add(DirectoryObject(
        key=Callback(HandleBestBooksByPeriod, title=unicode(L("By Week")), period='7'),
        title=unicode(L("By Week"))
    ))

    oc.add(DirectoryObject(
        key=Callback(HandleBestBooksByPeriod, title=unicode(L("By Month")), period='30'),
        title=unicode(L("By Month"))
    ))

    oc.add(DirectoryObject(
        key=Callback(HandleBestBooksByPeriod, title=unicode(L("All Time")), period='all'),
        title=unicode(L("All Time"))
    ))

    return oc

@route(PREFIX + '/best_books_by_period')
def HandleBestBooksByPeriod(title, period, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_best_books(period=period, page=page)

    for item in response['items']:
        name = item['name']
        id = item['path']
        thumb = item['thumb']
        description = item['description']

        oc.add(DirectoryObject(
            key=Callback(HandleTracks, type='tracks', id=id, name=name, thumb=thumb, description=description),
            title=unicode(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleBestBooksByPeriod, title=title, period=period)

    return oc

@route(PREFIX + '/authors_letters')
def HandleAuthorsLetters(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_authors_letters()

    for letter in response:
        oc.add(DirectoryObject(
            key=Callback(HandleAuthorsLetterGroup, letter=letter),
            title=unicode(letter)
        ))

    return oc

@route(PREFIX + '/performers_letters')
def HandlePerformersLetters(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_performers_letters()

    for letter in response:
        oc.add(DirectoryObject(
            key=Callback(HandlePerformersLetterGroup, letter=letter),
            title=unicode(letter)
        ))

    return oc

@route(PREFIX + '/authors_letter_group')
def HandleAuthorsLetterGroup(letter, page=1):
    oc = ObjectContainer(title2=unicode(L(letter)))

    if letter == "Все":
        response = service.get_authors(page=page)

        for item in response['items']:
            name = item['name']
            url = item['path']

            oc.add(DirectoryObject(
                key=Callback(HandleAuthor, type='author', url=url, name=name),
                title=unicode(name)
            ))

        pagination.append_controls(oc, response['pagination'], page=page, callback=HandleAuthorsLetterGroup, letter=letter)
    else:
        for group_name, group in authors.iteritems():
            if group_name.find(letter) == 0:
                oc.add(DirectoryObject(
                    key=Callback(HandleAuthorsLetter, name=group_name, items=group),
                    title=group_name
                ))

    return oc


@route(PREFIX + '/performers_letter_group')
def HandlePerformersLetterGroup(letter, page=1):
    oc = ObjectContainer(title2=unicode(L(letter)))

    if letter == "Все":
        response = service.get_performers(page=page)

        for item in response['items']:
            name = item['name']
            url = item['path']

            oc.add(DirectoryObject(
                key=Callback(HandlePerformer, type='performer', url=url, name=name),
                title=unicode(name)
            ))

        pagination.append_controls(oc, response['pagination'], page=page, callback=HandlePerformersLetterGroup, letter=letter)
    else:
        for group_name, group in performers.iteritems():
            if group_name.find(letter) == 0:
                oc.add(DirectoryObject(
                    key=Callback(HandlePerformersLetter, name=group_name, items=group),
                    title=group_name
                ))

    return oc

@route(PREFIX + '/authors_letter', items=list)
def HandleAuthorsLetter(name, items):
    oc = ObjectContainer(title2=unicode(L(name)))

    for item in items:
        name = item['name']
        id = item['path']

        oc.add(DirectoryObject(
            key=Callback(HandleAuthor, type='author', name=name, id=id),
            title=unicode(name)
        ))

    return oc

@route(PREFIX + '/performers_letter', items=list)
def HandlePerformersLetter(name, items):
    oc = ObjectContainer(title2=unicode(L(name)))

    for item in items:
        name = item['name']
        id = item['path']

        oc.add(DirectoryObject(
            key=Callback(HandlePerformer, type='performer', name=name, id=id),
            title=unicode(name)
        ))

    return oc

@route(PREFIX + '/author')
def HandleAuthor(operation=None, **params):
    oc = ObjectContainer(title2=unicode(L(params['name'])))

    media_info = MediaInfo(**params)

    service.queue.handle_bookmark_operation(operation, media_info)

    oc.add(DirectoryObject(
        key=Callback(HandleBooks, **params),
        title=unicode(params['name']),
    ))

    service.queue.append_bookmark_controls(oc, HandleAuthor, media_info)

    return oc

@route(PREFIX + '/performer')
def HandlePerformer(operation=None, **params):
    oc = ObjectContainer(title2=unicode(L(params['name'])))

    media_info = MediaInfo(**params)

    service.queue.handle_bookmark_operation(operation, media_info)

    oc.add(DirectoryObject(
        key=Callback(HandleBooks, **params),
        title=unicode(params['name']),
    ))

    service.queue.append_bookmark_controls(oc, HandlePerformer, media_info)

    return oc

@route(PREFIX + '/books')
def HandleBooks(page=1, **params):
    oc = ObjectContainer(title2=unicode(L(params['name'])))

    response = service.get_books(path=params['id'], page=page)

    for item in response['items']:
        name = item['name']
        id = item['path']
        thumb = item['thumb']
        description = item['description']

        new_params = {
            'type': 'tracks',
            'id': id,
            'name': name,
            'thumb': thumb,
            # 'artist': author,
            'content': description,
            # 'rating': rating
        }
        oc.add(DirectoryObject(
            key=Callback(HandleTracks, **new_params),
            title=unicode(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleBooks, name=params['name'], id=params['id'])

    return oc

@route(PREFIX + '/performers')
def HandlePerformers(title, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_performers(page=page)

    for item in response['items']:
        name = item['name']
        url = item['path']

        oc.add(DirectoryObject(
            key=Callback(HandlePerformer, url=url, name=name),
            title=unicode(name)
        ))

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandlePerformers, title=title)

    return oc

@route(PREFIX + '/genres')
def HandleGenres(title, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_genres(page=page)

    for item in response['items']:
        name = item['name']
        id = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleGenre, type='genre', name=name, id=id),
            title=unicode(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleGenres, title=title)

    return oc

@route(PREFIX + '/genre')
def HandleGenre(operation=None, page=1, **params):
    oc = ObjectContainer(title2=unicode(L(params['name'])))

    media_info = MediaInfo(**params)

    service.queue.handle_bookmark_operation(operation, media_info)

    Log(params)

    response = service.get_genre(path=params['id'], page=page)

    for item in response['items']:
        name = item['name']
        id = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleTracks, type='tracks', id=id, name=name, thumb=thumb),
            title=unicode(name),
            thumb=thumb
        ))

    service.queue.append_bookmark_controls(oc, HandleGenre, media_info)

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleGenre, name=params['name'], id=params['id'])

    return oc

@route(PREFIX + '/tracks')
def HandleTracks(operation=None, container=False, **params):
    media_info = MediaInfo(**params)

    service.queue.handle_bookmark_operation(operation, media_info)

    oc = ObjectContainer(title2=unicode(L(params['name'])))

    response = service.get_audio_tracks(params['id'])

    for index, item in enumerate(response):
        #name = "Part " + str(index+1)
        name = str(item['title'])
        path = str(item['mp3'])

        format = 'mp3'
        bitrate = 0
        #duration = item['duration']
        # duration = 30 * 60 * 1000
        thumb = str(params['thumb'])
        artist = params['name']

        new_params = {
            'type': 'track',
            'id': path,
            'name': name,
            'thumb': thumb,
            'artist': artist,
            'format': format,
            'bitrate': bitrate
        }

        oc.add(HandleTrack(**new_params))

    if str(container) == 'False':
        history.push_to_history(Data, media_info)
        service.queue.append_bookmark_controls(oc, HandleTracks, media_info)

    return oc

@route(PREFIX + '/track')
def HandleTrack(container=False, **params):
    media_info = MediaInfo(**params)

    url = media_info['id']

    url = urllib.unquote_plus(url)

    if 'm4a' in media_info['format']:
        format = 'm4a'
    else:
        format = 'mp3'

    metadata = FlowBuilder.get_metadata(format)

    if 'bitrate' in media_info:
        metadata["bitrate"] = media_info['bitrate']

    metadata_object = FlowBuilder.build_metadata_object(media_type=media_info['type'], title=media_info['name'])

    metadata_object.key = Callback(HandleTrack, container=True, **media_info)
    metadata_object.rating_key = unicode(media_info['name'])
    metadata_object.title = media_info['name']
    metadata_object.artist = media_info['name']
    metadata_object.thumb = media_info['thumb']

    if 'artist' in media_info:
        metadata_object.artist = media_info['artist']

    media_object = FlowBuilder.build_media_object(Callback(common_routes.PlayAudio, url=url), metadata)

    metadata_object.items.append(media_object)

    if container:
        oc = ObjectContainer(title2=unicode(media_info['name']))

        oc.add(metadata_object)

        return oc
    else:
        return metadata_object

@route(PREFIX + '/container')
def HandleContainer(**params):
    type = params['type']

    if type == 'author':
        return HandleAuthor(**params)
    elif type == 'performer':
        return HandlePerformer(**params)
    elif type == 'genre':
        return HandleGenre(**params)
    elif type == 'tracks':
        return HandleTracks(**params)

@route(PREFIX + '/search')
def HandleSearch(query, page=1):
    oc = ObjectContainer(title2=unicode(L('Search')))

    response = service.search(query=query, page=page)

    for item in response['items']:
        name = item['name']
        id = item['path']
        thumb = item['thumb']
        description = item['description']

        new_params = {
            'type': 'tracks',
            'id': id,
            'name': name,
            'thumb': thumb,
            # 'artist': author,
            'content': description,
            # 'rating': rating
        }
        oc.add(DirectoryObject(
            key=Callback(HandleTracks, **new_params),
            title=unicode(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleSearch, query=query)

    return oc

@route(PREFIX + '/queue')
def HandleQueue():
    oc = ObjectContainer(title2=unicode(L('Queue')))

    service.queue.handle_queue_items(oc, HandleContainer, service.queue.data)

    if len(service.queue.data) > 0:
        oc.add(DirectoryObject(
            key=Callback(ClearQueue),
            title=unicode(L("Clear Queue"))
        ))

    return oc

@route(PREFIX + '/clear_queue')
def ClearQueue():
    service.queue.clear()

    return HandleQueue()

@route(PREFIX + '/history')
def HandleHistory():
    history_object = history.load_history(Data)

    oc = ObjectContainer(title2=unicode(L('History')))

    if history_object:
        data = sorted(history_object.values(), key=lambda k: k['time'], reverse=True)

        service.queue.handle_queue_items(oc, HandleContainer, data)

    return oc

