import boto3
from botocore.exceptions import ClientError
# Initialize AWS clients
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
dynamodbTableName = 'Employee'
employeeTable = dynamodb.Table(dynamodbTableName)

def lambda_handler(event, context):
    print("Received event:", event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try:
        response = index_employee_image(bucket, key)
        print("Rekognition response:", response)
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']
            name = key.split('.')[0].split('_')
            firstName = name[0]
            lastName = name[1] if len(name) > 1 else ''
            register_employee(faceId, firstName, lastName)
        
        return response
    
    except Exception as e:
        print("Error:", e)
        print(f"Error processing employee image {key} from bucket {bucket}.")
        raise e

def index_employee_image(bucket, key):
    return rekognition.index_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        CollectionId="Devandu",  # Make sure this collection exists
        DetectionAttributes=['ALL']
    )

def register_employee(faceId, firstName, lastName):
    try:
        response = employeeTable.put_item(
            Item={
                'rekognitionId': faceId,
                'firstName': firstName,
                'lastName': lastName
            }
        )
        print("DynamoDB PutItem response:", response)
    except ClientError as e:
        print("DynamoDB PutItem error:", e.response['Error']['Message'])
        raise e
