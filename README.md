OmegaFind v2. Search differently.

Find files by file type, not by what they are called or claim to be.
Multi-processed and asynchronous for high performance.
A digital forensics tool.

Overview:

                                       [SCANNING]

    [ Learn ]
    Compiles a database of 'trusted' suffix, buffer associations which can be used when
    performing various scan techniques. Various scan techniques are only as good as the
    database(s) compiled using this learn feature. Use 'trusted' directories to learn
    from. A database compiled on both Linux and Windows operating systems is included
    however OmegaFindv2 can learn from scratch at any time. You may prefer to learn from
    scratch so that you have more control over what OmegaFindv2 learns and so that you
    can further trust OmegaFindv2 to return expected results from various scan techniques.
    Learning feature is designed to make suffix to buffer associations fast and hands free,
    creating associations faster and easier than it would take to do manually.

    [ Contents Scan (C-SCAN) ]
    Return files containing string.
    Attempts to find strings in many various types of files. Files are read using magic to
    filter how the file will be ultimately read during string search.

    [ Deobfuscation Scan (D-SCAN) ]
    Return files that may have incorrect filename suffix.
    This scan technique attempts to expose files that may have been
    obfuscated in a particular way. Attempted exposition is performed by comparing suffixes
    and buffers of files during deobfuscation scans to 'trusted' buffer, suffix associations
    in the database. False positives can simply be unrecognized files (no suffix to buffer
    relationship exists in the database for that suffix and buffer) or you learned something
    that is incorrect (creating a suffix buffer association that is not true) and the solution
    to reducing false positives is to learn more and learn carefully and on trusted files.

    [ Reveal Scan (R-SCAN) ]
    Return the file type of all files encountered during scan. 

    [ Type Scan (T-SCAN) ]
    Return files of certain types.
    Aggregates all file types specified. Again not by suffix but by known suffix, buffer
    associations according to the database.

    [ Password Scan (P-SCAN) ]
    Return files that may be password protected.
    pScan attempts to find password protected archives by first reading the files with magic
    to see if the file may be an archive of some kind. If the file appears to be
    compressed/archive then OmegaFindv2 will attempt to extract/decompress the file.

    [ String Scan (S-Scan) ]
    Return files containing x string.
    Regular filename search. Search for filenames containing specified string.

                                       [OPTIONS]
 
    [ Query ]
    Pass a space delimeted search string after -q argument. This should always be the last
    argument if used.

    [ Database ]
    OmegaFindv2 stores all learned suffix to buffer associations to it's database during
    learning. The database can be specified with -db argument. Note that larger databases
    can increase scan time however it still may be preferrable to have a large general
    purpose database like the one provided out of the box. This can be the included
    database or OmegaFindv2 can build a new database from files of your discretion.

    [ Extract ]
    OmegaFindv2 is capable of extraction/decompression of nested compressed files unless
    files are password protected. Extraction helps maximize the yield of various scan
    techniques where otherwise files may evade the gaze of OmegaFindv2. 
    Ensure enough spare disk space on any drive OmegaFindv2 is running on before using
    the -e argument.

    [ CMAX ]
    Chunk max. OmegaFindv2 scan teechniques are asynchronous and multiprocessed. CMAX
    specifies how many files will be in each chunk fed into the child processes.
    Exact optimum chunk max is variable predicated upon exactly how many files are
    being scanned. Best performance -cmax 1000 for say 300,000 files, although this
    vary depending on default or specified bmax and file sizes distributed accross
    chunks. An optional auto tune argument may be added in the future, such a feature
    would have to consider actual file sizes and bmax as well as file quantity. For now
    cmax is optionally specified and can greatly increase performance when an optimum
    cmax is specified.

    [ BMAX ]
    Buffer max. OmegaFindv2 is reading files to ascertain what the files are during
    various scan techniques. BMAX specifies how many bytes of each file to read.
    If you have very large files on the system then be careful increasing BMAX, while
    also considering that BMAX minimum should be at least 2048 bytes to get a good
    idea of what each file really is. CAREFULL consideration and preperation may be
    required when optionally specifying bmax, to ensure sufficient RAM/pagefile/swap
    will be available otherwise you may run into serious issues because this is
    potentially very high performance software. Ensure your system meets logical
    minimum requirements.

    [ RECURSIVE ]
    Scan techniques can be performed recursivley through all sub-directories of a
    specified directory by using -R switch.
    Omitting -R while specifying a directory should force OmegaFindv2 to only scan
    files in the immediate directory (no scanning in sub-directories).
    A file can also be specified with no extra arguments and -R if included should
    be ignored. Recurive depth specification may be added at some point.

    [ Interact ]
    Great care has been taken for special custom displaying of tables which has been
    implemented so that output does not get lost in the terminal buffer if there
    should be many lines of output.
    However this default behaviour can be turned of using -I which may be useful if
    running OmegaFindv2 with scripts that require promptless output.

    [ Digitless ]
    For the most part digits in a files resulting magic buffer read will pertain to
    things like, versioning, dimensions and timestamps.
    When OmegaFindv2 learns, digits are recorded in the database however when
    performing various scan techniques it may be preferrable to perform a digitless
    compartison of files being scanned against records in the database. This is so
    that if OmegaFindv2 learns an association between say a PNG of certain dimensions
    for example, OmegaFindv2 can then identify any similar PNG of any dimensions,
    with any verion number etc. This makes OmegaFindv2 extremely powerful at
    identification.
    Learning takes place with digits being recorded to the database however when
    performing various scan techniques (namely D-SCAN and T-SCAN) the buffer strings
    resulting from files being scanned during the scan technique can be digitlessly
    compared to the database enabling a powerful digitless comparison of buffer
    strings.
    This reduces false positives in a D-SCAN and increases identification yield in
    a T-SCAN.
    Digitless is only recommended if you have a reason to be more strict.
    To perform digitless comparisons use --digitless argument.
    For strict comparisons that do include digits simply omit --digitless argument
    when calling OmegaFindv2.
    Note: Digitless was on by default (inculuding when learning). If you have a
    digitless database then re-learning is reommended as now OmegaFindv2 learns
    with digits included.

    [ Decoding ]
    OmegaFindv2 contents scans brute force decoding to help maximize results yield
    from a contents scan. There are modules that guess encodings however they might
    choose the right encoding and so a brute force may be preferrable in order to
    scan characters in every which available way.


