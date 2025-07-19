# -*- coding: utf-8 -*-
__title__ = "Export DWG (Sheets)"

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import ViewType
from Autodesk.Revit.UI import *

# pyRevit
from pyrevit import forms

# .NET Imports (You often need List import)
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
doc = __revit__.ActiveUIDocument.Document #type: Document

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝
#==================================================
class ViewWrapper(object):
    def __init__(self, view):
        self.view = view
        self.Name = "{} ({})".format(view.Name, view.ViewType.ToString()) 

    def __str__(self):
        return self.Name
    
# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================
# START CODE HERE
selected_sheets = forms.select_sheets()

if not selected_sheets:
    exitscript = True

if selected_sheets:
    dwg_options = DWGExportOptions()
    dwg_options.MergedViews = True
    output_folder = forms.pick_folder(title="Select Folder To Save DWG File")

    if not output_folder:
        exitscript = True
    exported_count = 0
    for sheet in selected_sheets:
        try:
            view_set = List[ElementId]()
            view_set.Add(sheet.Id)
            file_name = "{}.dwg".format(sheet.Name.replace(" ", "_"))
            doc.Export(output_folder, file_name, view_set, dwg_options)
            exported_count += 1
        except Exception as e:
            forms.alert("Please Select Folder To Save DWG File", exitscript=True)
    forms.alert("Done")    