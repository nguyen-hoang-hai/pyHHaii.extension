# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector, Grid, DatumEnds, DatumExtentType, Transaction,
    XYZ, Line, ViewType, Parameter, BuiltInParameter
)
from Autodesk.Revit.UI import *

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
view = doc.ActiveView

offset_mm_on_paper = 16.0

if view.ViewType == ViewType.ThreeD or not hasattr(view, "CropBox"):
    print("Chỉ áp dụng cho view 2D có crop box.")
else:
    t = Transaction(doc, "Auto Enable Crop View and Move Grid Head")
    t.Start()
    try:
        # Bật crop view nếu chưa bật
        crop_active_param = view.get_Parameter(BuiltInParameter.VIEWER_CROP_REGION)
        if crop_active_param and not crop_active_param.AsInteger():
            crop_active_param.Set(1)
        # Bật crop box visible nếu muốn (không bắt buộc)
        crop_visible_param = view.get_Parameter(BuiltInParameter.VIEWER_CROP_REGION_VISIBLE)
        if crop_visible_param and not crop_visible_param.AsInteger():
            crop_visible_param.Set(1)

        # Lấy lại crop box sau khi bật
        crop_box = view.CropBox
        min_pt = crop_box.Min
        max_pt = crop_box.Max

        view_scale = getattr(view, "Scale", 1)
        offset_mm_in_model = offset_mm_on_paper * view_scale
        offset_ft = offset_mm_in_model / 304.8

        def get_crop_intersections(start, end, min_pt, max_pt):
            intersections = []
            x1, y1 = start.X, start.Y
            x2, y2 = end.X, end.Y
            crop_edges = [
                ((min_pt.X, min_pt.Y), (max_pt.X, min_pt.Y)),  # bottom
                ((max_pt.X, min_pt.Y), (max_pt.X, max_pt.Y)),  # right
                ((max_pt.X, max_pt.Y), (min_pt.X, max_pt.Y)),  # top
                ((min_pt.X, max_pt.Y), (min_pt.X, min_pt.Y)),  # left
            ]
            for (x3, y3), (x4, y4) in crop_edges:
                denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
                if abs(denom) < 1e-9:
                    continue  # song song
                px = ((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4)) / denom
                py = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)) / denom
                if (min(x1, x2)-1e-7 <= px <= max(x1, x2)+1e-7 and
                    min(y1, y2)-1e-7 <= py <= max(y1, y2)+1e-7 and
                    min(x3, x4)-1e-7 <= px <= max(x3, x4)+1e-7 and
                    min(y3, y4)-1e-7 <= py <= max(y3, y4)+1e-7):
                    intersections.append(XYZ(px, py, start.Z))
            unique = []
            for pt in intersections:
                if not any((pt - u).GetLength() < 1e-7 for u in unique):
                    unique.append(pt)
            return unique

        grids = FilteredElementCollector(doc, view.Id).OfClass(Grid).ToElements()

        for grid in grids:
            grid.SetDatumExtentType(DatumEnds.End0, view, DatumExtentType.ViewSpecific)
            grid.SetDatumExtentType(DatumEnds.End1, view, DatumExtentType.ViewSpecific)

            curves = grid.GetCurvesInView(DatumExtentType.ViewSpecific, view)
            if not curves or len(curves) == 0:
                continue
            grid_curve = curves[0]
            start = grid_curve.GetEndPoint(0)
            end = grid_curve.GetEndPoint(1)
            direction = (end - start).Normalize()

            intersections = get_crop_intersections(start, end, min_pt, max_pt)
            if len(intersections) == 2:
                d0 = (intersections[0] - start).DotProduct(direction)
                d1 = (intersections[1] - start).DotProduct(direction)
                if d0 < d1:
                    crop_start, crop_end = intersections[0], intersections[1]
                else:
                    crop_start, crop_end = intersections[1], intersections[0]
            else:
                crop_start, crop_end = start, end

            new_start = crop_start - direction.Multiply(offset_ft)
            new_end = crop_end + direction.Multiply(offset_ft)

            if (new_start - new_end).GetLength() < 1e-6:
                continue

            new_curve = Line.CreateBound(new_start, new_end)
            grid.SetCurveInView(DatumExtentType.ViewSpecific, view, new_curve)

    except Exception as e:
        print(e)
    t.Commit()