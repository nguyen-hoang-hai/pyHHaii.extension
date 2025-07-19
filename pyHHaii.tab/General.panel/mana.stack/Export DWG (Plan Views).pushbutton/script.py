# -*- coding: utf-8 -*-
__title__ = "Export DWG (Plan Views)"

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
all_views = FilteredElementCollector(doc).OfClass(View).ToElements()
plan_views = [v for v in all_views if v.ViewType in (
    ViewType.FloorPlan,
    ViewType.CeilingPlan
) and not v.IsTemplate]
wrapped_views = [ViewWrapper(v) for v in plan_views]

selected_views = forms.SelectFromList.show(wrapped_views,
                                          name_attr='Name',
                                          multiselect=True,
                                          title='Select Views')

if not selected_views:
    forms.alert("No view selected. Script will now exit.", exitscript=True)

if selected_views:
    dwg_options = DWGExportOptions()
    output_folder = forms.pick_folder(title="Select Folder To Save DWG File")

    if not output_folder:
        script.exit()
    exported_count = 0
    for view in selected_views:
        try:
            view_set = List[ElementId]()
            view_set.Add(view.Id)
            file_name = "{}.dwg".format(view.Name.replace(" ", "_"))
            doc.Export(output_folder, file_name, view_set, dwg_options)
            exported_count += 1
        except Exception as e:
            forms.alert("Error", exitscript=True)
    forms.alert("Done")    