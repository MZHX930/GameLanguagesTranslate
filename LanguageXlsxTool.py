# coding: utf-8
# 游戏多语言翻译工具类

import json
import os
import pandas as pd
import ParseConfig


class LanguageXlsxTool:
    def __init__(self):
        self.xlsx_path = ParseConfig.get_xlsx_path()
        self.data = None
        self.parse_xlsx()

    def parse_xlsx(self):
        """解析xlsx文件并加载数据"""
        try:
            self.data = pd.read_excel(self.xlsx_path)
            print(f"成功加载xlsx文件: {self.xlsx_path}")
        except FileNotFoundError:
            print(f"错误：找不到xlsx文件 {self.xlsx_path}")
        except pd.errors.EmptyDataError:
            print(f"错误：xlsx文件 {self.xlsx_path} 是空的")
        except Exception as e:
            print(f"解析xlsx文件时发生错误: {str(e)}")

    def get_languages(self):
        """获取所有可用的语言"""
        if self.data is not None:
            return list(self.data.columns)[3:]  # 假设第一列是键，其余列是语言
        return []

    def get_translation(self, key, language):
        """获取指定键和语言的翻译"""
        if self.data is not None:
            row = self.data[self.data.iloc[:, 0] == key]
            if not row.empty and language in self.data.columns:
                return row[language].values[0]
        return None
