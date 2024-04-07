# -*- coding: utf-8 -*-
import xbmc, xbmcgui
import sys
import json
def getchannelgroups():
    CHANNELGROUPS = []
    ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "PVR.GetChannelGroups", "params":{"channeltype":"tv"} }'))
    channelgroups = ret['result']['channelgroups']
    gr_groups = []
    for channelgroup in channelgroups:
        group_id = channelgroup.get("channelgroupid", "")
        ch_type = channelgroup.get("channeltype", "")
        group_label = channelgroup.get("label", "")
        if 'gr ' in group_label.lower() or 'gree' in group_label.lower() or 'grec' in group_label.lower() or '|gr|' in group_label.lower():
            gr_groups.append(channelgroup)
    return channelgroups, gr_groups


def opengroups(g):
    xbmc.executebuiltin('ActivateWindow(TVChannels)')
    c = 2
    xbmc.executebuiltin('SendClick(28)')
    xbmc.executebuiltin( "Action(FirstPage)" )
    if g > 1:
        while (c <= g): 
            c = c + 1
            xbmc.executebuiltin( "Action(Down)" )
    if g >= 1:      
        xbmc.executebuiltin( "Action(Select)" )
        xbmc.executebuiltin( "Action(Right)" )
        xbmc.executebuiltin( "ClearProperty(SideBladeOpen)" )

def finish():
    exit()

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

all_groups, gr_groups = getchannelgroups()
yes = xbmcgui.Dialog().yesno("[B][COLOR blue]GKoBu Build Υποστήριξη PVR[/COLOR][/B]", "Μπορείτε να επιλέξετε [B][COLOR yellow]Ελληνικά[/COLOR][/B] για να εμφανιστεί το βασικό γκρουπ Ελληνικών καναλιών. Υπάρχει όμως η πιθανότητα σε ορισμένα portal να υπάρχουν επιμέρους γκρουπ με ελληνικά κανάλια. Η επιλογή αυτών γίνεται μέσω της επιλογής [B][COLOR yellow]Όλα τα γκρουπ[/COLOR][/B][CR]Μπορείτε να επιλέξετε [B][COLOR yellow]Όλα τα γκρουπ[/COLOR][/B] αν θέλετε να διαλέξετε από την συνολική λίστα με τα γκρουπ καναλιών", nolabel='[B][COLOR yellow]Ελληνικά[/COLOR][/B]', yeslabel='[B][COLOR yellow]Όλα τα γκρουπ[/COLOR][/B]')
if yes == False:
    gr_select = xbmcgui.Dialog().select('Επέλεξε Group Καναλιών', [el.get("label","-") for el in gr_groups])
    labl = gr_groups[gr_select].get("label")
    g = find(all_groups, "label", labl)+1
    if not xbmc.getCondVisibility('System.HasPVRAddon'):
        xbmc.executebuiltin('Notification(PVR addon, is not enabled)')
        finish()
    opengroups(g)
    finish()
else:
    xbmc.executebuiltin('ActivateWindow(TVChannels)')
    xbmc.executebuiltin('SendClick(28)')

