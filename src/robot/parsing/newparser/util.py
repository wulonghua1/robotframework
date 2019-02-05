
def append_to_list_value(p):
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        value = p[1]
        if (p[2]) is not None:
            value.append(p[2])
        p[0] = value
