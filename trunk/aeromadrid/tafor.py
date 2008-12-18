#!/usr/bin/env python
# coding=UTF-8
import xml.dom.minidom as minidom
import urllib, httplib2, sys
from mechanize import Browser
import mechanize as mech
import logging, sys
import httplib2
import wx
import ToasterBox as TB

def getTafor2(icao="lemd"):
	br = Browser()
	#response = br.submit()
	br.open("http://weather.noaa.gov/weather/taf.shtml")
	br.select_form(name="textbox")
	br["cccc"] = icao
	response = br.submit()
	print response.read()
	print response.info()
	ini = response.read().find('<pre>') + len('<pre>')
	fin = response.read().find('</pre>', ini)
	return response.read()[ini:fin]

def getTafor(icao="lemd"):
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	http = httplib2.Http()
	url = 'http://weather.noaa.gov/cgi-bin/mgettaf.pl'
	body = {'cccc':icao, 'Submit':'SUBMIT'}
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
	ini = content.find('<pre>') + len('<pre>')
	fin = content.find('</pre>', ini)
	return content[ini:fin]

class Popup(wx.Frame):
	def __init__(self, parent, id=wx.ID_ANY, title="ToasterBox Demo", pos = wx.DefaultPosition, size=(400,550)):
		wx.Frame.__init__(self, parent, id, title, pos, size)
		
	
	def showPopup(self, titulo, texto):
		tbstyle = TB.TB_SIMPLE
		#windowstyle = TB.TB_ONTIME
		windowstyle = TB.TB_ONCLICK
		#closingstyle = TB.TB_COMPLEX
		closingstyle = TB.TB_SIMPLE
		tb = TB.ToasterBox(self, tbstyle, windowstyle, closingstyle)
		tb.SetTitle(titulo)
		sizex = 200
		sizey = 200
		posx = wx.GetClientDisplayRect().GetWidth()-sizex
		posy = wx.GetClientDisplayRect().GetHeight()-sizey
		tb.SetPopupPosition((posx,posy))
		tb.SetPopupSize((sizex,sizey))
		tb.SetPopupText(texto)
		tb.SetPopupScrollSpeed(20)
		tb.SetPopupPauseTime(10000)
		tb.SetPopupBackgroundColor(wx.GREEN)
		tb.SetPopupTextColor(colour=wx.BLUE)
		#tb.SetPopupTextFont(None)
		#tb.SetPopupBitmap(bitmap=None)
		tb.Play()
	
	def run(self, titulo, texto):
		tbstyle = TB.TB_SIMPLE
		#windowstyle = TB.TB_ONTIME
		windowstyle = TB.TB_ONCLICK
		#closingstyle = TB.TB_COMPLEX
		closingstyle = TB.TB_SIMPLE
		tb = TB.ToasterBox(self, tbstyle, windowstyle, closingstyle)
		self.runner(tb, titulo, texto)
		tb.Play()
	
	def runner(self, tb, titulo, texto):
		tb.SetTitle('hola')
		sizex = 600
		sizey = 80
		posx = wx.GetClientDisplayRect().GetWidth()-sizex
		posy = wx.GetClientDisplayRect().GetHeight()-sizey
		tb.SetPopupPosition((posx,posy))
		tb.SetPopupSize((sizex,sizey))
		tb.SetPopupText(texto)
		tb.SetPopupScrollSpeed(20)
		tb.SetPopupPauseTime(10000)
		tb.SetPopupBackgroundColor(wx.GREEN)
		tb.SetPopupTextColor(colour=wx.BLUE)

def lanzarPopup(titulo, texto):
	app = wx.PySimpleApp()
	tbd = Popup(None)
	#tbd.showPopup(titulo, texto)
	tbd.run(titulo, texto)
	#tbd.Play()
	app.MainLoop()
	app.ExitMainLoop()
	#tbd.Show()

print getTafor()
tafor = getTafor()
# while tafor.find(' TEMPO') > -1:
	# tafor = tafor.replace('TEMPO', '\nTEMPO')
# print tafor
lanzarPopup('titulo', tafor)