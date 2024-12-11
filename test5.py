import zipfile
import xml.etree.ElementTree as ET
import pandas as pd

def accept_changes_in_docx(docx_path):
    # 解压 .docx 文件，读取 document.xml 文件
    with zipfile.ZipFile(docx_path, 'r') as docx:
        document_xml = docx.read('word/document.xml')

    # 解析 document.xml
    tree = ET.ElementTree(ET.fromstring(document_xml))
    root = tree.getroot()

    # XML 命名空间
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # 获取文档中的所有表格
    tables = root.findall('.//w:tbl', ns)
    if not tables:
        raise ValueError("文档中没有找到表格")

    # 假设只有一个表格
    table = tables[0]

    # 遍历表格中的每一行和每个单元格
    table_data = []
    for row in table.findall('.//w:tr', ns):
        row_data = []
        for cell in row.findall('.//w:tc', ns):
            # 获取单元格中的所有段落
            paragraphs = cell.findall('.//w:p', ns)
            cell_text = ""
            for para in paragraphs:
                # 获取所有插入（<w:ins>）的文本并合并
                for ins in para.findall('.//w:ins', ns):
                    if ins.text:
                        cell_text += ins.text
                # 移除删除的文本（<w:delText>）
                for del_text in para.findall('.//w:del', ns):
                    para.remove(del_text)  # 删除删除标记
                # 合并原段落文本
                if para.text:
                    cell_text += para.text
            row_data.append(cell_text.strip())  # 清除多余的空白字符
        table_data.append(row_data)

    # 转化为 DataFrame
    df = pd.DataFrame(table_data)
    return df

# 示例使用
df = accept_changes_in_docx('input_with_changes.docx')
print(df)
