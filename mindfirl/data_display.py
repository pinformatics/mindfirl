# this module is for formatting raw data into html-friendly data

DATA_MODE_BASE = ['base', 'base', 'base', 'base', 'base', 'base']
DATA_MODE_FULL = ['full', 'full', 'full', 'full', 'full', 'full']
DATA_MODE_MASKED = ['masked', 'masked', 'masked', 'masked', 'masked', 'masked']
DATA_MODE_MINIMUM = ['partial', 'partial', 'partial', 'partial', 'full', 'masked']
DATA_MODE_MODERATE = ['partial', 'partial', 'partial', 'partial', 'full', 'masked']


def get_string_display(attr1, attr2, helper1, helper2, attribute_mode):
    """
    get the attribute mode for string
    attribute mode can be:
    'base', 'full', 'partial', 'masked'
    Note that some attribute does not have partial mode, in this case, partial mode will return masked mode
    Remeber to call has_partial_mode function to check if it actually has partial mode!
    Example: 
    Input:
        attr1: '1000151475'
        attr2: '1000151575'
        helper1: '*******4**'
        helper2: '*******5**'
        attribute_mode: 'partial'
    Output:
        ['*******<span style="color:red">4</span>**', '*******<span style="color:red">5</span>**']
    """
    if attribute_mode == 'base':
        if not attr1:
            attr1_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
        else:
            attr1_display = attr1
        if not attr2:
            attr2_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
        else:
            attr2_display = attr2
        return [attr1_display, attr2_display]
    elif attribute_mode == 'full':
        if not attr1 or not attr2:
            if not attr1:
                attr1_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr1_display = attr1

            if not attr2:
                attr2_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr2_display = attr2
        else:
            if '*' not in helper1 and '*' not in helper2:
                attr1_display = attr1
                attr2_display = attr2
            else:
                attr1_display = ''
                attr2_display = ''
                i = 0
                j = 0
                k = 0
                while k < len(helper1):
                    if helper1[k] == '*':
                        attr1_display += attr1[i]
                        attr2_display += attr2[j]
                        k += 1
                        i += 1
                        j += 1
                    elif k+1 < len(helper1) and i+1 < len(attr1) and j+1 < len(attr2) and \
                    helper1[k] not in ['*', '_', '?'] and helper1[k+1] not in ['*', '_', '?'] and attr1[i] == attr2[j+1] and attr1[i+1] == attr2[j]:
                        attr1_display += '<span class="transpose_text">' + attr1[i] + attr1[i+1] + '</span>'
                        attr2_display += '<span class="transpose_text">' + attr2[j] + attr2[j+1] + '</span>'
                        k += 2
                        i += 2
                        j += 2
                    elif helper1[k] == '_' or helper1[k] == '?':
                        attr2_display += '<span class="indel_text">' + attr2[j] + '</span>'
                        k += 1
                        j += 1
                    elif helper2[k] == '_' or helper2[k] == '?':
                        attr1_display += '<span class="indel_text">' + attr1[i] + '</span>'
                        k += 1
                        i += 1
                    else:
                        attr1_display += '<span class="replace_text">' + attr1[i] + '</span>'
                        attr2_display += '<span class="replace_text">' + attr2[j] + '</span>'
                        k += 1
                        i += 1
                        j += 1
        return [attr1_display, attr2_display]
    elif attribute_mode == 'partial':
        if not attr1 or not attr2:
            if not attr1:
                attr1_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr1_display = '*'*len(attr1)

            if not attr2:
                attr2_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr2_display = '*'*len(attr2)
        else:
            if '*' not in helper1 and '*' not in helper2:
                attr1_display = len(attr1)*'@'
                attr2_display = len(attr2)*'&'
            elif helper1 == helper2:
                attr1_display = '<img src="/static/images/site/checkmark.png" alt="checkmark" class="freq_icon">'
                attr2_display = '<img src="/static/images/site/checkmark.png" alt="checkmark" class="freq_icon">'
            else:
                attr1_display = ''
                attr2_display = ''
                i = 0
                j = 0
                k = 0
                while k < len(helper1):
                    if helper1[k] == '*':
                        attr1_display += '*'
                        attr2_display += '*'
                        k += 1
                        i += 1
                        j += 1
                    elif k+1 < len(helper1) and i+1 < len(attr1) and j+1 < len(attr2) and \
                    helper1[k] not in ['*', '_', '?'] and helper1[k+1] not in ['*', '_', '?'] and attr1[i] == attr2[j+1] and attr1[i+1] == attr2[j]:
                        attr1_display += '<span class="transpose_text">' + attr1[i] + attr1[i+1] + '</span>'
                        attr2_display += '<span class="transpose_text">' + attr2[j] + attr2[j+1] + '</span>'
                        k += 2
                        i += 2
                        j += 2
                    elif helper1[k] == '_' or helper1[k] == '?':
                        attr2_display += '<span class="indel_text">' + attr2[j] + '</span>'
                        k += 1
                        j += 1
                    elif helper2[k] == '_' or helper2[k] == '?':
                        attr1_display += '<span class="indel_text">' + attr1[i] + '</span>'
                        k += 1
                        i += 1
                    else:
                        attr1_display += '<span class="replace_text">' + attr1[i] + '</span>'
                        attr2_display += '<span class="replace_text">' + attr2[j] + '</span>'
                        k += 1
                        i += 1
                        j += 1
        return [attr1_display, attr2_display]
    elif attribute_mode == 'masked':
        if not attr1 or not attr2:
            if not attr1:
                attr1_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr1_display = '*'*len(attr1)

            if not attr2:
                attr2_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr2_display = '*'*len(attr2)
        else:
            if '*' not in helper1 and '*' not in helper2:
                attr1_display = len(attr1)*'@'
                attr2_display = len(attr2)*'&'
            elif helper1 == helper2:
                attr1_display = '<img src="/static/images/site/checkmark.png" alt="checkmark" class="freq_icon">'
                attr2_display = '<img src="/static/images/site/checkmark.png" alt="checkmark" class="freq_icon">'
            else:
                attr1_display = ''
                attr2_display = ''
                i = 0
                j = 0
                k = 0
                while k < len(helper1):
                    if helper1[k] == '*':
                        attr1_display += '*'
                        attr2_display += '*'
                        k += 1
                        i += 1
                        j += 1
                    elif k+1 < len(helper1) and i+1 < len(attr1) and j+1 < len(attr2) and \
                    helper1[k] not in ['*', '_', '?'] and helper1[k+1] not in ['*', '_', '?'] and attr1[i] == attr2[j+1] and attr1[i+1] == attr2[j]:
                        attr1_display += '<span class="transpose_text">' + '@&' + '</span>'
                        attr2_display += '<span class="transpose_text">' + '&@' + '</span>'
                        k += 2
                        i += 2
                        j += 2
                    elif helper1[k] == '_' or helper1[k] == '?':
                        attr2_display += '<span class="indel_text">' + '&' + '</span>'
                        k += 1
                        j += 1
                    elif helper2[k] == '_' or helper2[k] == '?':
                        attr1_display += '<span class="indel_text">' + '@' + '</span>'
                        k += 1
                        i += 1
                    else:
                        attr1_display += '<span class="replace_text">' + '@' + '</span>'
                        attr2_display += '<span class="replace_text">' + '&' + '</span>'
                        k += 1
                        i += 1
                        j += 1
        return [attr1_display, attr2_display]


