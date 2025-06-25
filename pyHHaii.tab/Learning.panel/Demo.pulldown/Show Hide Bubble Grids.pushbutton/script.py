# -*- coding: utf-8 -*-


# TODO: Import library and modules
import clr  # This is .NET's Common Language Runtime.
import System  # The System namespace at the root of .NET
import math  # Math library from Python
import string

from MainForm import MainForm
from Functions import filter_grids

from System.Collections.Generic import *  # Lets you handle generics.
from pyrevit import forms, revit, script

clr.AddReference('ProtoGeometry')  # A Dynamo library for its proxy geometry class
from Autodesk.DesignScript.Geometry import *  # Loads everything in Dynamo's

clr.AddReference("RevitAPI")  # Adding reference to Revit's API DLLs
clr.AddReference("RevitAPIUI")  # Adding reference to Revit's API DLLs

import Autodesk  # Loads the Autodesk namespace
from Autodesk.Revit.DB import *  # Loading Revit's API classes
from Autodesk.Revit.UI import *  # Loading Revit's API UI classes
from Autodesk.Revit.UI.Selection import ObjectType  # Import ObjectType to handle selection

clr.AddReference("RevitNodes")  # Dynamo's nodes for Revit
import Revit  # Loads in the Revit namespace in RevitNodes

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import \
    DocumentManager  # An internal Dynamo class that keeps track of the document that Dynamo is currently attached to
from RevitServices.Transactions import \
    TransactionManager  # A Dynamo class for opening and closing transactions to change the Revit document's database

# TODO: Prepare variable and input
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
DB = Autodesk.Revit.DB
output = script.get_output()
unit = doc.GetUnits()
version = int(app.VersionNumber)

"----------------------MAIN CODE----------------------------"
try:
    grid_activeview = FilteredElementCollector(doc, view.Id).OfClass(Grid).WhereElementIsNotElementType().ToElements()

    "----------------------------RUN FORMS----------------------------"
    f = MainForm()
    f.ShowDialog()
    "----------------------------ACTION----------------------------"
    if f.DialogResult == System.Windows.Forms.DialogResult.OK:
        # DATA FROM FORM
        left_box = f._LeftBox.Checked
        right_box = f._Rigthbox.Checked
        top_box = f._Topbox.Checked
        bot_box = f._Botbox.Checked

        hide_checked = f._hidebutton.Checked
        show_checked = f._showbutton.Checked

        vertical_grids, horizontal_grids = filter_grids(grid_activeview)

        with Transaction(doc, 'Show Hide Bubble') as t:
            t.Start()

            # Loop through horizontal grids
            for grid in horizontal_grids:
                curve = grid.Curve
                start_point = curve.GetEndPoint(0)  # End0 of the grid line
                end_point = curve.GetEndPoint(1)  # End1 of the grid line

                # Perform action based on direction (left/right)
                if show_checked:
                    if left_box:
                        if start_point.X < end_point.X:
                            grid.ShowBubbleInView(DatumEnds.End1, view)
                        if start_point.X > end_point.X:
                            grid.ShowBubbleInView(DatumEnds.End0, view)

                    if right_box:
                        if start_point.X > end_point.X:
                            grid.ShowBubbleInView(DatumEnds.End1, view)
                        if start_point.X < end_point.X:
                            grid.ShowBubbleInView(DatumEnds.End0, view)

                if hide_checked:
                    if left_box:
                        if start_point.X < end_point.X:
                            grid.HideBubbleInView(DatumEnds.End1, view)
                        if start_point.X > end_point.X:
                            grid.HideBubbleInView(DatumEnds.End0, view)

                    if right_box:
                        if start_point.X > end_point.X:
                            grid.HideBubbleInView(DatumEnds.End1, view)
                        if start_point.X < end_point.X:
                            grid.HideBubbleInView(DatumEnds.End0, view)

            # Loop through vertical grids
            for grid in vertical_grids:
                curve = grid.Curve
                start_point = curve.GetEndPoint(0)  # End0 of the grid line
                end_point = curve.GetEndPoint(1)  # End1 of the grid line

                # Perform action based on direction (top/bottom)
                if show_checked:
                    if top_box:
                        if start_point.Y < end_point.Y:
                            grid.ShowBubbleInView(DatumEnds.End0, view)
                        if start_point.Y > end_point.Y:
                            grid.ShowBubbleInView(DatumEnds.End1, view)

                    if bot_box:
                        if start_point.Y > end_point.Y:
                            grid.ShowBubbleInView(DatumEnds.End0, view)
                        if start_point.Y < end_point.Y:
                            grid.ShowBubbleInView(DatumEnds.End1, view)

                if hide_checked:
                    if top_box:
                        if start_point.Y < end_point.Y:
                            grid.HideBubbleInView(DatumEnds.End0, view)
                        if start_point.Y > end_point.Y:
                            grid.HideBubbleInView(DatumEnds.End1, view)

                    if bot_box:
                        if start_point.Y > end_point.Y:
                            grid.HideBubbleInView(DatumEnds.End0, view)
                        if start_point.Y < end_point.Y:
                            grid.HideBubbleInView(DatumEnds.End1, view)

            t.Commit()  # Commit the transaction to apply changes to the Revit model

except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))
