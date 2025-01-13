# -*- coding: utf-8 -*-

from __future__ import absolute_import
__author__ = "Lululla"
__email__ = "ekekaz@gmail.com"
__copyright__ = 'Copyright (c) 2024 Lululla'
__license__ = "GPL-v2"
__version__ = "1.0.0"

from Components.Language import language
from enigma import getDesktop
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import gettext
import os


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