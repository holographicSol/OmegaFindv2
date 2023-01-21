

def omega_help():
    print('')
    print(' [OmegaFind v2]  [Version 2. Multi-processed async for better performance]')
    print('                 [Forensics tool. Search differently]')
    print('')
    print(' [--learn]          [Learn]           [Scans and learns from specified target location]')
    print(' [--proc-max]       [Max Processes]   [Maximum number of child processes]')
    print(' [--buffer-max]     [Max Buffer]      [Maximum number of bytes read from each file during a scan]')
    print(' [--database]       [Database]        [Specify a database file to use for scanning]')
    print('')
    print(' [Scan Techniques]')
    print(' [--de-scan]        [Deobfuscation]   [Attempt to ascertain if file(s) suffix matches its contents]')
    print(' [--type-scan]      [Type Scan]       [Scan and compare files to known suffix/buffer relationships]')
    print('                    [--suffix]        [Specify a single suffix. Suffix resolves to buffer data in DB]')
    print('                    [--group-suffix]  [Specify a group of suffixes. Suffix(s) resolve to buffer data in DB]')
    print('                                      [archive]')
    print('                                      [audio]')
    print('                                      [book]')
    print('                                      [code]')
    print('                                      [executable]')
    print('                                      [font]')
    print('                                      [image]')
    print('                                      [sheet]')
    print('                                      [slide]')
    print('                                      [text]')
    print('                                      [video]')
    print('                                      [web]')
    print('')
    print(' [-v]  [Verbosity]  [Increase verbosity]')
    print(' [-h]  [Help]       [Displays this help message]')
    print('')
