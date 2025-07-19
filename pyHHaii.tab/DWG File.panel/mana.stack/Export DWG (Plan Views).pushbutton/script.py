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
from pyrevit import forms, script

# .NET Imports (You often need List import)
import clr
clr.AddReference("System")
from System.Collections.Generic import List
import re

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
        view_type_clean = re.sub(r"(\w)([A-Z])", r"\1 \2", view.ViewType.ToString())
        self.Name = "{} ({})".format(view.Name, view_type_clean)

    def __str__(self):
        return self.Name

def sanitize_filename(name):
    return re.sub(r'[\\/:*?"<>|]', "_", name)
    
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

selected_wrapped = forms.SelectFromList.show(wrapped_views,
                                          name_attr='Name',
                                          multiselect=True,
                                          title='Select Views')

if not selected_wrapped:
    script.exit()
    
selected_views = [vw.view for vw in selected_wrapped]

if selected_wrapped:
    dwg_options = DWGExportOptions()
    output_folder = forms.pick_folder(title="Select Folder To Save DWG File")

    if not output_folder:
        script.exit()
    exported_count = 0
    for view in selected_views:
        try:
            view_set = List[ElementId]()
            view_set.Add(view.Id)
            file_name = "{}.dwg".format(view.Name.replace(" ", "_"),sanitize_filename(view.Name))
            doc.Export(output_folder, file_name, view_set, dwg_options)
            exported_count += 1
        except Exception as e:
            forms.alert(str(e), exitscript=True)
    forms.alert("Done")    