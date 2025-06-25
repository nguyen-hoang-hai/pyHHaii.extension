# -*- coding: utf-8 -*-

# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# Revit Imports
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

# Variables
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document # Type: Document
selection = uidoc.Selection # Type: Selection

# Coding
class FileCADSelection(ISelectionFilter):
    def AllowElement(self, elem):
        return isinstance(elem, ImportInstance)
try:    
    cad_ref = selection.PickObject(ObjectType.Element, FileCADSelection())
    cad_elem = doc.GetElement(cad_ref.ElementId)
    print(cad_elem.Name)
except Exception as e:
    print(e)
