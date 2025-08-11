# -*- coding: utf-8 -*-

# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# Revit Imports
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit import forms
from pyrevit.forms import ProgressBar

# Variables
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView

# Coding
grid_collector = FilteredElementCollector(doc, view.Id).OfClass(Grid).ToElements()
max_value = len(grid_collector)
t = Transaction(doc,"Change Grid To 3D")
t.Start()
with ProgressBar() as pb:
    for counter in range(0, max_value):
        pb.update_progress(counter, max_value)
        for grid in grid_collector:
            grid.SetDatumExtentType(DatumEnds.End0, view, DatumExtentType.Model)
            grid.SetDatumExtentType(DatumEnds.End1, view, DatumExtentType.Model)
t.Commit()