def get_date_display(attr1, attr2, helper1, helper2, attribute_mode):
    """
    get the attribute mode for date
    attribute mode can be:
    'base', 'full', 'partial', 'masked'
    Note that some attribute does not have partial mode, in this case, partial mode will return masked mode
    Remeber to call has_partial_mode function to check if it actually has partial mode!
    Example: 
    Input:
        attr1 = '12/28/1950'
        attr2 = '12/28/1905'
        helper1 = '**/**/**50'
        helper2 = '**/**/**05'
        attribute_mode: 'partial'
    Output:
        ['**/**/**<span style="color:blue">50</span>', '**/**/**<span style="color:blue">05</span>']
    """
    if attribute_mode == 'base':
        if not attr1:
            attr1_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
        else:
            attr1_display = attr1
        if not attr2:
            attr2_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
        else:
            attr2_display = attr2
        return [attr1_display, attr2_display]
    elif attribute_mode == 'full':
        if not attr1 or not attr2:
            if not attr1:
                attr1_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr1_display = attr1

            if not attr2:
                attr2_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr2_display = attr2
        else:
            if '*' not in helper1 and '*' not in helper2:
                attr1_display = attr1
                attr2_display = attr2
            elif helper1 == helper2:
                attr1_display = attr1
                attr2_display = attr2
            else:
                attr1_display = ''
                attr2_display = ''
                M1 = helper1[0:2]
                M2 = helper2[0:2]
                D1 = helper1[3:5]
                D2 = helper2[3:5]
                Y1 = helper1[6:]
                Y2 = helper2[6:]
                k = 0
                if M1 != '**' and D1 != '**' and M1 == D2 and M2 == D1:
                    attr1_display += attr1[0:6]
                    attr2_display += attr2[0:6]
                    k = 6
                while k < 10:
                    if helper1[k] == '/':
                        attr1_display += '/'
                        attr2_display += '/'
                        k += 1
                    elif k+1 < 10 and helper1[k] != '*' and helper1[k+1] != '*' and helper1[k] == helper2[k+1] and helper1[k+1] == helper2[k]:
                        attr1_display += '<span class="transpose_text">' + helper1[k:k+2] + '</span>'
                        attr2_display += '<span class="transpose_text">' + helper2[k:k+2] + '</span>'
                        k += 2
                    elif helper1[k] != '*':
                        attr1_display += '<span class="replace_text">' + attr1[k] + '</span>'
                        attr2_display += '<span class="replace_text">' + attr2[k] + '</span>'
                        k += 1
                    else:
                        attr1_display += attr1[k]
                        attr2_display += attr2[k]
                        k += 1
        return [attr1_display, attr2_display]
    elif attribute_mode == 'partial':
        if not attr1 or not attr2:
            if not attr1:
                attr1_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr1_display = '**/**/****'

            if not attr2:
                attr2_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr2_display = '**/**/****'
        else:
            if '*' not in helper1 and '*' not in helper2:
                attr1_display = '@@/@@/@@@@'
                attr2_display = '&&/&&/&&&&'
            elif helper1 == helper2:
                attr1_display = '<img src="/static/images/site/checkmark.png" alt="checkmark" class="freq_icon">'
                attr2_display = '<img src="/static/images/site/checkmark.png" alt="checkmark" class="freq_icon">'
            else:
                attr1_display = ''
                attr2_display = ''
                M1 = helper1[0:2]
                M2 = helper2[0:2]
                D1 = helper1[3:5]
                D2 = helper2[3:5]
                Y1 = helper1[6:]
                Y2 = helper2[6:]
                k = 0
                if M1 != '**' and D1 != '**' and M1 == D2 and M2 == D1:
                    attr1_display += attr1[0:6]
                    attr2_display += attr2[0:6]
                    k = 6
                while k < 10:
                    if helper1[k] == '/':
                        attr1_display += '/'
                        attr2_display += '/'
                        k += 1
                    elif k+1 < 10 and helper1[k] != '*' and helper1[k+1] != '*' and helper1[k] == helper2[k+1] and helper1[k+1] == helper2[k]:
                        attr1_display += '<span class="transpose_text">' + helper1[k:k+2] + '</span>'
                        attr2_display += '<span class="transpose_text">' + helper2[k:k+2] + '</span>'
                        k += 2
                    elif helper1[k] != '*':
                        attr1_display += '<span class="replace_text">' + attr1[k] + '</span>'
                        attr2_display += '<span class="replace_text">' + attr2[k] + '</span>'
                        k += 1
                    else:
                        attr1_display += '*'
                        attr2_display += '*'
                        k += 1
        return [attr1_display, attr2_display]
    elif attribute_mode == 'masked':
        if not attr1 or not attr2:
            if not attr1:
                attr1_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr1_display = '**/**/****'

            if not attr2:
                attr2_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr2_display = '**/**/****'
        else:
            if '*' not in helper1 and '*' not in helper2:
                attr1_display = '@@/@@/@@@@'
                attr2_display = '&&/&&/&&&&'
            elif helper1 == helper2:
                attr1_display = '<img src="/static/images/site/checkmark.png" alt="checkmark" class="freq_icon">'
                attr2_display = '<img src="/static/images/site/checkmark.png" alt="checkmark" class="freq_icon">'
            else:
                attr1_display = ''
                attr2_display = ''
                M1 = helper1[0:2]
                M2 = helper2[0:2]
                D1 = helper1[3:5]
                D2 = helper2[3:5]
                Y1 = helper1[6:]
                Y2 = helper2[6:]
                k = 0
                if M1 != '**' and D1 != '**' and M1 == D2 and M2 == D1:
                    attr1_display += '@@/&&/'
                    attr2_display += '&&/@@/'
                    k = 6
                while k < 10:
                    if helper1[k] == '/':
                        attr1_display += '/'
                        attr2_display += '/'
                        k += 1
                    elif k+1 < 10 and helper1[k] != '*' and helper1[k+1] != '*' and helper1[k] == helper2[k+1] and helper1[k+1] == helper2[k]:
                        attr1_display += '<span class="transpose_text">' + '@&' + '</span>'
                        attr2_display += '<span class="transpose_text">' + '&@' + '</span>'
                        k += 2
                    elif helper1[k] != '*':
                        attr1_display += '<span class="replace_text">' + '@' + '</span>'
                        attr2_display += '<span class="replace_text">' + '&' + '</span>'
                        k += 1
                    else:
                        attr1_display += '*'
                        attr2_display += '*'
                        k += 1
        return [attr1_display, attr2_display]

