ext_archive = [
    "7z",
    "a",
    "apk",
    "ar",
    "bz2",
    "cab",
    "cpio",
    "deb",
    "dmg",
    "egg",
    "gz",
    "iso",
    "jar",
    "lha",
    "mar",
    "pak",
    "pea",
    "rar",
    "rpm",
    "s7z",
    "shar",
    "tar",
    "tbz2",
    "tgz",
    "tlz",
    "war",
    "whl",
    "xpi",
    "xz",
    "zip",
    "zipx"
]

ext_audio = [
    "aac",
    "aiff",
    "ape",
    "au",
    "flac",
    "gsm",
    "it",
    "m3u",
    "m4a",
    "mid",
    "mod",
    "mp3",
    "mpa",
    "pls",
    "ra",
    "s3m",
    "sid",
    "wav",
    "wma",
    "xm"
]

ext_book = [
    "azw",
    "azw1",
    "azw3",
    "azw4",
    "azw6",
    "cbr",
    "cbz",
    "epub",
    "mobi"
]

ext_code = [
    "1.ada",
    "2.ada",
    "ada",
    "adb",
    "ads",
    "asm",
    "asp",
    "aspx",
    "bas",
    "bash",
    "bat",
    "c",
    "c++",
    "cbl",
    "cc",
    "class",
    "clj",
    "cob",
    "cpp",
    "cs",
    "csh",
    "cxx",
    "d",
    "diff",
    "e",
    "el",
    "f",
    "f77",
    "f90",
    "fish",
    "for",
    "fth",
    "ftn",
    "go",
    "groovy",
    "h",
    "hh",
    "hpp",
    "hs",
    "htm",
    "html",
    "hxx",
    "inc",
    "java",
    "js",
    "jsp",
    "jsx",
    "ksh",
    "kt",
    "lhs",
    "lisp",
    "lua",
    "m",
    "m4",
    "nim",
    "patch",
    "php",
    "php3",
    "php4",
    "php5",
    "phtml",
    "pl",
    "po",
    "pp",
    "py",
    "r",
    "rb",
    "rs",
    "s",
    "scala",
    "sh",
    "swg",
    "swift",
    "v",
    "vb",
    "vcxproj",
    "xcodeproj",
    "xml",
    "zsh"
]

ext_executable = [
    "bash",
    "bat",
    "bin",
    "command",
    "crx",
    "csh",
    "exe",
    "fish",
    "ksh",
    "msi",
    "sh",
    "zsh"
]

ext_font = [
    "eot",
    "otf",
    "ttf",
    "woff",
    "woff2"
]

ext_image = [
    "3dm",
    "3ds",
    "ai",
    "bmp",
    "dds",
    "dwg",
    "dxf",
    "eps",
    "gif",
    "gpx",
    "jpeg",
    "jpg",
    "kml",
    "kmz",
    "max",
    "png",
    "ps",
    "psd",
    "svg",
    "tga",
    "thm",
    "tif",
    "tiff",
    "webp",
    "xcf",
    "yuv"
]

ext_sheet = [
    "csv",
    "ics",
    "ods",
    "vcf",
    "xls",
    "xlsx"
]

ext_slide = [
    "odp",
    "ppt"
]

ext_text = [
    "doc",
    "docx",
    "ebook",
    "log",
    "md",
    "msg",
    "odt",
    "org",
    "pages",
    "pdf",
    "rst",
    "rtf",
    "tex",
    "txt",
    "wpd",
    "wps"
]

ext_video = [
    "3g2",
    "3gp",
    "aaf",
    "asf",
    "avchd",
    "avi",
    "drc",
    "flv",
    "m2v",
    "m4p",
    "m4v",
    "mkv",
    "mng",
    "mov",
    "mp2",
    "mp4",
    "mpe",
    "mpeg",
    "mpg",
    "mpv",
    "mxf",
    "nsv",
    "ogg",
    "ogm",
    "ogv",
    "qt",
    "rm",
    "rmvb",
    "roq",
    "srt",
    "svi",
    "vob",
    "webm",
    "wmv"
]

ext_web = [
    "asp",
    "aspx",
    "css",
    "htm",
    "html",
    "inc",
    "js",
    "jsp",
    "jsx",
    "less",
    "php",
    "php3",
    "php4",
    "php5",
    "phtml",
    "scss",
    "wasm"
]


ext_list = [ext_archive,
            ext_audio,
            ext_book,
            ext_code,
            ext_executable,
            ext_font,
            ext_image,
            ext_sheet,
            ext_slide,
            ext_text,
            ext_video,
            ext_web]

ext_name = ['Archive',
            'Audio',
            'Book',
            'Code',
            'Executable',
            'Font',
            'Image',
            'Sheet',
            'Sheet',
            'Text',
            'Video',
            'Web']


def get_specified_suffix_group(suffix_: str):
    suffix = ''
    if suffix_ == 'archive':
        suffix = ext_archive
    elif suffix_ == 'audio':
        suffix = ext_audio
    elif suffix_ == 'book':
        suffix = ext_book
    elif suffix_ == 'code':
        suffix = ext_code
    elif suffix_ == 'executable':
        suffix = ext_executable
    elif suffix_ == 'font':
        suffix = ext_font
    elif suffix_ == 'image':
        suffix = ext_image
    elif suffix_ == 'sheet':
        suffix = ext_sheet
    elif suffix_ == 'slide':
        suffix = ext_slide
    elif suffix_ == 'text':
        suffix = ext_text
    elif suffix_ == 'video':
        suffix = ext_video
    elif suffix_ == 'web':
        suffix = ext_web
    if suffix:
        return suffix
