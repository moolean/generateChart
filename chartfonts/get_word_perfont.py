"""
    废弃，采用其他策略，但保留代码
"""

import jieba
import matplotlib.font_manager as fm
import matplotlib.ft2font as ft

# Step 1: 获取结巴分词的词典文件中的所有词
dict_file = jieba.get_dict_file()
words = [line.decode("utf-8").split()[0] for line in dict_file.readlines()]

# Step 2: 定义一个函数获取指定字体支持的字符集
def get_supported_chars(font_path):
    # 加载字体文件
    font = ft.FT2Font(font_path)

    # 遍历字体的所有字符
    all_chars = []
    for cmap in font.get_charmap().items():
        char_code, glyph_index = cmap
        all_chars.append(chr(char_code))
    return all_chars

# Step 3: 定义一个函数过滤出可以显示的词并保存到文件
def save_filtered_words(font_path, words, output_file):
    supported_chars = get_supported_chars(font_path)
    filtered_words = [word for word in words if all(char in supported_chars for char in word)]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in filtered_words:
            f.write(word + '\n')

# Step 4: 获取所有可用的字体文件路径
font_paths = fm.findSystemFonts(fontpaths=None, fontext='ttf')

# Step 5: 对每个字体，生成对应的可用字文件
for font_path in font_paths:
    font_name = fm.FontProperties(fname=font_path).get_name()
    output_file = f"{font_name}_filtered_words.txt"
    save_filtered_words(font_path, words, output_file)
    print(f"Filtered words for {font_name} saved to {output_file}")