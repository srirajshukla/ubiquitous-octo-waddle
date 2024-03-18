import fitz
import requests
import pandas as pd
import re
from llm.vector_chain import gen_esg_vector

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

endpoint = "https://team-orange.cognitiveservices.azure.com/"
key = "6c106509d1c34958aeb7fff48c806a5a"

class Table:
    def __init__(self, rows, columns, default_value=""):
        self.rows = rows
        self.columns = columns
        self.table = [[default_value for _ in range(columns)] for _ in range(rows)]

    def get_value(self, row, column):
        return self.table[row][column]

    def set_value(self, row, column, value):
        self.table[row][column] = value

    def get_table(self):
        strTable = ""
        for row in self.table:
            strTable += str(row) + ","
        return strTable

    def print_table(self):
        for row in self.table:
            print(row)

def find_matching_texts(text):
    regex_pattern = r"(?s)\((C(?:-FS)?\d+(?:\.\d+)?[a-z]?)\)(.*?)(?=\((C(?:-FS)?\d+(?:\.\d+)?[a-z]?)\)|$)"
    matches = re.findall(regex_pattern, text)

    result_dict = {}

    for match in matches:
        start_pattern, captured_text, end_pattern = match
        result_dict[start_pattern] = captured_text.strip()

    all_c_patterns = re.findall(r"(?s)\((C(?:-FS)?\d+(?:\.\d+)?[a-z]?)\)", text)

    for c_pattern in all_c_patterns:
        if c_pattern not in result_dict:
            result_dict[c_pattern] = ""

    return result_dict

def analyze_layout(pdf_path):
    tables = {}
    tablecells = {}
    print_table = {}

    with open(pdf_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-layout", pdf_content
    )
    result = poller.result()
    data = ""
    for table_idx, table in enumerate(result.tables):
        mytable = Table(table.row_count, table.column_count)
        for cell in table.cells:
            mytable.set_value(cell.row_index, cell.column_index, cell.content)
            if len(cell.spans) == 0:
                continue
            tablecells[cell.spans[0].offset] = table_idx
        tables[table_idx] = mytable
        print_table[table_idx] = False
    
    for element in result.paragraphs:
        if len(element.spans) == 0:
            continue
        item = tablecells.get(element.spans[0].offset)
        if item is not None:
            if print_table[item] == False:
                data += tables[item].get_table() + "\n"
                print_table[item] = True
        else:
            # print(element.content)
            if element.content.startswith("Page"):
                continue
            data += str(element.content) + "\n"
    
    return data

def extract_specific_questions_from_pdf(pdf_path):
    questions = []
    pdf_document = fitz.open(pdf_path)

    question_pattern = r"\((C(?:-FS)?\d+(?:\.\d+)?[a-z]?)\) (.+?)(?:\.|\?)(?=\s)"

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]

        text = page.get_text()
        question_matches = re.findall(question_pattern, text, re.DOTALL)
        questions.extend(question_matches)

    pdf_document.close()

    return questions

