import io
import os
from typing import Tuple
import paramiko
from paramiko import SFTPClient, SFTPFile
import boto3

s3 = boto3.client('s3')
ssh = paramiko.SSHClient()


def get_sftp_client(hostname: str, port: int, username: str, password: str) -> SFTPClient:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=port, username=username,
                password=password, look_for_keys=False)
    return ssh.open_sftp()


def download_chunk(sftp_client, sftp_file_path, start_byte, end_byte) -> Tuple[str, SFTPFile]:
    file_buffer = sftp_client.open(sftp_file_path, "r")
    file_buffer.seek(start_byte)
    buffer = io.BytesIO(file_buffer.read(end_byte - start_byte))
    file_buffer.close()
    return buffer


def lambda_handler(event, context):
    bucket_name = event["bucket_name"]
    sftp_file_path = event['sftp_file_path']
    file_key = event['s3_file_key']

    chunk_number = event['chunk_number']
    start_byte = event['start_byte']
    end_byte = event['end_byte']
    upload_id = event['upload_id']

    sftp_host = os.getenv('SFTP_HOST')
    sftp_username = os.getenv('SFTP_USERNAME')
    sftp_password = os.getenv('SFTP_PASSWORD')
    sftp_port = int(os.getenv('SFTP_PORT', 22))

    sftp_client = get_sftp_client(
        hostname=sftp_host, username=sftp_username, password=sftp_password, port=sftp_port)

    obj = download_chunk(sftp_client, sftp_file_path, start_byte, end_byte)
    if obj:
        response = s3.upload_part(
            Bucket=bucket_name,
            Key=file_key,
            PartNumber=chunk_number,
            UploadId=upload_id,
            Body=obj
        )

    sftp_client.close()
    ssh.close()

    return {
        "statusCode": 200,
        "body": {
            "PartNumber": chunk_number,
            "ETag": response['ETag'],
        },
    }
