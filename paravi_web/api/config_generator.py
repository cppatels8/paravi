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
                "font": "Amiri-Regular",
                "size": 14,
                "color": "black",
                "weight": 0.01,
                "bg_color": "transparent"
            },
            "recs": recs
        }
    }
    config["show_text"]["global_text_params"].update(**global_text_params)
    return config
