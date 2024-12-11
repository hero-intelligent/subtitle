from zipfile import ZipFile
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from docx import Document

from io import BytesIO

from tqdm import tqdm

import pandas as pd


def accept_changes_in_docx(docx_path):
    # Open the docx file (it's a zip archive)
    with ZipFile(docx_path, 'r') as docx:
        # Extract the document.xml file, which contains the main content
        document_xml = docx.read('word/document.xml')

    # Parse the XML content using BeautifulSoup
    soup = BeautifulSoup(document_xml, 'lxml-xml')

    # Loop through all the "w:ins" and "w:del" elements
    # "w:ins" means inserted text and "w:del" means deleted text in tracked changes
    for ins_tag in tqdm(soup.find_all('w:ins'),"accept addition"):
        ins_tag.unwrap()  # This removes the insertion mark but keeps the text

    for del_tag in tqdm(soup.find_all('w:del'),"accept deletion"):
        del_tag.decompose()  # Completely remove the deleted element

    # # Convert the modified BeautifulSoup object back to XML
    # modified_xml = str(soup)

    # Step 4: Find all tables in the document
    tables = soup.find_all('w:tbl')  # Look for all tables (w:tbl) elements
    
    if not tables:
        raise ValueError("No table found in the document.")
    
    # Step 5: Get the first table (assuming only one table exists)
    table = tables[0]

    # Step 6: Build the HTML for the table
    html = '<table border="1">'  # Start HTML table
    
    rows = table.find_all('w:tr')  # Find all table rows
    
    for row in rows:
        html += '<tr>'  # Start a new row
        cells = row.find_all('w:tc')  # Find all table cells in the row
        
        for cell in cells:
            # Extract text from each <w:t> (text) tag inside the cell
            cell_text = combine_cell_text(cell)
            html += f'<td>{cell_text}</td>'  # Add the cell data to the HTML row
        
        html += '</tr>'  # End the row
    
    html += '</table>'  # End HTML table
    
    # Step 7: Parse the HTML table with BeautifulSoup
    table_soup = BeautifulSoup(html, 'html.parser')
    
    # Step 8: Convert the HTML table to a Pandas DataFrame
    df = pd.read_html(str(table_soup))[0]  # The first table in the HTML
    
    return df



def combine_cell_text(cell):
    t = []
    for text in cell.find_all('w:t'):
        clean_text = text.get_text().strip()
        if clean_text:
            t.append(clean_text)
    cell_text = ' '.join(t)
    return cell_text







import zipfile
from bs4 import BeautifulSoup
import pandas as pd

def docx_table_to_dataframe(docx_file):
    # Step 1: Open the DOCX file (which is essentially a ZIP archive)
    with zipfile.ZipFile(docx_file, 'r') as docx:
        # Step 2: Extract the document.xml file containing the table data
        xml_content = docx.read('word/document.xml')
    
    # Step 3: Parse the XML content with BeautifulSoup
    soup = BeautifulSoup(xml_content, 'xml')  # We use 'xml' parser for XML content
    
    # Step 4: Find all tables in the document
    tables = soup.find_all('w:tbl')  # Look for all tables (w:tbl) elements
    
    if not tables:
        raise ValueError("No table found in the document.")
    
    # Step 5: Get the first table (assuming only one table exists)
    table = tables[0]

    # Step 6: Build the HTML for the table
    html = '<table border="1">'  # Start HTML table
    
    rows = table.find_all('w:tr')  # Find all table rows
    
    for row in rows:
        html += '<tr>'  # Start a new row
        cells = row.find_all('w:tc')  # Find all table cells in the row
        
        for cell in cells:
            # Extract text from each <w:t> (text) tag inside the cell
            cell_text = ' '.join([text.get_text().strip() for text in cell.find_all('w:t') if text.get_text().strip()])
            html += f'<td>{cell_text}</td>'  # Add the cell data to the HTML row
        
        html += '</tr>'  # End the row
    
    html += '</table>'  # End HTML table
    
    # Step 7: Parse the HTML table with BeautifulSoup
    table_soup = BeautifulSoup(html, 'html.parser')
    
    # Step 8: Convert the HTML table to a Pandas DataFrame
    df = pd.read_html(str(table_soup))[0]  # The first table in the HTML
    
    return df

# Usage example:
docx_file = 'your_file.docx'  # Path to your DOCX file
df = docx_table_to_dataframe(docx_file)

# Print the DataFrame
print(df)
