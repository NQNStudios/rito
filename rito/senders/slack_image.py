import requests
import json
import os
import code
import cv2
from . import slack

if 'RITO_SLACK_TOKEN' not in os.environ:
    print("To use Rito's slack functions, first create a Slack app on your workspace following these instructions: https://api.slack.com/messaging/sending#getting_started")
    print("Your app needs the permissions channel:read, chat:write, and chat:write.public")
    print("After creating the app and installing it to your workspace, copy its auth token into an environment variable called RITO_SLACK_TOKEN")
    print("For very large images, set the environment variable OPENCV_IO_MAX_IMAGE_PIXELS to a sensible value.")
    exit(1)

auth_token = os.environ['RITO_SLACK_TOKEN']

# Instead of a string containing a message, the slack_image sender expects a string containing an image filename
def send_message(channel, filename):
    # According to https://slack.com/intl/en-gb/help/articles/201330736-Add-files-to-Slack
    # "the preview will only display inline if it's smaller than 11,000 pixels on the longest side,
    # or less than 45 million pixels total."
    side_limit = 11000
    total_limit = 45000000

    try:
        image = cv2.imread(filename)
    except:
        # Image is too large for OPENCV_IO_MAX_IMAGE_PIXELS
        slack.send_message(channel, "Failed to send {} because it is too large. To fix this, set the environment variable OPENCV_IO_MAX_IMAGE_PIXELS to a sensible value.".format(filename))
        return

    height = image.shape[0]
    width = image.shape[1]
    pixels_total = height * width

    if pixels_total >= total_limit or height >= side_limit or width >= side_limit:
        new_size = (int(width/2), int(height/2))
        new_image = cv2.resize(image, new_size)
        base_filename, ext = os.path.splitext(filename)
        new_filename = base_filename + '-small' + ext
        cv2.imwrite(new_filename, new_image)
        send_message(channel, new_filename)
        return

    payload = {
        "channels": channel
    }

    headers = {
        "Authorization": "Bearer {}".format(auth_token)
    }

    files = {
        'file': open(filename, 'rb')
    }

    resp = requests.post("https://slack.com/api/files.upload", data=payload, headers=headers, files=files)
    resp = json.loads(resp.text)
    if not resp["ok"]:
        raise Exception(resp["error"])