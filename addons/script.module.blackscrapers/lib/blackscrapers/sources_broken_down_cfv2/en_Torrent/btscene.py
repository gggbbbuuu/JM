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

import re

from blackscrapers import parse_qs, urljoin, urlencode, quote_plus, unquote_plus
from blackscrapers.modules import cleantitle, client, debrid, source_utils

from blackscrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['btscene.today']
        self.base_link = custom_base or 'http://btscene.nl'
        self.search_link = '/search?q=%s'
        self.aliases = []

    def movie(self, imdb, tmdb, title, localtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
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
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources
            if debrid.status() is False:
                return sources
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = ' '.join((title, hdlr))
            query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % quote_plus(query)
            url = urljoin(self.base_link, url)

            r = client.request(url)
            posts = client.parseDOM(r, 'tr')
            for post in posts:
                try:
                    links = re.findall('a title="Download Torrent Magnet" href="(magnet:.+?)"', post, re.DOTALL)
                    try:
                        size = re.findall(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', post)[0]
                        dsize, isize = source_utils._size(size)
                    except:
                        dsize, isize = 0.0, ''
                    for link in links:
                        link_name = unquote_plus(link)

                        url = link_name.split('&tr=')[0]
                        if any(x in url for x in ['FRENCH', 'Ita', 'italian', 'TRUEFRENCH', '-lat-', 'Dublado']):
                            continue

                        name = cleantitle.get_title(url.split('&dn=')[1])
                        if not source_utils.is_match(name, title, hdlr, self.aliases):
                            continue

                        quality, info = source_utils.get_release_quality(name, url)
                        info.insert(0, isize)
                        info = ' | '.join(info)
                        sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                        'direct': False, 'debridonly': True, 'size': dsize, 'name': name})
                except:
                    pass
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
