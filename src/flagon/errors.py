class FlagonError(Exception):
    """
    Base Flagon error.
    """
    pass


class UnknownFeatureError(FlagonError):
    """
    When a feature is not configured but is used.
    """
    pass
