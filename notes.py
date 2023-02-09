"""
current archive/compressed compatibility:
patool supports 7z (.7z), ACE (.ace), ADF (.adf), ALZIP (.alz), APE (.ape), AR (.a), ARC (.arc), ARJ (.arj),
BZIP2 (.bz2), CAB (.cab), COMPRESS (.Z), CPIO (.cpio), DEB (.deb), DMS (.dms), FLAC (.flac), GZIP (.gz), ISO (.iso),
LRZIP (.lrz), LZH (.lha, .lzh), LZIP (.lz), LZMA (.lzma), LZOP (.lzo), RPM (.rpm), RAR (.rar), RZIP (.rz), SHN
(.shn), TAR (.tar), XZ (.xz), ZIP (.zip, .jar), ZOO (.zoo) and ZPAQ (.zpaq) formats.
It relies on helper applications to handle those archive formats (for example bzip2 for BZIP2 archives).




todo:

* step through each argument and refine results output/grouping.
deScan: checked and ready for refined output.
typeScan: checked and ready for refined output.
pScan: checked and ready for refined output.

revealScan: no-extract: checked and ready for refined output.
            extract: remove duplicates. todo
                     remove arbitrary grouping effect. todo


* display database files

* refine output, logs, results files

"""