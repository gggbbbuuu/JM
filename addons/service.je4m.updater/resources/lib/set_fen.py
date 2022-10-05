# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcgui, xbmcvfs, os, sys
from resources.lib import notify, monitor
import main
transPath  = xbmcvfs.translatePath
logo = transPath('special://home/addons/plugin.video.fen/icon.png')

def setFenSettings():
    try:
        addons_folder = transPath('special://home/addons/')
        setaddon = xbmcaddon.Addon('plugin.video.fen')
        setversionaddon = main.addon
        gkobufenprev = setversionaddon.getSetting('gkobusetfen')
        gkobufennew = '1.1'
        if gkobufenprev == '' or gkobufenprev is None:
            gkobufenprev = '0'
        if os.path.exists(os.path.join(addons_folder, 'plugin.video.fen')) and str(gkobufennew) > str(gkobufenprev):
            if monitor.waitForAbort(0.5):
                sys.exit()
            notify.progress('Ξεκινάει η ρύθμιση του Fen', t=1, image=logo)
            try:
                # xbmcgui.Dialog().notification("[B]GKoBu-Υπηρεσία Ενημέρωσης[/B]", "Εφαρμογή ρυθμίσεων Fen...", xbmcgui.NOTIFICATION_INFO, 3000, False)
                setaddon.setSetting('meta_language_display', 'Greek')
                setaddon.setSetting('meta_language', 'el')
                setaddon.setSetting('results.sort_order_display', 'Quality, Size, Provider')
                setaddon.setSetting('results.ignore_filter', '1')
                setaddon.setSetting('subtitles.subs_action', '0')
                setaddon.setSetting('subtitles.language', 'Greek')
                setaddon.setSetting('reuse_language_invoker', 'false')
                setversionaddon.setSetting('gkobusetfen', gkobufennew)
                notify.progress('H ρύθμιση του Fen ολοκληρώθηκε', t=1, image=logo)
            except BaseException:
                notify.progress('Αδυναμία εφαρμογής ρυθμίσεων Fen...', t=1, image=logo)
                # xbmcgui.Dialog().notification("[B]GKoBu-Υπηρεσία Ενημέρωσης[/B]", "Αδυναμία εφαρμογής ρυθμίσεων Fen...", xbmcgui.NOTIFICATION_INFO, 3000, False)
                return
        else:
            return
    except BaseException:
        # notify.progress('Αδυναμία εφαρμογής ρυθμίσεων Fen...', t=1, image=logo)
        # xbmcgui.Dialog().notification("[B]GKoBu-Υπηρεσία Ενημέρωσης[/B]", "Αδυναμία εφαρμογής ρυθμίσεων Fen...", xbmcgui.NOTIFICATION_INFO, 3000, False)
        return
    return True


if __name__ == '__main__':
    setFenSettings()

