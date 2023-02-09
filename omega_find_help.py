import omega_find_banner


def omega_help():
    omega_find_banner.banner()
    print(' [-l]    [Learn. Scans and learns from specified target location]')
    print(' [-r]    [Reveal. Attempt to reveal what all files encountered really are]')
    print(' [-p]    [Password Protected. Attempt to find only password protected archives]')
    print(' [-d]    [De-Obfuscation. Attempt to ascertain if suffix is associated with file]')
    print(' [-t]    [Type. Return all files of a certain type]')
    print('         [-sfx]     [Suffix. Specify suffix]')
    print('         [-csfx]    [Custom Suffix Group]')
    print('         [-gsfx]    [Group Suffix. Specify a default suffix group ]')
    print('                    [archive]')
    print('                    [audio]')
    print('                    [book]')
    print('                    [code]')
    print('                    [executable]')
    print('                    [font]')
    print('                    [image]')
    print('                    [sheet]')
    print('                    [slide]')
    print('                    [text]')
    print('                    [video]')
    print('                    [web]')
    print('')
    print(' [-e]       [Extract. Extract archives while scanning]')
    print(' [-db]      [Database. Specify a database file to use for scanning]')
    print(' [-cmax]    [Chunk Max. Maximum items in each chunk. Default 16]')
    print(' [-bmax]    [Buffer Max. Maximum bytes read. Default 2048]')
    print(' [-nsfx]    [New Suffix Group. Create a new suffix group]')
    print(' [-R]       [Recognized. Display number of recognized buffers and suffixes]')
    print(' [-v]       [Verbosity]')
    print(' [-h]       [Help]')
    print('')
    print(' omega_find -l PATH -cmax 16 -bmax 2048')
    print(' omega_find -d PATH -cmax 16 -bmax 2048')
    print(' omega_find -t PATH -sfx sh')
    print(' omega_find -t PATH -csfx')
    print(' omega_find -t PATH -gsfx image -e')
    print(' omega_find PATH QUERY')
    print('')
    print(' Developed and written by Benjamin Jack Cullen.')
    print('')
