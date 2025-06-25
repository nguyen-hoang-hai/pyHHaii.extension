# -*- coing: utf-8 -*-

# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# Revit Imports
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# Variables
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

output = script.get_output()

# Coding
get_rvt_links = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
try:
    for elem in get_rvt_links:
        print(elem.Name)
except AttributeError:
    print("Error")
