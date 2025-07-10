# -*- coding: utf-8 -*-
__title__ = "Change Workset"
__doc__ = """Version = 1.0
Date    = 10.07.2025
_____________________________________________________________________
Description:
This is a "Change Workset" tool based on my rule. If you want to use it with another rule, just update the logic.
_____________________________________________________________________
How-to:
-> Just click on the button.
_____________________________________________________________________
Last update:
- [10.07.2025] - 1.0 Release.
_____________________________________________________________________
Author: HHaii"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# pyRevit
from pyrevit import revit, forms

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
def select_element_of_category(doc, categories):
    if not isinstance(categories, list):
        categories = [categories]
    category_filter = [ElementCategoryFilter(cat) for cat in categories]

    category_multi_filter = LogicalOrFilter(category_filter)
    return FilteredElementCollector(doc).WherePasses(category_multi_filter).WhereElementIsNotElementType().ToElements()

def change_workset(workset, ws_name, ws_elem):
    ws_id = None
    for ws in workset:
        if ws.Name == ws_name:
            ws_id = ws.Id
            break
    if ws_id is None:
        print("{} is not existing".format(ws_name))  
        return

    t = Transaction(doc,"Change Workset")
    t.Start()
    for elem in ws_elem:
        param = elem.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
        if param and not param.IsReadOnly:
            param.Set(ws_id.IntegerValue)
    t.Commit()

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================
# START CODE HERE
ws_power_equipment  = "KDV_E_POWER_EQUIPMENT"
ws_cable_tray       = "KDV_E_CABLE TRAY"
ws_socket           = "KDV_E_SOCKET"
ws_elv              = "KDV_E_ELV"
ws_lighting         = "KDV_E_LTG"
ws_exit_emergency   = "KDV_E_EMER_LTG"

categories_ws_power_equipment   = [BuiltInCategory.OST_ElectricalEquipment]
categories_ws_cable_tray        = [BuiltInCategory.OST_CableTray,
                                   BuiltInCategory.OST_CableTrayFitting]
categories_ws_socket            = [BuiltInCategory.OST_ElectricalFixtures]
categories_ws_elv               = [BuiltInCategory.OST_CommunicationDevices,
                                   BuiltInCategory.OST_DataDevices,
                                   BuiltInCategory.OST_TelephoneDevices,
                                   BuiltInCategory.OST_FireAlarmDevices]
categories_ws_lighting_vs_exit_emergency = [BuiltInCategory.OST_LightingFixtures,
                                            BuiltInCategory.OST_LightingDevices]

power_equipment = select_element_of_category(doc, categories_ws_power_equipment)
cable_tray      = select_element_of_category(doc, categories_ws_cable_tray)
socket          = select_element_of_category(doc, categories_ws_socket)
elv             = select_element_of_category(doc, categories_ws_elv)
lighting_vs_exit_emergency = select_element_of_category(doc, categories_ws_lighting_vs_exit_emergency)

user_ws = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()

change_workset(user_ws, ws_power_equipment, power_equipment)

cable_tray_ltg = []
cable_tray_others = []

for elem in cable_tray:
    elem_type = doc.GetElement(elem.GetTypeId())
    type_name = elem_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    if type_name and "ltg" in type_name.lower():
        cable_tray_ltg.append(elem)
    else:
        cable_tray_others.append(elem)

change_workset(user_ws, ws_cable_tray, cable_tray_others)
change_workset(user_ws, ws_lighting, cable_tray_ltg)
change_workset(user_ws, ws_socket, socket)
change_workset(user_ws, ws_elv, elv)

lighting = []
exit_emergency = []

for elem in lighting_vs_exit_emergency:
    try:
        family_name = elem.Symbol.Family.Name.lower()
    except:
        family_name = ""

    if "exit" in family_name or "emergency" in family_name:
        exit_emergency.append(elem)
    else:
        lighting.append(elem)

change_workset(user_ws, ws_lighting, lighting)
change_workset(user_ws, ws_exit_emergency, exit_emergency)

forms.alert("Complete")