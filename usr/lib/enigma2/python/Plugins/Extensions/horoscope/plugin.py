#!/usr/bin/python
# -*- coding: utf-8 -*-

# ======================================================================
# Horoscope Plugin
#
# written by Lululla
#
# ***************************************
#        coded by Lululla              *
#  update     12/01/2025               *
#       Graphics by Oktus              *
# ***************************************
# ATTENTION PLEASE...
# This is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2, or (at your option) any later
# version.
# You must not remove the credits at
# all and you must make the modified
# code open to everyone. by Lululla
# ======================================================================


from . import _, isDreambox, isWQHD, isFHD, isHD

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from datetime import datetime
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import fileExists
from Tools.LoadPixmap import LoadPixmap
from enigma import eTimer
from xml.dom import minidom
import unicodedata
import requests

version = '1.0'
INFO_RI = _("Horoscope v.%s\n\nAuthor: Lululla\n\nGraphics: Oktus\n\nRss Horoscope: https://www.findyourfate.com\n\n") % version

today = datetime.now()
formatted_date = today.strftime("%B %d, %Y")


def removeAccents(content):
    if isinstance(content, bytes):
        try:
            content = content.decode('utf-8')
        except UnicodeDecodeError:
            content = content.decode('latin-1')

    content = unicodedata.normalize('NFKD', content)
    content = ''.join(c for c in content if not unicodedata.combining(c))
    return content


