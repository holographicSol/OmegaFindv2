# OmegaFindv2
Multiprocessed and Asynced.

Forensics Tool. Are file(s) what the suffix claims to be? Search Differenlty.


 [OmegaFind v2]     [Version 2. Multi-processed async for better performance]
                    [Forensics tool. Search differently]

 [--learn]             [Learn]                    [Scans and learns from specified target location]
 [--proc-max]          [Max Processes]            [Maximum number of child processes]
 [--buffer-max]        [Max Buffer]               [Maximum number of bytes read from each file during a scan]
 [--database]          [Database]                 [Specify a database file to use for scanning]
 [--new-suffix-group]  [Create New Suffix Group]

 [Scan Techniques]
 [--de-scan]        [Deobfuscation]    [Attempt to ascertain if file(s) suffix matches its contents]
 [--type-scan]      [Type Scan]        [Scan and compare files to known suffix/buffer relationships]
                    [--suffix]         [Specify a single suffix. Suffix resolves to buffer data in DB]
                    [--custom-suffix]  [Select a custom suffix group]
                    [--group-suffix]   [Specify a group of suffixes. Suffix(s) resolve to buffer data in DB]
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

 [Example]  [omega_find --type-scan PATH --group-suffix image --chunk-max 16 --buffer-max 1024 -v]
 [Example]  [omega_find --type-scan PATH --custom-suffix --chunk-max 16 --buffer-max 1024 -v]

 [-v]  [Verbosity]  [Increase verbosity]
 [-h]  [Help]       [Displays this help message]


Note: Requires pool.py be placed in aiomultiprocessing. backup original pool first.
My edit marked '# my edit' on line 339 in pool.py enables variables to be passed into
the child processes when using pool.map() as there is no manager.dict and
obviously no previously set globals for the child processes.
Lines edited: 337, 339, 345.
