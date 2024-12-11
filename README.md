# PDF Details Extractor API

This Flask application provides an API to upload PDF files and extract structured information using regular expressions and text processing techniques. The extracted details include certificate, employer, employee, salary, tax, and verification information.

---

## Features
- Upload and process PDF files.
- Extract detailed, structured information from the uploaded PDF.
- Designed to process specific structured text data like Form 16.
- Uses regular expressions for precise data extraction.

---

## Prerequisites
Before running this application, ensure you have the following installed:

1. Python 3.6+
2. Flask library
3. PyPDF2 library

---

## Installation

### Step 1: Clone the Repository
```bash
$ git clone <repository-url>
$ cd <repository-folder>
```

### Step 2: Set Up a Virtual Environment (Optional but Recommended)
```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
$ pip install -r requirements.txt
```

**Note:** If `requirements.txt` does not exist, manually install dependencies:
```bash
$ pip install flask pypdf2
```

---

## Running the Application

### Step 1: Start the Flask Application
```bash
$ python app.py
```

### Step 2: Access the API

The application will start on `http://127.0.0.1:5000` by default. You can use tools like `Postman` or `curl` to interact with the API.

---

## API Endpoint

### Endpoint: `/upload`

**Method:** `POST`

**Description:** Accepts a PDF file and returns extracted details.

#### Request
- Content-Type: `multipart/form-data`
- Field: `file`
- Value: PDF file to be uploaded

#### Example Using `curl`
```bash
curl -X POST -F "file=@<path-to-your-pdf>.pdf" http://127.0.0.1:5000/upload
```

#### Example Using Postman
1. Open Postman.
2. Set the request type to `POST`.
3. Enter `http://127.0.0.1:5000/upload` as the URL.
4. Under the `Body` tab, choose `form-data`.
5. Add a key named `file` and upload your PDF.
6. Hit `Send`.

---

## Explanation of the Code

### Step-by-Step Breakdown

1. **Import Libraries**:
   - `Flask`: To create the web API.
   - `request`: To handle incoming HTTP requests.
   - `jsonify`: To send JSON responses.
   - `PyPDF2`: To extract text from PDF files.
   - `re`: For regular expression-based text extraction.

2. **Define the Flask Application**:
   - Initialize the app using `Flask(__name__)`.

3. **PDF Text Extraction Function**:
   - The `extract_details_from_pdf` function parses PDF text and extracts data using regex patterns.
   - Includes helper functions:
     - `safe_search`: Safely perform regex matching.
     - `clean_text`: Clean unwanted characters from extracted values.

4. **Structured Data**:
   - Organizes the extracted data into a nested dictionary for easy access.

5. **File Upload Endpoint (`/upload`)**:
   - Accepts `POST` requests.
   - Reads the uploaded PDF file and extracts text using `PyPDF2`.
   - Calls `extract_details_from_pdf` to structure the extracted text.
   - Returns the structured data as a JSON response.

6. **Error Handling**:
   - Returns meaningful error messages if no file is uploaded or if any exception occurs.

7. **Run the Application**:
   - Starts the Flask server in debug mode.

---

## Example Output
### Request:
```json
POST /upload
{
  "file": "form16.pdf"
}
```

### Response:
```json
{
  "data": {
    "form_no": 16,
    "certificate_details": {
      "certificate_no": "123456",
      "updated_on": "12-Dec-2024",
      "assessment_year": "2023-24"
    },
    "employer_details": {
      "name": "ABC Corp",
      "address": "1234 Street Name",
      "contact": "9876543210",
      "email": "hr@abccorp.com",
      "pan": "ABCDE1234F",
      "tan": "TAN1234ABC"
    },
    "employee_details": {
      "name": "John Doe",
      "address": "5678 Avenue",
      "pan": "EFGHI5678J",
      "period_with_employer": {
        "from": "01-Apr-2023",
        "to": "31-Mar-2024"
      }
    },
    ...
  }
# PDF Details Extractor API

This Flask application provides an API to upload PDF files and extract structured information using regular expressions and text processing techniques. The extracted details include certificate, employer, employee, salary, tax, and verification information.

---

## Features
- Upload and process PDF files.
- Extract detailed, structured information from the uploaded PDF.
- Designed to process specific structured text data like Form 16.
- Uses regular expressions for precise data extraction.

---

## Prerequisites
Before running this application, ensure you have the following installed:

1. Python 3.6+
2. Flask library
3. PyPDF2 library

---

## Installation

### Step 1: Clone the Repository
```bash
$ git clone <repository-url>
$ cd <repository-folder>
```

### Step 2: Set Up a Virtual Environment (Optional but Recommended)
```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
$ pip install -r requirements.txt
```

**Note:** If `requirements.txt` does not exist, manually install dependencies:
```bash
$ pip install flask pypdf2
```

---

## Running the Application

### Step 1: Start the Flask Application
```bash
$ python app.py
```

### Step 2: Access the API

The application will start on `http://127.0.0.1:5000` by default. You can use tools like `Postman` or `curl` to interact with the API.

---

## API Endpoint

### Endpoint: `/upload`

**Method:** `POST`

**Description:** Accepts a PDF file and returns extracted details.

#### Request
- Content-Type: `multipart/form-data`
- Field: `file`
- Value: PDF file to be uploaded

#### Example Using `curl`
```bash
curl -X POST -F "file=@<path-to-your-pdf>.pdf" http://127.0.0.1:5000/upload
```

#### Example Using Postman
1. Open Postman.
2. Set the request type to `POST`.
3. Enter `http://127.0.0.1:5000/upload` as the URL.
4. Under the `Body` tab, choose `form-data`.
5. Add a key named `file` and upload your PDF.
6. Hit `Send`.

---

## Explanation of the Code

### Step-by-Step Breakdown

1. **Import Libraries**:
   - `Flask`: To create the web API.
   - `request`: To handle incoming HTTP requests.
   - `jsonify`: To send JSON responses.
   - `PyPDF2`: To extract text from PDF files.
   - `re`: For regular expression-based text extraction.

2. **Define the Flask Application**:
   - Initialize the app using `Flask(__name__)`.

3. **PDF Text Extraction Function**:
   - The `extract_details_from_pdf` function parses PDF text and extracts data using regex patterns.
   - Includes helper functions:
     - `safe_search`: Safely perform regex matching.
     - `clean_text`: Clean unwanted characters from extracted values.

4. **Structured Data**:
   - Organizes the extracted data into a nested dictionary for easy access.

5. **File Upload Endpoint (`/upload`)**:
   - Accepts `POST` requests.
   - Reads the uploaded PDF file and extracts text using `PyPDF2`.
   - Calls `extract_details_from_pdf` to structure the extracted text.
   - Returns the structured data as a JSON response.

6. **Error Handling**:
   - Returns meaningful error messages if no file is uploaded or if any exception occurs.

7. **Run the Application**:
   - Starts the Flask server in debug mode.

---
