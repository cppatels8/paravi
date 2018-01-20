fields_mapping = \
    {
        "param_name": [
            {
                "start": 2,
                "end": 5,
                "position": ["center", "center"],
            },
            {
                "start": 7,
                "end": 11,
                "position": [45, "center"],
            }
        ]
    }


def generate_config_from_params(param_dict, fields_mapping, **global_text_params):
    recs = []
    for param_name, value in param_dict.items():
        if param_name in fields_mapping:
            for rec in fields_mapping[param_name]:
                rec['text'] = str(value)
                recs.append(rec)
    config = {
        "show_text": {
            "global_text_params": {
                "font": "Amiri-Bold",
                "size": 25,
                "color": "black",
                "weight": 2,
                "bg_color": "white",
                **global_text_params
            },
            "recs": recs
        }
    }
    return config
