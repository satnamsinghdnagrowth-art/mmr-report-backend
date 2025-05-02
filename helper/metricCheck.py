from config.MetricBehaviour import NEGATIVE_METRICS


def isMetricPositive(title: str, value: float) -> bool:
    """
    Determines whether a metric should be considered positive or negative.

    Args:
        title (str): The title of the metric (e.g., 'Revenue', 'Cost of Goods Sold').
        difference (float): The numeric difference to evaluate.

    Returns:
        bool: True if positive, False if negative.
    """
    if title in NEGATIVE_METRICS:
        return value <= 0
    return value >= 0
