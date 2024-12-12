from zipfile import ZipFile
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

from io import BytesIO
import json
from tqdm import tqdm

from docx import Document
import pandas as pd

def get_content(docx_path):
    # Open the docx file (it's a zip archive)
    with ZipFile(docx_path, 'r') as docx:
        # Extract the document.xml file, which contains the main content
        document_xml = docx.read('word/document.xml')

    return document_xml

def accept_changes(xml_str):
    # Parse the XML content using BeautifulSoup
    soup = BeautifulSoup(xml_str, 'lxml-xml')

    # Loop through all the "w:ins" and "w:del" elements
    # "w:ins" means inserted text and "w:del" means deleted text in tracked changes
    for ins_tag in tqdm(soup.find_all('w:ins'),"accept addition"):
        ins_tag.unwrap()  # This removes the insertion mark but keeps the text

    for del_tag in tqdm(soup.find_all('w:del'),"accept deletion"):
        del_tag.decompose()  # Completely remove the deleted element

    # # Convert the modified BeautifulSoup object back to XML
    modified_xml = str(soup)

    return modified_xml

# def xml_to_dataframe(xml_str):
#     soup = BeautifulSoup(xml_str, 'lxml-xml')
#     # Step 4: Find all tables in the document
#     tables = soup.find_all('w:tbl')  # Look for all tables (w:tbl) elements

#     if not tables:
#         raise ValueError("No table found in the document.")

#     # Step 5: Get the first table (assuming only one table exists)
#     table = tables[0]

#     # Step 6: Build the HTML for the table
#     xml = '<table border="1">'  # Start HTML table

#     rows = table.find_all('w:tr')  # Find all table rows

#     for row in rows:
#         xml += '<tr>'  # Start a new row
#         cells = row.find_all('w:tc')  # Find all table cells in the row

#         for cell in cells:
#             # Extract text from each <w:t> (text) tag inside the cell
#             cell_text = combine_cell_text(cell)
#             xml += f'<td>{cell_text}</td>'  # Add the cell data to the HTML row

#         xml += '</tr>'  # End the row

#     xml += '</table>'  # End HTML table

#     # Step 7: Parse the HTML table with BeautifulSoup
#     table_soup = BeautifulSoup(xml, 'html.parser')

#     # Step 8: Convert the HTML table to a Pandas DataFrame
#     df = pd.read_xml(str(table_soup))[0]  # The first table in the HTML

#     return df

# def combine_cell_text(cell):
#     t = []
#     for text in cell.find_all('w:t'):
#         clean_text = text.get_text().strip()
#         if clean_text:
#             t.append(clean_text)
#     cell_text = ' '.join(t)
#     return cell_text

def get_row_data(row):
    row_data = []

    # Find all cells in the row
    cells = row.find_all('w:tc')

    for cell in cells:
        cell_text = combine_cell(cell)
        row_data.append(cell_text)

    return row_data

def combine_cell(cell):
    paragraphs = cell.find_all('w:p')

    combined_paragraphs = []
    for para in paragraphs:
        texts = para.find_all('w:t')

        combined_text = ""
        for text in texts:
            combined_text = combined_text + text.get_text()
        combined_text = combined_text.strip()

        combined_paragraphs.append(combined_text)

    combined_cell = "\n".join(combined_paragraphs)

    return combined_cell

def xml_to_json(xml_str):
    soup = BeautifulSoup(xml_str, 'lxml-xml')

    tables = soup.find_all('w:tbl')
    if not tables:
        raise ValueError("No table found in the document.")

    table = tables[0]

    table_data = []

    # Iterate over rows (<w:tr>) in the table
    rows = table.find_all('w:tr')
    for row in rows:
        row_data = get_row_data(row)

        table_data.append(row_data)

    table_json = json.dumps(table_data, indent=4, ensure_ascii=False)
    # print(table_json)
    return table_json

def docx_to_df(docx_file):
    c = get_content(docx_file)
    s= accept_changes(c)
    jt = xml_to_json(s)
    j = json.loads(jt)
    df = pd.DataFrame(j)
    df.columns = ["index","time","original","translated"]
    return df

# Usage example:
docx_file = "testfile\\20241211\\test6.docx"  # Path to your DOCX file

# Print the DataFrame
df = docx_to_df(docx_file)
print(df)