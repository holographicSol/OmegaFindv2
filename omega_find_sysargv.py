import sys


def mode():
    modes = ['--learn', '--de-scan']
    _mode = ''
    learn = False
    de_scan = False
    for m in modes:
        if m in sys.argv:
            _mode = m
    if _mode == '--learn':
        learn = True
    elif _mode == '--de-scan':
        de_scan = True
    return _mode, learn, de_scan


def target(mode) -> str:
    return sys.argv[sys.argv.index(mode) + 1]


def proc_max() -> int:
    return int(sys.argv[sys.argv.index('--proc-max') + 1])


def buffer_max() -> int:
    return int(sys.argv[sys.argv.index('--buffer-max')+1])


def database() -> str:
    if '--database' in sys.argv:
        return sys.argv[sys.argv.index('--database') + 1]


def digits() -> bool:
    _digits = False
    if '--digits' in sys.argv:
        _digits = True
    return _digits


def verbosity() -> bool:
    verbose = False
    if '-v' in sys.argv:
        verbose = True
    return verbose
