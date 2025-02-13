import os
import sys
import traceback
from tqdm import tqdm
from zipfile import ZipFile
from bs4 import BeautifulSoup
from io import BytesIO

def accept_changes(input, output):
    # Open the docx file (it's a zip archive)
    with ZipFile(input, 'r') as docx:
        modified = []

        # accept changes in word/document.xml, which contains inserts and deletions
        document_xml = docx.read('word/document.xml')
        modified.append('word/document.xml')

        soup_document = BeautifulSoup(document_xml, 'lxml-xml')
        for ins_tag in tqdm(soup_document.find_all('w:ins'),"accepting inserts"):
            ins_tag.unwrap()
        for del_tag in tqdm(soup_document.find_all('w:del'),"accepting deletions"):
            if del_tag.find("w:delText"):
                del_tag.decompose()
        for del_tag in tqdm(soup_document.find_all('w:del'),"accepting deletions"):
            if del_tag.decomposed:
                continue
            if not del_tag.contents:
                rpr_tag = del_tag.parent
                ppr_tag = rpr_tag.parent
                ppr_name = ppr_tag.name
                if ppr_name == "pPr":
                    p_tag = ppr_tag.parent
                    p2_tag = p_tag.find_next_sibling('p')
                    t_tags = p2_tag.find_all('t')
                    if t_tags:
                        r_tags = p_tag.find_all('r')
                        r2_tags = p2_tag.find_all('r')
                        for tag in reversed(r2_tags):
                            r_tags[-1].insert_after(tag)
                    p2_tag.decompose()
                del_tag.decompose()

        for style_change_tag in tqdm(soup_document.find_all('w:pPrChange'),"accepting style change"):
            style_change_tag.unwrap()
        for style_change_tag in tqdm(soup_document.find_all('w:rPrChange'),"accepting style change"):
            style_change_tag.unwrap()

        modified_document_xml = str(soup_document)

        # accept style change in word/styles.xml
        styles_xml = docx.read('word/styles.xml')
        modified.append('word/styles.xml')

        soup_style = BeautifulSoup(styles_xml, 'lxml-xml')
        for style_change_tag in tqdm(soup_style.find_all('w:pPrChange'),"accepting style change"):
            style_change_tag.unwrap()
        for style_change_tag in tqdm(soup_style.find_all('w:rPrChange'),"accepting style change"):
            style_change_tag.unwrap()

        modified_styles_xml = str(soup_style)

        # Write back the modified files
        with ZipFile(output, 'w') as docx_out:
            # Add all original files except the modified
            for file in docx.namelist():
                if file not in modified:
                    docx_out.writestr(file, docx.read(file))

            # Write the modified files into the DOCX package
            docx_out.writestr('word/document.xml', modified_document_xml)
            docx_out.writestr('word/styles.xml', modified_styles_xml)

    print(f"Changes accepted and saved to {output}")

def comments_anonymize(input, output, name):
    with ZipFile(input, "r") as docx, ZipFile(output, "w") as docx_out:
        for file_name in docx.namelist():
            try:  
                with docx.open(file_name, 'r') as file:  
                    chunk = file.read(1024)  # 读取前1024个字节  
                    file.seek(0)  # 重置文件指针到开始位置  
                    # 尝试以UTF-8编码解码  
                    chunk.decode('utf-8')  
                is_text = True  
            except UnicodeDecodeError:  
                is_text = False  

            xml_content = docx.read(file_name)
            if is_text:
                soup = BeautifulSoup(xml_content, 'lxml-xml')

                if file_name == "docProps/core.xml":
                    dc_creator = soup.find('dc:creator')
                    if dc_creator:
                        dc_creator.string = name
                    cp_last_modified_by = soup.find('cp:lastModifiedBy')
                    if cp_last_modified_by:
                        cp_last_modified_by.string = name

                # for tag in soup.find_all(attrs={'author': True}):
                for tag in tqdm(soup.find_all(), file_name):
                    for attr in tag.attrs:
                        if "author" in attr:
                            tag[attr] = name
                modified_xml_content = str(soup)

                docx_out.writestr(file_name, modified_xml_content)
            else:
                docx_out.writestr(file_name, xml_content)

    print(f"Changes accepted and saved to {output}")

