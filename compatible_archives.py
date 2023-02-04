# Note: this already accounts for many archive suffixes. an epub for example can be a zip archive (index 0 below).
compatible_arch = ['Zip', '7-zip', 'gzip', 'bzip2']

# Add beginning (concise) or full (strict) result of magic buffer to below groups appropriately if needed.
# If add new group, then also add new method to handler_file.py.
group_zipfile_compat = ['Zip archive']
group_py7zr_compat = ['7-zip archive']
group_tarfile_compat = ['bzip2 compressed']
group_gzip_compat = ['gzip compressed']
