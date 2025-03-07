# -*- coding: utf-8 -*-

from __future__ import absolute_import
__author__ = "Lululla"
__email__ = "ekekaz@gmail.com"
__copyright__ = 'Copyright (c) 2024 Lululla'
__license__ = "GPL-v2"
__version__ = "1.0.0"

from Components.Language import language
from enigma import (
	RT_HALIGN_RIGHT,
	RT_HALIGN_LEFT,
	getDesktop,
)
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import gettext
import os
import sys

global HALIGN
HALIGN = RT_HALIGN_LEFT
plugin_path = os.path.dirname(sys.modules[__name__].__file__)

PluginLanguageDomain = 'horoscope'
PluginLanguagePath = 'Extensions/horoscope/locale'


isDreambox = False
if os.path.exists("/usr/bin/apt-get"):
	isDreambox = True


def getDesktopSize():
	s = getDesktop(0).size()
	return (s.width(), s.height())


def isWQHD():
	desktopSize = getDesktopSize()
	return desktopSize[0] >= 2560


def isFHD():
	desktopSize = getDesktopSize()
	return desktopSize[0] >= 1920


def isHD():
	desktopSize = getDesktopSize()
	return desktopSize[0] <= 1280


def localeInit():
	if isDreambox:
		lang = language.getLanguage()[:2]
		os.environ["LANGUAGE"] = lang
	gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))


if isDreambox:
	def _(txt):
		return gettext.dgettext(PluginLanguageDomain, txt) if txt else ""
else:
	def _(txt):
		translated = gettext.dgettext(PluginLanguageDomain, txt)
		if translated:
			return translated
		else:
			print(("[%s] fallback to default translation for %s" % (PluginLanguageDomain, txt)))
			return gettext.gettext(txt)

localeInit()
language.addCallback(localeInit)


# language
locl = "ar", "ae", "bh", "dz", "eg", "in", "iq", "jo", "kw", "lb", "ly", "ma", "om", "qa", "sa", "sd", "ss", "sy", "tn", "ye"
global lngx
lngx = 'en'
try:
	from Components.config import config
	lngx = config.osd.language.value
	lngx = lngx[:-3]
except:
	lngx = 'en'
	pass


def add_skin_font():
	global HALIGN
	from enigma import addFont
	from os import path as os_path
	FNTPath = os_path.join(plugin_path + "/fonts")
	# print('FNTPath=', FNTPath)
	# addFont(filename, name, scale, isReplacement, render)
	if any(s in lngx for s in locl):
		HALIGN = RT_HALIGN_RIGHT
		# addFont((FNTPath + '/NotoSansArabic.ttf'), 'lsat', 100, 1)
		addFont((FNTPath + '/DejaVuSans.ttf'), 'lsat', 100, 1)
	else:
		addFont((FNTPath + '/DejaVuSans.ttf'), 'lsat', 100, 1)


def checkGZIP(url):
	from io import BytesIO  # Usa BytesIO per la compatibilità
	import gzip
	import requests
	import sys
	if sys.version_info[0] == 3:
		from urllib.request import urlopen, Request
	else:
		from urllib2 import urlopen, Request
	AgentRequest = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3'
	hdr = {"User-Agent": AgentRequest}
	response = None
	request = Request(url, headers=hdr)
	try:
		response = urlopen(request, timeout=10)
		if response.info().get('Content-Encoding') == 'gzip':
			buffer = BytesIO(response.read())  # Leggi i dati in un buffer di byte
			with gzip.GzipFile(fileobj=buffer) as deflatedContent:  # Decomprimi i dati
				if sys.version_info[0] == 3:
					return deflatedContent.read().decode('utf-8')  # Decodifica in utf-8 per Python 3
				else:
					return deflatedContent.read()  # Ritorna i byte per Python 2
		else:
			if sys.version_info[0] == 3:
				return response.read().decode('utf-8')  # Decodifica per Python 3
			else:
				return response.read()  # Ritorna i byte per Python 2
	except requests.exceptions.RequestException as e:
		print("Request error:", e)
	except Exception as e:
		print("Unexpected error:", e)
	return None
