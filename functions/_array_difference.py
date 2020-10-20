from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Custom')
def array_difference(array1, array2, feature, parent):
    """
    Zieht das zweite Array vom ersten Array ab, so dass im resultierenden Array nur Werte enthalten sind, die nicht im zweiten Array vorkommen.
    <br>
    <h2>Syntax</h2>
    array_difference(array1, array2)
    """
    return list(set(array1) - set(array2))
