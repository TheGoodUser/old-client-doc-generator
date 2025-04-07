# 📂 old-client

Generates monthly attendance `.xlsx` reports from Firebase Firestore for a client’s employee management system. Supports **local testing** and **cloud deployment via AWS Lambda**.

---

## ⚙️ Tech Stack

- AWS Lambda
- Firebase (Firestore + Storage)
- Python (`firebase-admin`, `openpyxl`, `dotenv` (only till local testing))
- CI/CD via GitHub Actions
- Deployment via YAML config

---

## 📁 Firestore Structure

Ensure your Firestore looks like:

- `documents-generation`
  - `attendance-documents`
    - `{2025-04-01}` (date document)
  - `attendance-fetch-daily-limit`
- `employee-details`
  - `<employee_doc_id>`

📌 Refer to the image ![Firestore Structure](https://i.ibb.co/4n93RMSx/Untitled.png) for visual reference.

---

## 🌍 `.env` Setup

```
# Firestore
DOCUMENTS_GENERATION_COLLECTION_NAME=documents-generation
EMPLOYEE_DETAILS_COLLECTION_NAME=employee-details

# Document names
ATTENDANCE_DOCUMENTS=attendance-documents
ATTENDANCE_FETCH_DAILY_LIMIT_DOCUMENT=attendance-fetch-daily-limit
EMPLOYEE_DETAILS_DOCUMENT_NAME=<your_employee_doc_id>

# Firebase Storage
FIREBASE_STORAGE_BUCKET_URL=<your-firebase-bucket-url>

# exclue gs:// at the begining of the <your-firebase-bucket-url>
```

#### 🔒 Note: In production, manage these via Lambda Environment Variables instead of .env.

## 🧪 Local Testing
✅ Both file generation and Firestore/Storage operations are supported locally.

## Steps: 
  - <i>Make sure to :-</i>
    - Place your Firebase Admin SDK as `firebase-config.json`.
    - Populate Firestore following the structure above.
    - 📌 `lambda_handler()` is the AWS Lambda entry point.
Manually invoke it for local testing.
1. Set up a <b>virtual environment</b>

  - #### Windows
```
python -m venv myvenv
myvenv\Scripts\activate
```
- #### Linux/macOS
```
python3 -m venv myvenv
source myvenv/bin/activate
```
---
2. Install dependencies

  - #### Windows
```
pip install -r requirements.txt
```
- #### Linux/macOS
```
pip3 install -r requirements.txt
```
---
3. launch the program

  - #### Windows
```
python lambda_function.py
```
- #### Linux/macOS
```
python3 lambda_function.py
```






## 🔐 Security Concerns
 - ❌ Never commit `.env` or `firebase-config.json` to version control.

 - ✅ Use Firebase rules to restrict Firestore/Storage access.

 - ✅ Set Lambda Function URL access to authenticated only or use API key headers (you can test without authentication too).

 - ✅ Follow least privilege for IAM roles (Lambda, Firebase, CloudWatch).
---

## 📦 File Structure

| File              | Purpose                                                                 |
|-------------------|-------------------------------------------------------------------------|
| `pdf_generator.py` | Generates `.xlsx` files (legacy name from PDF generation functionality) |
| `firebase_crud.py` | Handles Firebase Firestore and Storage operations                       |
| `.env`            | Local environment configuration (use Lambda environment in production)  |
| `*.yaml`          | AWS Lambda deployment configuration files                              |
| `README.md`       | Project documentation (this file)                                      |
## Usage

### Environment Configuration
- In production, set these variables in AWS Lambda environment

### Deployment
- Configure AWS Lambda settings in the respective `.yaml` files, go through the `.github\workflows\lambda_deplayment.yaml` file for more information.

## Notes
- The `.xlsx` generation in `pdf_generator.py` maintains a legacy name but handles PDF generation

## 👨‍💻 Author / Contact
Built by [Siddharth Roy](https://www.linkedin.com/in/siddharth--roy/).
<br>
DM on LinkedIn if any setup issues arise or for help with AWS/Firebase.

