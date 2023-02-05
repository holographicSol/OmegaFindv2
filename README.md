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

    [OmegaFind v2] Multi-processed async for better performance.
                   Forensics tool. Search differently.
                   Developed and written by Benjamin Jack Cullen.
    
     [--recognized]        [Display number of recognized buffers and suffixes]
     [--learn]             [Scans and learns from specified target location]
     [--chunk-max]         [Maximum items in each chunk. Default 16]
     [--buffer-max]        [Maximum bytes read. Default 2048]
     [--extract]           [Extract Zip Archives while scanning]
     [--database]          [Specify a database file to use for scanning]
     [--new-suffix-group]  [Create a new suffix group]
    
     [--p-scan]     [Attempt to find only password protected archives]
     [--de-scan]    [Attempt to ascertain if suffix match contents]
     [--type-scan]  [Scan file type]
                    [--suffix]         [Specify suffix]
                    [--custom-suffix]  [Select custom suffix group]
                    [--group-suffix]   [Use predefined suffix group]
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
    
     [-v]  [Verbosity]  [Increase verbosity]
     [-h]  [Help]       [Displays this help message]
    
     [omega_find --learn PATH --chunk-max 16 --buffer-max 2048 -v]
     [omega_find --de-scan PATH --chunk-max 16 --buffer-max 2048 -v]
     [omega_find --type-scan PATH --suffix sh -v]
     [omega_find --type-scan PATH --custom-suffix -v]
     [omega_find --type-scan PATH --group-suffix image]


User:

    * Recommended only currently running omega_find from within omega_find directory.
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

    Todo:
    * Add compatibility for archives not yet supported by current extraction
      methods.
    * Add multiple methods of extraction to existing archive extraction methods.
    * refine logs, results.
    * f search (scandir, (also use windows index if on windows)).
    * --reveal argument. (new scan technique).
    * mod times.
    * --map argument. (new scan technique).


Compatibility:
    
    Logging: Compatibility issues such as a file appearing to be a b2z archive (for example)
    but however tarfile module cannot extract the contents. This would require donations to
    the relevant team and or OmegaFindv2 itself being armed with multiple different extraction
    methods per archive type (zip, 7izp, b2z etc..). Compatibility for OmegaFindv2's extraction
    capabilities is in progress. 


Gratitude and Thanks:

    Powered by asyncio, aiomultiprocess, aiofiles, python-magic, patool and of course
    the python standard library.
