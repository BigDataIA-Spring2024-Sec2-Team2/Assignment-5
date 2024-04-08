
from PyPDF2 import PdfReader
import os


pdf_files = ['sample-question-pdfs/sample-level-i-questions.pdf', 'sample-question-pdfs/sample-level-i-questions.pdf', 'sample-question-pdfs/sample-level-i-questions.pdf']
start_line = "Answers to Sample Level"

output_directory = "parsed-text-files/"

for idx, pdf_file in enumerate(pdf_files):
    with open(pdf_file, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)

        all_text = ''

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            all_text += page.extract_text()

        sections = all_text.split(start_line)

        text_file_name = f'sample-level-i-questions{idx + 1}'

        for i, section in enumerate(sections[1:]): 
            section = section.strip()  
       
            text_file_path = os.path.join(output_directory, f'{text_file_name}_{i + 1}.txt')
            with open(text_file_path, 'w') as text_file:
                text_file.write(section)

