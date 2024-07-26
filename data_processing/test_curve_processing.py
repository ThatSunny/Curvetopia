import numpy as np
from curve_processing import segment_curve
from symmetry_detection import has_reflection_symmetry, has_rotational_symmetry
from curve_completion import complete_curve_symmetry, complete_curve_interpolation, complete_curve_extrapolation
import visualization


# Add visualization to the test function
def test_curve_completion():
    # Define test cases with known inputs and expected outputs
    test_cases = [
        {
            "input": np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]),
            "expected_symmetry": [],  # No symmetry expected
            "expected_completion": np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])  # Should return the same
        },
        {
            "input": np.array([[0, 0], [1, 1], [2, 2], [3, 3]]),
            "expected_symmetry": [((0, 0), (3, 3))],  # Expect symmetry along the diagonal
            "expected_completion": np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5]])
        },
        # Add more test cases as needed
    ]

    # Run tests
    for i, test in enumerate(test_cases):
        print(f"Running test case {i+1}")

        # Run segmentation (adjust threshold as needed)
        segments = segment_curve(test["input"], segment_length_threshold=2)

        # Detect symmetry
        for segment in segments:
            symmetry_axes = has_reflection_symmetry(segment)
            print(f"Detected symmetry axes: {symmetry_axes}")

            # Complete the curve only if symmetry is detected
            if symmetry_axes:
                completed_segment = complete_curve_symmetry(segment, symmetry_axes)
                completed_segment = complete_curve_interpolation(completed_segment)
                completed_segment = complete_curve_extrapolation(completed_segment)
            else:
                completed_segment = segment.copy()  # Avoid modifying original

            # Compare completed segment with expected completion
            assert np.allclose(completed_segment, test["expected_completion"]), f"Test case {i+1} failed completion"

            # Visualize the input and completed segments
            visualization.plot([test["input"], completed_segment], colors=['red', 'green'])

    print("All test cases passed!")

if __name__ == "__main__":
    test_curve_completion()