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

# Coding
option = ViewScheduleExportOptions()
option.FieldDelimiter = ","

selected_schedules = forms.select_schedules()
if selected_schedules:
    save_folder = forms.pick_folder()
    if save_folder:
        max_value = len(selected_schedules)
        with ProgressBar() as pb:
            for counter in range (0, max_value):
                pb.update_progress(counter, max_value)
                for schedule in selected_schedules:
                        name = schedule.Name
                        schedule_name = name + ".csv"
                        schedule.Export(save_folder, schedule_name, option)
forms.alert("Complete")