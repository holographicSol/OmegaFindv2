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

    [OmegaFind v2]  Multi-processed async for better performance.
                    Forensics tool. Search differently.
    
     [-l]    [Learn. Scans and learns from specified target location]
     [-r]    [Reveal Scan. Attempt to reveal what all files encountered really are]
     [-p]    [Password Protected Scan. Attempt to find only password protected archives]
     [-d]    [De-Obfuscation Scan. Attempt to ascertain if suffix is associated with file]
     [-t]    [Type Scan. Return all files of a certain type]
             [-sfx]     [Suffix. Specify suffix]
             [-csfx]    [Custom Suffix Group]
             [-gsfx]    [Group Suffix. Specify a default suffix group ]
                        [archive]
                        [audio]
                        [book]
                        [code]
                        [executable]
                        [font]
                        [image]
                        [sheet]
                        [slide]
                        [text]
                        [video]
                        [web]
    
     [-e]       [Extract. Extract archives while scanning]
     [-db]      [Database. Specify a database file to use for scanning]
     [-cmax]    [Chunk Max. Maximum items in each chunk. Default 16]
     [-bmax]    [Buffer Max. Maximum bytes read. Default 2048]
     [-nsfx]    [New Suffix Group. Create a new suffix group]
     [-R]       [Recognized. Display number of recognized buffers and suffixes]
     [-v]       [Verbosity]
     [-h]       [Help]
    
     omega_find -l PATH -cmax 16 -bmax 2048
     omega_find -d PATH -cmax 16 -bmax 2048
     omega_find -t PATH -sfx sh
     omega_find -t PATH -csfx
     omega_find -t PATH -gsfx image -e
     omega_find PATH QUERY
    
     Developed and written by Benjamin Jack Cullen.


User:

    * Portable. Except where sys.executabe path may not be path to omega_find.exe.
    * Ensure sufficient ram/page-file/swap if changing buffer_max. ensure chunk_max suits your system while also considering buffer_max.
    * If using --extract then ensure sufficient storage in working directory while also considering buffer_max and chunk_max.


Developer:

    Python Version: 3.9+
    OS: Tested and running on Windows 10 and Linux.

    Install modules run: requirements.bat
    
    Running the source code: Requires pool.py be placed in aiomultiprocessing.
    Backup original pool.py first.
    My edit marked '# my edit' on line 339 in pool.py enables a dictionary to
    be passed into the child processes when using pool.map() along with the
    initial iterables as there is no manager.dict and obviously no previously
    set globals for the child processes. Lines edited: 337, 339, 345.


Compatibility:
    
    Logging: Compatibility issues such as a file appearing to be a b2z archive (for example)
    but however tarfile module cannot extract the contents. This would require donations to
    the relevant team and or OmegaFindv2 itself being armed with multiple different extraction
    methods per archive type (zip, 7izp, b2z etc..). Compatibility for OmegaFindv2's extraction
    capabilities is in progress. 


Gratitude and Thanks:

    Powered by asyncio, aiomultiprocess, aiofiles, python-magic, patool and of course
    the python standard library.