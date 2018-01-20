# Import everything needed to edit video clips
from moviepy.editor import *
from moviepy.video.fx import resize

def bulletedText(text_arr, start_time=0, start_x=360, start_y=20, duration=4,is_active=False):
    clips = []
    img = "images/aviva/blue_unpicked.png"
    if(is_active):
        img = "images/aviva/blue_picked.png"

    img_clip = ImageClip(img, duration=4)
    img_clip = img_clip.set_pos((start_x, start_y )).set_duration(duration).set_start(start_time)
    clips.append(img_clip)

    for i,t in enumerate (text_arr):
        if(i == 0):
            txt_clip = TextClip(t,fontsize=24,color='yellow')
        else:
            txt_clip = TextClip(t,fontsize=20,color='#FFF')
        txt_clip = txt_clip.set_pos(( start_x + 20, start_y + 30 + (i * 60))).set_duration((duration - 1)).set_start(start_time + .250 +  (i * .250))
        clips.append(txt_clip)
    return clips

def sticker(text, start_time=0, start_x=0, start_y=0,duration=4):
    clips = []
    img_clip = ImageClip('images/aviva/sticker.png', duration=4)
    img_clip = img_clip.set_pos((start_x, start_y )).set_duration(duration).set_start(start_time)
    clips.append(img_clip)
    
    txt_clip = TextClip(text,fontsize=14,color='#000')
    txt_clip = txt_clip.set_pos((start_x + 36, start_y + 60)).set_duration((duration)).set_start(start_time)
    clips.append(txt_clip)

    return clips

def easeInQuad(t):
    return 20 * t * t

def easeInOut(t):
    if( t < .5):
        return 8 * t * t * t * t
    else:
        return 1 - 8 * (--t) * t * t * t

def aviva_video(config):    
    # Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
    clip = VideoFileClip("images/aviva/aviva.mp4", audio_buffersize=500000)

    cut_time = 0
    investment_per_month = config['investment_per_month']
    maturity_time = (21 - config['child_age'])
    maturity_year = maturity_time + 2018
    total_deposited = (maturity_time - 5) * 12 * investment_per_month
    maturity_amount = (2 * 12 * investment_per_month)
    maturity_amount_growth = (5 * 12 * investment_per_month)

    total_return = total_deposited + maturity_amount
    if(config['plan_type'] == 'growth'):
        total_return = total_deposited + maturity_amount_growth



    if(config['reason'] == 'secure'):
        clip = clip.cutout(8.20,21.00)
        cut_time = 12.8

    # clip = clip.cutout(7.00,12.00)
    # clip = clip.cutout(7.00,11.00)

    # Reduce the audio volume (volume x 0.8)
    aud = AudioFileClip('images/aviva/bg-score.mp3')
    aud = aud.volumex(0.2).set_duration(82.2 - cut_time)

    d = 1
    if(config['reason'] == 'secure'):
        a_start = AudioFileClip('images/aviva/secure.aiff').set_start(d)
    else:
        a_start = AudioFileClip('images/aviva/abroad.aiff').set_start(d)
    d= d + 3

    intro_text = ""
    if(config['reason'] == 'secure'):
        if(config['child_age'] < 9):
            a_join = AudioFileClip('images/aviva/start_early.aiff').set_start(d)
            intro_text = "Secure your child at early age"
        else:
            a_join= AudioFileClip('images/aviva/start_early2.aiff').set_start(d)
            intro_text = "It's never too late to secure your child"

    else:
        if(config['child_age'] < 9):
            a_join = AudioFileClip('images/aviva/soon.aiff').set_start(d)
            intro_text = "Plan early for higher education"
        else:
            a_join = AudioFileClip('images/aviva/soon2.aiff').set_start(d)
            intro_text = "Delayed in planning funds for childs higher education"


    a_understand = AudioFileClip('images/aviva/understand.aiff').set_start(21.2 - cut_time)
    a_savings = AudioFileClip('images/aviva/savings.aiff').set_start(28 - cut_time)
    a_compare = AudioFileClip('images/aviva/plan_comparison.aiff').set_start(37 - cut_time)
    a_notAround = AudioFileClip('images/aviva/not_around.aiff').set_start(47 - cut_time)
    a_enjoy = AudioFileClip('images/aviva/enjoy.aiff').set_start(58 - cut_time)
    a = CompositeAudioClip([aud, a_start, a_join, a_understand, a_savings, a_compare, a_notAround, a_enjoy])
    clip = clip.set_audio(a)


    clips = [clip]

    # BULLETED COMPARISONS
    clips = clips + bulletedText(["Growth Based Child Plan", "Dual Advantage", "Greater Returns", "Min Sum Assured", "Bonus (approx) Rs" + str(maturity_amount_growth/100000) + "lks"], 37.7 - cut_time, 330, 10,8, config['plan_type'] == 'growth')
    clips = clips + bulletedText(["Child Plan", "Sum Assured","Retirement Benefits", "Free Tution Fees", "Money Back (approx) Rs" + str(maturity_amount/100000) + "lks"], 37.7 - cut_time, 10, 10,8, config['plan_type'] != 'growth')

    # STICKERS IN VARIOUS POINTS
    clips = clips + sticker("In 2018\nUS $80000",5, 30,70,5)
    clips = clips + sticker("By " + str(maturity_year) + "\nUS $150000",6, 470,20,4)
    clips = clips + sticker("Pay\nRs." + str(investment_per_month) + "\nper mnt\nfor " + str(maturity_time) + " yrs",17, 40,60,4)
    
    if(config['plan_type'] == 'growth'):
        clips = clips + sticker("Earn from\nmarket success",17, 460,30,4)
        clips = clips + sticker("Gain upto\nRs." + str(maturity_amount_growth/100000) + "lks",17, 270,150,4)
    else:
        clips = clips + sticker("Assured Sum\nNo Tuition Fees",17, 460,30,4)
        clips = clips + sticker("Gain upto\nRs." + str(maturity_amount/100000) + "lks",17, 270,150,4)

            
    if(config['child_age'] >= 9):
        clips = clips + sticker("Only " + str(maturity_time) + " yrs\nto secure\nyour child",.5, 40,40,2)
        
    # INTRODUCTION TEXT
    txt_clip = TextClip(intro_text,fontsize=24, font='Arial', stroke_width=3,color='#D44')
    txt_clip = txt_clip.set_pos(lambda t: ('center', 310  )).set_duration(4).set_start(.01)
    clips.append(txt_clip)


    # Overlay the text clip on the first video clip
    video = CompositeVideoClip(clips)

    # Write the result to a file (many options available !)
    video.write_videofile("aviva-new.mp4")




aviva_video({'reason':'higher-studies'
            , 'child_age':5
            , 'plan_type' : 'child_plan'
            , 'investment_per_month' : 20000
            })



