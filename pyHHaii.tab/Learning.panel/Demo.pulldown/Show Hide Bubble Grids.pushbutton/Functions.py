# -*- coding: utf-8 -*-

# TODO: Import library and modules
import clr  # This is .NET's Common Language Runtime.
import System  # The System namespace at the root of .NET
import math  # Math library from Python
import string


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


# TODO: Functions
def is_vertical(grid):
    """
    Determines if a grid line is vertical by checking its direction.
    """
    grid_curve = grid.Curve
    direction = grid_curve.Direction
    return abs(direction.X) < 0.01  # Tolerant check for vertical (close to Y axis)

def is_horizontal(grid):
    """
    Determines if a grid line is horizontal by checking its direction.
    """
    grid_curve = grid.Curve
    direction = grid_curve.Direction
    return abs(direction.Y) < 0.01  # Tolerant check for horizontal (close to X axis)


def filter_grids(grids):
    vertical_grids = []
    horizontal_grids = []

    for grid in grids:
        if is_vertical(grid):
            vertical_grids.append(grid)
        if is_horizontal(grid):
            horizontal_grids.append(grid)

    return vertical_grids,horizontal_grids


"----------------------Main Code----------------------------"
