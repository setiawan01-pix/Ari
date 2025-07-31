import os
import re
import pandas as pd
from typing import List, Tuple, Dict
from datetime import datetime

class FileConverter:
    def __init__(self, temp_folder: str = "temp"):
        self.temp_folder = temp_folder
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
    
    def txt_to_vcf_tutor_kiks(self, txt_file_path: str, base_filename: str, 
                             base_contact_name: str, contacts_per_file: int, 
                             start_order: int) -> List[str]:
        """
        Convert TXT to VCF with TUTOR KIKS format
        """
        # Read phone numbers from TXT file
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            phone_numbers = [line.strip() for line in f if line.strip()]
        
        # Remove duplicates and clean numbers
        phone_numbers = list(set(phone_numbers))
        phone_numbers = [self.clean_phone_number(num) for num in phone_numbers]
        phone_numbers = [num for num in phone_numbers if num]
        
        if not phone_numbers:
            raise ValueError("Tidak ada nomor telepon yang valid dalam file")
        
        # Split into chunks
        chunks = [phone_numbers[i:i + contacts_per_file] 
                 for i in range(0, len(phone_numbers), contacts_per_file)]
        
        vcf_files = []
        
        for i, chunk in enumerate(chunks):
            file_number = start_order + i
            vcf_filename = f"{base_filename}-{file_number}.vcf"
            vcf_path = os.path.join(self.temp_folder, vcf_filename)
            
            with open(vcf_path, 'w', encoding='utf-8') as vcf_file:
                for j, phone in enumerate(chunk):
                    contact_number = j + 1
                    contact_name = f"{base_contact_name}-{file_number}-{contact_number}"
                    
                    vcf_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{contact_name}
