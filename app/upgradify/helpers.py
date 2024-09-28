def get_ram_value(ram_key, RAM_HIERARCHY):
    for ram_dict in RAM_HIERARCHY:
        if ram_key in ram_dict:
            return ram_dict[ram_key]
    return None
