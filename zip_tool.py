try:
    import BytesIO
except ImportError:
    from io import BytesIO  # Python 3
import zipfile


class InMemoryZip(object):
    def __init__(self):
        # Create the in-memory file-like object for working w/IMZ
        self.in_memory_zip = BytesIO()

    # Just zip it, zip it
    def append(self, filename_in_zip, file_contents):
        # Appends a file with name filename_in_zip and contents of
        # file_contents to the in-memory zip.
        # Get a handle to the in-memory zip in append mode
        zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)

        # Write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)

        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
            zfile.create_system = 0

        return self

    def read(self):
        # Returns a string with the contents of the in-memory zip.
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()

    # Zip it, zip it, zip it
    def writetofile(self, filename):
        # Writes the in-memory zip to a physical file.
        with open(filename, "wb") as file:
            file.write(self.read())


if __name__ == "__main__":
    # Run a test
    imz = InMemoryZip()
    imz.append('./test_files/test.epub', "Make a test").append("testfile2.txt", "And another one")
    # imz.writetofile("testfile.zip")
    read_imz = imz.read()
    print(read_imz)
    print("testfile.zip created")
