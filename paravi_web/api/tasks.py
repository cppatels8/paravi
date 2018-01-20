from __future__ import absolute_import, unicode_literals

import os

from celery import shared_task
from celery.app import log
from django.conf import settings
from django.core.mail import EmailMessage
from .config_generator import generate_config_from_params
from .video_generator import generate_video_from_config
from boto3.s3.transfer import S3Transfer
import boto3

logger = log.get_logger(__name__)


def template_path(file_name):
    return os.path.join(settings.BASE_DIR, "api", "template", file_name)


def output_path(file_name):
    return os.path.join(settings.BASE_DIR, "api", "output", file_name)


INPUT_VIDEO_FILE = template_path("240.mp4")
FIELD_MAPPING = {
    "nominee": [
        {
            "start": 48,
            "end": 51,
            "position": [750, 450],
        }
    ],
    "emi": [
        {
            "start": 56,
            "end": 63,
            "position": [520, 520],
        }
    ],
    "payout": [
        {
            "start": 65,
            "end": 71,
            "position": [520, 550],
            "text_params": {
                "size": 40
            }
        }
    ],

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
    post_compose(request_id, output_file_path, data)
    logger.info("Saved video for {0} at {1}".format(data, output_file_path))


def post_compose(request_id, output_file, data):
    logger.info("uploading output_file: {0} to s3".format(output_file))
    # have all the variables populated which are required below
    client = boto3.client('s3',
                          aws_access_key_id=settings.S3_ACCESS_KEY,
                          aws_secret_access_key=settings.S3_SECRET_KEY)
    transfer = S3Transfer(client)
    transfer.upload_file(output_file, settings.BUCKET, "hashathon" + "/" + request_id  + ".mp4",
                         extra_args={"Content-Type": "video/mp4"
                                     }
                         )

    send_email_with_video(output_file, data['email'])


def send_email_with_video(video_file_path, recipient_email):
    f = open(video_file_path, 'rb')
    email = EmailMessage(subject='Term Life Insurance Policy Details (Video)',
                         body='',
                         to=[recipient_email],
                         attachments=[('Policy.mp4', f.read())])
    email.send()
