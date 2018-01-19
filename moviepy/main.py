# Import everything needed to edit video clips
from moviepy.editor import *
import pytweening

# Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
clip = VideoFileClip("/home/nishant/video.mp4").subclip(0,60)

duration = clip.duration


def pos(t):
    x = pytweening.easeOutSine(t/2) * 100
    # print(t, x)
    return x, 'center'


txt_clip = TextClip("My Holidays 2013", fontsize=20, color='yellow')
txt_clip = (txt_clip
            .set_position(pos)
            .set_duration(2))

# Overlay the text clip on the first video clip
video = CompositeVideoClip([clip, txt_clip])

# Write the result to a file (many options available !)
video.write_videofile("/home/nishant/output.mp4")