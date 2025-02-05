# main.py
import numpy as np
import matplotlib.pyplot as plt
from src.read_data import read_csv
from src.visualize import plot_shapes, plot_regularized_shapes
from src.regularize import regularize_shapes
from src.symmetry import detect_reflection_symmetry, detect_rotational_symmetry
from src.complete import complete_curve

def main():
    # Path to the input CSV file
    input_path = "data/examples/csv/isolated.csv"
    
    # Read the CSV file
    paths_XYs = read_csv(input_path)
    
    # Visualize the original shapes (non-blocking)
    plot_shapes(paths_XYs, title="Original Shapes", block=False)
    
    # Regularize the shapes
    regularized_shapes = regularize_shapes(paths_XYs)
    
    # Visualize the regularized shapes (non-blocking)
    plot_regularized_shapes(regularized_shapes, title="Regularized Shapes", block=False)
    
    # Detect symmetry in the regularized shapes
    for index, shape in enumerate(regularized_shapes):
        shape_type = shape[0]
        print(f"\nDetecting symmetry for {shape_type} #{index + 1}:")

        if shape_type == "line":
            print("  - (Skipped) Lines have infinite symmetry axes.")
            continue  # Skip lines
        
        elif shape_type == "circle":
            # Generate points on the circle's boundary
            center_x, center_y, radius = shape[1], shape[2], shape[3]
            angles = np.linspace(0, 2 * np.pi, 100)  # 100 points on the circle
            x = center_x + radius * np.cos(angles)
            y = center_y + radius * np.sin(angles)
            points = np.column_stack((x, y))  # Combine x and y into a 2D array
        
        elif shape_type == "rectangle":
            points = np.array(shape[1])  # Convert vertices to NumPy array
        
        else:
            continue  # Skip unsupported shapes
        
        # Detect reflection symmetry
        has_reflection, line_of_symmetry = detect_reflection_symmetry(points)
        if has_reflection:
            print(f"  - Reflection symmetry detected.\n  - Line of symmetry: {line_of_symmetry}")
        else:
            print("  - No reflection symmetry detected.")

        # Detect rotational symmetry
        has_rotation, angle_of_rotation = detect_rotational_symmetry(points)
        if has_rotation:
            print(f"  - Rotational symmetry detected.\n  - Angle of rotation: {angle_of_rotation}°")
        else:
            print("  - No rotational symmetry detected.")
    
    # Complete incomplete curves
    for index, shape in enumerate(regularized_shapes):
        if shape[0] == "line":
            continue  # Skip lines
        
        print(f"\nCompleting curve for {shape[0]} #{index + 1}:")
        if shape[0] == "circle":
            # Generate points on the circle's boundary
            center_x, center_y, radius = shape[1], shape[2], shape[3]
            angles = np.linspace(0, 2 * np.pi, 100)  # 100 points on the circle
            x = center_x + radius * np.cos(angles)
            y = center_y + radius * np.sin(angles)
            points = np.column_stack((x, y))  # Combine x and y into a 2D array
        elif shape[0] == "rectangle":
            points = np.array(shape[1])  # Convert vertices to NumPy array
        
        # Complete the curve
        completed_points = complete_curve(points)
        
        # Visualize the original and completed curves
        plt.figure()
        plt.plot(points[:, 0], points[:, 1], 'b-', label="Original")
        plt.plot(completed_points[:, 0], completed_points[:, 1], 'r--', label="Completed")
        plt.legend()
        plt.title(f"Completed Curve for {shape[0]} #{index + 1}")
        plt.show(block=False)
    
    # Keep the script running
    input("Press Enter to exit...")  # Wait for user input to exit

if __name__ == "__main__":
    main()