class horoscopeMain(Screen):

    if isWQHD() or isFHD():
        skin = """
                <screen name="horoscopeMain" position="center,center" size="1920,1080" backgroundColor="transparent" flags="wfNoBorder">
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/horoscope/backg.png" position="0,0" zPosition="-2" size="1920,1080" scale="fill" alphatest="blend" />
                    <ePixmap position="0,0" size="1920,1080" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/horoscope/backtr.png" scale="1" alphatest="blend" zPosition="-1" />
                    <eLabel backgroundColor="red" cornerRadius="3" position="34,1064" size="296,6" zPosition="11" />
                    <eLabel backgroundColor="green" cornerRadius="3" position="342,1064" size="300,6" zPosition="11" />
                    <!--
                    <eLabel backgroundColor="yellow" cornerRadius="3" position="652,1064" size="300,6" zPosition="11" />
                    <eLabel backgroundColor="blue" cornerRadius="3" position="962,1064" size="300,6" zPosition="11" />
                    -->
                    <widget name="key_red" render="Label" position="32,1016" size="300,45" zPosition="11" font="Regular; 30" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                    <widget name="key_green" render="Label" position="342,1016" size="300,45" zPosition="11" font="Regular; 30" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                    <!--
                    <widget name="key_yellow" render="Label" position="652,1016" size="300,45" zPosition="11" font="Regular; 30" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                    <widget name="key_blue" render="Label" position="962,1016" size="300,45" zPosition="11" font="Regular; 30" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                    -->
                    <widget name="date" position="585,90" halign="center" size="745,65" zPosition="5" font="Regular; 42" valign="center" transparent="1" />
                    <widget name="lab1" position="461,953" halign="center" size="1000,50" zPosition="5" font="Regular; 36" valign="center" transparent="1" />
                    <widget name="lab2" position="585,400" halign="center" size="745,50" zPosition="5" font="Regular; 36" valign="top" transparent="1" />
                    <widget name="lab3" position="864,178" size="200,200" cornerRadius="20" zPosition="5" scale="1" transparent="0" alphatest="blend" />
                    <widget name="lab4" position="585,470" halign="center" size="745,453" zPosition="5" font="Regular;34" valign="top" transparent="1" />
                </screen>"""

    elif isHD():
        skin = """
            <screen name="horoscopeMain" position="center,center" size="1280,720" backgroundColor="transparent" flags="wfNoBorder">
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/horoscope/backg.png" position="0,0" zPosition="-2" size="1280,720" scale="fill" alphatest="blend" />
                <ePixmap position="0,0" size="1280,720" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/horoscope/backtr.png" scale="1" alphatest="blend" zPosition="-1" />
                <eLabel backgroundColor="red" cornerRadius="3" position="22,709" size="197,4" zPosition="11" />
                <eLabel backgroundColor="green" cornerRadius="3" position="228,709" size="200,4" zPosition="11" />
                <!--
                <eLabel backgroundColor="yellow" cornerRadius="3" position="434,709" size="200,4" zPosition="11" />
                <eLabel backgroundColor="blue" cornerRadius="3" position="641,709" size="200,4" zPosition="11" />
                -->
                <widget name="key_red" render="Label" position="21,677" size="200,30" zPosition="11" font="Regular; 20" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                <widget name="key_green" render="Label" position="228,677" size="200,30" zPosition="11" font="Regular; 20" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                <!--
                <widget name="key_yellow" render="Label" position="434,677" size="200,30" zPosition="11" font="Regular; 20" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                <widget name="key_blue" render="Label" position="641,677" size="200,30" zPosition="11" font="Regular; 20" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                -->
                <widget name="date" position="290,60" halign="center" size="725,43" zPosition="5" font="Regular; 28" valign="center" transparent="1" />
                <widget name="lab1" position="290,630" halign="center" size="725,35" zPosition="5" font="Regular; 22" valign="top" transparent="1" />
                <widget name="lab2" position="290,215" halign="center" size="725,35" zPosition="5" font="Regular; 24" valign="top" transparent="1" />
                <widget name="lab3" position="612,125" size="80,80" cornerRadius="20" zPosition="5" scale="1" transparent="0" />
                <widget name="lab4" position="290,265" halign="center" size="725,350" zPosition="5" font="Regular;22" valign="top" transparent="1" />
            </screen>
            """

    def __init__(self, session):
        Screen.__init__(self, session)
        self["lab1"] = Label(_("Please wait, connecting to the server..."))
        self["lab2"] = Label("")
        self["lab3"] = Pixmap()
        self["lab4"] = Label("")
        self["date"] = Label("")
        self['key_red'] = Label(_('Change'))
        self['key_green'] = Label(_('Information'))
        self["actions"] = ActionMap(
            ["WizardActions", "ColorActions"],
            {
                "red": self.key_red,
                "green": self.key_green,
                "back": self.close,
                "ok": self.close
            }
        )

        self.timer = eTimer()
        if isDreambox:
            self.timer_conn = self.timer.timeout.connect(self.startConnection)
        else:
            self.timer.callback.append(self.startConnection)
        self.onShow.append(self.startShow)
        self.onClose.append(self.delTimer)

    def startShow(self):
        self["lab1"].setText(_("Please wait, connecting to the server..."))
        self.timer.start(10)

    def startConnection(self):
        self.timer.stop()
        self["date"].setText(formatted_date)
        self.updateInfo()

    def updateInfo(self):
        myurl = "https://www.findyourfate.com/rss/horoscope-astrology.php"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(myurl, headers=headers)
            if response.status_code == 200:
                try:
                    xml_response = response.text
                    xml_response = removeAccents(xml_response)
                    dom = minidom.parseString(xml_response)
                    maintext = ""
                    zodiac = []
                    if dom:
                        zsign_items = ('title', 'description')
                        for zsign in dom.getElementsByTagName('item'):
                            tmp_zsign = {}
                            for tag in zsign_items:
                                try:
                                    element = zsign.getElementsByTagName(tag)
                                    if element and element[0].firstChild:
                                        tmp_zsign[tag] = element[0].firstChild.nodeValue.strip()
                                    else:
                                        tmp_zsign[tag] = ""
                                except Exception as e:
                                    print("Error extracting tag {}:".format(tag), e)
                                    tmp_zsign[tag] = ""
                            zodiac.append(tmp_zsign)
                        dom.unlink()

                        print("Zodiac signs found:", zodiac)
                        maintext = _("Today's Horoscope ")
                        idx = self.get_Sign()
                        title = str(idx)
                        self["lab2"].setText(title)
                        icon_name = idx[:3].lower()
                        icon_path = pluginpath + "/icons/" + icon_name + ".png"
                        if fileExists(icon_path):
                            png = LoadPixmap(icon_path)
                            self["lab3"].instance.setPixmap(png)
                        else:
                            print("[updateHoroscope] Icon no found:", icon_path)

                        found_sign = None
                        for sign in zodiac:
                            if sign['title'][:3].lower() == idx[:3].lower():
                                found_sign = sign
                                break
                        if found_sign:
                            description = found_sign['description']
                            pos = description.find('<a')
                            if pos != -1:
                                description = description[:pos]  # Rimuovi il link se presente
                            self["lab4"].setText(description)
                        else:
                            self["lab4"].setText(_("Sign not found"))

                    else:
                        maintext = "Error getting XML!"

                    self["lab1"].setText(maintext)

                except Exception as e:
                    print("Error parsing XML:", e)
                    return
            else:
                print("Error:", response.status_code)
                maintext = "Error: Page not available!"
                print(maintext)
                return

        except requests.exceptions.RequestException as e:
            print("Error connection:", e)
            maintext = "Error: Connection failed!"
            print(maintext)
            return

    def get_Sign(self):
        idx = 0
        cfgfile = pluginpath + "/" + "horoscope.cfg"
        if fileExists(cfgfile):
            with open(cfgfile, 'r') as f:
                line = f.readline()
                idx = str(line.strip())
        return idx

    def delTimer(self):
        del self.timer

    def key_green(self):
        box = self.session.open(MessageBox, INFO_RI, MessageBox.TYPE_INFO)
        box.setTitle(_("Information"))

    def key_red(self):
        self.session.openWithCallback(self.updateInfo, horoscopeSelectsign)