def get_character_display(attr1, attr2,  helper1, helper2, attribute_mode):
    """
    """
    if attribute_mode == 'base' or attribute_mode == 'full':
        if not attr1:
            attr1 = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
        if not attr2:
            attr2 = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
        return [attr1, attr2]
    else:
        if not attr1 or not attr2:
            if not attr1:
                attr1_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr1_display = '*'
            if not attr2:
                attr2_display = '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">'
            else:
                attr2_display = '*'
        elif attr1 == attr2:
            attr1_display = '<img src="/static/images/site/checkmark.png" alt="checkmark" class="freq_icon">'
            attr2_display = '<img src="/static/images/site/checkmark.png" alt="checkmark" class="freq_icon">'
        else:
            attr1_display = '@'
            attr2_display = '&'
        return [attr1_display, attr2_display]


def get_name_freq(freq, mode):
    if mode == 'base':
        return ''
    freq = int(freq)
    if freq == 1:
        return '<img src="/static/images/site/unique.png" alt="unique" class="freq_icon">'
    elif freq <= 5:
        return '<img src="/static/images/site/rare.png" alt="rare" class="freq_icon">'
    elif freq <= 100:
        return '<img src="/static/images/site/common.png" alt="common" class="freq_icon" value="%s">'%freq
    else:
        return '<img src="/static/images/site/infinity.png" alt="infinity" class="freq_icon" value="">'%freq


