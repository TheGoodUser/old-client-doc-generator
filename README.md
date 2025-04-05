# Attendance PDF Generator

This project is designed to generate attendance reports in XLSX format for clients. It automates the process of creating professional and organized attendance documents.

## Features

- Generate attendance reports in XLSX format.
- Supports exporting and saving XLSX locally.
- It generates the the XLSX files with a daily limit of 10 API requests

## Prerequisites

- Python 3.x
- Required libraries:
    - `reportlab`
    - `openpyxl`

## Installation

1. Clone the repository:
     ```bash
     git clone https://github.com/TheGoodUser/old-client-doc-generator.git
     ```
2. Navigate to the project directory:
     ```bash
     cd old-client-doc-generator
     ```
3. Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

## Usage

1. For now these command are execute on the basis of the aws lambda function url.

## Project Structure

```
/old-client-doc-generator
project-root/
├── firebase_crud.py             # Handles Firebase Storage/Firestore CRUD operations
├── firebase-config.json         # Firebase config JSON file (service account credentials)
├── lambda_function.py           # Entry point for AWS Lambda deployment
├── package.json                 # (Optional) Node.js config file (possibly unused here)
├── package-lock.json            # Lock file for exact package versions (if using Node.js)
├── pdf_generator.py             # Generates PDFs (likely attendance or report-related)
├── README.md                    # Project overview, usage, setup instructions
├── requirements.txt             # Python dependencies list
└── reports/                     # Directory to store generated PDF or report files
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries, please contact [your-email@example.com].
