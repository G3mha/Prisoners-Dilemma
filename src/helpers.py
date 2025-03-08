def normalize(value, min_val, max_val):
    """Normalize a value to range [0,1]"""
    if max_val == min_val:
        return 0.5
    return (value - min_val) / (max_val - min_val)
