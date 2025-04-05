from datetime import datetime as dt
import firebase_admin # type: ignore
from firebase_admin import credentials, firestore, storage # type: ignore
import os
from dotenv import load_dotenv # type: ignore


# load .env file
load_dotenv()


class FirebaseCrud:
    def __init__(self):
                
        
        # * * * * * * * * * * * * * * * * * * * * * * 
        # * * * * * * * COLLECTION NAME(S)* * * * * * 
        # * * * * * * * * * * * * * * * * * * * * * * 
        self.__document_generation_collection = os.getenv("DOCUMENTS_GENERATION_COLLECTION_NAME")        
        self.__employee_details_collection = os.getenv("EMPLOYEE_DETAILS_COLLECTION_NAME")

        # * * * * * * * * * * * * * * * * * * * * * * 
        # * * * * * * * DOCUMENT NAME(S)* * * * * * * 
        # * * * * * * * * * * * * * * * * * * * * * * 
        self.__attendance_documents_doc_ref = os.getenv("ATTENDANCE_DOCUMENTS")
        self.__attendance_daily_fetch_doc_ref = os.getenv("ATTENDANCE_FETCH_DAILY_LIMIT_DOCUMENT")
        self.__employee_details_doc_ref = os.getenv("EMPLOYEE_DETAILS_DOCUMENT_NAME")

        
        # * * * * * * * * * * * * * * * * * * * * * * 
        # * * FIREBASE STORAGE BUCKET NAME NAME * * *
        # * * * * * * * * * * * * * * * * * * * * * * 
        self.__firebase_storage_bucket = os.getenv("FIREBASE_STORAGE_BUCKET_URL")

        # load credentials
        self.__cred = credentials.Certificate("firebase-config.json")
        firebase_admin.initialize_app(self.__cred, {'storageBucket': self.__firebase_storage_bucket})


        # firestore client reference
        self.__db = firestore.client()

        # storage bucket reference
        self.__bucket = storage.bucket()


        # daily limits
        '''
        DAILY LIMITS:
        {
            "limits": 10
        }
        This is reference to the Daily Limits being assigned to the Admin to generate the attendance documents
        '''
        self.__attendance_fetch_limit = self.__db.collection(self.__document_generation_collection).document(self.__attendance_daily_fetch_doc_ref)
        # .document(self.__attendance_daily_fetch_doc_ref)

        # attendance documents
        self.__attendance_documents = self.__db.collection(self.__document_generation_collection).document(self.__attendance_documents_doc_ref)

        # employee details
        self.__employee_details = self.__db.collection(self.__employee_details_collection).document(self.__employee_details_doc_ref)

    
    def __fetch_days_limit(self) -> int:  
        '''
        This function returns the limit number of requests an admin can request
        Its being dynamically managed from firestore to have a variable approach 
        ''' 
        limit = self.__attendance_fetch_limit.get().to_dict().get("limit")
        return limit


    # fetch and format document from firebase accordingly
    def fetch_attendance_details(self, *, month: str):
        """
        This code fetches the attendances details from firestore and returns json file with following strucuture:-

        {
            "status": "OK" if is_data_available else "FAIL",
            "statusCode": 200 if is_data_available else 404,
            "details": parsing_details,
            "body": full_report
        }
        """

        employees_information = None


        # Add a None check at first
        try:
            employees_information = self.__employee_details.get().to_dict()
        except:
            print("ERROR: there are no employee details listed yet")
            employees_information = None


        _a = '''NAME   EID   DEPARTMENT   DATE    MONTH   CHECK-IN-TIME   CHECK-OUT-TIME   TOTAL-WORKING-HOURS   TOTAL-WORKING-DAYS   STATUS'''
        
        # the data being returned to generate the doc
        full_report = []

        # this will store all the success fetches and errors details
        parsing_details = []

        # total present employees this month
        

        if employees_information != None:
            
            for emails in employees_information.items():

                # its providing the value inside the dictionary (or map)
                # i.e. the full information of each
                employeeInfo = emails[1]
                
                try:
                    attendance_record = employeeInfo.get("attendanceRecords").get(month.title(), None)
                    if attendance_record != None:

                        total_attendent_days = 0

                        for date in attendance_record:
                            name = employeeInfo.get("personalInfo").get("name")
                            punch_in = attendance_record[date].get("punchInTime") if len(attendance_record[date].get("punchInTime")) != 0 else "NA"
                            punch_out = attendance_record[date].get("punchOutTime") if len(attendance_record[date].get("punchOutTime")) != 0 else "NA"
                            date_as_datetime = dt.strptime(date, "%Y-%m-%d")
                            daily_hours = self.__calculate_daily_hours(punch_in, punch_out)
                            # total_days = self.calculate_total_days(attendance_record=attendance_record, month=month, year=date_as_datetime.year)
                            
                            # count the no. of the days the employee is present
                            if attendance_record[date]["present"] == "yes":
                                total_attendent_days += 1

                            # print(daily_hours)
                            
                            full_report.append(
                                {   
                                    "name": name,
                                    "eid": employeeInfo.get("employeeDetails").get("uid"),
                                    "department": employeeInfo.get("employeeDetails").get("department"),
                                    "date": date,
                                    "month": date_as_datetime.strftime("%B"),
                                    "check_in": punch_in,
                                    "check_out": punch_out,
                                    "total_hours": daily_hours,
                                    "total_days": total_attendent_days,
                                    "status": "PRESENT" if len(punch_in) >= 7 and punch_out != "NA" else "HALF DAY"
                                }
                            )

                            '''     
                            print(
                                f'{employeeInfo.get("personalInfo").get("name")} '
                                f'{employeeInfo.get("employeeDetails").get("uid")} '
                                f'{employeeInfo.get("employeeDetails").get("department")} '
                                f'{date}  '
                                f'{date_as_datetime.strftime("%B")}  '
                                f'{punch_in}  '
                                f'{punch_out}  '
                                f'{daily_hours}  '
                                f'{total_days}  '
                                f'{"PRESENT" if attendance_record[date]["present"] == "yes" else "ABSENT"} '
                            )
                            '''
                            
                            parsing_details.append(f"{employeeInfo.get('personalInfo').get('name')} :: Attendance record is available")
                    else:
                        parsing_details.append(f"{employeeInfo.get('personalInfo').get('name')} :: Attendance record is not available")
                        pass
                except Exception as e:
                    print(f'Error Accessing month "{month}" in the attendanceRecords Field.\n{e}')
                    parsing_details.append(f"Error Accessing month '{month}' in the attendanceRecords Field.")
                    pass
        else:
            pass
        
        is_data_available: bool = True if len(full_report) != 0 else False 

        return {
            "status": "OK" if is_data_available else "FAIL",
            "statusCode": 200 if is_data_available else 404,
            "details": parsing_details,
            "body": full_report
        }


    # the generated documents are uploaded to firebase storage and the download link extracted is returned
    def __upload_document(self, *, file_path:str) -> dict:
        """
        The filename being must be provided with its extension 

        filename list contains a list with elements:-
            1. ATTENDANCE_REPORT  (filename prefix)
            2. month_name         (filename suffix)
            3. .xlsx              (extension)
        """
        data = {
            "statusCode": 200,
            "download_url": "",
            "details": ""
        }

        todays_date = dt.now().strftime("%Y-%m-%d") # yyyy-MM-dd format

        '''
        this is the folder structure of the firebase storage
        attendance_documents_records
            |- datetime
                  |- file_path
        '''
        attendance_storage_path: str = f"attendance_documents_records/{todays_date}/{file_path}"
        blob = self.__bucket.blob(attendance_storage_path)

        try:
            blob.upload_from_filename(f'{file_path}')
            blob.make_public()

            data["download_url"] = blob.public_url
            data["details"] = "[*] File uploaded successfully\n[*] File link generated successfully"
                    
        except FileNotFoundError as fnfe:
            data["statusCode"] = 404
            data["download_url"] = ""
            data["details"] = "File Not Found :-\n It must be an Internal Server File Generation Issue\nContact your administration"
        
        except Exception as e:
            data["statusCode"] = 404
            data["download_url"] = ""
            data["details"] = f"An Unknown Error Occured:- \n{e}"
        
        return data


    # push attendance details to firebase storage and update details in firebase
    def push_attendance_document(self, *, monthname: str, file_path: str):

        status: dict = {
            "status": "OK",
            "statusCode": 200,
            "details": "",
            "downloadUrl": ""
        }

        todays_date = dt.now().strftime("%Y-%m-%d") # yyyy-MM-dd format

        """
        filename list contains a list with elements:-
            1. ATTENDANCE_REPORT  (filename prefix)
            2. month_name         (filename suffix)
            3. .xlsx              (extension)
        """
        file_name: list[str] = ["ATTENDANCE_REPORT_", monthname.upper(), ".xlsx"]

        referencer = self.__attendance_documents
        
        # this avoid multiple db hits
        data_dict = referencer.get().to_dict()

        if data_dict != {}: # documents are generated at least once
            daily_fetch_limit = data_dict.get(todays_date)
            if daily_fetch_limit != None: # documents generated of the given month
                limit:int = daily_fetch_limit.get("limit")
                if limit < self.__fetch_days_limit(): # admin has today's limit

                    # generate the download url
                    download_url_data: dict = self.__upload_document(file_path=file_path) 
                    
                    if(download_url_data['statusCode'] == 200):  # file uploading and link generation success

                        download_url = download_url_data['download_url']

                        # update the status
                        status["status"] = "OK"
                        status["statusCode"] = 200
                        status["details"] = "Your Document Generated Successfully"
                        status["downloadUrl"] =  download_url

                        # update the limit
                        referencer.update({
                            todays_date: {
                                "limit": limit+1, # increase the limit by 1
                                "download_url": download_url
                            }
                        })

                        return status
                    else:                                       #  File not found or any other issue see the logs
                        status = download_url_data
                        return status
                else:                                 # admin hit today's limit
                    # update the status
                    status["status"] = "FAIL"
                    status["statusCode"] = 429
                    status["details"] = "You Hit Today's Attendance Document Generation Limit"
                    status["downloadUrl"] = ""
                    return status
            else:                                                     # documents aren't generated of the given month
                # generate new documents with this skeleton field
                '''
                "datetime": {
                    "file_url": "url",
                    "daily_limits": int
                }
                '''

                # generate the download url
                download_url_data: dict = self.__upload_document(file_path=file_path) 
                
                if(download_url_data['statusCode'] == 200):  # file uploading and link generation success
                    download_url = download_url_data['download_url']

                    # update the status
                    status["status"] = "OK"
                    status["statusCode"] = 200
                    status["details"] = "Your Document Generated Successfully"
                    status["downloadUrl"] =  download_url

                    # update the limit
                    referencer.update({
                        todays_date: {
                            "limit": 1, # set to 1
                            "download_url": download_url
                        }
                    })
                    return status
                else:                                       #  File not found or any other issue see the logs
                        status = download_url_data
                        return status

        else:                               # not a single document generated yet
            # generate the download url
            download_url_data: dict = self.__upload_document(file_path=file_path) 
            
            if(download_url_data['statusCode'] == 200):  # file uploading and link generation success
                download_url = download_url_data['download_url']

                # update the status
                status["status"] = "OK"
                status["statusCode"] = 200
                status["details"] = "Your Document Generated Successfully"
                status["downloadUrl"] =  download_url

                # update the limit
                referencer.update({
                    todays_date: {
                        "limit": 1, # set to 1
                        "download_url": download_url
                    }
                })
                return status
            else:                                       #  File not found or any other issue see the logs
                    status = download_url_data
                    return status
        

    # To calculate the daily working hours based on the punch in and out timing(s)
    def __calculate_daily_hours(self, punch_in, punch_out):
        if punch_in == "NA" or punch_out == "NA":
            return 0
        try:
            fmt = "%H:%M:%S"  # For HH:mm:ss format (e.g., "08:00:00")
            in_time = dt.strptime(punch_in, fmt)
            out_time = dt.strptime(punch_out, fmt)
            hours = (out_time - in_time).total_seconds() / 3600
            return max(0, round(hours, 2))  # Ensure no negative hours
        except (ValueError, TypeError):
            return 0
