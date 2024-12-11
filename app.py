from flask import Flask, request, jsonify
import PyPDF2
import re

app = Flask(__name__)

def extract_details_from_pdf(pdf_text):
    """
    Extract structured details from the PDF text with precise regex matching and data cleaning.
    """
    def safe_search(pattern, text, group_index=1):
        """
        Perform a safe regex search and return the specified group or None.
        """
        match = re.search(pattern, text)
        return match.group(group_index).strip() if match else None

    def clean_text(value):
        """
        Clean unwanted characters or trailing artifacts from the extracted text.
        """
        return value.replace("\n", " ").strip() if value else None

    data = {
        "form_no": 16,
        "certificate_details": {},
        "employer_details": {},
        "employee_details": {},
        "salary_details": {
            "gross_salary": {"breakup": {}},
            "deductions": {"under_section_16": {}},
            "income": {},
            "chapter_vi_a_deductions": {},
        },
        "tax_details": {},
        "verification": {"verified_by": {}},
    }

    # Extract certificate details
    data["certificate_details"]["certificate_no"] = safe_search(r"Certificate Number:\s*(\S+)", pdf_text)
    data["certificate_details"]["updated_on"] = safe_search(r"Last updated on\s*([\d\-A-Za-z]+)", pdf_text)
    data["certificate_details"]["assessment_year"] = safe_search(r"Assessment Year\s*([\d\-]+)", pdf_text)

    # Extract employer details
    employer_address_match = re.search(
        r"Name and address of the Employer.*?\n([\s\S]*?)\n([\s\S]*?),\s*(Karnataka|[\w\-]+)", pdf_text
    )
    if employer_address_match:
        data["employer_details"]["name"] = clean_text(employer_address_match.group(1))
        data["employer_details"]["address"] = clean_text(employer_address_match.group(2))
    data["employer_details"]["contact"] = safe_search(r"\+\(91\)([\d\-]+)", pdf_text)
    data["employer_details"]["email"] = safe_search(r"([\w\.-]+@[\w\.-]+)", pdf_text).lower()
    data["employer_details"]["pan"] = safe_search(r"PAN of the Deductor\s*([\w\d]+)", pdf_text)
    data["employer_details"]["tan"] = safe_search(r"TAN of the Deductor\s*([\w\d]+)", pdf_text)

    # Extract employee details
    employee_address_match = re.search(
        r"Name and address of the Employee.*?\n(.*?)\n([\s\S]*?),\s*(Karnataka|[\w\-]+)", pdf_text
    )
    if employee_address_match:
        data["employee_details"]["name"] = clean_text(employee_address_match.group(1))
        data["employee_details"]["address"] = clean_text(employee_address_match.group(2))
    data["employee_details"]["pan"] = safe_search(r"PAN of the Employee.*?\s([\w\d]+)", pdf_text)
    data["employee_details"]["period_with_employer"] = {
        "from": safe_search(r"From\s([\d\-]+\w+)", pdf_text),
        "to": safe_search(r"To\s([\d\-]+\w+)", pdf_text),
    }

    # Extract salary details
    data["salary_details"]["gross_salary"]["total"] = safe_search(r"Total\s([\d\.]+)", pdf_text)
    data["salary_details"]["gross_salary"]["breakup"]["section_17_1"] = safe_search(r"17\(1\)\s([\d\.]+)", pdf_text)
    data["salary_details"]["gross_salary"]["breakup"]["profits_in_lieu"] = safe_search(r"17\(3\)\s([\d\.]+)", pdf_text)
    data["salary_details"]["deductions"]["under_section_16"]["standard_deduction"] = safe_search(
        r"Standard deduction under section 16\(ia\)\s([\d\.]+)", pdf_text
    )
    data["salary_details"]["deductions"]["under_section_16"]["entertainment_allowance"] = safe_search(
        r"Entertainment allowance under section 16\(ii\)\s([\d\.]+)", pdf_text
    )
    data["salary_details"]["deductions"]["under_section_16"]["tax_on_employment"] = safe_search(
        r"Tax on employment under section 16\(iii\)\s([\d\.]+)", pdf_text
    )
    data["salary_details"]["income"]["salary_received"] = safe_search(r"Income chargeable.*\s([\d\.]+)", pdf_text)
    data["salary_details"]["income"]["gross_total_income"] = data["salary_details"]["income"]["salary_received"]
    data["salary_details"]["chapter_vi_a_deductions"]["total"] = safe_search(r"Chapter VI-A deductions.*\s([\d\.]+)", pdf_text)
    data["salary_details"]["income"]["taxable_income"] = data["salary_details"]["income"]["gross_total_income"]

    # Extract tax details
    data["tax_details"]["total_tax"] = safe_search(r"Total tax payable.*\s([\d\.]+)", pdf_text)
    data["tax_details"]["surcharge"] = safe_search(r"Surcharge.*\s([\d\.]+)", pdf_text)
    data["tax_details"]["rebate_under_section_87A"] = safe_search(r"Rebate under section 87A.*\s([\d\.]+)", pdf_text)
    data["tax_details"]["health_and_education_cess"] = safe_search(r"Health and education cess.*\s([\d\.]+)", pdf_text)
    data["tax_details"]["relief_under_section_89"] = safe_search(r"Relief under section 89.*\s([\d\.]+)", pdf_text)
    data["tax_details"]["net_tax_payable"] = safe_search(r"Net tax payable.*\s([\d\.]+)", pdf_text)

    # Extract verification details
    data["verification"]["place"] = safe_search(r"Place\s([^\n]+)", pdf_text)
    data["verification"]["date"] = safe_search(r"Date\s([\d\-A-Za-z]+)", pdf_text)
    data["verification"]["verified_by"]["name"] = clean_text(safe_search(r"Full Name:\s*([\w\s]+)", pdf_text))
    data["verification"]["verified_by"]["designation"] = safe_search(r"Designation:\s*([\w\s]+)", pdf_text)

    return data

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    try:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_text = ''
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()

        extracted_data = extract_details_from_pdf(pdf_text)
        return jsonify({"data": extracted_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
