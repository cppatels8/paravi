from __future__ import absolute_import, unicode_literals

import os

from celery import shared_task
from celery.app import log
from django.conf import settings
from django.core.mail import EmailMessage
from twilio.rest import Client

from .config_generator import generate_config_from_params
from .video_generator import generate_video_from_config

logger = log.get_logger(__name__)


def template_path(file_name):
    return os.path.join(settings.BASE_DIR, "api", "template", file_name)


def output_path(file_name):
    return os.path.join(settings.BASE_DIR, "api", "output", file_name)


INPUT_VIDEO_FILE = '/home/nishant/video.mp4'
FIELD_MAPPING = {
    "premium": [
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
    ],
    "email": []
}



@shared_task
def run_moviepy(request_id, data):
    logger.info("Starting to create config for {0}".format(data))
    config = generate_config_from_params(data, FIELD_MAPPING)
    logger.info("Saving output video for {0}".format(data))
    output_dir = output_path(request_id)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file_path = output_path("{0}/output.mp4".format(output_dir))
    generate_video_from_config(config, INPUT_VIDEO_FILE, output_file_path)
    logger.info("Saved video for {0} at {1}".format(data, output_file_path))
    send_email_with_video(output_file_path, data['email'])


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


def send_email_with_video(video_file_path, recipient_email):
    f = open(video_file_path, 'rb')
    email = EmailMessage(subject='Video is ready',
                         body='video is ready',
                         to=[recipient_email],
                         attachments=[('video.mp4', f.read())])
    email.send()
