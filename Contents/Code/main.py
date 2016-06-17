# -*- coding: utf-8 -*-

import urllib

import history
import pagination
import common_routes
from media_info import MediaInfo
from flow_builder import FlowBuilder

@route(PREFIX + '/new_books')
def HandleNewBooks(title, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_new_books(page=page)

    for item in response['books']:
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
def HandleBestBooks(title, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_best_books(page=page)

    for item in response['books']:
        name = item['name']
        id = item['path']
        thumb = item['thumb']
        description = item['description']

        oc.add(DirectoryObject(
            key=Callback(HandleTracks, id=id, name=name, thumb=thumb, description=description),
            title=unicode(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleBestBooks, title=title)

    return oc

@route(PREFIX + '/authors')
def HandleAuthors(title, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_authors(page=page)

    for item in response['authors']:
        name = item['name']
        id = item['path']

        oc.add(DirectoryObject(
            key=Callback(HandleAuthorBooks, id=id, name=name),
            title=unicode(name)
        ))

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleAuthors, title=title)

    return oc

@route(PREFIX + '/author_books')
def HandleAuthorBooks(title, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_author_books(page=page)

    for item in response['books']:
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

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleAuthorBooks, title=title)

    return oc

@route(PREFIX + '/performers')
def HandlePerformers(title, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_performers(page=page)

    for item in response['performers']:
        name = item['name']
        id = item['path']

        oc.add(DirectoryObject(
            key=Callback(HandlePerformerBooks, id=id, name=name),
            title=unicode(name)
        ))

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandlePerformers, title=title)

    return oc

@route(PREFIX + '/performer_books')
def HandlePerformerBooks(title, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_performer_books(page=page)

    for item in response['books']:
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

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandlePerformerBooks, title=title)

    return oc

@route(PREFIX + '/genres')
def HandleGenres(title, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_genres(page=page)

    for item in response['genres']:
        name = item['name']
        id = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleGenre, title=name, id=id),
            title=unicode(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleGenres, title=title)

    return oc

@route(PREFIX + '/genre')
def HandleGenre(title, id, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_genres(page=page)

    for item in response['genres']:
        name = item['name']
        id = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleTracks, id=id, name=name, thumb=thumb),
            title=unicode(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response['pagination'], page=page, callback=HandleGenres, title=title)

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
def HandleSearch(query=None):
    oc = ObjectContainer(title2=unicode(L('Search')))

    response = service.search(query=query)

    for movie in response:
        name = movie['name']
        path = movie['path']

        oc.add(DirectoryObject(
            key=Callback(HandleAuthor, id=path, name=name),
            title=unicode(name)
        ))

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

