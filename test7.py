from zipfile import ZipFile
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import pandas as pd

def get_content(docx_path):
    with ZipFile(docx_path, 'r') as docx:
        document_xml = docx.read('word/document.xml')
    return document_xml

def accept_changes(xml_str):
    soup = BeautifulSoup(xml_str, 'lxml-xml')
    for ins_tag in tqdm(soup.find_all('w:ins'),"accept addition"):
        ins_tag.unwrap()
    for del_tag in tqdm(soup.find_all('w:del'),"accept deletion"):
        del_tag.decompose()
    modified_xml = str(soup)
    return modified_xml

def get_row_data(row):
    row_data = []
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
    rows = table.find_all('w:tr')
    for row in rows:
        row_data = get_row_data(row)
        table_data.append(row_data)
    table_json = json.dumps(table_data, indent=4, ensure_ascii=False)
    return table_json

def docx_to_df(docx_file):
    c = get_content(docx_file)
    s= accept_changes(c)
    jt = xml_to_json(s)
    j = json.loads(jt)
    df = pd.DataFrame(j)
    df.columns = ["index","time","original","translated"]
    return df

docx_file = "testfile\\20241211\\test6.docx"
df = docx_to_df(docx_file)
print(df)