

def omega_help():
    print('')
    print(' [OmegaFind v2]  [2.0. Multi-processed async for better performance]')
    print('                 [Forensics tool. Search differently]')
    print('                 [Developed and written by Benjamin Jack Cullen]')
    print('')
    print(' [--recognized]        [Display number of recognized buffers and suffixes]')
    print(' [--learn]             [Scans and learns from specified target location]')
    print(' [--chunk-max]         [Maximum items in each chunk. Default 16]')
    print(' [--buffer-max]        [Maximum bytes read. Default 1024]')
    print(' [--database]          [Specify a database file to use for scanning]')
    print(' [--new-suffix-group]  [Create a new suffix group]')
    print(' [--clean-db]          [Removes any duplicates and empty lines]')
    print('')
    print(' [--de-scan]    [Attempt to ascertain if suffix match contents]')
    print(' [--type-scan]  [Scan file type]')
    print('                [--suffix]         [Specify suffix]')
    print('                [--custom-suffix]  [Select custom suffix group]')
    print('                [--group-suffix]   [Use predefined suffix group]')
    print('                                   [archive]')
    print('                                   [audio]')
    print('                                   [book]')
    print('                                   [code]')
    print('                                   [executable]')
    print('                                   [font]')
    print('                                   [image]')
    print('                                   [sheet]')
    print('                                   [slide]')
    print('                                   [text]')
    print('                                   [video]')
    print('                                   [web]')
    print('')
    print(' [-v]  [Verbosity]  [Increase verbosity]')
    print(' [-h]  [Help]       [Displays this help message]')
    print('')
    print(' [omega_find --learn PATH --chunk-max 16 --buffer-max 1024 -v]')
    print(' [omega_find --de-scan PATH --chunk-max 16 --buffer-max 1024 -v]')
    print(' [omega_find --type-scan PATH --suffix sh -v]')
    print(' [omega_find --type-scan PATH --custom-suffix -v]')
    print(' [omega_find --type-scan PATH --group-suffix image]')
    print('')
