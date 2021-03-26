#Let's use Amazon s3
from __future__ import unicode_literals
import logging
import boto3
import youtube_dl
from botocore.exceptions import ClientError


def generateURL(client, bucket, object_name):
    url = client.generate_presigned_url('get_object', 
    Params = {'Bucket': bucket, 'Key': object_name},
    ExpiresIn = 900)
    print("====limited time file sharing link(15 mins)====")
    print(url)


s3_client = boto3.client('s3')
bucket = "monosparta-test"
url = "https://www.youtube.com/watch?v=8ME8woURUm0"
opts = {}

## 準備影片資料 Prepare the information of the video
with youtube_dl.YoutubeDL() as ydl:
    print("====Get the information of the video====\n")
    info = ydl.extract_info(url, download=False)
    video_id = info.get("id", None)
    opts['outtmpl'] = str(video_id + '.mp4')
    print('opts[outtmpl]: ', opts['outtmpl'])
    opts['objectName'] = str(video_id)[0].lower() + "/" + str(video_id)[1].lower() + "/" + str(video_id)[2].lower() + "/" + opts['outtmpl']
    
## 下載影片 Download the video
with youtube_dl.YoutubeDL(opts) as ydl2:
    print("====Downloading the video====\n")
    info = ydl2.extract_info(url, download = True)

## 上傳影片 Upload the video to the Amazon s3
print("====Uploading the video to " + bucket + "====\n")
try:
    response = s3_client.upload_file(opts['outtmpl'], bucket, opts['objectName'])
except ClientError as e:
    logging.error(e)

## 產生URL Generate the URL
generateURL(s3_client, bucket, opts['objectName'])

