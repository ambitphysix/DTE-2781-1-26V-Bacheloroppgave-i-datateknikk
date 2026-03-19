def generate_sectors_from_ipp(ipp):
    """
    Generates sectors based on the provided IPP (Input Parameter).
    """
    return {
        "status": "ok",
        "ipp": ipp,
        "sectors": [
            {"id": 1, "name": "Sektor 1"},
            {"id": 2, "name": "Sektor 2"}
        ]
    }