import json
from firebase_crud import FirebaseCrud
import pdf_generator

def lambda_handler(event, context):

    month_name = "march"
    file_name = ["ATTENDANCE_REPORT_", month_name.upper(), ".xlsx"]
    
    firebase_crud = FirebaseCrud()

    # fetch detailss
    report = firebase_crud.fetch_attendance_details(month=month_name)

    print(report)

    # # if True:
    # if report['statusCode'] == 200:
    #     # Data is available then generate the document
    #     file_path = pdf_generator.generate_document(filename=file_name, data=report['body'])

    #     # upload and get the download url
    #     data = firebase_crud.push_attendance_document(monthname=''.join(file_name), file_path=file_path)
    #     print(data)
    # #     firebase_crud.upload_document(filename=filename)
    # else:
    #     # this is the FAILED CASE, causing some issues
    #     return {
    #         "statusCode": report['statusCode'],
    #         'details': report['details'],
    #         'body': report['body']
    #    }

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda! From GitHub Actions!')
    }

'''
def _random_characters(*, count: int=10) -> str:
    count = 25 if(count > 25) else count
    count = 8 if(count < 0) else count
    letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    random.shuffle(letters)
    # random_characters = "".join(random.shuffle(letters))
    # return random_characters
    return "".join(letters[0: count])
'''


# lambda_handler('', '')

