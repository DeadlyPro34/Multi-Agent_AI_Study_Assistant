def format_time(seconds):
    """
    Format seconds into a readable string (e.g., 2h 15m).
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m" if h else f"{m}m {s}s"
