
# Attendance PDF Generator (AWS Lambda + Firebase)

This small project auto-generates attendance reports in XLSX format. Built for client-side usage with Firebase and AWS Lambda integration.

## 🔥 Features

- Create clean attendance XLSX reports.
- Can be exported/downloaded locally.
- AWS Lambda supported (with 10 request/day limit).
- Firebase Storage used for uploading files.

## 🛠️ Prerequisites

- Python 3.x installed
- Setup a virtual environment locally (important!)
- Required packages (via `requirements.txt`):
  - `firebase_admin`
  - `openpyxl`
  - `dotenv` *(exclude this in production)*

> Note: On production (Lambda), `firebase_admin` & `openpyxl` are added as AWS Lambda layers. So locally, make sure to install them via pip.

## 📦 Installation (for local use)

```bash
git clone https://github.com/TheGoodUser/your-repo-name.git
cd your-repo-name
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 🚀 Usage

This tool is triggered via an AWS Lambda POST API. It fetches data, processes the attendance, and uploads the file to Firebase.

```python
# Just run the lambda_function.py locally (or test using API)
python lambda_function.py
```

Or send a POST request to the AWS Lambda endpoint with:
```json
{ "monthname": "April" }
```

## 🧱 Project Structure

```
project-root/
├── firebase_crud.py          # Handles Firebase interaction
├── firebase-config.json      # Firebase service account key
├── lambda_function.py        # Entry point (Lambda or local test)
├── pdf_generator.py          # Creates the XLSX attendance sheet
├── requirements.txt          # Local-only Python dependencies
├── reports/                  # Stores generated files locally
└── README.md                 # This file
```

## 🤝 Contributing

Clone it, tweak it, test it — then send a pull request. Let's keep it simple.

## 📄 License

MIT — do whatever you want but don’t blame me later 😄

## 📬 Contact

For issues or help: [your-email@example.com]
```

Let me know if you want the Lambda deploy instructions too.