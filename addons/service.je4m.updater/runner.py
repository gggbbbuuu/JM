# -*- coding: utf-8 -*-
import xbmc, xbmcgui, os, json
import main
from resources.lib import monitor

addon = main.addon

# from contextlib import contextmanager

# @contextmanager
# def busy_dialog():
    # xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    # try:
        # yield
    # finally:
        # xbmc.executebuiltin('Dialog.Close(busydialognocancel)')

def isenabled(addonid):
    query = '{ "jsonrpc": "2.0", "id": 1, "method": "Addons.GetAddonDetails", "params": { "addonid": "%s", "properties" : ["name", "thumbnail", "fanart", "enabled", "installed", "path", "dependencies"] } }' % addonid
    addonDetails = xbmc.executeJSONRPC(query)
    details_result = json.loads(addonDetails)
    if "error" in details_result:
        return False
    elif details_result['result']['addon']['enabled'] == True:
        return True
    else:
        return False

if __name__ == '__main__':
    if monitor.waitForAbort(3):
        sys.exit()
    if isenabled('plugin.video.scrubsv2'):
        if not addon.getSetting('set_scrubsv2') == 'false':
            # with busy_dialog():
                from resources.lib import set_scrubsv2
                set_scrubsv2.setScrubsSettings()
    if isenabled('plugin.video.fen'):
        if not addon.getSetting('set_fen') == 'false':
            # with busy_dialog():
                from resources.lib import set_fen
                set_fen.setFenSettings()
    if isenabled('plugin.video.themoviedb.helper'):
        if not addon.getSetting('set_tmdbhelper') == 'false':
            # with busy_dialog():
                from resources.lib import set_tmdbhelper
                set_tmdbhelper.setTMDBhSettings()
    if isenabled('service.subtitles.subtitles.gr'):
        if not addon.getSetting('set_subtitlesgr') == 'false':
            # with busy_dialog():
                from resources.lib import set_subsgr
                set_subsgr.setSubsGRSettings()
    if isenabled('plugin.video.seren'):
        if not addon.getSetting('set_seren') == 'false':
            # with busy_dialog():
                from resources.lib import set_seren
                set_seren.setSerenSettings()
    if isenabled('plugin.video.AliveGR'):
        if not addon.getSetting('set_alivegr') == 'false':
            # with busy_dialog():
                from resources.lib import set_alivegr
                set_alivegr.setAliveGRSettings()
    if isenabled('plugin.video.youtube'):
        if not addon.getSetting('set_youtube') == 'false':
            # with busy_dialog():
                from resources.lib import set_youtube
                set_youtube.setYoutubeSettings()
    if not addon.getSetting('set_gui') == 'false':
        # with busy_dialog():
            from resources.lib import set_gui
            set_gui.setguiSettings()
    from resources.lib import set_stalker
    set_stalker.setpvrstalker()
    main.updatezip()
    main.addon_remover()
    main.reporescue()
    update_toggle = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"general.addonupdates"}, "id":1}'
    resp_toggle = xbmc.executeJSONRPC(update_toggle)
    toggle = json.loads(resp_toggle)
    if toggle['result']['value'] != 0:
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"general.addonupdates","value":0}}')
    if monitor.waitForAbort(1):
        sys.exit()
    xbmc.executebuiltin('UpdateAddonRepos()')
