import vobject
import openpyxl
from io import BytesIO

def txt_to_vcf(txt_content, file_name_base, contact_name_base, contacts_per_file, start_order):
    lines = [line.strip() for line in txt_content.splitlines() if line.strip()]  # Remove empty lines
    total_contacts = len(lines)
    files = []
    
    current_file_number = start_order

    for i in range(0, total_contacts, contacts_per_file):
        vcf_content = ""
        contact_counter = 1
        
        for j in range(i, min(i + contacts_per_file, total_contacts)):
            vcard = vobject.vCard()
            # Format: REXX-1-1, REXX-1-2 (contact_name_base-file_number-contact_number)
            vcard.add('fn').value = f"{contact_name_base}-{current_file_number}-{contact_counter}"
            vcard.add('tel').value = lines[j]
            vcf_content += vcard.serialize()
            contact_counter += 1

        # Format: OLXX-1.vcf, OLXX-2.vcf (file_name_base-file_number.vcf)
        files.append({
            "name": f"{file_name_base}-{current_file_number}.vcf",
            "content": vcf_content
        })
        current_file_number += 1

    return files

def split_txt(txt_content, lines_per_file):
    lines = txt_content.splitlines()
    total_lines = len(lines)
    files = []

    for i in range(0, total_lines, lines_per_file):
        chunk = lines[i:i + lines_per_file]
        files.append({
            "name": f"split_{i // lines_per_file + 1}.txt",
            "content": "\n".join(chunk)
        })

    return files

def vcf_to_txt(vcf_content):
    txt_content = ""
    for vcard in vobject.readComponents(vcf_content):
        if hasattr(vcard, 'tel'):
            txt_content += vcard.tel.value + "\n"
    return txt_content

def xls_to_vcf(xls_content):
    vcf_content = ""
    workbook = openpyxl.load_workbook(BytesIO(xls_content))
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=1):
        name = row[0].value
        phone = row[1].value
        if name and phone:
            vcard = vobject.vCard()
            vcard.add('fn').value = str(name)
            vcard.add('tel').value = str(phone)
            vcf_content += vcard.serialize()

    return vcf_content