Help:

    [OmegaFind v2] Forensics tool. Search differently.
    
     -l       Learn                 Specify location to learn from.
     -c       Contents Scan         Specify a directory in which file contents will be scanned.
     -d       De-Obfuscation        Attempt to find files where suffix does not match contents.
     -p       Password Protected    Only scan for password protected archives.
     -r       Reveal Scan           Display all file types.
     -t       Type Scan             Display all files of type.
     -m       Modified Time Scan    Display modified time for all files.
     -s       String Scan           Display all files containing string. Used with -q.
     -q       Query                 Specify a search query. Used with -c. -c PATH -q QUERY.
     -sfx     Suffix                Specify suffix. Used with -t.
     -csfx    Custom Suffix         Specify custom suffix group. Used with -t.
     -gsfx    Group Suffix          Specify default suffix group. Used with -t.
     -nsfx    New Suffix Group      Create new custom suffix group.
                                    archive, audio, book, code, exe, font, image, sheet, slide, text, video, web.
    
     -db      Database              Specify database to use while learning/scanning.
     -e       Extract               Attempt archive extraction while scanning.
     -bmax    Buffer Max            Specify in digits maximum number of bytes to read of each file.
     -cmax    Chunk Max             Specify in digits max chunk size.
    
     -A       Associations          Display buffer associations to specified suffix.
     -AV      All Associations      Display all known suffix buffer associations.
     -G       Group                 Display specified suffix group.
     -I       Interact              Disables interaction. No prompt mode.
     -L       List Scan Reports     List and select previously completed scan report.
     -O       Write Output          Save logging and results to file. Takes no further arguments.
     -R       Recursive             Scan directories recursively. (Scans all sub-directories).
     -XP      Experience            Display how many associations have been learned.
    
     --digitless                    Omit versioning,timestamps,dimensions etc. when comparing magic buffers.
     --human-size                   Display bytes in human sizes.
     --sort=mtime                   Sort by Modified Time
     --sort=buffer                  Sort by Buffer
     --sort=size                    Sort by Size
     --sort=file                    Sort by Filename
     --sort-reverse=mtime           Sort by Modified Time
     --sort-reverse=buffer          Sort by Buffer
     --sort-reverse=size            Sort by Size
     --sort-reverse=file            Sort by Filename
     --csfx-remove                  Specify a custom suffix group to be removed.
    
     -v       Verbosity             Increase verbosity.
     -h       Help                  Display this help message.
    
    [Author] Developed and written by Benjamin Jack Cullen.


User:

    * Ensure sufficient ram/page-file/swap if changing buffer_max. Ensure chunk_max suits your system while also
      considering buffer_max. Think memory and think free disk space.
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
          Further test extraction compatibilies for adding further extraction compatibilities.
          Possibly cat files feature as there is a lot of file compatibility already built in.

    Omegafindv2 output tries to blend in with the dir/ls command. Simple and clean non verbose output.


