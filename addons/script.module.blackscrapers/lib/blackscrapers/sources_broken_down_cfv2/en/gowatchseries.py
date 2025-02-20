# -*- coding: utf-8 -*-

'''
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

import requests
import simplejson as json

from blackscrapers import parse_qs, urljoin, urlencode, quote
from blackscrapers.modules import cleantitle
from blackscrapers.modules import client
from blackscrapers.modules import source_utils, log_utils
from blackscrapers import cfScraper

from blackscrapers import custom_base_link
custom_base = custom_base_link(__name__)

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['gowatchseries.io', 'gowatchseries.co', 'www5.gowatchseries.bz', 'gowatchseries.online', 'gowatchseries.ch']
        self.base_link = custom_base or 'https://gowatchseries.eu'
        self.search_link = '/ajax-search.html?keyword=%s&id=-1'
        self.search_link2 = '/search.html?keyword=%s'
        self.session = requests.Session()

    def movie(self, imdb, tmdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('gowatchseries0 - Exception', 1)
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {
                'imdb': imdb,
                'tvdb': tvdb,
                'tvshowtitle': tvshowtitle,
                'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('gowatchseries1 - Exception', 1)
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return

            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            log_utils.log('gowatchseries2 - Exception', 1)
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return sources

            host_dict = hostprDict + hostDict

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            if 'season' in data:
                season = data['season']
            if 'episode' in data:
                episode = data['episode']
            year = data['year']

            # r = client.request(self.base_link, output='extended')
            # headers = r[2]
            # headers['X-Requested-With'] = 'XMLHttpRequest'
            # result = r[0]

            headers = {'Referer': self.base_link, 'User-Agent': client.agent(), 'X-Requested-With': 'XMLHttpRequest'}

            query = urljoin(self.base_link, self.search_link2 % quote(title).lower())
            r = self.session.get(query, headers=headers, timeout=10).text
            r = client.parseDOM(r, 'ul', attrs={'class': 'listing items'})[0]
            r = client.parseDOM(r, 'li')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'div', attrs={'class': 'name'})) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]

            if 'tvshowtitle' in data:
                cltitle = cleantitle.get(title + 'season' + season)
                cltitle2 = cleantitle.get(title + 'season%02d' % int(season))
                r = [i for i in r if cltitle == cleantitle.get(i[1]) or cltitle2 == cleantitle.get(i[1])]
                vurl = '%s%s-episode-%s' % (self.base_link, str(r[0][0]).replace('/info', ''), episode)
                vurl2 = None

            else:
                cltitle = cleantitle.getsearch(title)
                cltitle2 = cleantitle.getsearch('%s (%s)' % (title, year))
                r = [i for i in r if cltitle2 == cleantitle.getsearch(i[1]) or cltitle == cleantitle.getsearch(i[1])]
                vurl = '%s%s-episode-0' % (self.base_link, str(r[0][0]).replace('/info', ''))
                vurl2 = '%s%s-episode-1' % (self.base_link, str(r[0][0]).replace('/info', ''))

            r = self.session.get(vurl, headers=headers, timeout=10).text
            headers['Referer'] = vurl

            slinks = client.parseDOM(r, 'li', ret='data-video')
            if len(slinks) == 0 and vurl2 is not None:
                r = self.session.get(vurl2, headers=headers, timeout=10).text
                headers['Referer'] = vurl2
                slinks = client.parseDOM(r, 'li', ret='data-video')
            slinks = [slink if slink.startswith('http') else 'https:{0}'.format(slink) for slink in slinks]

            for url in slinks:
                url = client.replaceHTMLCodes(url)
                #log_utils.log('gowatchseries_url: ' + repr(url))
                valid, host = source_utils.is_host_valid(url, host_dict)
                if valid:
                    sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                elif ('vidembed' in url and '/goto.' in url) or '/hls/' in url:
                    sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

            return sources
        except:
            log_utils.log('gowatchseries3 - Exception', 1)
            return sources

    def resolve(self, url):
        return url



