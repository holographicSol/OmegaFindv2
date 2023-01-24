 [OmegaFind v2]  [Multiprocess async for better performance]
                 [Forensics tool. Search differently]
                 [Developed and written by Benjamin Jack Cullen]

 [--recognized]        [Display number of recognized buffers and suffixes]
 [--learn]             [Scans and learns from specified target location]
 [--chunk-max]         [Maximum items in each chunk. Default 16]
 [--buffer-max]        [Maximum bytes read. Default 1024]
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

 [omega_find --learn PATH --chunk-max 16 --buffer-max 1024 -v]
 [omega_find --de-scan PATH --chunk-max 16 --buffer-max 1024 -v]
 [omega_find --type-scan PATH --suffix sh -v]
 [omega_find --type-scan PATH --custom-suffix -v]
 [omega_find --type-scan PATH --group-suffix image]


Note: Requires pool.py be placed in aiomultiprocessing. backup original pool first.
My edit marked '# my edit' on line 339 in pool.py enables a dictionary to be passed into
the child processes when using pool.map() along with the initial iterables as there
is no manager.dict and obviously no previously set globals for the child processes.
Lines edited: 337, 339, 345.
