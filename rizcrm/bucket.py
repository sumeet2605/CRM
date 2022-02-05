
import boto3

# configure session and client
session = boto3.session.Session()
client = session.client(
    's3',
    region_name='sgp1',
    endpoint_url='https://sgp1.digitaloceanspaces.com',
    aws_access_key_id='DLLPBVAT5QJDLVHOFZOK',
    aws_secret_access_key='pCrW752iCk2E9qzwMFezrbgjQDnfKhZlJc8uNBSDxGU',
)

# create new bucket
client.create_bucket(Bucket='rizcrm')

# upload file
with open('../requirements.txt', 'rb') as file_contents:
    client.put_object(
        Bucket='rizcrm',
        Key='test.txt',
        Body=file_contents,
    )

# download file
client.download_file(
    Bucket='rizcrm',
    Key='test.txt',
    Filename='tmp/test.txt',
)