def get_ffreq(freq, mode='full'):
    return get_name_freq(freq, mode)


def get_lfreq(freq, mode='full'):
    return get_name_freq(freq, mode)


def format_pair(p1, p2, data_mode):
    result1 = list()
    result2 = list()

    if data_mode == 'base':
        mode = DATA_MODE_BASE
    elif data_mode == 'full':
        mode = DATA_MODE_FULL
    elif data_mode == 'masked':
        mode = DATA_MODE_MASKED
    elif data_mode == 'minimum':
        mode = DATA_MODE_MINIMUM
    elif data_mode == 'moderate':
        mode = DATA_MODE_MODERATE

    # pair id
    result1.append(p1[0])
    result2.append(p2[0])

    # record attribute ID
    id_format = get_string_display(p1[1], p2[1], p1[9], p2[9], mode[0])
    result1.append(id_format[0])
    result2.append(id_format[1])

    # first name frequency
    freq_mode = 'full'
    if data_mode == 'base':
        freq_mode = 'base'
    result1.append(get_ffreq(p1[2], mode=freq_mode))
    result2.append(get_ffreq(p2[2], mode=freq_mode))

    # first name
    first_name_format = get_string_display(p1[3], p2[3], p1[10], p2[10], mode[1])
    result1.append(first_name_format[0])
    result2.append(first_name_format[1])

    # last name
    last_name_format = get_string_display(p1[4], p2[4], p1[11], p2[11], mode[2])
    result1.append(last_name_format[0])
    result2.append(last_name_format[1])

    # special case: first name and last name swap
    if mode[1] in ['partial', 'masked'] and mode[2] in ['partial', 'masked']:
        if p1[3] != p2[3] and p1[4] != p2[4] and p1[3] == p2[4] and p1[4] == p2[3]:
            result1[3] = '@'*len(p1[3])
            result2[3] = '&'*len(p2[3])
            result1[4] = '&'*len(p1[4])
            result2[4] = '@'*len(p2[4])

    # last name frequency
    result1.append(get_lfreq(p1[5], mode=freq_mode))
    result2.append(get_lfreq(p2[5], mode=freq_mode))

    # DoB
    DoB_format = get_date_display(p1[6], p2[6], p1[12], p2[12], mode[3])
    result1.append(DoB_format[0])
    result2.append(DoB_format[1])

    # gender
    gender_format = get_character_display(attr1=p1[7], attr2=p2[7], helper1='', helper2='', attribute_mode=mode[4])
    result1.append(gender_format[0])
    result2.append(gender_format[1])

    # race
    race_format = get_character_display(attr1=p1[8], attr2=p2[8], helper1='', helper2='', attribute_mode=mode[5])
    result1.append(race_format[0])
    result2.append(race_format[1])
    
    return [result1, result2]


