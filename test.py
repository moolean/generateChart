import matplotlib.font_manager as fm
import matplotlib.ft2font as ft

# 查找字体路径
font_path = fm.findfont(fm.FontProperties(family='SimSun'))  # 替换成你需要的字体名称

# 加载字体文件
font = ft.FT2Font(font_path)

# 遍历字体的所有字符
all_chars = []
for cmap in font.get_charmap().items():
    char_code, glyph_index = cmap
    all_chars.append(chr(char_code))

# 打印字体包含的所有字符
print("".join(all_chars))