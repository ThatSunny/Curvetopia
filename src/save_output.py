# src/save_output.py
import svgwrite
import numpy as np

def save_to_svg(shapes, output_path):
    """Saves regularized shapes to an SVG file as Bézier curves."""
    dwg = svgwrite.Drawing(output_path, profile='full')

    for shape in shapes:
        shape_type = shape[0]
        if shape_type == "circle":
            center_x, center_y, radius = shape[1], shape[2], shape[3]
            circle = dwg.circle(center=(center_x, center_y), r=radius, fill='none', stroke='black')
            dwg.add(circle)
        elif shape_type == "rectangle":
            points = np.array(shape[1])
            polygon = dwg.polygon(points=points.tolist(), fill='none', stroke='black')  # points must be a list
            dwg.add(polygon)

    dwg.save()