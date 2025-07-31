def merge_files(files):
    """Merges multiple text-based files into one."""
    merged_content = ""
    for file_content in files:
        merged_content += file_content + "\n"
    return merged_content

def check_duplicates(content):
    """Checks for duplicate lines in a string."""
    lines = content.splitlines()
    total = len(lines)
    unique = len(set(lines))
    duplicates = total - unique
    return total, unique, duplicates

import vobject

def remove_duplicates(content):
    """Removes duplicate lines from a string."""
    lines = content.splitlines()
    return "\n".join(sorted(list(set(lines))))

def add_contact(content, name, phone, is_vcf):
    """Adds a contact to a VCF or TXT file."""
    if is_vcf:
        vcard = vobject.vCard()
        vcard.add('fn').value = name
        vcard.add('tel').value = phone
        return content + "\n" + vcard.serialize()
    else:
        return content + "\n" + phone

def delete_number(content, number, is_vcf):
    """Deletes a number from a VCF or TXT file."""
    if is_vcf:
        new_content = ""
        for vcard in vobject.readComponents(content):
            if hasattr(vcard, 'tel') and vcard.tel.value != number:
                new_content += vcard.serialize()
        return new_content
    else:
        lines = content.splitlines()
        new_lines = [line for line in lines if line != number]
        return "\n".join(new_lines)

def split_file(content, contacts_per_file, is_vcf):
    """Splits a VCF or TXT file into multiple parts."""
    files = []
    if is_vcf:
        vcards = list(vobject.readComponents(content))
        total_contacts = len(vcards)
        for i in range(0, total_contacts, contacts_per_file):
            chunk = vcards[i:i + contacts_per_file]
            files.append({
                "name": f"split_{i // contacts_per_file + 1}.vcf",
                "content": "".join([v.serialize() for v in chunk])
            })
    else:
        lines = content.splitlines()
        total_lines = len(lines)
        for i in range(0, total_lines, contacts_per_file):
            chunk = lines[i:i + contacts_per_file]
            files.append({
                "name": f"split_{i // contacts_per_file + 1}.txt",
                "content": "\n".join(chunk)
            })
    return files

def create_file_from_manual_input(contacts, as_vcf):
    """Creates a TXT or VCF file from manual input."""
    if as_vcf:
        vcf_content = ""
        for contact in contacts:
            vcard = vobject.vCard()
            vcard.add('fn').value = contact['name']
            vcard.add('tel').value = contact['phone']
            vcf_content += vcard.serialize()
        return vcf_content
    else:
        return "\n".join([contact['phone'] for contact in contacts])
