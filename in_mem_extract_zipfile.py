import zipfile


def extract_zip(input_zip):
    input_zip = zipfile.ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}


mem_ex = extract_zip(input_zip='./test_files/test.epub')
print(str(mem_ex))
