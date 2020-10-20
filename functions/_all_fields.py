from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Custom')
def all_fields(layer, feature, parent):
    """
    Erstellt ein Array mit den Feldern(Spalten) eines Layers
    <br>
    <h2>Syntax</h2>
    all_fields(layer)
    """
    provider = layer.dataProvider()
    field_names = [field.name() for field in provider.fields()]
    return field_names
