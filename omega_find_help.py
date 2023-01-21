

def omega_help():
    print('')
    print(' [OmegaFind v2] [Version 2. Multi-processed async for better performance]')
    print('')
    print(' [Forensics tool. Search differently by reading files to see what they might really be]')
    print('')
    print(' [--learn]       [Learn]          [Scans and learns from specified target location]')
    print(' [--proc-max]    [Max Processes]  [Maximum number of child processes]')
    print(' [--buffer-max]  [Max Buffer]     [Maximum number of bytes read from each file during a scan]')
    print(' [--database]    [Database]       [Specify a database file to use for scanning. (Compiled by --learn)]')
    print('')
    print(' [Scan Techniques]')
    print(' [--de-scan]    [Deobfuscation]   [Scans and tries to ascertain if file(s) suffix matches its contents]')
    print(' [--type-scan]  [Type Scan]       [Scans for files of certain type(s) according to known suffix/buffer relationships]')
    print('                [--suffix]        [Specify a single suffix. Buffers in DB associated with suffix will be matched during scan]')
    print('                [--group-suffix]  [Specify a group of suffixes]')
    print('                                  [archive]')
    print('                                  [audio]')
    print('                                  [book]')
    print('                                  [code]')
    print('                                  [executable]')
    print('                                  [font]')
    print('                                  [image]')
    print('                                  [sheet]')
    print('                                  [slide]')
    print('                                  [text]')
    print('                                  [video]')
    print('                                  [web]')
    print('')
    print(' [-v]            [Verbosity]      [Increase verbosity]')
    print(' [-h]            [Help]           [Displays this help message]')
    print('')
