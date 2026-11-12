def prepare_class_records(records: list[dict], holidays: list[str]) -> list[dict]:
    """
    Prepare class records for attendance calculations.

    Args:
        records (list[dict]): Class records containing:
            subject (str): Non-empty subject name.
            date (str): Class date in YYYY-MM-DD format.
            start_time (str): Start time in HH:MM format.
            end_time (str): End time in HH:MM format.
            attended (bool): Whether the student attended.
            cancelled (bool): Whether the class was cancelled.
        holidays (list[str]): Holiday dates in YYYY-MM-DD format.

    Returns:
        list[dict]: Records sorted by date and start time,
        excluding holidays and cancelled classes.

    Input requirements:
        Dates and times must be valid.
        Each record represents one complete class session.
        End time must be later than start time on the same day.
        Records must not be duplicated.
        Input data must already be validated.
    """
