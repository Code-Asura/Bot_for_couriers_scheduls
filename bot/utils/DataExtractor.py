import pygsheets

class DataExtractor:
    def __init__(self, spreadsheet_neme: str) -> None:
        self.gc = pygsheets.authorize(service_account_file="bot/data/credentials.json")
        self.sheet = self.gc.open(spreadsheet_neme)
    
    # Получение индекса столбца по заголовку
    def _get_column_index(self, sheet, column_value: str):
        header = sheet.get_values("A1", "Z1")[0]
        return header.index(column_value) + 1
    
    # Получение индекса строки по значению в первом столбце
    def _get_row_index(self, sheet, row_value: str):
        values = sheet.get_col(1, include_tailing_empty=False)
        
        if row_value in values:
            return values.index(row_value) + 1    
    
    # Получение индексов строк в другом листе
    def _get_index_row_another_list(self, target_list, another_sheet_name: str):
        another_sheet = self.sheet.worksheet("title", another_sheet_name)
        coll = another_sheet.get_col(2, include_tailing_empty=False)
        result = []

        for value in target_list:
            if value in coll:
                row_index = coll.index(value) + 1
                result.append(row_index)

        return result

    # Получение значения целевой ячейки
    def _get_target_value(self, sheet, row_index: int, column_index: int):
        return sheet.cell((row_index, column_index)).value
    
    # Основной метод для извлечения данных
    def extract_data(self, sheet_name: str, column_value: str, row_value: str) -> list:
        sheet = self.sheet.worksheet("title", sheet_name)
        column_index = self._get_column_index(sheet, column_value)
        row_index = self._get_row_index(sheet, row_value)

        if row_index is not None:
            target_value = self._get_target_value(sheet, row_index, column_index)
            return target_value.split("\n")
        
        return []
    
    # Поиск данных в другом листе
    def find_data_another_sheet(self, target_list, another_sheet_name: str) -> list:
        indices_row = self._get_index_row_another_list(target_list, another_sheet_name)
        wks = self.sheet.worksheet("title", another_sheet_name)
        result = []

        for row_index in indices_row:
            row_data = wks.get_values((row_index, 3), (row_index, 5), include_tailing_empty=False)
            result.append(row_data[0])

        return result
