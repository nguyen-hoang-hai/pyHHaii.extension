# -*- coding: utf-8 -*-

# .Net Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# Revit Imports
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.Exceptions import OperationCanceledException

# Variables 
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document # Type: Document
selection = uidoc.Selection # Type: Selection

# Coding
try:
    ref_pickobjects = selection.PickObjects(ObjectType.Element)
    pickobjects = [doc.GetElement(ref) for ref in ref_pickobjects]
    #Diễn giải cách trên đơn giản hơn theo từng bước
    """
    pickobjects = []
    for ref in ref_pickobjects:
    elem = doc.GetElement(ref)
    pickobjects.append(elem)
    """
    for ob in pickobjects:
        print(ob.Name)
except OperationCanceledException:
    print("Ban Da Bam Cancel")
except Exception:
    print("Bi Loi Rui Nhe")
