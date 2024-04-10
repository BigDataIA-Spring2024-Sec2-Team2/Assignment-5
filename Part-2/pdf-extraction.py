
from PyPDF2 import PdfReader
import os
import io

from google.cloud import storage


PATH = os.path.join(os.getcwd() , 'assignment-5-419501-a5d63f5d9476.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

def gcp_store_from_string(string_data, file_name):
    bucket = storage_client.get_bucket('assignment5-group2')
    blob = bucket.blob(file_name)
    blob.upload_from_string(string_data)

def gcp_read_string(file_name):
    file_obj = io.BytesIO()
    bucket = storage_client.get_bucket('assignment5-group2')
    blob = bucket.blob(file_name)
    blob.download_to_file(file_obj)
    return file_obj


pdf_files = ['pdfFiles/sample-level-i-questions.pdf', 'pdfFiles/sample-level-i-questions.pdf', 'pdfFiles/sample-level-i-questions.pdf']
start_line = "Answers to Sample Level"

output_directory = "pdfToText/"

for idx, pdf_file in enumerate(pdf_files):
    pdf_reader = PdfReader(gcp_read_string(pdf_file))
    num_pages = len(pdf_reader.pages)

    all_text = ''

    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        all_text += page.extract_text()

    sections = all_text.split(start_line)

    text_file_name = f'sample-questions{idx + 1}'

    for i, section in enumerate(sections[1:]): 
        section = section.strip()  
        
        file_name = f'{output_directory}{text_file_name}.txt'
        print(file_name)
            
        gcp_store_from_string(section, file_name)

