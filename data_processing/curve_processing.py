def segment_curve(polyline, segment_length_threshold):
    """Segments a polyline into smaller segments based on segment length.

    Args:
        polyline: A list of (x, y) points representing the polyline.
        segment_length_threshold: The maximum length of a segment.

    Returns:
        A list of segments, where each segment is a list of points.
    """

    segments = []
    current_segment = []

    for i in range(len(polyline) - 1):
        p1, p2 = polyline[i], polyline[i + 1]
        segment_length = ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5
        if len(current_segment) == 0 or segment_length <= segment_length_threshold:
            current_segment.append(p1)
        else:
            segments.append(current_segment)
            current_segment = [p1]

    if current_segment:
        segments.append(current_segment)

    return segments
