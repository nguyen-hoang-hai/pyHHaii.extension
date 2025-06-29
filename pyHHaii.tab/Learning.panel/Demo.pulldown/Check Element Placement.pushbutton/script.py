# -*- coding: utf-8 -*-
import clr
import os, csv, codecs, subprocess
from pyrevit import revit, DB, script, forms
from Autodesk.Revit.DB import *
from System.Collections.Generic import List
from pyrevit.forms import WPFWindow, save_file

doc = revit.doc
if doc.IsFamilyDocument:
    forms.alert("⚠️ This tool must be used in a project, not in Family Editor.", title="Wrong Context", exitscript=True)

class MainWindow(WPFWindow):
    def __init__(self, xaml_file):
        WPFWindow.__init__(self, xaml_file)
        self.all_links = list(FilteredElementCollector(revit.doc).OfClass(RevitLinkInstance))
        self.filtered_links = [l for l in self.all_links if "KDV" not in l.Name]
        self.link_listbox.ItemsSource = self.filtered_links
        self.link_listbox.DisplayMemberPath = 'Name'

        self.ok_button.Click += self.ok_click
        self.cancel_button.Click += self.cancel_click
        self.show_kdv.Checked += self.filter_links
        self.show_kdv.Unchecked += self.filter_links

        self.selected_links = []
        self.export_excel_result = True

    def filter_links(self, sender, e):
        if self.show_kdv.IsChecked:
            self.link_listbox.ItemsSource = self.all_links
        else:
            self.link_listbox.ItemsSource = [l for l in self.all_links if "KDV" not in l.Name]

    def ok_click(self, sender, e):
        self.selected_links = list(self.link_listbox.SelectedItems)
        self.export_excel_result = self.export_excel.IsChecked
        self.Close()

    def cancel_click(self, sender, e):
        self.selected_links = []
        self.Close()

xaml_path = os.path.join(os.path.dirname(__file__), 'UI.xaml')
form = MainWindow(xaml_path)
form.ShowDialog()

if not form.selected_links:
    script.exit()

selected_links = form.selected_links
export_excel = form.export_excel_result
export_path = None

if export_excel:
    export_path = save_file(file_ext='csv', default_name='MEP_Misplaced')
    if not export_path:
        export_excel = False
        forms.alert("⚠️ Export cancelled. No file will be saved.", title="Notice")

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

MEP_CATEGORIES = [
    BuiltInCategory.OST_LightingFixtures,
    BuiltInCategory.OST_LightingDevices,
    BuiltInCategory.OST_ElectricalFixtures,
    BuiltInCategory.OST_ElectricalEquipment,
    BuiltInCategory.OST_CommunicationDevices,
    BuiltInCategory.OST_TelephoneDevices,
    BuiltInCategory.OST_DataDevices,
    BuiltInCategory.OST_FireAlarmDevices
]

def get_elements_by_categories(doc, categories):
    return list(
        FilteredElementCollector(doc)
        .WherePasses(ElementMulticategoryFilter(List[BuiltInCategory](categories)))
        .WhereElementIsNotElementType()
    )

arch_bboxes = []
for link in selected_links:
    link_doc = link.GetLinkDocument()
    transform = link.GetTotalTransform()
    if link_doc:
        elements = get_elements_by_categories(link_doc, ARCH_CATEGORIES)
        for el in elements:
            bbox = el.get_BoundingBox(None)
            if bbox:
                min_pt = transform.OfPoint(bbox.Min)
                max_pt = transform.OfPoint(bbox.Max)
                outline = Outline(min_pt, max_pt)
                arch_bboxes.append(outline)

mep_elements = get_elements_by_categories(doc, MEP_CATEGORIES)

def bbox_intersects_any(mep_bbox, arch_outlines):
    if not mep_bbox:
        return False
    outline = Outline(mep_bbox.Min, mep_bbox.Max)
    for arch_outline in arch_outlines:
        if outline.Intersects(arch_outline, 0.01):
            return True
    return False

invalid_mep = []
for el in mep_elements:
    bbox = el.get_BoundingBox(None)
    if not bbox_intersects_any(bbox, arch_bboxes):
        level_name = doc.GetElement(el.LevelId).Name if el.LevelId != DB.ElementId.InvalidElementId else "N/A"
        invalid_mep.append((el, level_name))

if export_excel:
    def check_file_in_use(path):
        try:
            with open(path, 'a'):
                return False
        except IOError:
            return True

    csv_path = export_path if export_path else os.path.join(os.path.expanduser("~\Desktop"), "MEP_Misplaced.csv")

    if check_file_in_use(csv_path):
        forms.alert("🚫 Cannot write to '{}'.\nPlease close the file before running this tool.".format(csv_path),
                    title="File In Use", exitscript=True)

    f = codecs.open(csv_path, 'w', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(['Device Name', 'Element ID', 'Category', 'Level'])
    for el, level in invalid_mep:
        cat_name = el.Category.Name if el.Category else "Unknown"
        writer.writerow([el.Name, el.Id, cat_name, level])
    f.close()

    result = forms.alert("✅ Checked {0} MEP elements.\n🚫 {1} element(s) not properly placed.\n📄 CSV saved at:\n{2}".format(len(mep_elements), len(invalid_mep), csv_path), title="Finished", options=["OK", "Open Excel"])
    if result == "Open Excel":
        subprocess.Popen(csv_path, shell=True)
else:
    forms.alert("✅ Checked {0} MEP elements.\n🚫 {1} element(s) not properly placed.".format(len(mep_elements), len(invalid_mep)), title="Finished")
