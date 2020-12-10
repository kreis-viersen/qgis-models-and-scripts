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
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterString,
                       QgsProcessingFeedback,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterField,
                       QgsProcessingParameterVectorLayer)
from qgis import (processing,utils)
from qgis.core import (QgsMessageLog,QgsProject)

class alleLayerFilter(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    FINPUT = 'FINPUT'
    FILTER = 'FILTER'
    FILTERATT = 'FILTERATT'
    OPERATOR = 'OPERATOR'
    OPERATORX = 'OPERATORX'   
    OPERATORS  = ['=','!=']
    OPERATORSX  = ['AND','OR']
    METHODE = 'METHODE'
    METHODES = ['0','1']
    
    def tr(self, string):        
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return alleLayerFilter()

    def name(self):        
        return 'alleLayerFilter'

    def displayName(self):        
        return self.tr('Layer filtern')

    
    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return ''

    def shortHelpString(self):        
        return self.tr("Mit diesem Script können mehrere Layer gefiltert werden")
    
    def shortDescription(self):
        return self.tr("Mit diesem Script können mehrere Layer gefiltert werden")
    
    def initAlgorithm(self, config=None):
        self.operators = ['=','≠']
        self.operatorsX = ['AND','OR']
        self.methoden = ['Filtern','Filter Löschen']
        
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                name = self.INPUT,
                description  = self.tr('Input Layer'),
                layerType = QgsProcessing.TypeVectorAnyGeometry
            )
        )
        
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                name = self.FINPUT,
                description  = self.tr('Mit Feldern dieses Layers filtern')
            )
        )
        
        
        self.addParameter(
            QgsProcessingParameterField(
                name = self.FILTERATT,
                description  = self.tr('Filter Attribut'),
                defaultValue = "",
                parentLayerParameterName = self.FINPUT,
                optional = 1
            )
        ) 
        
        
        self.addParameter(
            QgsProcessingParameterString(
                name = self.FILTER,
                description  = self.tr('Filter Werte'),
                optional = 1
            )
        )      
       
        
        self.addParameter(
            QgsProcessingParameterEnum(
            name = self.OPERATOR,
            description  = self.tr('Vergleich Operator'),
            options = self.operators,
            allowMultiple = False,
            defaultValue=1
            )
        )     
        
        self.addParameter(
            QgsProcessingParameterEnum(
            name = self.OPERATORX,
            description  = self.tr('Logischer Operator'),
            options = self.operatorsX,
            allowMultiple = False,
            defaultValue=1
            )
        )
        
        self.addParameter(
            QgsProcessingParameterEnum(
            name = self.METHODE,
            description  = self.tr('Methode'),
            options = self.methoden,
            defaultValue = 0
            )
        )

    def processAlgorithm(self, parameters, context, feedback):        
        
        sourceLayer = self.parameterAsLayerList(parameters,self.INPUT,context)
        methode = self.parameterAsEnum(parameters, self.METHODE, context)        
        
        if methode == 0:        
                    
            filterValues = self.parameterAsMatrix(parameters,self.FILTER,context)
            filterOpLog = self.OPERATORS[self.parameterAsEnum(parameters, self.OPERATOR, context)]
            filterOpCon = self.OPERATORSX[self.parameterAsEnum(parameters, self.OPERATORX, context)]
            filterAtt = self.parameterAsString(parameters,self.FILTERATT,context)   
            
            count = 0
            countMax = len(filterValues)
            while count < countMax:
                if count == 0:
                    filterListe = '"'+filterAtt+'"'+ filterOpLog +'\''+filterValues[0]+'\' '
                else:
                    filterListe = filterListe +filterOpCon+ ' "'+filterAtt+'"'+ filterOpLog +'\''+filterValues[count]+'\' ' 
                count=count+1
                    
            for layer in sourceLayer:
                layer.setSubsetString(filterListe) 
           
            return {self.FILTER: filterValues}
        
        if methode == 1:
            for layer in sourceLayer:
                    layer.setSubsetString('') 
            return {self.METHODE: methode}
