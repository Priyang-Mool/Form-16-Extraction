# PDF Details Extraction API

This project is a Flask-based web application that processes uploaded PDF files, extracts relevant data using regular expressions, and returns the structured details in JSON format. The primary purpose of this application is to parse Form 16 or similar tax-related documents to extract structured information about certificates, employers, employees, salary, tax details, and verification.

---

## Features

- Extracts certificate details such as certificate number, assessment year, and last updated date.
- Extracts employer and employee details, including names, addresses, contact information, PAN, and TAN.
- Parses salary details, including gross salary breakdown, deductions, and taxable income.
- Extracts tax details such as total tax, surcharges, and health cess.
- Parses verification details like place, date, and verified-by details.

---

## Prerequisites

Ensure the following are installed on your system:

1. Python 3.6 or higher
2. pip (Python package manager)

---

## Installation

Follow these steps to set up and run the application:

### 1. Clone the repository
```bash
$ git clone <repository_url>
$ cd <repository_directory>
```

### 2. Set up a virtual environment (Optional but recommended)
```bash
$ python -m venv venv
$ source venv/bin/activate   # On Linux/MacOS
$ venv\Scripts\activate    # On Windows
```

### 3. Install dependencies
```bash
$ pip install flask pypdf2
```

### 4. Start the Flask server
```bash
$ python app.py
```

The server will run at `http://127.0.0.1:5000` by default.

---

## Usage

### API Endpoint
**POST /upload**

### Request
Send a `POST` request to the `/upload` endpoint with a PDF file attached under the key `file`.

#### Example using `curl`:
```bash
$ curl -X POST -F "file=@path_to_pdf_file.pdf" http://127.0.0.1:5000/upload
```

```

### Response
On success, the server returns a JSON object containing extracted details. Example:
```json
{
    "data": {
        "form_no": 16,
        "certificate_details": {
            "certificate_no": "ABC12345",
            "updated_on": "12-Dec-2024",
            "assessment_year": "2024-25"
        },
        "employer_details": {
            "name": "ABC Pvt Ltd",
            "address": "123, Main Street",
            "contact": "1234567890",
            "email": "example@company.com",
            "pan": "ABCDE1234F",
            "tan": "ABCDE12345"
        },
        ...
    }
}
```

In case of an error (e.g., invalid file format), the server responds with an error message and a 400/500 HTTP status code.

---

## Code Explanation

### 1. **`extract_details_from_pdf` function**
This is the core function that processes the text extracted from the PDF and organizes it into a structured format. It uses:

- **`safe_search`**: A helper function for safely applying regex patterns to extract specific information.
- **`clean_text`**: A helper function to clean up unwanted characters from extracted text.

The function organizes the extracted details into the following categories:

1. **Certificate Details**: Certificate number, assessment year, and update date.
2. **Employer Details**: Name, address, PAN, TAN, and contact information.
3. **Employee Details**: Name, address, PAN, and employment period.
4. **Salary Details**: Gross salary breakdown, deductions, and taxable income.
5. **Tax Details**: Total tax payable, surcharges, rebates, and cess.
6. **Verification Details**: Place, date, and details of the verifier.

### 2. **PDF Upload Endpoint (`/upload`)**
This Flask route handles file uploads and:

- Validates the presence of a file.
- Reads the content of the PDF using `PyPDF2.PdfReader`.
- Passes the extracted text to `extract_details_from_pdf` for processing.
- Returns the structured JSON response or an error message.

### 3. **Error Handling**
Handles various exceptions such as missing files or PDF parsing errors and provides meaningful error messages.

---

## Testing

1. Use the provided `curl` or Python examples to test the API.
2. Upload a valid PDF (e.g., a Form 16 document) and check the response JSON.

---

## Dependencies

- **Flask**: Web framework for handling API requests.
- **PyPDF2**: Library for reading and extracting text from PDFs.
- **re**: Python's regular expression module for text parsing.

---