def format_data(data, data_mode):
    """
    INPUT: 
        data - raw data
        data_mode - 'base', 'full', 'masked', 'minimum', 'moderate'
    OUTPUT: data for display
    Example:
    input: 
    data = [
        ['1','','206','NELSON','MITCHELL','1459','03/13/1975','M','B','','******','********___','03/13/1975','*','*','34','6','0'],
        ['1','1000142704,174','NELSON','MITCHELL SR','1314','07/03/1949','M','B','1000142704','******','******** SR','07/03/1949','*','*','34','6','0']
    ]
    data_mode = full
    output: [
        ['1', '<img src="/static/images/site/missing.png" alt="missing" class="missing_icon">', '<img src="/static/images/site/infinity.png" alt="infinity" class="freq_icon">', 'NELSON', 'MITCHELL', '<img src="/static/images/site/infinity.png" alt="infinity" class="freq_icon">', '03/13/1975','M','B'],
        ['1', '1000142704', '<img src="/static/images/site/infinity.png" alt="infinity" class="freq_icon">', 'NELSON', 'MITCHELL <span style="color:green">SR</span>', '<img src="/static/images/site/infinity.png" alt="infinity" class="freq_icon">', '07/03/1949','M','B']
    ]
    """
    ret = list()
    for i in range(0, len(data), 2):
        result = format_pair(data[i], data[i+1], data_mode)
        ret += result
    return ret


