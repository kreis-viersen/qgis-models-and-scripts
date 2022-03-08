# -*- coding: utf-8 -*-

"""
***************************************************************************
Verbindungen im QGIS-Browser löschen
QGIS-Skript

        Date                 : March 2022
        Copyright            : (C) 2022 by Kreis Viersen
        Email                : open@kreis-viersen.de

***************************************************************************

***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterEnum)

from qgis.PyQt.QtCore import QSettings
from qgis.utils import iface

class deleteBrowserConnections(QgsProcessingAlgorithm):
    connections = ['ArcGIS-REST-Server','Vector Tiles','WCS','WFS / OGC API - Features','WMS / WMTS','XYZ Tiles']
    connectionsId = ['arcgisfeatureserver','vector-tile','wcs','wfs','wms','xyz']
    connectionsId2 = ['ARCGISFEATURESERVER','WCS','WFS','WMS']

    def createInstance(self):
        return deleteBrowserConnections()

    def name(self):
        return 'deleteBrowserConnections'

    def displayName(self):
        return 'Verbindungen im QGIS-Browser löschen'

    def group(self):
        return self.groupId()

    def groupId(self):
        return ''

    def shortHelpString(self):
        return "Mit diesem Tool können Verbindungen im QGIS-Browser gelöscht werden."+'\n'\
        +'\n'\
        +"Für gewählte Verbindungstypen werden ALLE selbst hinzugefügten Verbindungen dauerhaft gelöscht!"

    def shortDescription(self):
        return "Mit diesem Tool können Verbindungen im QGIS-Browser gelöscht werden."

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterEnum(
            name = 'connectionsToDelete',
            description = 'Verbindungen im QGIS-Browser löschen',
            options= self.connections,
            allowMultiple=True,
            usesStaticStrings=False
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        input = self.parameterAsEnums(parameters,'connectionsToDelete',context)

        outputList = []

        settings = QSettings()

        for i in input:
            connection = self.connectionsId[i]
            connectionUpperCase = connection.upper()

            settings.beginGroup('qgis/connections-' + connection)
            settings.remove("")
            settings.endGroup()

            # for some connection types some information is stored differently
            if connectionUpperCase in self.connectionsId2:
                settings.beginGroup('qgis/' + connectionUpperCase)
                settings.remove("")
                settings.endGroup()

            outputList.append(self.connections[i])

        iface.reloadConnections()

        return {'Folgende Verbindungen wurden gelöscht': outputList}