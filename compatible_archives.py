# Note: this already accounts for many archive suffixes. an epub for example can be a zip archive (index 0 below).
compatible_arch = ['Zip', '7-zip', 'gzip', 'bzip2']

group_zipfile_compat = ['Zip archive']
group_py7zr_compat = ['7-zip archive']
group_tarfile_compat = ['gzip compressed', 'bzip2 compressed']
