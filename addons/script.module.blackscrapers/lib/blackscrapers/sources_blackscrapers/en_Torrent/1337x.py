# -*- coding: utf-8 -*-


import re

from blackscrapers import cfScraper
from blackscrapers import parse_qs, urljoin, urlencode, quote
from blackscrapers.modules import cache, cleantitle, client, debrid, log_utils, source_utils, workers
from blackscrapers.modules import dom_parser as dom

from blackscrapers import custom_base_link
custom_base = custom_base_link(__name__)

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['1337x.to'] # cf: '1337x.st', '1337x.gd', 'x1337x.se', 'x1337x.eu', 'x1337x.ws'
        self.base_link = custom_base or 'https://1337x.to'
        self.aliases = []

    def movie(self, imdb, tmdb, title, localtitle, aliases, year):
        if debrid.status() is False:
            return

        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('1337x - Exception', 1)
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if debrid.status() is False:
            return

        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('1337x - Exception', 1)
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if debrid.status() is False:
            return

        try:
            if url is None:
                return

            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            log_utils.log('1337x - Exception', 1)
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            self._sources = []
            self.items = []
            if url is None:
                return self._sources

            if debrid.status() is False:
                return self._sources

            self.tvsearch = '%s/sort-category-search/%s/TV/seeders/desc/1/' % (self.base_link, '%s')
            self.moviesearch = '%s/sort-category-search/%s/Movies/size/desc/1/' % (self.base_link, '%s')

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.title = cleantitle.get_query(self.title)
            self.hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = ' '.join((self.title, self.hdlr))
            query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            urls = []
            if 'tvshowtitle' in data:
                urls.append(self.tvsearch % (quote(query)))
                '''
                Why spam for multiple pages, since it gives plenty on each page?

                urls.append(self.tvsearch.format(quote(query), '2'))
                urls.append(self.tvsearch.format(quote(query), '3'))
                '''
            else:
                urls.append(self.moviesearch % (quote(query)))
                '''
                Why spam for multiple pages, since it gives plenty on each page?

                urls.append(self.moviesearch.format(quote(query), '2'))
                urls.append(self.moviesearch.format(quote(query), '3'))
                '''
            threads = []
            for url in urls:
                threads.append(workers.Thread(self._get_items, url))
            [i.start() for i in threads]
            [i.join() for i in threads]

            self.hostDict = hostDict + hostprDict
            threads2 = []
            for i in self.items:
                threads2.append(workers.Thread(self._get_sources, i))
            [i.start() for i in threads2]
            [i.join() for i in threads2]

            return self._sources
        except:
            log_utils.log('1337x_exc2', 1)
            return self._sources

    def _get_items(self, url):
        try:
            r = cfScraper.get(url, timeout=10).text
            posts = client.parseDOM(r, 'tbody')[0]
            posts = client.parseDOM(posts, 'tr')
            for post in posts:
                data = dom.parse_dom(post, 'a', req='href')[1]
                link = urljoin(self.base_link, data.attrs['href'])
                name = cleantitle.get_title(data.content)

                if not source_utils.is_match(name, self.title, self.hdlr, self.aliases):
                    continue

                try:
                    size = re.findall(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', post)[0]
                    dsize, isize = source_utils._size(size)
                except:
                    dsize, isize = 0.0, ''

                self.items.append((name, link, isize, dsize))
            return self.items
        except:
            log_utils.log('1337x_exc0', 1)
            return self.items

    def _get_sources(self, item):
        try:
            name = item[0]
            quality, info = source_utils.get_release_quality(name, item[1])
            info.insert(0, item[2])
            data = cfScraper.get(item[1], timeout=10).text
            data = client.parseDOM(data, 'a', ret='href')
            url = [i for i in data if 'magnet:' in i][0]
            url = url.split('&tr')[0]
            info = ' | '.join(info)

            self._sources.append(
                {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False,
                 'debridonly': True, 'size': item[3], 'name': name})
        except:
            log_utils.log('1337x_exc1', 1)
            pass

    def resolve(self, url):
        return url
