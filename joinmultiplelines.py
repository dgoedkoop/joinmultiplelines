#-------------------------------------------------------------------------------
# Name:        joinmultiplelines
# Purpose:     Join multiple lines into one continuous line
#
# Author:      Daan Goedkoop
#
# Created:     26-04-2013
# Copyright:   (c) Daan Goedkoop 2013-2014
# Licence:     All rights reserved.
#
#              Redistribution and use in source and binary forms, with or
#              without modification, are permitted provided that the following
#              conditions are met:
#
#              - Redistributions of source code must retain the above copyright
#                notice, this list of conditions and the following disclaimer.
#              - Redistributions in binary form must reproduce the above
#                copyright notice, this list of conditions and the following
#                disclaimer in the documentation and/or other materials
#                provided with the distribution.
#
#              THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
#              CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#              INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#              MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#              DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#              CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#              SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#              LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
#              USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
#              AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#              LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#              IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
#              THE POSSIBILITY OF SUCH DAMAGE.
#
# Version 0.1: 26-04-2013
#              initial version
#         0.2: 29-04-2013
#              Produce valid geometry if begin and end vertices are identical.
#         0.3: 03-02-2014
#              Update for QGis 2.0
#              Operation is now a single undo/redo-step, instead of having a
#                  separate step for the removal of the superfluous features.
#-------------------------------------------------------------------------------

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar

# initialize Qt resources from file resouces.py
import resources

class joinmultiplelines:
    def __init__(self, iface):
        # save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        self.action = QAction(QIcon(":/plugins/joinmultiplelines/icon.png"), "Join multiple lines", self.iface.mainWindow())
        self.action.setWhatsThis("Permanently join multiple lines")
        self.action.setStatusTip("Permanently join multiple lines (removes lines used for joining)")

        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        if hasattr( self.iface, "addPluginToVectorMenu" ):
            self.iface.addVectorToolBarIcon(self.action)
            self.iface.addPluginToVectorMenu("&Join multiple lines", self.action)
        else:
            self.iface.addToolBarIcon(self.action)
            self.iface.addPluginToMenu("&Join multiple lines", self.action)

    def unload(self):
        if hasattr( self.iface, "addPluginToVectorMenu" ):
            self.iface.removePluginVectorMenu("&Join multiple lines",self.action)
            self.iface.removeVectorToolBarIcon(self.action)
        else:
            self.iface.removePluginMenu("&Join multiple lines",self.action)
            self.iface.removeToolBarIcon(self.action)

    def Distance(self, vertex1, vertex2):
        return vertex1.sqrDist(vertex2)

    def FirstVertex(self, geom):
        return geom.vertexAt(0)

    def LastVertexIndex(self, geom):
        return len(geom.asPolyline()) - 1

    def LastVertex(self, geom):
        return geom.vertexAt(self.LastVertexIndex(geom))

    # First: GEOM does not check for duplicate vertices or intersecting lines.
	# Second: QGis does, and simply uses '==' when comparing coordinates.
	# However, if we use '==' here too (likewise when using the '==' operator
	# for vertices), it will sometimes return "false" when the validity check
	# in QGis would return "true". That's the reason for this function.
    def PointEquality(self, vertex1, vertex2):
        return ((abs(vertex1.x() - vertex2.x()) < 0.000001) and
                (abs(vertex1.y() - vertex2.y()) < 0.000001))

    def Step(self, geom, queue_list):
        if geom is None:
            if len(queue_list) > 0:
                return queue_list.pop()
            else:
                return None
        base_firstvertex = self.FirstVertex(geom)
        base_lastvertex = self.LastVertex(geom)
        found_geom = None
        found_distance = 0
        for i_geom in queue_list:
            i_firstvertex = self.FirstVertex(i_geom)
            i_lastvertex = self.LastVertex(i_geom)
            distance_baselast_ifirst = self.Distance(base_lastvertex, i_firstvertex)
            distance_baselast_ilast = self.Distance(base_lastvertex, i_lastvertex)
            distance_basefirst_ifirst = self.Distance(base_firstvertex, i_firstvertex)
            distance_basefirst_ilast = self.Distance(base_firstvertex, i_lastvertex)
            distance = distance_baselast_ifirst
            base_reverse = False
            i_reverse = False
            if distance_baselast_ilast < distance:
                distance = distance_baselast_ilast
                base_reverse = False
                i_reverse = True
            if distance_basefirst_ifirst < distance:
                distance = distance_basefirst_ifirst
                base_reverse = True
                i_reverse = False
            if distance_basefirst_ilast < distance:
                distance = distance_basefirst_ilast
                base_reverse = True
                i_reverse = True
            if (found_geom is None) or (distance < found_distance):
                found_geom = i_geom
                found_distance = distance
                found_base_reverse = base_reverse
                found_i_reverse = i_reverse
        if found_geom is not None:
            queue_list.remove(found_geom)
            base_pts = geom.asPolyline()
            found_pts = found_geom.asPolyline()
            if found_base_reverse:
                base_pts.reverse()
            if found_i_reverse:
                found_pts.reverse()
            if self.PointEquality(base_pts[-1], found_pts[0]):
                base_pts.pop()
            base_pts.extend(found_pts)
            return QgsGeometry.fromPolyline(base_pts)
        else:
            return None

    def run(self):
        cl = self.iface.mapCanvas().currentLayer()

        if (cl == None):
            self.iface.messageBar().pushMessage("Join multiple lines","No layers selected", QgsMessageBar.WARNING, 10)
            return
        if (cl.type() != cl.VectorLayer):
            self.iface.messageBar().pushMessage("Join multiple lines","Not a vector layer", QgsMessageBar.WARNING, 10)
            return
        if cl.geometryType() != QGis.Line:
            self.iface.messageBar().pushMessage("Join multiple lines","Not a line layer", QgsMessageBar.WARNING, 10)
            return

        selfeats = cl.selectedFeatures()
        if (len(selfeats) < 2):
            self.iface.messageBar().pushMessage("Join multiple lines","At least two lines should be selected", QgsMessageBar.WARNING, 10)
            return

        geomlist = []
        for feat in selfeats:
            geom = QgsGeometry(feat.geometry())
            if geom.isMultipart():
                self.iface.messageBar().pushMessage("Join multiple lines","Multipart lines are not supported.", QgsMessageBar.WARNING, 10)
                return
            geomlist.append(geom)

        newgeom = None
        while len(geomlist) > 0:
            newgeom = self.Step(newgeom, geomlist)

        cl.startEditing()
        cl.beginEditCommand( "Join multiple lines" )
        cl.changeGeometry( selfeats[0].id(), newgeom )
#        cl.endEditCommand()
#        cl.beginEditCommand( "Delete feature" )
        for feat in selfeats:
            if feat != selfeats[0]:
                cl.deleteFeature( feat.id() )

        cl.endEditCommand()
        self.iface.mapCanvas().refresh()