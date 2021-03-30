def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def trim_tags(s, start_tag, end_tag):
    return s.replace(start_tag, '', 1).replace(end_tag, '', 1).strip()
