import library_bridge

Log = library_bridge.bridge.objects['Log']

from urllib import quote

@route(PREFIX + '/play_audio')
def PlayAudio(url):
    Log(url)
    Log(type(url))
    url = 'http://get.sweetbook.net/b/40274/wgqlV2BFSDkEDvynFKrdQT5pgpz7GrRugCbe3txVOes,/12_Vyzhit za bortom.mp3'

    return Redirect(url)
