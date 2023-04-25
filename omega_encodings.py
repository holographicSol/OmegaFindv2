""" Written by Benjamin Jack Cullen (for me with my module parser to list program) """
import codecs
import os

idx_enc_logical = 0

# enc alpha order
enc = ['ascii', 'base64_codec', 'big5', 'big5hkscs', 'bz2_codec', 'cp037', 'cp1026', 'cp1125', 'cp1140',
               'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'cp273',
               'cp424', 'cp437', 'cp500', 'cp775', 'cp850', 'cp852', 'cp855', 'cp857', 'cp858', 'cp860', 'cp861',
               'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp932', 'cp949', 'cp950', 'euc_jis_2004',
               'euc_jisx0213', 'euc_jp', 'euc_kr', 'gb18030', 'gb2312', 'gbk', 'hex_codec', 'hp_roman8', 'hz',
               'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext',
               'iso2022_kr', 'iso8859_10', 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'iso8859_16',
               'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9',
               'johab', 'koi8_r', 'kz1048', 'latin_1', 'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2',
               'mac_roman', 'mac_turkish', 'mbcs', 'ptcp154', 'quopri_codec', 'rot_13', 'shift_jis', 'shift_jis_2004',
               'shift_jisx0213', 'tis_620', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_32', 'utf_32_be', 'utf_32_le',
               'utf_7', 'utf_8', 'uu_codec', 'zlib_codec']

# enc alpha order
enc_logical = ['utf_8', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_32', 'utf_32_be', 'utf_32_le', 'utf_7',
               'ascii', 'base64_codec', 'big5', 'big5hkscs', 'bz2_codec', 'cp037', 'cp1026', 'cp1125', 'cp1140',
               'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'cp273',
               'cp424', 'cp437', 'cp500', 'cp775', 'cp850', 'cp852', 'cp855', 'cp857', 'cp858', 'cp860', 'cp861',
               'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp932', 'cp949', 'cp950', 'euc_jis_2004',
               'euc_jisx0213', 'euc_jp', 'euc_kr', 'gb18030', 'gb2312', 'gbk', 'hex_codec', 'hp_roman8', 'hz',
               'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext',
               'iso2022_kr', 'iso8859_10', 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'iso8859_16',
               'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9',
               'johab', 'koi8_r', 'kz1048', 'latin_1', 'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2',
               'mac_roman', 'mac_turkish', 'mbcs', 'ptcp154', 'quopri_codec', 'rot_13', 'shift_jis', 'shift_jis_2004',
               'shift_jisx0213', 'tis_620', 'uu_codec', 'zlib_codec']


def power_read(_file: str, _verbose=False, _encoding=enc_logical[idx_enc_logical]):
    global idx_enc_logical
    if os.path.exists(_file):
        try:
            data = codecs.open(_file, 'r', encoding=_encoding)
            if _verbose is True:
                print(f'accepted encoding {_encoding}: {_file}')
            return data
        except Exception as e:
            if _verbose is True:
                print(f'[{_encoding}] {e}: {_file}')
            if "codec can't decode" in str(e) or 'stream does not start with BOM' in str(
                    e) or 'Incorrect padding' in str(e) \
                    or 'Invalid' in str(e):
                idx_enc_logical += 1
                power_read(_file=_file,
                           _verbose=_verbose,
                           _encoding=enc_logical[idx_enc_logical])
