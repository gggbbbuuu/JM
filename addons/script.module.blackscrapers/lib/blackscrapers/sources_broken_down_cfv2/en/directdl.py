# -*- coding: utf-8 -*-

'''
    Covenant Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib,urlparse,json,base64

from blackscrapers.modules import cleantitle
from blackscrapers.modules import client
from blackscrapers.modules import debrid
from blackscrapers.modules import log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['directdownload.tv']
        self.base_link = 'https://directdownload.tv'
        self.search_link = base64.b64decode('L2FwaT9rZXk9NEIwQkI4NjJGMjRDOEEyOSZrZXl3b3JkPQ==')
        self.b_link = 'aHR0cDovL2lwdjYuaWNlZmlsbXMuaW5mbw=='
        self.u_link = 'aHR0cDovL2lwdjYuaWNlZmlsbXMuaW5mby9tZW1iZXJzb25seS9jb21wb25lbnRzL2NvbV9pY2VwbGF5ZXIvdmlkZW8ucGhwP2g9Mzc0Jnc9NjMxJnZpZD0lcyZpbWc9'
        self.r_link = 'aHR0cDovL2lwdjYuaWNlZmlsbXMuaW5mby9pcC5waHA/dj0lcyY='
        self.j_link = 'aHR0cDovL2lwdjYuaWNlZmlsbXMuaW5mby9tZW1iZXJzb25seS9jb21wb25lbnRzL2NvbV9pY2VwbGF5ZXIvdmlkZW8ucGhwQWpheFJlc3AucGhwP3M9JXMmdD0lcw=='
        self.p_link = 'aWQ9JXMmcz0lcyZpcXM9JnVybD0mbT0lcyZjYXA9KyZzZWM9JXMmdD0lcw=='

    def movie(self, imdb, tmdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def request(self, url, post=None, cookie=None, referer=None, output='', close=True):
        try:
            headers = {'Accept': '*/*'}
            if cookie is not None:
                headers['Cookie'] = cookie
            if referer is not None:
                headers['Referer'] = referer
            result = client.request(url, post=post, headers=headers, output=output, close=close)
            result = result.decode('iso-8859-1').encode('utf-8')
            result = urllib.unquote_plus(result)
            return result
        except:
            return

    def directdl_cache(self, url):
        try:
            url = urlparse.urljoin(base64.b64decode(self.b_link), url)
            result = self.request(url)
            result = re.compile(r'id=(\d+)>.+?href=(.+?)>').findall(result)
            result = [(re.sub('http.+?//.+?/','/', i[1]), 'tt' + i[0]) for i in result]
            return result
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return sources
            if debrid.status() is False:
                raise Exception()

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            try:
                links = []

                f = ['S%02dE%02d' % (int(data['season']), int(data['episode']))]
                t = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', data['tvshowtitle'])
                t = t.replace("&", "")
                
                q = self.search_link + urllib.quote_plus('%s %s' % (t, f[0]))
                
                q = urlparse.urljoin(self.base_link, q)
                result = client.request(q)
                result = json.loads(result)

                result = result['results']
            except:
                links = result = []
            
            for i in result:
                try:
                    if not cleantitle.get(t) == cleantitle.get(i['showName']):
                        raise Exception()

                    y = i['release']
                    y = re.compile(r'[\.|\(|\[|\s](\d{4}|S\d*E\d*)[\.|\)|\]|\s]').findall(y)[-1]
                    y = y.upper()
                    if not any(x == y for x in f):
                        raise Exception()

                    quality = i['quality']
                    
                    quality = quality.upper()

                    size = i['size']
                    size = float(size)/1024
                    size = '[B]%.2f GB[/B]' % size
   
                    info = size

                    if '4k' in quality:
                        quality = '4K'
                    elif '1080P' in quality:
                        quality = '1080p'
                    elif '720P' in quality:
                        quality = 'HD'
                    else: quality = 'SD'

                    url = i['links']
                    #for x in url.keys(): links.append({'url': url[x], 'quality': quality, 'info': info})
                    
                    links = []
                    
                    for x in url.keys():
                        links.append({'url': url[x], 'quality': quality})
                    
                    for link in links:
                        try:
                            url = link['url']
                            quality2 = link['quality']
                            #url = url[1]
                            #url = link
                            if len(url) > 1:
                                raise Exception()
                            url = url[0].encode('utf-8')
                            
                            host = re.findall(r'([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                            if host not in hostprDict:
                                raise Exception()
                            host = host.encode('utf-8')

                            sources.append({'source': host, 'quality': quality2, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                        except:
                            pass
                    
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            b = urlparse.urlparse(url).netloc
            b = re.compile(r'([\w]+[.][\w]+)$').findall(b)[0]

            if b not in base64.b64decode(self.b_link):
                return url
            
            u, p, h = url.split('|')
            r = urlparse.parse_qs(h)['Referer'][0]

            c = self.request(r, output='cookie', close=False)
            result = self.request(u, post=p, referer=r, cookie=c)

            url = result.split('url=')
            url = [urllib.unquote_plus(i.strip()) for i in url]
            url = [i for i in url if i.startswith('http')]
            url = url[-1]

            return url
        except:
            return


