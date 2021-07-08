# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterString,
                       QgsProject,
                       QgsRasterLayer)

class addWMSlayer(QgsProcessingAlgorithm):
    urlWithParams = 'urlWithParams'
    layername = 'layername'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return addWMSlayer()

    def name(self):
        return 'addWMSlayer'

    def displayName(self):
        return self.tr('WMS-Layer aus Modell hinzufügen')

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return ''

    def shortHelpString(self):
        return self.tr("Mit diesem Tool kann ein WMS-Layer aus einem QGIS Modell heraus hinzugefügt werden."+'\n'\
        +"Die für die Verwendung erforderliche 'URL/Parameter Zeichenkette' kann wie folgt erstellt werden:"+'\n'\
        +"1. WMS layer dem Projekt hinzufügen"+'\n'\
        +"2. Rechtsklick auf den Layer -> Eigenschaften"+'\n'\
        +"3. Im Reiter 'Information' findet sich die 'URL/Parameter Zeichenkette' unter 'Quelle'")

    def shortDescription(self):
        return self.tr("Mit diesem Tool kann ein WMS-Layer aus einem QGIS Modell heraus hinzugefügt werden")

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterString(
                name = self.urlWithParams,
                description  = self.tr('URL/Parameter Zeichenkette'),
                defaultValue  = 'crs=EPSG:25832&dpiMode=7&format=image/png&layers=adv_alkis_flurstuecke&styles&url=https://alkisservices.krzn.de/WMS_ALKIS_viersen/FlurkarteADV'
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                name = self.layername,
                description  = self.tr('Layername'),
                defaultValue  = 'Anzeigename des Layers im Layerfenster'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        urlWithParams = self.parameterAsString(parameters,self.urlWithParams,context)
        layername = self.parameterAsString(parameters,self.layername,context)

        rlayer = QgsRasterLayer(urlWithParams, layername, 'wms')

        QgsProject.instance().addMapLayer(rlayer)

        return {'WMS-Layer hinzugefügt': layername}