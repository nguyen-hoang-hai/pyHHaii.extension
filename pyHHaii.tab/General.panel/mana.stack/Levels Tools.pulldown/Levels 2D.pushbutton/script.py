# -*- coding: utf-8 -*-

# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# Revit Imports
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit.forms import ProgressBar

# Variables
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView

# Coding
levels_collector = FilteredElementCollector(doc, view.Id).OfClass(Level).ToElements()
max_value = len(levels_collector)
t = Transaction(doc,"Change Level 2D")
t.Start()
with ProgressBar() as pb:
    for counter in range(0, max_value):
        pb.update_progress(counter, max_value)
        for level in levels_collector:
            level.SetDatumExtentType(DatumEnds.End0,view,DatumExtentType.ViewSpecific)
            level.SetDatumExtentType(DatumEnds.End1,view,DatumExtentType.ViewSpecific)
t.Commit() 