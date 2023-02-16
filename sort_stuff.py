import variables_suffix


ext_list = ['ext_archive',
            'ext_audio',
            'ext_book',
            'ext_code',
            'ext_executable',
            'ext_font',
            'ext_image',
            'ext_sheet',
            'ext_slide',
            'ext_text',
            'ext_video',
            'ext_web']

i = 0
for _list in variables_suffix.ext_list:
    print('')
    _list.sort()
    print(f'{ext_list[i]} = [')
    for x in _list:
        print(f'    "{x}",')
    print(']')
    i += 1
