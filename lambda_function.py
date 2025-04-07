import json
from firebase_crud import FirebaseCrud
import pdf_generator


def lambda_handler(event, context):
     # Handle preflight CORS request
    if event['requestContext']['http']['method'] == "OPTIONS":
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'message': 'CORS preflight success'})
        }
        
    try:
        # Parse incoming data
        event_body = json.loads(event['body'])
        month_name = event_body['monthname']

        # NOTE Do not remove below code
        # NOTE this format is being used because the file_name's 1st index i.e. monthname will be used in pdf generation
        file_name = ["ATTENDANCE_REPORT_", month_name.upper(), ".xlsx"]
    
        download_metadata = {
            'statusCode': 200,
            'details': '',
            'downloadUrl': '',
        }

        firebase_crud = FirebaseCrud()

        # Fetch attendance data
        report = firebase_crud.fetch_attendance_details(month=month_name)

        if report['statusCode'] == 200:
            # Generate file
            file_path = pdf_generator.generate_document(filename=file_name, data=report['body'])

            # Upload and get download URL
            file_generation_status = firebase_crud.push_attendance_document(file_path=file_path)

            download_metadata['statusCode'] = file_generation_status['statusCode']
            download_metadata['details'] = file_generation_status['details']
            download_metadata['downloadUrl'] = file_generation_status['downloadUrl']
        else:
            download_metadata['statusCode'] = report['statusCode']
            download_metadata['details'] = report['details']
            download_metadata['downloadUrl'] = None

        # Return proper CORS headers for web access
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(download_metadata)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST, GET'
            },
            'body': json.dumps({
                'statusCode': 500,
                'details': str(e),
                'downloadUrl': None
            })
        }
