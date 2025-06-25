# -*- coding: utf-8 -*-

# .Net Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# Revit Imports
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# Variables
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# Codes
collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
try:
    for elem in collector:
        print(elem.Name)
except AttributeError:
    print("Error")
