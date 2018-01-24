# -*- coding: utf-8 -*-
def classFactory(iface):
  from .joinmultiplelines import joinmultiplelines
  return joinmultiplelines(iface)
