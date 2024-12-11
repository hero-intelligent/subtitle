import zipfile
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from docx import Document

def accept_changes_in_docx(docx_path, output_path):
    # Open the docx file (it's a zip archive)
    with zipfile.ZipFile(docx_path, 'r') as docx:
        # Extract the document.xml file, which contains the main content
        document_xml = docx.read('word/document.xml')

        # Parse the XML content using BeautifulSoup
        soup = BeautifulSoup(document_xml, 'xml')

        # Loop through all the "w:ins" and "w:del" elements
        # "w:ins" means inserted text and "w:del" means deleted text in tracked changes
        for ins_tag in soup.find_all('w:ins'):
            ins_tag.unwrap()  # This removes the insertion mark but keeps the text

        for del_tag in soup.find_all('w:del'):
            del_tag.decompose()  # Completely remove the deleted element

        # Convert the modified BeautifulSoup object back to XML
        modified_xml = str(soup)

        # Write the modified XML content back into the DOCX file
        with zipfile.ZipFile(output_path, 'w') as docx_out:
            # Add all original files except the document.xml
            for file in docx.namelist():
                if file != 'word/document.xml':
                    docx_out.writestr(file, docx.read(file))

            # Write the modified document.xml into the DOCX package
            docx_out.writestr('word/document.xml', modified_xml)

    print(f"Changes accepted and saved to {output_path}")

# Example usage:
# docx_path = 'example_with_changes.docx'  # Path to the DOCX file
# output_path = 'output_accepted_changes.docx'  # Output path for the modified DOCX file

docx_path = "F:\workdir\DONT GIVE UP_EP23_cn_es-Mooo-lq.docx"
output_path = "test6.docx"
accept_changes_in_docx(docx_path, output_path)
