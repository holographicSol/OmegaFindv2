OmegaFind v2.


Overview:

    Learn - Uses python-magic during a filesystem scan(s) to compile a database of
    'trusted' suffix, buffer associations which can be used when performing various
    scan techniques.

    Deobfuscation - This scan technique attempts to expose files that may have been
    obfuscated. Attempted exposition is performed by comparing suffixes and buffers
    of files during deobfuscation scans to 'trusted' buffer, suffix associations
    in the database.

    Type scanning - Aggregates all file types specified. Again not by suffix but by
    known suffix, buffer associations according to the database. Useful in different
    situations including where file(s) may be evading a deobfuscation scan.
 

Help:

    [OmegaFind v2]  [Multiprocess async for better performance]
                     [Forensics tool. Search differently]
                     [Developed and written by Benjamin Jack Cullen]
    
     [--recognized]        [Display number of recognized buffers and suffixes]
     [--learn]             [Scans and learns from specified target location]
     [--chunk-max]         [Maximum items in each chunk. Default 16]
     [--buffer-max]        [Maximum bytes read. Default 2048]
     [--database]          [Specify a database file to use for scanning]
     [--new-suffix-group]  [Create a new suffix group]
    
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


Developer:

    Python Version: 3.9+
    OS: Testing and running on Windows 10 and Linux.
    
    Running the source code: Requires pool.py be placed in aiomultiprocessing.
    Backup original pool.py first.
    My edit marked '# my edit' on line 339 in pool.py enables a dictionary to
    be passed into the child processes when using pool.map() along with the
    initial iterables as there is no manager.dict and obviously no previously
    set globals for the child processes. Lines edited: 337, 339, 345.


Gratitude and thanks:

    Powered by asyncio, aiomultiprocess, aiofiles, python-magic and of course
    the python standard library.