TEL;TYPE=CELL:{phone}
END:VCARD
"""
                    vcf_file.write(vcf_content)
            
            vcf_files.append(vcf_path)
        
        return vcf_files
    
    def split_txt_file(self, txt_file_path: str, lines_per_file: int) -> List[str]:
        """
        Split TXT file into multiple files
        """
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Split into chunks
        chunks = [lines[i:i + lines_per_file] 
                 for i in range(0, len(lines), lines_per_file)]
        
        split_files = []
        base_name = os.path.splitext(os.path.basename(txt_file_path))[0]
        
        for i, chunk in enumerate(chunks):
            split_filename = f"{base_name}-{i+1}.txt"
            split_path = os.path.join(self.temp_folder, split_filename)
            
            with open(split_path, 'w', encoding='utf-8') as split_file:
                split_file.writelines(chunk)
            
            split_files.append(split_path)
        
        return split_files
    
    def vcf_to_txt(self, vcf_file_path: str) -> str:
        """
        Extract phone numbers from VCF file to TXT
        """
        phone_numbers = []
        
        with open(vcf_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract phone numbers using regex
        phone_pattern = r'TEL;TYPE=CELL:(\+?[\d\s\-\(\)]+)'
        matches = re.findall(phone_pattern, content)
        
        for match in matches:
            phone = self.clean_phone_number(match)
            if phone:
                phone_numbers.append(phone)
        
        # Remove duplicates
        phone_numbers = list(set(phone_numbers))
        
        # Save to TXT file
        output_filename = f"extracted_numbers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        output_path = os.path.join(self.temp_folder, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for phone in phone_numbers:
                f.write(f"{phone}\n")
        
        return output_path
    
    def xls_to_vcf(self, xls_file_path: str) -> str:
        """
        Convert Excel file to VCF
        """
        try:
            # Read Excel file
            if xls_file_path.endswith('.xlsx'):
                df = pd.read_excel(xls_file_path, engine='openpyxl')
            else:
                df = pd.read_excel(xls_file_path, engine='xlrd')
            
            # Check if we have at least 2 columns
            if len(df.columns) < 2:
                raise ValueError("File Excel harus memiliki minimal 2 kolom (Nama dan Nomor)")
            
            # Use first two columns as name and phone
            names = df.iloc[:, 0].astype(str)
            phones = df.iloc[:, 1].astype(str)
            
            # Clean phone numbers
            phones = [self.clean_phone_number(phone) for phone in phones]
            
            # Create VCF file
            output_filename = f"converted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.vcf"
            output_path = os.path.join(self.temp_folder, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as vcf_file:
                for name, phone in zip(names, phones):
                    if phone:  # Only add if phone number is valid
                        vcf_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL;TYPE=CELL:{phone}
END:VCARD
"""
                        vcf_file.write(vcf_content)
            
            return output_path
            
        except Exception as e:
            raise ValueError(f"Error membaca file Excel: {str(e)}")
    
    def clean_phone_number(self, phone: str) -> str:
        """
        Clean and validate phone number
        """
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d\+]', '', phone)
        
        # Handle Indonesian phone numbers
        if cleaned.startswith('+62'):
            return cleaned
        elif cleaned.startswith('62'):
            return '+' + cleaned
        elif cleaned.startswith('0'):
            return '+62' + cleaned[1:]
        elif len(cleaned) >= 10:
            return '+62' + cleaned
        
        return cleaned
    
    def merge_files(self, file_paths: List[str], output_filename: str) -> str:
        """
        Merge multiple files into one
        """
        if not file_paths:
            raise ValueError("Tidak ada file yang diberikan")
        
        # Determine output extension based on first file
        first_ext = os.path.splitext(file_paths[0])[1].lower()
        output_path = os.path.join(self.temp_folder, f"{output_filename}{first_ext}")
        
        with open(output_path, 'w', encoding='utf-8') as output_file:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as input_file:
                        output_file.write(input_file.read())
                        output_file.write('\n')  # Add separator
        
        return output_path
    
    def check_duplicates(self, file_path: str) -> Dict:
        """
        Check for duplicates in file
        """
        phone_numbers = []
        
        if file_path.endswith('.vcf'):
            # Extract from VCF
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            phone_pattern = r'TEL;TYPE=CELL:(\+?[\d\s\-\(\)]+)'
            matches = re.findall(phone_pattern, content)
            phone_numbers = [self.clean_phone_number(match) for match in matches]
        else:
            # Read from TXT
            with open(file_path, 'r', encoding='utf-8') as f:
                phone_numbers = [self.clean_phone_number(line.strip()) for line in f]
        
        # Remove empty numbers
        phone_numbers = [num for num in phone_numbers if num]
        
        # Count duplicates
        total = len(phone_numbers)
        unique = len(set(phone_numbers))
        duplicates = total - unique
        
        return {
            'total': total,
            'unique': unique,
            'duplicates': duplicates,
            'duplicate_numbers': [num for num in set(phone_numbers) if phone_numbers.count(num) > 1]
        }
    
    def remove_duplicates(self, file_path: str) -> str:
        """
        Remove duplicates from file
        """
        phone_numbers = []
        
        if file_path.endswith('.vcf'):
            # Extract from VCF
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            phone_pattern = r'TEL;TYPE=CELL:(\+?[\d\s\-\(\)]+)'
            matches = re.findall(phone_pattern, content)
            phone_numbers = [self.clean_phone_number(match) for match in matches]
        else:
            # Read from TXT
            with open(file_path, 'r', encoding='utf-8') as f:
                phone_numbers = [self.clean_phone_number(line.strip()) for line in f]
        
        # Remove empty numbers and duplicates
        phone_numbers = list(set([num for num in phone_numbers if num]))
        
        # Create output file
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_filename = f"{base_name}_no_duplicates"
        
        if file_path.endswith('.vcf'):
            output_path = os.path.join(self.temp_folder, f"{output_filename}.vcf")
            with open(output_path, 'w', encoding='utf-8') as vcf_file:
                for i, phone in enumerate(phone_numbers):
                    vcf_content = f"""BEGIN:VCARD
VERSION:3.0
FN:Contact-{i+1}
TEL;TYPE=CELL:{phone}
END:VCARD
"""
                    vcf_file.write(vcf_content)
        else:
            output_path = os.path.join(self.temp_folder, f"{output_filename}.txt")
            with open(output_path, 'w', encoding='utf-8') as txt_file:
                for phone in phone_numbers:
                    txt_file.write(f"{phone}\n")
        
        return output_path
    
    def add_contact(self, file_path: str, name: str, phone: str) -> str:
        """
        Add new contact to file
        """
        phone = self.clean_phone_number(phone)
        if not phone:
            raise ValueError("Nomor telepon tidak valid")
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_filename = f"{base_name}_with_new_contact"
        
        if file_path.endswith('.vcf'):
            output_path = os.path.join(self.temp_folder, f"{output_filename}.vcf")
            
            # Copy existing content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add new contact
            new_vcf = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL;TYPE=CELL:{phone}