Vulnerabilities:

    tarbombs and alike are a thing. This software may be vulnerable to malicious compressed files when using
    -e (extract) and or -c (contents scan) and or -p (password scan) arguments.


Extraction Compatibility (Below compatibility accounts for many more file suffixes listed as different suffixes use
    the same compression as below. Like epubs for one example):
    
    patool supports: 7z (.7z), ACE (.ace), ADF (.adf), ALZIP (.alz), APE (.ape), AR (.a), ARC (.arc), ARJ (.arj),
    BZIP2 (.bz2), CAB (.cab), COMPRESS (.Z), CPIO (.cpio), DEB (.deb), DMS (.dms), FLAC (.flac), GZIP (.gz), ISO (.iso),
    LRZIP (.lrz), LZH (.lha, .lzh), LZIP (.lz), LZMA (.lzma), LZOP (.lzo), RPM (.rpm), RAR (.rar), RZIP (.rz), SHN
    (.shn), TAR (.tar), XZ (.xz), ZIP (.zip, .jar), ZOO (.zoo) and ZPAQ (.zpaq) formats.
    It relies on helper applications to handle those archive formats (for example bzip2 for BZIP2 archives).


Examples:

    Learn (Asynchronous and Multiprocessed):
    omega_find -l ".\test_files\"
    omega_find -R -l ".\test_files\"

    Contents Scan (Asynchronous and Multiprocessed):
    omega_find -c ".\test_files\afile.xyz" -q string
    omega_find -cmax 1 -c ".\test_files\" -q string
    omega_find -cmax 1 -R -c ".\test_files\" -q string
    omega_find -cmax 1 -R -e -c ".\test_files\" -q string

    De-Obfuscation Scan (Asynchronous and Multiprocessed):
    omega_find --digitless -d ".\test_files\afile.xyz"
    omega_find -cmax 1 --digitless -d ".\test_files\"
    omega_find -cmax 1 --digitless -R -d ".\test_files\"
    omega_find -cmax 1 --digitless -R -d ".\test_files\"
    omega_find -cmax 1 --digitless -R -e -d ".\test_files\"

    Type Scan (Built in Group Suffix) (Asynchronous and Multiprocessed):
    omega_find -cmax 1 --digitless -t ".\test_files\" -gsfx video
    omega_find -cmax 1 --digitless -R -t ".\test_files\" -gsfx video
    omega_find -cmax 1 --digitless -R -e -t ".\test_files\" -gsfx video

    Type Scan (Specified Suffix) (Asynchronous and Multiprocessed):
    omega_find -cmax 1 --digitless -t ".\test_files\" -sfx mp4
    omega_find -cmax 1 --digitless -R -t ".\test_files\" -sfx mp4
    omega_find -cmax 1 --digitless -R -e -t ".\test_files\" -sfx mp4

    Type Scan (Custom Group Suffix) (Asynchronous and Multiprocessed):
    omega_find -cmax 1 --digitless -R -e -t ".\test_files\" -csfx

    Reveal Scan (Asynchronous and Multiprocessed):
    omega_find -r ".\test_files\afile.xyz"
    omega_find -cmax 1 -r ".\test_files\"
    omega_find -cmax 1 -R -r ".\test_files\"
    omega_find -cmax 1 -R -e -r ".\test_files\"

    Regular String in filename search (Linear Synchronous):
    omega_find -s ".\test_files\" -q .mp4
    omega_find -s ".\test_files\" -q partoffilename


Summary:

    So maybe your wondering what that file really is? Need to search contents of all kinds of different files for
    information, or you lost some files of a certain type somewhere? Or are you wondering if someone buried some
    videos in somewhere like system32 and renamed those videos as .bat and .exe files to try and hide them? Or
    perhaps your just curious? Maybe for whatever reason you need a better handle on what your looking for
    other than a simple string match in a filename search?
    Then OmegaFindv2 may be suibtable for your needs.
    Like Apple/IOS systems, python-magic allows OmegaFindv2 to know what a file really is. This is infinitely useful
    in infinite different ways. And depending what your looking for may determine how you scan, and then of course
    what you decide to do with/about the results.
    While OmegaFindv2 is designed to run and present its output much like dir or ls it is also designed with running
    promptlessly in mind to 'make friendly' being ran by another program that could have any intention, like
    security, forensic analysis or simple probing for example.
    Think of scan techniques as filters, while a reveal scan attempts to reveal everything it can.
    Note that running this software is potentially extremely resource intensive so it is also potentially expensive
    to run.


Gratitude and Thanks:

    Powered by asyncio, aiomultiprocess, aiofiles, python-magic, patool, tabulate and of course
    the python standard library.
