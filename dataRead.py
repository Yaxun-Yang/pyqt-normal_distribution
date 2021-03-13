import xlrd


def read_by_excel(path, index_of_sheet, index_of_row):
    # 通过序号获取表格
    data = xlrd.open_workbook(path)
    sheet = data.sheets()[index_of_sheet]

    # 数据量
    num_of_data = sheet.nrows

    data_list = []

    for i in range(1, num_of_data):
        data_list.append(sheet.cell(i, index_of_row).value)

    return data_list

