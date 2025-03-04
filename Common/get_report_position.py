from openpyxl import load_workbook
from openpyxl.styles import Font
from Common.config import Config

class GetReportPosition:
    def __init__(self, file_path):
        self.file_path = file_path

    def find_scenario_position_by_keyword(self, keyword, sheet_name):
        wb = load_workbook(self.file_path)
        sheet = wb[sheet_name]
        for row in sheet.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and keyword in cell.value:
                    # 获取单元格的行和列（注意行和列是从1开始的）, 返回x, y
                    wb.close()
                    return [cell.row, cell.column]

    def get_light_lux_position(self, key_word, sheet_name):
        key_position = self.find_scenario_position_by_keyword(key_word, sheet_name)
        return key_position


if __name__ == '__main__':
    g_p_s = GetReportPosition(Config.original_template_path)
    print(g_p_s.get_light_lux_position(Config.light_lux, Config.ae_stability_sheet_name))
