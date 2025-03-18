def truncate_description_for_table(s):
    tmp = s.split()[0:5]
    return f"{' '.join(tmp)}..."