END:VCARD
"""
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                f.write(new_vcf)
        else:
            output_path = os.path.join(self.temp_folder, f"{output_filename}.txt")
            
            # Copy existing content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                f.write(f"{phone}\n")
        
        return output_path
    
    def delete_number(self, file_path: str, number_to_delete: str) -> str:
        """
        Delete specific number from file
        """
        number_to_delete = self.clean_phone_number(number_to_delete)
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_filename = f"{base_name}_without_{number_to_delete.replace('+', '')}"
        
        if file_path.endswith('.vcf'):
            output_path = os.path.join(self.temp_folder, f"{output_filename}.vcf")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into vCards
            vcards = content.split('BEGIN:VCARD')
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for vcard in vcards:
                    if vcard.strip():
                        # Check if this vCard contains the number to delete
                        if number_to_delete not in vcard:
                            f.write('BEGIN:VCARD' + vcard)
        else:
            output_path = os.path.join(self.temp_folder, f"{output_filename}.txt")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if self.clean_phone_number(line.strip()) != number_to_delete:
                        f.write(line)
        
        return output_path
    
    def split_large_file(self, file_path: str, contacts_per_part: int) -> List[str]:
        """
        Split large file into smaller parts
        """
        phone_numbers = []
        
        if file_path.endswith('.vcf'):
            # Extract from VCF
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            phone_pattern = r'TEL;TYPE=CELL:(\+?[\d\s\-\(\)]+)'
            matches = re.findall(phone_pattern, content)
            phone_numbers = [self.clean_phone_number(match) for match in matches]
        else:
            # Read from TXT
            with open(file_path, 'r', encoding='utf-8') as f:
                phone_numbers = [self.clean_phone_number(line.strip()) for line in f]
        
        # Remove empty numbers
        phone_numbers = [num for num in phone_numbers if num]
        
        # Split into chunks
        chunks = [phone_numbers[i:i + contacts_per_part] 
                 for i in range(0, len(phone_numbers), contacts_per_part)]
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        split_files = []
        
        for i, chunk in enumerate(chunks):
            if file_path.endswith('.vcf'):
                split_filename = f"{base_name}_part_{i+1}.vcf"
                split_path = os.path.join(self.temp_folder, split_filename)
                
                with open(split_path, 'w', encoding='utf-8') as vcf_file:
                    for j, phone in enumerate(chunk):
                        vcf_content = f"""BEGIN:VCARD
VERSION:3.0
FN:Contact-{j+1}
TEL;TYPE=CELL:{phone}
END:VCARD
"""
                        vcf_file.write(vcf_content)
            else:
                split_filename = f"{base_name}_part_{i+1}.txt"
                split_path = os.path.join(self.temp_folder, split_filename)
                
                with open(split_path, 'w', encoding='utf-8') as txt_file:
                    for phone in chunk:
                        txt_file.write(f"{phone}\n")
            
            split_files.append(split_path)
        
        return split_files
    
    def manual_input_to_file(self, contacts: List[Tuple[str, str]], file_type: str) -> str:
        """
        Save manual input contacts to file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if file_type == 'vcf':
            output_filename = f"manual_contacts_{timestamp}.vcf"
            output_path = os.path.join(self.temp_folder, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as vcf_file:
                for name, phone in contacts:
                    phone = self.clean_phone_number(phone)
                    if phone:
                        vcf_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL;TYPE=CELL:{phone}
END:VCARD
"""
                        vcf_file.write(vcf_content)
        else:
            output_filename = f"manual_contacts_{timestamp}.txt"
            output_path = os.path.join(self.temp_folder, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as txt_file:
                for name, phone in contacts:
                    phone = self.clean_phone_number(phone)
                    if phone:
                        txt_file.write(f"{phone}\n")
        
        return output_path

# Global instance
converter = FileConverter()
