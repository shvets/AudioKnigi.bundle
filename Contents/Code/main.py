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
            key=Callback(HandleTracks, id=id, name=name, thumb=thumb, description=description),
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
            key=Callback(HandleLetterGroup, letter=letter, type='authors'),
            title=unicode(letter)
        ))

    return oc

@route(PREFIX + '/performers_letters')
def HandlePerformersLetters(title):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_performers_letters()

    for letter in response:
        oc.add(DirectoryObject(
            key=Callback(HandleLetterGroup, letter=letter, type='performers'),
            title=unicode(letter)
        ))

    return oc

@route(PREFIX + '/letter_group')
def HandleLetterGroup(letter, type):
    oc = ObjectContainer(title2=unicode(L(letter)))

    if type == 'authors':
        items = authors
    else:
        items = performers

    for group_name, group in items.iteritems():
        if group_name.find(letter) == 0:
            oc.add(DirectoryObject(
                key=Callback(HandleLetter, name=group_name, items=group),
                title=group_name
            ))

    return oc

@route(PREFIX + '/letter', items=list)
def HandleLetter(name, items):
    oc = ObjectContainer(title2=unicode(L(name)))

    for item in items:
        name = item['name']
        path = item['path']

        oc.add(DirectoryObject(
            key=Callback(HandleBooks, name=name, path=path),
            title=unicode(name)
        ))

    # pagination.append_controls(oc, response['pagination'], page=page, callback=HandleLetter, name=name)

    return oc

@route(PREFIX + '/books')
def HandleBooks(name, path, page=1):
    oc = ObjectContainer(title2=unicode(L(name)))

    response = service.get_books(path=path, page=page)

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

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleBooks, name=name, path=path)

    return oc

@route(PREFIX + '/performers')
def HandlePerformers(title, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_performers(page=page)

    for item in response['items']:
        name = item['name']
        url = item['path']

        oc.add(DirectoryObject(
            key=Callback(HandleBooks, url=url, name=name),
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
        path = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleGenre, title=name, path=path),
            title=unicode(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleGenres, title=title)

    return oc

@route(PREFIX + '/genre')
def HandleGenre(title, path, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_genre(path=path, page=page)

    for item in response['items']:
        name = item['name']
        id = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleTracks, id=id, name=name, thumb=thumb),
            title=unicode(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleGenre, title=title, path=path)

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
        duration = 100000
        thumb = str(params['thumb'])
        artist = params['name']

        new_params = {
            'type': 'track',
            'id': path,
            'name': name,
            'thumb': thumb,
            'artist': artist,
            'format': format,
            'bitrate': bitrate,
            'duration': duration
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

    if 'duration' in media_info:
        metadata["duration"] = media_info['duration']

    metadata_object = FlowBuilder.build_metadata_object(media_type=media_info['type'], title=media_info['name'])

    metadata_object.key = Callback(HandleTrack, container=True, **media_info)
    metadata_object.rating_key = unicode(media_info['name'])
    metadata_object.title = media_info['name']
    metadata_object.artist = media_info['name']
    metadata_object.thumb = media_info['thumb']

    if 'duration' in media_info:
        metadata_object.duration = int(media_info['duration'])

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
        return HandleAuthorBooks(**params)
    if type == 'performer':
        return HandlePerformerBooks(**params)
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

