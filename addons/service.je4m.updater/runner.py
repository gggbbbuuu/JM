# -*- coding: utf-8 -*-
import xbmc, xbmcgui, os
import main
from resources.lib import set_theoath, set_tmdbhelper, set_subsgr, set_seren, set_alivegr, set_youtube, set_gui, set_stalker, notify, monitor
from contextlib import contextmanager

@contextmanager
def busy_dialog():
    xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    try:
        yield
    finally:
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')

if __name__ == '__main__':
    if monitor.waitForAbort(3):
        sys.exit()
    with busy_dialog():
        set_theoath.setTheOathSettings()
    with busy_dialog():
        set_tmdbhelper.setTMDBhSettings()
    with busy_dialog():
        set_subsgr.setSubsGRSettings()
    with busy_dialog():
        set_seren.setSerenSettings()
    with busy_dialog():
        set_alivegr.setAliveGRSettings()
    with busy_dialog():
        set_youtube.setYoutubeSettings()
    with busy_dialog():
        set_gui.setguiSettings()
    with busy_dialog():
        set_stalker.setpvrstalker()
    with busy_dialog():
        main.updatezip()
    with busy_dialog():
        main.addon_remover()
    with busy_dialog():
        main.reporescue()
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"general.addonupdates","value":0}}')
        if monitor.waitForAbort(1):
            sys.exit()
        xbmc.executebuiltin('UpdateAddonRepos()')
