import xlrd
def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception:
        print(str(e))

def excel_table_byindex(file = 'file.xls', colnameindex = 0, by_index = 0, by_val = -1):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows
    ncols = table.ncols
    colnames = table.row_values(colnameindex)
    list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        validate = True
        if row:
            app = {}
            for i in range(len(colnames)):
                if by_val == -1:
                    app[colnames[i]] = row[i]
                elif colnames[i] == 'trend' and row[i] != by_val:
                    validate = False
                    break
                else:
                    app[colnames[i]] = row[i]
            if validate:
                list.append(app)
    return  list
