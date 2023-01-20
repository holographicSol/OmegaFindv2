# OmegaFindv2
Multiprocessed and Asynced.

Are file(s) what the suffix claims to be.

Note: Requires pool.py be placed in aiomultiprocessing. backup original pool first.
My edit marked '# my edit' on line 339 in pool.py enables variables to be passed into
the child processes when using pool.map() as there is no manager.dict and
obviously no previously set globals for the child processes.
Lines edited: 337, 339, 345.