def get_icon_string(s1, s2, helper1, helper2):
    if not s1 or not s2:
        return ''
    else:
        if s1 == s2:
            return ''
        else:
            if '*' not in helper1 and '*' not in helper2:
                return '<img class="diff_icon" src="/static/images/site/diff.png" alt="diff">'
            else:
                icons = list()
                ret = ''
                i = 0
                j = 0
                k = 0
                prev_indel = 0
                prev_repl = 0
                while k < len(helper1):
                    if helper1[k] == '*' and helper2[k] == '*':
                        # ret += '<img class="space_icon_full" src="/static/images/site/space.png" alt="space">'
                        # ret += '<span class="hidden_element">*</span>' 
                        icons.append('E')
                        k += 1
                        i += 1
                        j += 1
                    elif k+1 < len(helper1) and i+1 < len(s1) and j+1 < len(s2) and helper1[k] not in ['*', '_', '?'] and helper1[k+1] not in ['*', '_', '?'] and s1[i] == s2[j+1] and s1[i+1] == s2[j]:
                        # ret += '<img class="transpose_icon" src="/static/images/site/transpose.png" alt="transpose">'
                        icons.append('T')
                        icons.append('T')
                        k += 2
                        i += 2
                        j += 2
                    elif helper1[k] == '_' or helper1[k] == '?':
                        if helper1[k] == "_":
                            # if not k+1 == len(helper1) and helper1[k+1] == "_":
                               # ret += '<img class="space_icon" src="/static/images/site/space.png" alt="space">'
                               # prev_indel += 1
                            # else:
                               # ret += '<img class="indel_icon" src="/static/images/site/indel.png" alt="indel">'
                               # for z in range(prev_indel):
                                   # ret += '<img class="space_icon" src="/static/images/site/space.png" alt="space">' 
                               # prev_indel = 0

                            icons.append('I')
                        k += 1
                        j += 1
                    elif helper2[k] == '_' or helper2[k] == '?':
                        if helper2[k] == '_':
                            # if not k+1 == len(helper2) and helper2[k+1] == "_":
                            #    ret += '<img class="space_icon" src="/static/images/site/space.png" alt="space">'
                            #    prev_indel += 1
                            # else:
                            #    ret += '<img class="indel_icon" src="/static/images/site/indel.png" alt="indel">'
                            #    for z in range(prev_indel):
                            #        ret += '<img class="space_icon" src="/static/images/site/space.png" alt="space">' 
                            #    prev_indel = 0
                            icons.append('I')
                        k += 1
                        i += 1
                    else:
                        # if not k+1 == len(helper1) and not helper1[k+1] in ["*", "_", "?"] and not helper2[k+1] in ["*", "_", "?"]:
                        #    ret += '<img class="space_icon" src="/static/images/site/space.png" alt="space">'
                        #    prev_repl += 1
                        # else:
                        #    ret += '<img class="replace_icon" src="/static/images/site/replace.png" alt="replace">'
                        #    for z in range(prev_repl):
                        #            ret += '<img class="space_icon" src="/static/images/site/space.png" alt="space">' 
                        #    prev_repl = 0
                        icons.append('R')
                        k += 1
                        i += 1
                        j += 1

                end = 0
                i = 0
                while i < len(icons):
                    item = ''
                    if icons[i] == 'R':
                        l = i;
                        while i+1 < len(icons) and icons[i+1] == 'R':
                            i += 1
                        pos = 0.5*(l+i)
                        item = '<img class="replace_icon" src="/static/images/site/replace.png" alt="replace" style="margin-left:%fpx;">' % (8.8*pos-end-2)
                        end = 8.8*pos-2 + 13
                    elif icons[i] == 'I':
                        l = i;
                        while i+1 < len(icons) and icons[i+1] == 'I':
                            i += 1
                        pos = 0.5*(l+i)
                        item = '<img class="indel_icon" src="/static/images/site/indel.png" alt="indel" style="margin-left:%fpx;">' % (8.8*pos-end-2)
                        end = 8.8*pos-2 + 13
                    elif icons[i] == 'T':
                        pos = i;
                        item = '<img class="transpose_icon" src="/static/images/site/transpose.png" alt="transpose" style="margin-left:%fpx;">' % (8.8*pos-end)
                        end = 8.8*pos + 20
                        i += 1
                    ret += item
                    i += 1
                item = '<img class="space_icon" src="/static/images/site/space.png" alt="space" style="margin-left:%fpx;">' % (8.8*len(icons)-end)
                ret += item
                return ret


def get_icon_nameswap(n11, n12, n21, n22):
    if n11 != n21 and n12 != n22 and n11 == n22 and n21 == n12:
        return '<img class="name_swap_icon" src="/static/images/site/name_swap.png" alt="name_swap">'
    else:
        return ''


