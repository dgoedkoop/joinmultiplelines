# -*- coding: utf-8 -*-
mVersion = "0.1"
def name():
  return "Join multiple lines"
def description():
  return "Permanently join multiple lines"
def category():
  return "Vector"
def qgisMinimumVersion():
  return "1.0"
def version():
  return mVersion
def authorName():
  return "Daan Goedkoop, dgoedkoop@gmx.net"
def icon():
  return "icon.png"
def classFactory(iface):
  from joinmultiplelines import joinmultiplelines
  return joinmultiplelines(iface)
