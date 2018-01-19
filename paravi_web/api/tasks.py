from __future__ import absolute_import, unicode_literals
from celery import shared_task
from moviepy.editor import *
import pytweening
from celery.app import log
from django.conf import settings
import os
from twilio.rest import Client
import boto3

logger = log.get_logger(__name__)


def template_path(file_name):
    return os.path.join(settings.BASE_DIR, "api", "template", file_name)


def output_path(file_name):
    return os.path.join(settings.BASE_DIR, "api", "output", file_name)


@shared_task
def run_moviepy(request_id, **kwargs):
    # Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
    logger.info("Starting to create video for {0}".format(kwargs['name']))

    clip = VideoFileClip(template_path(kwargs['name'])).subclip(0, 5)

    def pos(t):
        x = pytweening.easeOutSine(t / 2) * 100
        return x, 'center'

    txt_clip = TextClip("My Holidays 2013", fontsize=20, color='yellow')
    txt_clip = (txt_clip
                .set_position(pos)
                .set_duration(2))

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip, txt_clip])

    # Write the result to a file (many options available !)
    logger.info("Saving output video for {0}".format(kwargs['name']))
    output_dir = output_path(request_id)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = output_path("{0}/output.mp4".format(output_dir))
    video.write_videofile(output_file)
    logger.info("Saved video for {0} at {1}".format(kwargs['name'], output_file))
    post_compose(output_file, **kwargs)


def post_compose(request_id, output_file, **kwargs):
    logger.info("uploading output_file: {0} to s3".format(output_file))
    f = open(output_file, 'rb')
    from boto3.s3.transfer import S3Transfer
    import boto3
    # have all the variables populated which are required below
    client = boto3.client('s3',
                          aws_access_key_id=settings.S3_ACCESS_KEY,
                          aws_secret_access_key=settings.S3_SECRET_KEY)
    transfer = S3Transfer(client)
    transfer.upload_file(output_file, settings.BUCKET, "hashathon" + "/" + request_id  + ".mp4")

    path = "https://s3.ap-south-1.amazonaws.com/hackathon-paravi/hashathon/{0}.mp4".format(request_id)
    sms_template = kwargs.get("sms_template")
    if not sms_template:
        sms_template = "Hi {0}, Here is quick video for you. {1}".format(kwargs['name'], path)
    send_sms(kwargs['number'], message=sms_template)


def send_sms(number, message):
    logger.info("Notifying user on number: {0}".format(number))
    # Your Account SID from twilio.com/console
    account_sid = settings.ACCOUNT_SID
    # Your Auth Token from twilio.com/console
    auth_token = settings.AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=number,
        from_=9886032650,
        body=message)
    logger.info("SMS sent to twilio: {0}".format(message.id))
