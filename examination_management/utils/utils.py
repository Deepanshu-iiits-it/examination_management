import pandas as pd


def create_empty_excel(path, columns):
    empty_excel = pd.DataFrame(columns=columns)
    excel_writer = pd.ExcelWriter(path)
    empty_excel.to_excel(excel_writer, index=False)
    excel_writer.save()


def create_excel(path, data):
    excel = pd.DataFrame(data=data)
    excel_writer = pd.ExcelWriter(path)
    excel.to_excel(excel_writer, index=False)
    excel_writer.save()
