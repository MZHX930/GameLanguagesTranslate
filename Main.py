# coding: utf-8
import asyncio
import tkinter as tk
from tkinter import filedialog
import ParseConfig
import LanguageXlsxTool
import BaiduTranslate

# 翻译结果
translate_result_components = {}


def select_file():
    """打开文件选择对话框并更新路径标签"""
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    if file_path:
        ParseConfig.set_xlsx_path(file_path)
        path_label.config(text=f"XLSX路径: {file_path}")


async def translate_word_async(word, selected_channel, root):
    selected_index = selected_channel.get()
    for index, language in enumerate(translate_languages):
        # 调用异步翻译函数
        result = await BaiduTranslate.translate_text_async(word, to_lang="en")
        translated_text = result
        translate_result_components[language].config(state="normal")
        translate_result_components[language].delete("1.0", tk.END)
        translate_result_components[language].insert("1.0", translated_text)
        translate_result_components[language].config(state="disabled")

        # 强制更新UI
        root.update()

        # 等待1秒
        await asyncio.sleep(1)


def translate_word(word, selected_channel, root):
    # 使用 asyncio.run 来运行异步函数
    asyncio.run(translate_word_async(word, selected_channel, root))


def create_ui():
    """创建800x800的UI界面"""
    global root
    root = tk.Tk()
    root.title("游戏多语言翻译")  # 设置窗口标题
    root.geometry("800x800")

    # 创建一个Frame用于路径和按钮
    path_frame = tk.Frame(root)
    path_frame.pack(fill="x", padx=10, pady=5)

    # 获取xlsx路径
    global path_label
    xlsx_path = ParseConfig.get_xlsx_path()
    path_label = tk.Label(
        path_frame, text=f"XLSX路径: {xlsx_path}", anchor="w", justify="left"
    )
    path_label.pack(side="left")

    # 添加选择按钮在路径标签后面
    select_button = tk.Button(path_frame, text="选择", command=select_file)
    select_button.pack(side="right")

    # 创建一个Frame用于单选按钮组
    radio_frame = tk.Frame(root)
    radio_frame.pack(pady=10)

    # 创建单选按钮组
    channels = ParseConfig.get_all_channels()
    selected_channel = tk.IntVar(value=0)  # 默认选择第一个

    for index, channel in enumerate(channels):
        radio_button = tk.Radiobutton(
            radio_frame, text=channel, variable=selected_channel, value=index
        )
        radio_button.pack(side="left", padx=5)  # 使用pack布局管理器

    # 单行输入框
    translate_frame = tk.Frame(root, bg="lightgray", bd=2, relief="sunken")
    translate_frame.pack(fill="both", expand=True, padx=10, pady=10)
    # 在Frame中添加一个Label
    label = tk.Label(translate_frame, text="请输入中文文本:")
    label.pack(side="top", anchor="nw", pady=5)
    # 在Frame中添加一个Entry（单行输入框）
    inputFiled = tk.Entry(translate_frame)
    inputFiled.pack(side="top", anchor="nw", pady=5, fill="x")
    # 居中添加按钮“翻译”
    btnTranlate = tk.Button(
        translate_frame,
        text="翻译",
        command=lambda: translate_word(inputFiled.get(), selected_channel, root),
    )
    btnTranlate.pack(side="top", anchor="n", pady=5)

    # 显示翻译结果
    result_frame = tk.Frame(translate_frame)
    result_frame.pack(fill="both", expand=True, pady=10)

    for index, language in enumerate(translate_languages):
        tk.Label(result_frame, text=language).grid(
            row=index, column=0, sticky="w", padx=5, pady=2
        )

    # 创建文本框和滚动条
    for index, language in enumerate(translate_languages):
        text_widget = tk.Text(result_frame, height=1, width=50)
        text_widget.insert("1.0", "")  # 初始文本
        text_widget.config(state="disabled")  # 只读模式
        text_widget.grid(row=index, column=1, sticky="w", padx=5, pady=2)
        translate_result_components[language] = text_widget

    # 启动主循环
    root.mainloop()


if __name__ == "__main__":
    xlsxTool = LanguageXlsxTool.LanguageXlsxTool()  # 初始化xlsxTool
    translate_languages = xlsxTool.get_languages()
    create_ui()
