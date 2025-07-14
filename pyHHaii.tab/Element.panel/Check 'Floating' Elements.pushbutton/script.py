# -*- coding: utf-8 -*-
__title__ = "Check 'Floating' Elements"

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit import *

# pyRevit
from pyrevit import forms

# .NET Imports
import os, csv, codecs
import subprocess
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
doc   = __revit__.ActiveUIDocument.Document #type: Document

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝
#==================================================
def get_element_by_categories(doc, categories):
    bic_list = List[BuiltInCategory]()
    for cat in categories:
        bic_list.Add(cat)
    return FilteredElementCollector(doc).WherePasses(ElementMulticategoryFilter(bic_list)).WhereElementIsNotElementType()

def bbox_intersects_any(mep_bbox, arch_outlines):
    if not mep_bbox:
        return False
    outline = Outline(mep_bbox.Min, mep_bbox.Max)
    for arch_outline in arch_outlines:
        if outline.Intersects(arch_outline, 0.01):
            return True
    return False

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

selected_links = forms.SelectFromList.show(link_instances,
                                          name_attr='Name',
                                          multiselect=True,
                                          title='Select Revit Links')

if not selected_links:
    forms.alert("No links selected. Script will now exit.", exitscript=True)

target_folder = forms.pick_folder(title="Pick folder to save results")
if not target_folder:
    forms.alert("No folder selected. Script will now exit.", exitscript=True)

arch_bboxes = []
for link in selected_links:
    link_doc = link.GetLinkDocument()
    link_transform = link.GetTotalTransform()
    if link_doc:
        arch_elements = get_element_by_categories(link_doc, ARCH_CATEGORIES)
        for elem in arch_elements:
            bbox = elem.get_BoundingBox(None)
            if bbox:
                min_pt = link_transform.OfPoint(bbox.Min)
                max_pt = link_transform.OfPoint(bbox.Max)
                outline = Outline(min_pt, max_pt)
                arch_bboxes.append(outline)

electrical_elements = get_element_by_categories(doc, ELECTRICAL_CATEGORIES)

invalid_mep = []
for el in electrical_elements:
    bbox = el.get_BoundingBox(None)
    if not bbox_intersects_any(bbox, arch_bboxes):
        level_name = doc.GetElement(el.LevelId).Name if el.LevelId != ElementId.InvalidElementId else "N/A"
        invalid_mep.append((el, level_name))

# Export CSV
if invalid_mep:
    filename = os.path.join(target_folder, "Floating_MEP_Elements.csv")
    try:
        with codecs.open(filename, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Element Name', 'Element ID', 'Category', 'Level'])
            for el, level in invalid_mep:
                cat_name = el.Category.Name if el.Category else "Unknown"
                writer.writerow([el.Name, el.Id, cat_name, level])
        
        forms.alert("Found {} floating MEP elements.\nResults saved to:\n{}".format(len(invalid_mep), filename),
                    title="Check Complete")

        # Tự động mở file CSV bằng Excel (nếu có cài Excel)
        subprocess.Popen(filename, shell=True)
        
    except Exception as e:
        forms.alert("Failed to write file:\n{}".format(str(e)), exitscript=True)
else:
    forms.alert("All MEP elements are properly placed within architectural bounding boxes.", title="Check Complete")