from moviepy.editor import *


config_example = \
{
    "show_text": {
        "global_text_params": {
            "font": "Amiri-Regular",
            "size": 14,
            "color": "black",
            "weight": 0.01,
            "bg_color": "transparent"
        },
        "recs": [
            {
                "text": "Chandan Patel",
                "start": 31.5,
                "end": 41,
                "position": [194, 86],
            },
            {
                "text": "29",
                "start": 32,
                "end": 41,
                "position": [194, 117],
            },
            {
                "text": "9886032650",
                "start": 33,
                "end": 41,
                "position": [194, 148],
            },
            {
                "text": "Vinit",
                "start": 47,
                "end": 51,
                "position": [252, 147],
            },
            {
                "text": "Rs 10,000",
                "start": 56,
                "end": 63,
                "position": [138, 171],
            },
            {
                "text": "Sum assured 1Cr",
                "start": 64.5,
                "end": 71,
                "position": [128, 184.5],
            },
            {
                "text": "Accident",
                "start": 73,
                "end": 81.5,
                "position": [58, 130],
            },
            {
                "text": "Disability",
                "start": 73.5,
                "end": 81.5,
                "position": [256, 130],
            },
            {
                "text": "Unnatural",
                "start": 74,
                "end": 81.5,
                "position": [58, 171],
            },
            {
                "text": "Suicide",
                "start": 75,
                "end": 81.5,
                "position": [256, 171],
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
    generate_video_from_config(config_example, "/Users/chandanpatel/workspace/paravi/paravi_web/api/template/240.mp4", "/Users/chandanpatel/Desktop/output_low.mp4")