def delete_comments(input, output):
    # Open the docx file (it's a zip archive)
    with ZipFile(input, 'r') as docx:
        modified = []

        # delete comments in word/document.xml
        document_xml = docx.read('word/document.xml')
        modified.append('word/document.xml')

        soup_document = BeautifulSoup(document_xml, 'lxml-xml')

        for comment_start in tqdm(soup_document.find_all("w:commentRangeStart"),"deleting start of comments"):
            comment_start.decompose()
        for comment_end in tqdm(soup_document.find_all("w:commentRangeEnd"),"deleting end of comments"):
            comment_end.decompose()

        comment_reference_tags = soup_document.find_all("w:commentReference")
        for comment_reference in tqdm(comment_reference_tags,"deleting dangling comments"):
            prv_sib = comment_reference.find_previous_sibling("w:rPr")
            if prv_sib.find("w:rStyle"):
                run = comment_reference.find_parent("w:r")
                run.decompose()

        modified_document_xml = str(soup_document)
        
        # delete comments-relevant references and files
        word_rels = docx.read('word/_rels/document.xml.rels')
        modified.append('word/_rels/document.xml.rels')

        soup_word_rels = BeautifulSoup(word_rels,"lxml-xml")
        for relationship in soup_word_rels.find_all('Relationship'):
            type_attr = relationship.get('Type')
            # delete comment-relevant files
            if 'comments' in type_attr:
                modified.append('word/' + relationship.get('Target'))
                relationship.decompose()
        modified_word_rels_xml =  str(soup_word_rels)

        content_types = docx.read('[Content_Types].xml')
        modified.append('[Content_Types].xml')

        soup_content_types = BeautifulSoup(content_types,"lxml-xml")
        for override in soup_content_types.find_all('Override'):
            content_type_attr = override.get('ContentType')
            # delete comment-relevant files
            if 'comments' in content_type_attr:
                # modified.append(override.get('Target'))
                override.decompose()
        modified_content_types_xml =  str(soup_content_types)

        # Write back the modified files
        modified = list(set(modified))
        with ZipFile(output, 'w') as docx_out:
            # Add all original files except the modified
            for file in docx.namelist():
                if file not in modified:
                    docx_out.writestr(file, docx.read(file))

            # Write the modified files into the DOCX package
            docx_out.writestr('word/document.xml', modified_document_xml)
            docx_out.writestr('word/_rels/document.xml.rels', modified_word_rels_xml)
            docx_out.writestr('[Content_Types].xml', modified_content_types_xml)


def yes_or_no(input: str) -> bool:
    if not input or input == "Y" or input == "y":
        result = True
    elif input == "N" or input == "n":
        result = False
    else:
        result = False
        print("You should type y or n", file = sys.stderr)
    
    return result


def process_file(path, review_need_accepted, comments_need_anonymized, comments_need_removed, name):
    with open(path, 'rb') as f:
        content = f.read()
    byte_io_original = BytesIO(content)

    appendix = ""
    path_split = os.path.splitext(path)
    
    if review_need_accepted:
        appendix = appendix + "_review_accepted"
        byte_io_review = BytesIO()
        accept_changes(byte_io_original, byte_io_review)
    else:
        byte_io_review = byte_io_original

    if comments_need_anonymized:
        appendix = appendix + "_comments_anonymized"
        byte_io_comments_anonymized = BytesIO()
        comments_anonymize(byte_io_review, byte_io_comments_anonymized, name)
    else:
        byte_io_comments_anonymized = byte_io_review

    if comments_need_removed:
        appendix = appendix + "_comments_removed"
        byte_io_comments_removed = BytesIO()
        delete_comments(byte_io_comments_anonymized, byte_io_comments_removed)
    else:
        byte_io_comments_removed = byte_io_comments_anonymized

    target = path_split[0] + appendix + path_split[1]
    with open(target, 'wb') as f:
        f.write(byte_io_comments_removed.getvalue())
    print(f"The modified file has been saved at {target}")

def input_name():
    exe_path = sys.executable
    file_path = os.path.dirname(exe_path) + "/name.txt"
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                print("Your name has been saved at name.txt at the same location of this exe.")
                print("Delete it when needed.")
                return lines[-1].strip()
            else:
                print("Your name will be saved at name.txt at the same location of this exe.")
                name = input("What is your name?")
                with open(file_path, 'w') as file:
                    file.write(name)
                return name
    else:
        print("Your name will be saved at name.txt at the same location of this exe.")
        name = input("What is your name?")
        if name:
            with open(file_path, 'w') as file:
                file.write(name)
        return name

def main():
    args = sys.argv[1:]

    review = input("Do you want all tracked changes accepted? Y/n")
    review_need_accepted = yes_or_no(review)

    anonymy = input("Do you want all comments anonymized? Y/n")
    comments_need_anonymized = yes_or_no(anonymy)

    if comments_need_anonymized:
        comments_need_removed = False
        name = input_name()
    else:
        comments = input("Do you want all comments be REMOVED? Y/n")
        comments_need_removed = yes_or_no(comments)
        name = ""

    if review_need_accepted or comments_need_anonymized or comments_need_removed:
        for arg in args:
            print(f"Processing {arg}......")
            process_file(arg, review_need_accepted, comments_need_anonymized, comments_need_removed, name)
            print(f"Done!")
        

if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        if args:
            main()
        else:
            raise ValueError("Please drag and drop your files onto this exe.")
    except Exception as e:
        print("An error occurred:", file=sys.stderr)
        print(e, file = sys.stderr)
        traceback.print_exc(file=sys.stderr)

    input("\n\nPress Enter to exit.")

