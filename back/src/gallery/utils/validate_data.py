def validate_list(raw_data, conversion_type_method):
    if raw_data is None or not callable(conversion_type_method):
        return list()

    result = list()
    if isinstance(raw_data, list):
        for entry in raw_data:
            try:
                result.append(conversion_type_method(entry))
            except ValueError:
                pass
    else:
        try:
            result.append(conversion_type_method(raw_data))
        except ValueError:
            pass
    return result
