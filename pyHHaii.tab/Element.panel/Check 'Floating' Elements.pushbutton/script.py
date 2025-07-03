# -*- coding: utf-8 -*-
__title__ = "Check 'Floating' Elements"

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# pyRevit
from pyrevit import forms

# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
uidoc = __revit__.ActiveUIDocument
doc   = __revit__.ActiveUIDocument.Document #type: Document

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝
#==================================================
def get_element_by_categories(doc, category):
    categories = list[BuiltInCategory]()
    for cat in category:
        categories.append(cat)
    return(FilteredElementCollector(doc).WherePasses(ElementMulticategoryFilter(categories)).WhereElementIsNotElementType())

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================
# START CODE 

# Lấy toàn bộ file Revit Link có trong mô hình
link_instances = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

# Lấy Category trong File Link
ARCH_CATEGORIES = [
    BuiltInCategory.OST_Walls,
    BuiltInCategory.OST_StructuralColumns,
    BuiltInCategory.OST_Ceilings,
    BuiltInCategory.OST_Floors,
    BuiltInCategory.OST_GenericModel,
    BuiltInCategory.OST_Columns,
    BuiltInCategory.OST_StructuralFraming,
    BuiltInCategory.OST_Roofs,
    BuiltInCategory.OST_StructuralFoundation
]
# Lấy Category trong File hiện tại
ELECTRICAL_CATEGORIES = [
    BuiltInCategory.OST_LightingFixtures,
    BuiltInCategory.OST_LightingDevices,
    BuiltInCategory.OST_ElectricalFixtures,
    BuiltInCategory.OST_ElectricalEquipment,
    BuiltInCategory.OST_CommunicationDevices,
    BuiltInCategory.OST_TelephoneDevices,
    BuiltInCategory.OST_DataDevices,
    BuiltInCategory.OST_FireAlarmDevices
]

selected_link = forms.SelectFromList.show(link_instances,
                                          name_attr='Name',
                                          multiselect=True,
                                          title='Select Revit Links')

if selected_link:
    target_folder = forms.pick_folder()
    if target_folder:
        arch_bboxes = []
        for link in selected_link:
            link_doc = link.GetLinkDocument()
            link_transform = link.GetTotalTransform()
            if link_doc:
                arch_elements = get_element_by_categories(doc, ARCH_CATEGORIES)
                for elem in arch_elements:
                    bbox = elem.get_BoundingBox(None)