def get_icon_date(d1, d2, helper1, helper2):
    if not d1 or not d2:
        return ''
    else:
        if d1 == d2:
            return ''
        else:
            if '*' not in helper1 and '*' not in helper2:
                return '<img class="diff_icon" src="/static/images/site/diff.png" alt="diff">'
            else:
                ret = ''
                M1 = helper1[0:2]
                M2 = helper2[0:2]
                D1 = helper1[3:5]
                D2 = helper2[3:5]
                Y1 = helper1[6:]
                Y2 = helper2[6:]
                k = 0
                if M1 != '**' and D1 != '**' and M1 == D2 and M2 == D1:
                    ret += '<img class="swap_date_icon" src="/static/images/site/swap_date.png" alt="swap_date">'
                    k = 6
                while k < 10:
                    if helper1[k] == '/':
                        ret += '<span class="hidden_element">/</span>'
                        k += 1
                    elif k+1 < 10 and helper1[k] != '*' and helper1[k+1] != '*' and helper1[k] == helper2[k+1] and helper1[k+1] == helper2[k]:
                        ret += '<img class="transpose_icon" src="/static/images/site/transpose.png" alt="transpose">'
                        k += 2
                    elif helper1[k] != '*':
                        if k+1 < len(helper1) and helper1[k+1] != "/" and helper1[k+1] != "*":
                            ret += '<img class="space_icon" src="/static/images/site/space.png" alt="space">'
                        else:
                            ret += '<img class="replace_icon" src="/static/images/site/replace.png" alt="replace">'
                        k += 1
                    else:
                        ret += '<span class="hidden_element">*</span>'
                        k += 1
                return ret


def get_icon_character(c1, c2):
    if c1 and c2 and c1 != c2:
        return '<img class="diff_icon" src="/static/images/site/diff.png" alt="diff">'
    else:
        return ''


def get_icon_for_pair(p1, p2):
    icon = list()

    # icon for ID
    icon.append(get_icon_string(p1[1], p2[1], p1[9], p2[9]))
    # icon for firstname
    icon.append(get_icon_string(p1[3], p2[3], p1[10], p2[10]))
    # icon for name swap
    icon.append(get_icon_nameswap(p1[3], p1[4], p2[3], p2[4]))
    # icon for lastname
    icon.append(get_icon_string(p1[4], p2[4], p1[11], p2[11]))
    # icon for DoB
    icon.append(get_icon_date(p1[6], p2[6], p1[12], p2[12]))
    # icon for sex
    icon.append(get_icon_character(p1[7], p2[7]))
    # icon for race
    icon.append(get_icon_character(p1[8], p2[8]))

    if icon[2] != '':
        icon[1] = ''
        icon[3] = ''

    return icon


def generate_icon(data):
    """
    INPUT: 
        data - raw data
    OUTPUT: 
        icon - the markup icons : [id, firstname, name_swap, lastname, DoB, gender, race]
    Example:
    input: 
    data = [
        ['1','','206','NELSON','MITCHELL','1459','03/13/1975','M','B','','******','********___','03/13/1975','*','*','34','6','0'],
        ['1','1000142704,174','NELSON','MITCHELL SR','1314','07/03/1949','M','B','1000142704','******','******** SR','07/03/1949','*','*','34','6','0']
    ]
    output: [
        ['', '', '<span class="hidden_element">MITCHELL</span><img class="indel_icon" src="/static/images/site/indel.png" alt="indel"><img class="indel_icon" src="/static/images/site/indel.png" alt="indel"><img class="indel_icon" src="/static/images/site/indel.png" alt="indel">', '<img class="diff_icon" src="/static/images/site/diff.png" alt="diff">', '', '']
    ]
    """
    ret = list()
    for i in range(0, len(data), 2):
        result = get_icon_for_pair(data[i], data[i+1])
        ret.append(result)
    return ret