class horoscopeSelectsign(Screen):

    if isWQHD() or isFHD():
        skin = """
                <screen name="horoscopeSelectsign" position="center,center" size="1920,1080" backgroundColor="transparent" flags="wfNoBorder">
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/horoscope/backg.png" position="0,0" zPosition="-2" size="1920,1080" scale="fill" alphatest="blend" />
                    <ePixmap position="0,0" size="1920,1080" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/horoscope/backtr.png" scale="1" alphatest="blend" zPosition="-1" />
                    <eLabel backgroundColor="red" cornerRadius="3" position="34,1064" size="296,6" zPosition="11" />
                    <eLabel backgroundColor="green" cornerRadius="3" position="342,1064" size="300,6" zPosition="11" />
                    <!--
                    <eLabel backgroundColor="yellow" cornerRadius="3" position="652,1064" size="300,6" zPosition="11" />
                    <eLabel backgroundColor="blue" cornerRadius="3" position="962,1064" size="300,6" zPosition="11" />
                    -->
                    <widget name="key_red" render="Label" position="32,1016" size="300,45" zPosition="11" font="Regular; 30" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                    <widget name="key_green" render="Label" position="342,1016" size="300,45" zPosition="11" font="Regular; 30" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                    <!--
                    <widget name="key_yellow" render="Label" position="652,1016" size="300,45" zPosition="11" font="Regular; 30" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                    <widget name="key_blue" render="Label" position="962,1016" size="300,45" zPosition="11" font="Regular; 30" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                    -->
                    <widget name="date" position="585,90" halign="center" size="745,65" zPosition="5" font="Regular; 42" valign="center" transparent="1" />
                    <widget name="lab1" position="461,953" halign="center" size="1000,50" zPosition="5" font="Regular; 36" valign="center" transparent="1" />
                    <widget source="list" render="Listbox" position="710,205" size="500,720" scrollbarMode="showOnDemand" transparent="1" zPosition="5" foregroundColor="#00a0a0a0" foregroundColorSelected="#ffffff" backgroundColor="#20000000" backgroundColorSelected="#0b2049">
                        <convert type="TemplatedMultiContent">
                            {"template": [
                                MultiContentEntryText(pos=(0, 0), size=(500, 50), font=0, flags=RT_HALIGN_LEFT, text=0),  # Nome script
                                <!-- MultiContentEntryText(pos=(300, 0), size=(500, 50), font=0, flags=RT_HALIGN_RIGHT, text=1),  # Descrizione -->
                            ],
                            "fonts": [gFont("Regular", 34)],
                            "itemHeight": 45}
                        </convert>
                    </widget>
                </screen>"""

    elif isHD():
        skin = """
            <screen name="horoscopeSelectsign" position="center,center" size="1280,720" backgroundColor="transparent" flags="wfNoBorder">
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/horoscope/backg.png" position="0,0" zPosition="-2" size="1280,720" scale="fill" alphatest="blend" />
                <ePixmap position="0,0" size="1280,720" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/horoscope/backtr.png" scale="1" alphatest="blend" zPosition="-1" />
                <eLabel backgroundColor="red" cornerRadius="3" position="22,709" size="197,4" zPosition="11" />
                <eLabel backgroundColor="green" cornerRadius="3" position="228,709" size="200,4" zPosition="11" />
                <!--
                <eLabel backgroundColor="yellow" cornerRadius="3" position="434,709" size="200,4" zPosition="11" />
                <eLabel backgroundColor="blue" cornerRadius="3" position="641,709" size="200,4" zPosition="11" />
                -->
                <widget name="key_red" render="Label" position="21,677" size="200,30" zPosition="11" font="Regular; 20" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                <widget name="key_green" render="Label" position="228,677" size="200,30" zPosition="11" font="Regular; 20" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                <!--
                <widget name="key_yellow" render="Label" position="434,677" size="200,30" zPosition="11" font="Regular; 20" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                <widget name="key_blue" render="Label" position="641,677" size="200,30" zPosition="11" font="Regular; 20" valign="center" halign="center" backgroundColor="background" transparent="1" foregroundColor="white" />
                -->
                <widget name="date" position="290,60" halign="center" size="725,43" zPosition="5" font="Regular; 28" valign="center" transparent="1" />
                <widget name="lab1" position="290,630" halign="center" size="725,35" zPosition="5" font="Regular; 22" valign="top" transparent="1" />
                <widget source="list" render="Listbox" position="455,125" size="420,470" scrollbarMode="showOnDemand" transparent="1" zPosition="5" foregroundColor="#00a0a0a0" foregroundColorSelected="#ffffff" backgroundColor="#20000000" backgroundColorSelected="#0b2049">
                    <convert type="TemplatedMultiContent">
                        {"template": [
                            MultiContentEntryText(pos=(0, 0), size=(400, 33), font=0, flags=RT_HALIGN_LEFT, text=0),  # Nome script
                            <!-- MultiContentEntryText(pos=(200, 0), size=(333, 33), font=0, flags=RT_HALIGN_RIGHT, text=1),  # Descrizione -->
                        ],
                        "fonts": [gFont("Regular", 22)],
                        "itemHeight": 30}
                    </convert>
                </widget>
            </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)

        self.list = [
            (_("ARIES"), 0), (_("TAURUS"), 1), (_("GEMINI"), 2), (_("CANCER"), 3),
            (_("LION"), 4), (_("VIRGO"), 5), (_("LIBRA"), 6), (_("SCORPION"), 7),
            (_("SAGITTARIUS"), 8), (_("CAPRICORN"), 9), (_("AQUARIUS"), 10), (_("PISCES"), 11)
        ]

        self["list"] = List(self.list)
        self["lab1"] = Label(_("Select a Zodiac Sign"))
        self["date"] = Label("")
        self["date"].setText(formatted_date)
        self['key_red'] = Label(_('Close'))
        self['key_green'] = Label(_('Select'))

        self["actions"] = ActionMap(
            ["WizardActions", "ColorActions"],
            {
                "red": self.close,
                "green": self.saveCfg,
                "back": self.close,
                "ok": self.saveCfg
            }
        )

    def key_green(self):
        box = self.session.open(MessageBox, INFO_RI, MessageBox.TYPE_INFO)
        box.setTitle(_("Information"))

    def saveCfg(self):
        sign = self["list"].getCurrent()
        if sign:
            cfgfile = pluginpath + "/horoscope.cfg"
            try:
                with open(cfgfile, "w") as out:
                    out.write(str(sign[0]).lower())
            except (IOError, OSError) as e:
                print("[saveCfg] Error saving file: %s" % str(e))
        self.close()


def main(session, **kwargs):
    session.open(horoscopeMain)


def Plugins(path, **kwargs):
    global pluginpath
    pluginpath = path
    return PluginDescriptor(name=_("Horoscope"), description=_("Today's Horoscope "), icon="plugin.png", where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)
