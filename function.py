import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from pytwitter import Api


def get_secret():
    secret_name = os.environ.get("SECRET_NAME")
    region_name = "us-west-2"
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(f"Error getting secret value: {e}")
        raise e

    return get_secret_value_response['SecretString']


def video_path():
    return "assets/serbian_goodbye.mp4"


def get_auth_bits():
    auth_bits = {"CONSUMER_KEY": None, "CONSUMER_SECRET": None, "CLIENT_ID": None, "CLIENT_SECRET": None}
    if os.environ.get("ENVIRONMENT") != "prod":
        load_dotenv()
        auth_bits["CONSUMER_KEY"] = os.environ.get("CONSUMER_KEY")
        auth_bits["CONSUMER_SECRET"] =  os.environ.get("CONSUMER_SECRET")
        auth_bits["ACCESS_TOKEN"] = os.environ.get("ACCESS_TOKEN")
        auth_bits["ACCESS_SECRET"] = os.environ.get("ACCESS_SECRET")
    else:
        secrets = get_secret()
        auth_bits["CONSUMER_KEY"] = secrets["CONSUMER_KEY"]
        auth_bits["CONSUMER_SECRET"] = secrets["CONSUMER_SECRET"]
        auth_bits["ACCESS_TOKEN"] = secrets.get("ACCESS_TOKEN")
        auth_bits["ACCESS_SECRET"] = secrets.get("ACCESS_SECRET")

    return auth_bits


def authenticate_twitter(auth_bits):
    return Api(
        consumer_key=auth_bits["CONSUMER_KEY"],
        consumer_secret=auth_bits["CONSUMER_SECRET"],
        access_token=auth_bits["ACCESS_TOKEN"],
        access_secret=auth_bits["ACCESS_SECRET"]
    )


def handler(event, context):
    try:
        api = authenticate_twitter(get_auth_bits())
        init_upload = api.upload_media_chunked_init(
            total_bytes=4651377,
            media_type="video/mp4"
        )
        media_id = init_upload.media_id_string
        with open(video_path(), "rb") as media:
            status = api.upload_media_chunked_append(
                media_id=media_id,
                media=media,
                segment_index=0
            )
            print(status)

        resp = api.upload_media_chunked_finalize(media_id=media_id)
        print(resp)

        api.create_tweet(
            text="It's gameday, Nuggets Nation! Let's give em the ol' Serbian Goodbye!",
            media_media_ids=[media_id]
        )
    except Exception as e:
        print(f"Error: {e}")
