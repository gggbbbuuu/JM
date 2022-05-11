"""
    Plugin for ResolveUrl
    Copyright (C) 2019 gujal

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
"""

import re
from resolveurl.lib import helpers
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError
import webbrowser, xbmc, xbmcgui
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'

myplatform = platform()

class StreamzResolver(ResolveUrl):
    name = 'streamz'
    domains = ['streamz.cc', 'streamz.vg', 'streamzz.to', 'streamz.ws']
    pattern = r'(?://|\.)(streamzz?\.(?:cc|vg|to|ws))/([0-9a-zA-Z]+)'

    def get_media_url(self, host, media_id):

        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.CHROME_USER_AGENT}
        html = self.net.http_GET(web_url, headers=headers).content

        if '<b>File not found, sorry!</b>' not in html:
            html += helpers.get_packed_data(html)
            v = re.search(r"player\s*=\s*.*?'([^']+)", html)
            if v:
                vurl = re.search(r'''{0}".+?src:\s*'([^']+)'''.format(v.group(1)), html)
                if vurl:
                    furl = helpers.get_redirect_url(vurl.group(1), headers) + helpers.append_headers(headers)
                    if 'issue.mp4' in furl:
                        xbmcgui.Dialog().ok('ResolveURL', 'Θα ανοίξει μία σελίδα στον internet browser για να ξεκλειδώσει το stream.[CR]Χωρίς να κάνετε κατι άλλο απλά επιστρέψτε στο kodi για το δείτε.')
                        if myplatform == 'android':
                            opensite = xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ('https://streamzz.to/fcnk0bjhianZxNGJiZXgw'))
                        else:
                            opensite = webbrowser.open('https://streamzz.to/fcnk0bjhianZxNGJiZXgw')
                        xbmc.sleep(5000)
                        if xbmcgui.Dialog().ok('ResolveURL', 'τώρα μπορείτε να συνεχίσετε με την προβολή του stream'):
                            html2 = self.net.http_GET(web_url, headers=headers).content

                            if '<b>File not found, sorry!</b>' not in html2:
                                html2 += helpers.get_packed_data(html2)
                                v = re.search(r"player\s*=\s*.*?'([^']+)", html2)
                                if v:
                                    vurl = re.search(r'''{0}".+?src:\s*'([^']+)'''.format(v.group(1)), html2)
                                    if vurl:
                                        furl = helpers.get_redirect_url(vurl.group(1), headers) + helpers.append_headers(headers)
                                        return furl
                    else:
                        return furl

        raise ResolverError('Video not found or removed')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://streamzz.to/{media_id}')
