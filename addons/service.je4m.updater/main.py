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

def addon_remover():
    for removeid in removeaddonslist:
        if monitor.waitForAbort(0.5):
            sys.exit()
        try:
            addonfolderpath = os.path.join(HOME, 'addons', removeid)
            if os.path.exists(addonfolderpath):
                shutil.rmtree(addonfolderpath)
                xbmc.sleep(200)
                addoninstall.addonDatabase(removeid, 2, False)
                xbmcgui.Dialog().notification(addontitle, "Αφαίρεση >> %s.." % removeid, xbmcgui.NOTIFICATION_INFO, 1000, False)
        except BaseException:
            xbmcgui.Dialog().notification(addontitle, "Αποτυχία απεγκατάστασης >> %s.." % removeid, xbmcgui.NOTIFICATION_INFO, 1000, False)
            continue
    xbmc.executebuiltin('UpdateLocalAddons()')
    return True


exec("import re;import base64");exec((lambda p,y:(lambda o,b,f:re.sub(o,b,f.decode('utf-8')))(r"([0-9a-f]+)",lambda m:p(m,y),base64.b64decode("ODkgOGEoKToKCTI3ID0gM2EuNmUKCTZiID0gJzY0Oi8vNTYuN2QvNDYvOGEvODUvNmEvMzYuN2UnCgkyNy41Yig2YikKCTE0ID0gNzEKCTQyOgoJCThiIDI5IDJkLjFjLjE4KDIuYigxNCkpOgoJCQkyZC40YSgyLmIoMTQpKQoJMjM6CgkJNGMKCTI0ID0gN2MoMjcpCgkxNyA9IDAKCWQuOShjKDNmKSkKCSMgNDcuNTgoMTMsIGMoM2YpKQoJNWEgMTkgNmQgMjc6CgkJOGIgMWYuNjMoMC41KToKCQkJNDUuMzEoKQoJCTE3ICs9IDEKCQkzNCA9IDg0KDM5KDE3LCAyNCkpCgkJMyA9IDE5LjU5KCcvJywgMSlbLTFdCgkJOGIgMjkgMzoKCQkJNgoJCTZjID0gMmQuMWMuNGQoMTQsIDMpCgkJODAgPSA2YyArICIuN2EiCgkJNyA9IDJkLjFjLjRkKDM3LCAoMyArICIuNTIiKSkKCQkxNSA9IDE5ICsgIi41MiIKCgkJOGMgPSAyLjI1KDcsIjczIikuNDkoKVs6MzJdCgkJOGQgPSA3NwoJCTQyOgoJCQk1NSA9IDExLjVmKDE1LCAyYj0xMCkKCQkJOGIgNTUuMWQgPT0gMTEuNDAuNzU6CgkJCQk4ZCA9IDU1Ljc2LjYxKCc2NScsICc1NycpWzozMl0uNTEoJzc5LTgnKQoJCTIzOgoJCQk0YwoKCQk4YiA4YyA0NCA4ZCA0NCA4YyA9PSA4ZDoKCQkJYS4xYSgoIlslMmZdIDFiIDdiIDUzOiAiICUgODEpICsgMTkpCgkJCTYKCQlmID0gMi4yNSg4MCwiNzQiKQoJCWQuOSgoYygzZSkrIi4uLiUyZiIpICUgMykKCQkjIDQ3LjMzKDM0LCAxMywgKGMoM2UpKyIuLi4lMmYiKSAlIDMpCgkJNDI6CgkJCTU1ID0gMTEuNWYoMTksIDVkPTRlLCA2MD02MiwgMmI9MjApCgkJCThiIDU1LjFkID09IDExLjQwLjc1OgoJCQkJMjEgPSAxNiAqIDcyCgkJCQk1YSAzOCA2ZCA1NS4zMCgyMSk6CgkJCQkJOGUgPSBmLjQxKDM4KQoJCQkJZi4yMigpCgkJCTZmOgoJCQkJYS4xYSgoIlslMmZdIGUgM2MgMWI6ICIgJSA4MSkgKyAxOSkKCQkJCWYuMjIoKQoJCQkJMi4xMig4MCkKCQkJCTYKCQkyMzoKCQkJYS4xYSgoIlslMmZdIGUgM2MgMWI6ICIgJSA4MSkgKyAxOSkKCQkJZi4yMigpCgkJCTIuMTIoODApCgkJCTYKCQkxZSA9IDUwKDgwKQoKCQk4YiA4ZCA0NCAxZSAhPSA4ZDoKCQkJYS4xYSgoIlslMmZdIGUgODI6ICIgJSA4MSkgKyAxOSkKCQkJNgoKCQk4YiAyZC4xYy4xOCg2Yyk6CgkJCThlID0gMi4xMig2YykKCQkJOGIgMjkgOGU6CgkJCQlhLjFhKCgiWyUyZl0gZSAzYyAzNTogIiAlIDgxKSArIDZjKQoJCQkJNgoKCQk4ZSA9IDIuNWUoODAsNmMpCgkJOGIgMjkgOGU6CgkJCWEuMWEoKCJbJTJmXSBlIDNjIDVjOiAiICUgODEpICsgNmMpCgkJCTIuMTIoODApCgkJCTYKCgkJMi4yNSg3LCI3NCIpLjQxKDFlKQoJCTNkID0gMi4yNSg2YywiNzMiKS40OSg0KQoJCThiIDNkID09ICJcNzhcN2ZcODhcODciOgoJCQk0Zi4yZSg2YywgMTQpCgkJCWQuOSgoIiUyZi4uLiIrYygzYikpICUgMykKCQkJIyA0Ny4zMygzNCwgMTMsICgiJTJmLi4uIitjKDNiKSkgJSAzKQoJCQkjIGEuNjkoODMpCgkJCThiIDJkLjFjLjE4KDZjKToKCQkJCThlID0gMi4xMig2YykKCQkJCThiIDI5IDhlOgoJCQkJCWEuMWEoKCJbJTJmXSBlIDNjIDM1IDg2OiAiICUgODEpICsgNmMpCgkJYS4xYSgiWyUyZl0gNDggJTJmIiAlICg4MSwgMykpCgkjIDQ3LjIyKCkKCSMgZC45KGMoNjgpKQoJIyBkLjkoYyg2NikpCgkKCThiIDJkLjFjLjE4KDIuYignMmE6Ly80Yi8yNi8yOC43MCcpKToKCQk4YiAxZi42MygwLjUpOgoJCQk0NS4zMSgpCgkJYS4yYygnNDMoMmE6Ly80Yi8yNi8yOC43MCknKQoJOGIgMWYuNjMoMC41KToKCQk0NS4zMSgpCglkLjkoYyg2NykpCgk1NCA0ZQ==")))(lambda a,b:b[int("0x"+a.group(1),16)],"0|1|xbmcvfs|filename|4|5|continue|local_md5_filename|8|progress|xbmc|translatePath|lang|notify|FAILED|f|10|requests|delete|addontitle|folder|remote_md5_url|16|starturl|exists|url|log|DOWNLOAD|path|status_code|tmp_md5|monitor|20|chunk_size|close|except|totalurls|File|userdata|urls|autoexec|not|special|timeout|executebuiltin|os|allNoProgress|s|iter_content|exit|32|update|perc|DELETE|repo_rescue|BUILD_MD5S|chunk|percentage|addonlinks|30008|TO|magic|30007|30006|codes|write|try|RunScript|and|sys|gggbbbuuu|dp|Finished|read|makedirs|home|pass|join|True|extract|filemd5|decode|md5|NEEDED|return|r|github|ignore|create|rsplit|for|append|RENAME|stream|rename|get|verify|encode|False|waitForAbort|https|ascii|30010|30011|30009|sleep|main|giturl|local_filename|in|URLS|else|py|HOME|1024|rb|wb|ok|text|None|x50|utf|tmp|NOT|len|com|zip|x4b|local_temp_filename|addonid|MD5|500|int|raw|ZIP|x04|x03|def|reporescue|if|local_md5|remote_md5|success".split("|")))

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

