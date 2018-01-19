from moviepy.editor import *


config_example = \
{
    "show_text": {
        "global_text_params": {
            "font": "Amiri-Bold",
            "size": 25,
            "color": "black",
            "weight": 2,
            "bg_color": "white"
        },
        "recs": [
            {
                "text": "HELLO",
                "start": 2,
                "end": 30,
                "position": ["center", "center"],
            },
            {
                "text": "HELLO 2",
                "start": 10,
                "end": 30,
                "position": ["center", 50],
            }
        ]
    }
}


config_format = \
{
    "show_text": {
        "global_text_params": {
            "font": "",
            "size": 0,
            "color": "",
            "weight": 0,
            "bg_color": ""
        },
        "recs": [
            {
                "text": "",
                "start": 0,
                "end": 0,
                "position": ["x", "y"],
                "text_params": {
                    "font": "",
                    "size": 0,
                    "color": "",
                    "bg_color": "",
                    "weight": 0
                }
            }
        ]
    }
}


def generate_video_from_config(config, input_video_path, output_video_path):

    if type(config) is not dict:
        raise Exception('Config argument must be a dict, got {}'.format(str(type(config))))
    if 'show_text' not in config:
        raise Exception("Config must have a 'show_text' key.")

    input_video_clip = VideoFileClip(input_video_path)

    show_text_config = config['show_text']
    global_text_params = show_text_config.get('global_text_params') or {}
    global_font = global_text_params.get('font')
    global_size = global_text_params.get('size')
    global_color = global_text_params.get('color')
    global_bg_color = global_text_params.get('bg_color')
    global_weight = global_text_params.get('weight')

    if not all([global_font, global_color, global_bg_color, global_size, global_weight]):
        raise Exception("Global text font, color, bg_color, size and weight must be defined.")

    show_text_recs = show_text_config['recs']

    text_clips = []
    for rec in show_text_recs:
        rec_text_params = rec.get('text_params') or {}
        rec_font = rec_text_params.get('font') or global_font
        rec_size = rec_text_params.get('size') or global_size
        rec_color = rec_text_params.get('color') or global_color
        rec_bg_color = rec_text_params.get('bg_color') or global_bg_color
        rec_weight = rec_text_params.get('weight') or global_weight

        rec_text = rec.get('text')
        rec_start = rec.get('start')
        rec_end = rec.get('end')
        rec_position = rec.get('position')

        if not all([rec_text, rec_start, rec_end, rec_position]):
            raise Exception("start, end, position and text should be defined for each record")
        if type(rec_position) is not list or len(rec_position) < 2:
            raise Exception("'position' must be a list of length 2, containing x and y coords")

        text_clips.append(TextClip(rec_text,
                                   font=rec_font,
                                   fontsize=rec_size,
                                   stroke_color=rec_color,
                                   bg_color=rec_bg_color,
                                   stroke_width=rec_weight)
                          .set_start(rec_start)
                          .set_duration(rec_end - rec_start)
                          .set_position((rec_position[0], rec_position[1])))

    output_video_clip = CompositeVideoClip([input_video_clip] + text_clips)

    output_video_clip.write_videofile(output_video_path)


if __name__ == "__main__":
    generate_video_from_config(config_example, "/home/nishant/video.mp4", "/home/nishant/output.mp4")

