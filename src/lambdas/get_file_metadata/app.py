import json
import os
from typing import Tuple
import paramiko
from paramiko import SFTPClient, SFTPFile

ssh = paramiko.SSHClient()


def get_sftp_client(hostname: str, port: int, username: str, password: str) -> SFTPClient:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=port, username=username,
                password=password, look_for_keys=False)
    return ssh.open_sftp()


def get_file_metadata(sftp_client, file_path) -> Tuple[str, SFTPFile]:
    return sftp_client.stat(file_path)


def lambda_handler(event, context):
    file_path = event.get('sftp_file_path', None)
    sftp_host = os.getenv('SFTP_HOST')
    sftp_username = os.getenv('SFTP_USERNAME')
    sftp_password = os.getenv('SFTP_PASSWORD')
    sftp_port = int(os.getenv('SFTP_PORT', 22))

    sftp_client = get_sftp_client(
        hostname=sftp_host, username=sftp_username, password=sftp_password, port=sftp_port)
    try:
        metadata = get_file_metadata(sftp_client, file_path)
        if metadata:
            sftp_client.close()

            return {
                "statusCode": 200,
                "body": {
                    "msg": "Finish Get file metadata from Sftp",
                    "metadata": {
                        "size": metadata.st_size
                    }
                },
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
