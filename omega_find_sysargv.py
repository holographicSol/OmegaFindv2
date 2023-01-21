import sys
import ext_module


def mode():

    modes = ['--learn', '--de-scan', '--type-scan']
    _mode = ''
    learn = False
    de_scan = False
    type_scan = False
    suffix = []
    for m in modes:
        if m in sys.argv:
            _mode = m
    if _mode == '--learn':
        learn = True
    elif _mode == '--de-scan':
        de_scan = True
    elif _mode == '--type-scan':
        type_scan = True
        if '--suffix' in sys.argv:
            idx = sys.argv.index('--suffix')
            suffix.append(sys.argv[idx + 1].strip())
        elif '--group-suffix' in sys.argv:
            idx = sys.argv.index('--group-suffix')
            suffix_ = sys.argv[idx + 1]
            if suffix_ == 'archive':
                suffix = ext_module.ext_archive
            elif suffix_ == 'audio':
                suffix = ext_module.ext_audio
            elif suffix_ == 'book':
                suffix = ext_module.ext_book
            elif suffix_ == 'code':
                suffix = ext_module.ext_code
            elif suffix_ == 'executable':
                suffix = ext_module.ext_executable
            elif suffix_ == 'font':
                suffix = ext_module.ext_font
            elif suffix_ == 'image':
                suffix = ext_module.ext_image
            elif suffix_ == 'sheet':
                suffix = ext_module.ext_sheet
            elif suffix_ == 'slide':
                suffix = ext_module.ext_slide
            elif suffix_ == 'text':
                suffix = ext_module.ext_text
            elif suffix_ == 'video':
                suffix = ext_module.ext_video
            elif suffix_ == 'web':
                suffix = ext_module.ext_web

    return _mode, learn, de_scan, type_scan, suffix


def target(mode) -> str:
    return sys.argv[sys.argv.index(mode) + 1]


def chunk_max() -> int:
    return int(sys.argv[sys.argv.index('--chunk-max') + 1])


def buffer_max() -> int:
    return int(sys.argv[sys.argv.index('--buffer-max')+1])


def database() -> str:
    _db_recognized_files = './db/database_file_recognition.txt'
    if '--database' in sys.argv:
        _db_recognized_files = sys.argv[sys.argv.index('--database')+1]
    return _db_recognized_files


def verbosity() -> bool:
    verbose = False
    if '-v' in sys.argv:
        verbose = True
    return verbose