def create_pdf_with_answers(year, input_pdf_path, output_pdf_path):
    questions = extract_specific_questions_from_pdf(input_pdf_path)
    que = find_matching_texts(analyze_layout(input_pdf_path))
    esg_vector_chain = gen_esg_vector(year)

    output_pdf = fitz.open() 
    y_coordinate = 50  # Initial y-coordinate for the first question
    page = output_pdf.new_page()  

    for question_number, question_text in questions:
        tableflag = 0
        # Check if inserting the next text would exceed the page height
        question_text = question_text.replace('\n', '')
        if y_coordinate + 150 >= page.rect.height:
            page = output_pdf.new_page()  # Create a new page
            y_coordinate = 50  # Reset y-coordinate

        # Insert question number with purple color
        page.insert_text((50, y_coordinate), f"{question_number}:", color=(0.5, 0, 0.5))  
        if y_coordinate + 20 >= page.rect.height:
            y_coordinate += 40  # Move to the next line
        else:
            y_coordinate += 20  # Move to the next line

        # Insert a horizontal line below the answer
        page.draw_line((50, y_coordinate - 2), (550, y_coordinate - 2))  
        if y_coordinate + 20 >= page.rect.height:
            y_coordinate += 40  # Move to the next line
        else:
            y_coordinate += 20  # Move to the next line
            
        # Insert question text
        #question_text = question_text.FONT_BOLD
        if len(question_text) > 99:
            substrings = []
            for i in range(0, len(question_text), 99):
                substrings.append(question_text[i:i+99])
            for i in substrings:
                page.insert_text((50, y_coordinate), f"{i}", color=(0.5, 0, 0.5))  # Adjust position and color as needed
                y_coordinate += 20  # Move to the next line
            
            
        else:
            page.insert_text((50, y_coordinate), f"{question_number}: {question_text}", color=(0.5, 0, 0.5)) 
            y_coordinate += 20  # Move to the next line
        if y_coordinate + 150 >= page.rect.height:
                    page = output_pdf.new_page()
                    y_coordinate  = 50  # new page and reset y cor
        #tablemap
        #print(matching_texts[question_number])
        print(f"Question: {question_text}")
        if "Please complete the following table" in que[question_number]:
            url = f'https://guidance.cdp.net/en/guidance?cid={question_number}&ctype=ExternalRef&gettags=0&idtype=RecordExternalRef&incchild=0%C2%B5site%3D0&otype=Guidance&page=1'
            html = requests.get(url).content
            column_dict = {}
            df_list = pd.read_html(html)
            for table in df_list:
                for column_name, column_data in table.items():
                    if not isinstance(column_name, str):
                         continue
                    column_values = column_data.tolist()
                    resquery = f"Question: {question_text} Sub-question: {column_name} Response-option: {column_values}"
                    response = esg_vector_chain.invoke(resquery)
                    column_dict[column_name] = response["result"]
            # print(column_dict)
            for column_name, column_values in column_dict.items():
                #columnname
                substrings = []
                for i in range(0, len(column_name), 99):
                        substrings.append(column_name[i:i+99])
                for i in substrings:
                    page.insert_text((50, y_coordinate), f"{i}", color=(0.5, 0, 0.5))  
                    y_coordinate += 20  # Move to the next line
                if y_coordinate + 50 >= page.rect.height:
                        page = output_pdf.new_page()
                        y_coordinate  = 50
                
                    #columnvalues
                substrings = []
                for i in range(0, len(column_values), 99):
                        ind = column_values[i: i+ 99].find('\n')
                        if ind != -1:
                            substrings.append(column_values[i:i+ind])
                            ind = - 1
                            continue
                        substrings.append(column_values[i:i+99])
                for i in substrings:
                    page.insert_text((50, y_coordinate), f"{i}")  
                    y_coordinate += 20  # Move to the next line
                if y_coordinate + 50 >= page.rect.height:
                        page = output_pdf.new_page()
                        y_coordinate  = 50
            
                y_coordinate += 20
            y_coordinate += 50  # Move to the next line after the table

        else:
            response = esg_vector_chain.invoke(question_text)
            answer = response["result"]
            # print(answer)
            if len(answer) > 99:
                substrings = []
                for i in range(0, len(answer), 99):
                    ind = answer[i: i+ 99].find('\n')
                    if ind != -1:
                        substrings.append(answer[i:i+ind])
                        ind = - 1
                        continue
                    substrings.append(answer[i:i+99])
                for i in substrings:
                    page.insert_text((50, y_coordinate), f"{i}")  
                    y_coordinate += 20  # Move to the next line
                if y_coordinate + 50 >= page.rect.height:
                        page = output_pdf.new_page()
                        y_coordinate  = 50  # new page and reset y cor
            
            else:
                page.insert_text((50, y_coordinate), f"{answer}") 
                y_coordinate += 40  # Move to the next line for the next question
        y_coordinate += 30
    # # Save the output PDF
    output_pdf.save(output_pdf_path)
    output_pdf.close()

    print("New PDF created successfully!")

# pdf_path = "D:\wfhack\challenge-assets\sustainability-survey-automation\Survey-Questions\Survey-Questionnire-Part2.pdf"
# output_pdf_path = 'output.pdf'
# year = "2021"

# # # Create PDF with sample answers for each question
# create_pdf_with_answers(year, pdf_path, output_pdf_path)