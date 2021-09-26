##
## Picon renderer by Gruffy .. some speedups by Ghost
## Moded by Raver(XX)
##
from Renderer import Renderer
from enigma import ePixmap
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename

import os

class LcdPicon(Renderer):
#	searchPaths = ('/usr/share/enigma2/%s/',
#				'/media/sda1/%s/',
#				'/media/USB/%s/')
# 1_0_19_2460_440_1_C00000_0_0_0
	def __init__(self):
		Renderer.__init__(self)
		self.path = "piconlcd"
		self.nameCache = { }
		self.pngname = ""
		
		pfad = "/media/"
		dirs = os.listdir(pfad)
		dirs.sort()
		self.searchPaths = []
		self.searchPaths.append('/usr/share/enigma2/%s/')
		for dir in dirs:
			p = pfad + dir
			if os.path.ismount(p):
				self.searchPaths.append(p + "/%s/")
		
	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "path":
				self.path = value
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			pngname = ""
			if what[0] != self.CHANGED_CLEAR:
				sname = self.source.text
				# strip all after last :
				pos = sname.rfind(':')
				if pos != -1:
					sname = sname[:pos].rstrip(':').replace(':','_')
				pngname = self.nameCache.get(sname, "")
				if pngname == "":
					pngname = self.findPicon(sname)
					if pngname != "":
						self.nameCache[sname] = pngname

			if pngname == "": # no picon for service found, trying to change channel reference => 1_0_19_2460_440_1_C00000_0_0_0 to 1_0_1_2460_440_1_C00000_0_0_0
				sname = "1_0_1" + sname[sname.index('_',4):]	
				pngname = self.nameCache.get(sname, "")
				if pngname == "":
					pngname = self.findPicon(sname)
					if pngname != "":
						self.nameCache[sname] = pngname									
			if pngname == "": # no picon for service found
				pngname = self.nameCache.get("default", "")
				if pngname == "": # no default yet in cache..
					pngname = self.findPicon("picon_default")
					if pngname == "":
						tmp = resolveFilename(SCOPE_CURRENT_SKIN, "picon_default.png")
						if fileExists(tmp):
							pngname = tmp
						else:
							pngname = resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/picon_default.png")
					self.nameCache["default"] = pngname
			if self.pngname != pngname:
				self.instance.setPixmapFromFile(pngname)
				self.pngname = pngname

	def findPicon(self, provider):
		for path in self.searchPaths:
			pngname = (path % self.path) + provider + ".png"
			if fileExists(pngname):
				return pngname
		return ""


