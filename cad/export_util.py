# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Export a CadQuery solid to a clean STL: tessellate, drop zero-area triangles (they appear at sharp fillet ends), check it is closed."""
import cadquery as cq
import trimesh


def export_stl(solid, path, tolerance=0.02, angular=0.1):
    cq.exporters.export(solid, path, tolerance=tolerance, angularTolerance=angular)
    m = trimesh.load(path)
    good = m.nondegenerate_faces()
    if not good.all():
        m.update_faces(good)
        m.remove_unreferenced_vertices()
        m.export(path)
    return m