if __name__ == '__main__':
    attr1 = 'AUSTIN'
    attr2 = 'AUTWELL'
    helper1 = attr1
    helper2 = attr2
    res = get_string_display(attr1, attr2, helper1, helper2, 'full')
    print(res)
    res = get_string_display(attr1, attr2, helper1, helper2, 'partial')
    print(res)
    res = get_string_display(attr1, attr2, helper1, helper2, 'masked')
    print(res)

    attr1 = '1022119365'
    attr2 = '1022119365'
    helper1 = '**********'
    helper2 = '**********'
    res = get_string_display(attr1, attr2, helper1, helper2, 'full')
    print(res)
    res = get_string_display(attr1, attr2, helper1, helper2, 'partial')
    print(res)
    res = get_string_display(attr1, attr2, helper1, helper2, 'masked')
    print(res)

    attr1 = '1000151475'
    attr2 = '1000151575'
    helper1 = '*******4**'
    helper2 = '*******5**'
    res = get_string_display(attr1, attr2, helper1, helper2, 'full')
    print(res)
    res = get_string_display(attr1, attr2, helper1, helper2, 'partial')
    print(res)
    res = get_string_display(attr1, attr2, helper1, helper2, 'masked')
    print(res)

    attr1 = 'SHIESHA'
    attr2 = 'SHAMEESHA'
    helper1 = '**I__****'
    helper2 = '**AME****'
    res = get_string_display(attr1, attr2, helper1, helper2, 'full')
    print(res)
    res = get_string_display(attr1, attr2, helper1, helper2, 'partial')
    print(res)
    res = get_string_display(attr1, attr2, helper1, helper2, 'masked')
    print(res)

    attr1 = '1530042971'
    attr2 = '1350082931'
    helper1 = '*53**4**7*'
    helper2 = '*35**8**3*'
    res = get_string_display(attr1, attr2, helper1, helper2, 'full')
    print(res)
    res = get_string_display(attr1, attr2, helper1, helper2, 'partial')
    print(res)
    res = get_string_display(attr1, attr2, helper1, helper2, 'masked')
    print(res)

    attr1 = '12/27/1944'
    attr2 = '12/27/1904'
    helper1 = '**/**/**4*'
    helper2 = '**/**/**0*'
    res = get_date_display(attr1, attr2, helper1, helper2, 'full')
    print(res)
    res = get_date_display(attr1, attr2, helper1, helper2, 'partial')
    print(res)
    res = get_date_display(attr1, attr2, helper1, helper2, 'masked')
    print(res)

    attr1 = '12/28/1950'
    attr2 = '12/28/1905'
    helper1 = '**/**/**50'
    helper2 = '**/**/**05'
    res = get_date_display(attr1, attr2, helper1, helper2, 'full')
    print(res)
    res = get_date_display(attr1, attr2, helper1, helper2, 'partial')
    print(res)
    res = get_date_display(attr1, attr2, helper1, helper2, 'masked')
    print(res)

    attr1 = '01/09/1960'
    attr2 = '09/01/1960'
    helper1 = '01/09/****'
    helper2 = '09/01/****'
    res = get_date_display(attr1, attr2, helper1, helper2, 'full')
    print(res)
    res = get_date_display(attr1, attr2, helper1, helper2, 'partial')
    print(res)
    res = get_date_display(attr1, attr2, helper1, helper2, 'masked')
    print(res)

    attr1 = '01/09/1935'
    attr2 = '01/09/1935'
    helper1 = '**/**/****'
    helper2 = '**/**/****'
    res = get_date_display(attr1, attr2, helper1, helper2, 'full')
    print(res)
    res = get_date_display(attr1, attr2, helper1, helper2, 'partial')
    print(res)
    res = get_date_display(attr1, attr2, helper1, helper2, 'masked')
    print(res)

    attr1 = '10/01/1990'
    attr2 = '09/19/1995'
    helper1 = '10/01/1990'
    helper2 = '09/19/1995'
    res = get_date_display(attr1, attr2, helper1, helper2, 'full')
    print(res)
    res = get_date_display(attr1, attr2, helper1, helper2, 'partial')
    print(res)
    res = get_date_display(attr1, attr2, helper1, helper2, 'masked')
    print(res)

    pairs = list()
    pairs.append(['1','1002415935','303','DARIUS','FLOWE','163','05/11/1994','M','B','*********5','***IUS','*****','**/**/****','*','*','8','2','0'])
    pairs.append(['1','1002415936','270','DARREN','FLOWE','184','05/11/1994','M','B','*********6','***REN','*****','**/**/****','*','*','8','2','0'])
    pairs.append(['2','1000255792','10','SOL','BADAME','1','07/16/1914','M','W','1000255792','SOL','BADAME','**/**/****','*','*','33','6','1'])
    pairs.append(['2','','1','BADAME','SOL','1','07/16/1914','M','W','','BADAME','SOL','**/**/****','*','*','33','6','1'])
    data = format_data(pairs, 'base')
    print(data)
    data = format_data(pairs, 'full')
    print(data)
    print(data[0][2])


