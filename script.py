import clr

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('AdWindows')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReferenceByPartialName('System')
clr.AddReferenceByPartialName('System.Windows.Forms')

from Autodesk.Revit import DB
from Autodesk.Revit import UI
import Autodesk
import Autodesk.Windows as aw


clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

uiapp = __revit__
# uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = uiapp.ActiveUIDocument
doc = uiapp.ActiveUIDocument.Document

import sys
sys.path.append("C:\Users\dolan.klock\OneDrive - HOK\desktop\OneDrive Sharing\PythonResources\Revit")

from pyrevit import forms
import math
from GetSetParameters import *
from System.Collections.Generic import List
from pyrevit import *
import pyrevit
import Selection
import Schedules
from rpw import db
import csv
from pyrevit import UI
from pyrevit import script

clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')


# CODE BELOW HERE #

__author__ = "Dolan Klock"

# Tooltip
__doc__ = "This tool will delete filters not in use"

if __name__ == "__main__":
    all_filters = DB.FilteredElementCollector(doc).OfClass(DB.ParameterFilterElement)
    all_views = Selection.GetElementsFromDoc.all_views(doc, elements_only=True)
    delete_filters = []
    for filter in all_filters:
        in_use = False
        for view in all_views:
            if view.IsFilterApplied(filter.Id):
                in_use = True
                break
        if not in_use:
            delete_filters.append(filter)
    num_filters_purged = len(delete_filters)
    for filter in delete_filters:
        with db.Transaction("Delete filter"):
                doc.Delete(filter.Id)
    forms.alert("{} filters purged from model".format(num_filters_purged))
               










