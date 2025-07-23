import boto3
import json

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodbTableName = 'Employee'
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
employeeTable = dynamodb.Table(dynamodbTableName)
bucketName = 'om-visitor-image'

def lambda_handler(event, context):
    print(event)
    objectKey = event['queryStringParameters']['objectKey']

    try:
        image_bytes = s3.get_object(Bucket=bucketName, Key=objectKey)['Body'].read()

        response = rekognition.search_faces_by_image(
            CollectionId='Devandu',
            Image={'Bytes': image_bytes}
        )

        for match in response['FaceMatches']:
            print(match['Face']['FaceId'], match['Face']['Confidence'])

            face = employeeTable.get_item(
                Key={'rekognitionId': match['Face']['FaceId']}
            )

            if 'Item' in face:
                print('Person Found:', face['Item'])
                return buildResponse(200, {
                    'Message': 'Success',
                    'firstName': face['Item']['firstName'],
                    'lastName': face['Item']['lastName']
                })

        print('Person not Found')
        return buildResponse(403, {'Message': 'Person Not Found'})

    except Exception as e:
        print(f"Error: {e}")
        return buildResponse(500, {'Message': 'Internal Server Error'})

def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body)
    return response
