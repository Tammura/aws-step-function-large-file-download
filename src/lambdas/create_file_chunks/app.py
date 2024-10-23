import os


def lambda_handler(event, context):
    file_size = event['file_size']
    if not file_size:
        return {
            'statusCode': 400,
            'body': 'Missing file_size in the event payload'
        }
    chunk_size = int(os.getenv('CHUNK_SIZE', 50 * 1024 * 1024))

    num_chunks = (file_size // chunk_size) + 1

    chunks = [{"chunk_number": i+1,
               "start_byte": (i * chunk_size),
               "end_byte": min((i + 1) * chunk_size, file_size)}
              for i in range(num_chunks)]

    return {
        "statusCode": 200,
        "body": {
            "msg": "Finish create file chunks",
            "chunks": chunks
        },
    }
