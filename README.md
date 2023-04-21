OmegaFind v2. Multi-processed async for better performance.


Overview:

    Learn: Compiles a database of 'trusted' suffix, buffer associations which can
    be used when performing various scan techniques.

    Deobfuscation: This scan technique attempts to expose files that may have been
    obfuscated. Attempted exposition is performed by comparing suffixes and buffers
    of files during deobfuscation scans to 'trusted' buffer, suffix associations
    in the database.

    Type scanning: Aggregates all file types specified. Again not by suffix but by
    known suffix, buffer associations according to the database. Useful in different
    situations including where file(s) may be evading a deobfuscation scan.

    Extract: --extract argument enables discovery of nested compressed files that can
    also be extracted and scanned during various scan techniques if --extract argument
    is used. Password protected archives can also be detected when using --extract,
    password protected files will be added to the results files for further analysis.

    Password scan (--p-scan): pScan attempts to find password protected archives.
    Skips reading database, does not hand database through to child processes and
    performs no buffer/suffix association checks.
 

Help:

    [OmegaFind v2] Forensics tool. Search differently.
    
     -l       Learn                 Specify location to learn from.
     -c       Contents Scan         Specify a directory in which file contents will be scanned.
     -d       De-Obfuscation        Attempt to find files where suffix does not match contents.
     -p       Password Protected    Only scan for password protected archives.
     -r       Reveal                Display all file types.
     -t       Type                  Display all files of type.
     -q       Query                 Specify a search query. Used with -c. -c PATH -q QUERY.
     -sfx     Suffix                Specify suffix. Used with -t.
     -csfx    Custom Suffix         Specify custom suffix group. Used with -t.
     -gsfx    Group Suffix          Specify default suffix group. Used with -t.
                                    archive, audio, book, code, exe, font, image, sheet, slide, text, video, web.
    
     -db      Database              Specify database to use while learning/scanning.
     -e       Extract               Attempt archive extraction while scanning.
     -bmax    Buffer Max            Specify in digits maximum number of bytes to read of each file.
     -cmax    Chunk Max             Specify in digits max chunk size.
     -nsfx    New Suffix Group      Create new custom suffix group.
    
     -A       Associations          Display buffer associations to specified suffix.
     -AV      All Associations      Display all known suffix buffer associations.
     -G       Group                 Display specified suffix group.
     -I       Interact              Disables interaction. No prompt mode.
     -L       List Scan Reports     List and select previously completed scan report.
     -R       Recognized            Display current learning XP.
    
     -v       Verbosity             Increase verbosity.
     -h       Help                  Display this help message.
    
    [Author] Developed and written by Benjamin Jack Cullen.

Download executable and source code bundled with compatible LibreOffice version:

    https://drive.google.com/drive/folders/16z-UuosDoe2DnTaiCxjqh-Sh8RUYtPC2?usp=sharing


Requirements:

    * LibreOffice_7.5.2_Win_x86-64.msi (This specific version of LibreOffice is currently required to ensure
      compatibiity between unoconv and the bundled python.exe version 3.11.2 so that unoconv can work correctly).
      I will try to bundle a portable LibreOffice with OmegaFindv2 to remove the LibreOffice installation dependancy.
      Unoconv is required to work properly only if OmegaFindv2 -c (contents scan) argument is used. 


User:

    * Portable. Except where sys.executabe path may not be path to omega_find.exe.
    * Ensure sufficient ram/page-file/swap if changing buffer_max. ensure chunk_max suits your system while also considering buffer_max.
    * If using --extract then ensure sufficient storage in working directory while also considering buffer_max and chunk_max.
    * Recommended use: 1TB external Storage containing omegaFindv2 at root, so that if using -e argument, there
      is plenty of space available for omegaFindv2 to extract files back into its working directory to scan the
      extracted files. OmegaFindv2 + at least 1TB external drive makes OmegaFindv2 plug n' play on many systems.


Developer:

    Python Version: 3.9+
    OS: Tested and running on Windows 10 and Linux.

    Install modules run: requirements.bat
    
    Running the source code:
    Requires pool.py be placed in aiomultiprocessing. (Backup original pool.py first).
    My edit in pool.py (marked '# my edit' on line 339 in pool.py) enables a dictionary
    to be passed into the child processes when using pool.map() along with the initial
    iterables as there is no manager.dict and obviously no previously set globals for
    the child processes. Lines edited: 337, 339, 345.

    Todo: Feed any errors encountered by patool back into the exception log.
          Refine exception log.
          Further test extraction compatibilies for adding further extractin compatibility.


Extraction Compatibility (Below compatibility accounts for many more file suffixes listed as different suffixes use
    the same compression as below. Like epubs for one example):
    
    patool supports: 7z (.7z), ACE (.ace), ADF (.adf), ALZIP (.alz), APE (.ape), AR (.a), ARC (.arc), ARJ (.arj),
    BZIP2 (.bz2), CAB (.cab), COMPRESS (.Z), CPIO (.cpio), DEB (.deb), DMS (.dms), FLAC (.flac), GZIP (.gz), ISO (.iso),
    LRZIP (.lrz), LZH (.lha, .lzh), LZIP (.lz), LZMA (.lzma), LZOP (.lzo), RPM (.rpm), RAR (.rar), RZIP (.rz), SHN
    (.shn), TAR (.tar), XZ (.xz), ZIP (.zip, .jar), ZOO (.zoo) and ZPAQ (.zpaq) formats.
    It relies on helper applications to handle those archive formats (for example bzip2 for BZIP2 archives).


Gratitude and Thanks:

    Powered by asyncio, aiomultiprocess, aiofiles, python-magic, patool, tabulate, unoconv and of course
    the python standard library.