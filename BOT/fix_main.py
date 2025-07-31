#!/usr/bin/env python3

with open('main.py', 'r') as f:
    lines = f.readlines()

# Fix the problematic lines
for i, line in enumerate(lines):
    if 'WAITING_FILE_FOR_INFO:' in line:
        lines[i] = '            # WAITING_FILE_FOR_INFO: [MessageHandler(filters.Document.ALL, # perform_get_file_info)],\n'
    elif 'perform_get_file_info' in line and 'WAITING_FILE_FOR_INFO' not in line:
        lines[i] = line.replace('perform_get_file_info', '# perform_get_file_info')
    elif 'cancel_file_info' in line:
        lines[i] = line.replace('cancel_file_info', 'cancel')
    elif 'file_info_conv_handler' in line and 'add_handler' in line:
        lines[i] = '    # ' + line

with open('main.py', 'w') as f:
    f.writelines(lines)

print('Fixed main.py')
