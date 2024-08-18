def dict_factory(column, row):
    data = {}
    for idx, col in enumerate(column.description):
        data[col[0]] = row[idx]
    return data
