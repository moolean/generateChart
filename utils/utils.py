import csv
import os
import random
import matplotlib, matplotlib.pyplot as plt
from scipy.spatial import distance
from math import sqrt
import colorsys

# 定义一些常见颜色的 RGBA 值和汉字名称
color_map = {
    "红色": (255, 0, 0, 255),
    "深红": (139, 0, 0, 255),
    "粉红": (255, 182, 193, 255),
    "亮粉红": (255, 105, 180, 255),
    "橙色": (255, 165, 0, 255),
    "金色": (255, 215, 0, 255),
    "黄色": (255, 255, 0, 255),
    "绿黄色": (173, 255, 47, 255),
    "绿色": (0, 255, 0, 255),
    "深绿色": (0, 100, 0, 255),
    "青色": (0, 255, 255, 255),
    "蓝色": (0, 0, 255, 255),
    "深蓝": (0, 0, 139, 255),
    "紫色": (128, 0, 128, 255),
    "靛青": (75, 0, 130, 255),
    "棕色": (165, 42, 42, 255),
    "浅棕": (210, 180, 140, 255),
    "灰色": (128, 128, 128, 255),
    "深灰": (169, 169, 169, 255),
    "黑色": (0, 0, 0, 255),
    "棕黄色": (222, 184, 135, 255)
}

def get_diff_color(num_colors):
    selected_keys = random.sample(list(color_map.keys()), num_colors)
    colors = []
    colorName = []
    for idx, i in enumerate(selected_keys):
        colors.append([i/255 for i in color_map[i]])
        colorName.append([i, idx])

    return colors, colorName


def generate_distinct_colors(num_colors):
    # 在色相环上均匀分布颜色
    hues = [i / num_colors for i in range(num_colors)]
    random.shuffle(hues)  # 随机打乱颜色顺序
    
    # 将色相转换为 RGB 颜色
    colors = [colorsys.hsv_to_rgb(h, 0.7, 0.9) for h in hues]
    # 将 RGB 颜色转换为 RGBA
    colors = [(r, g, b, 1) for r, g, b in colors]
    
    return colors

def rgba_to_ch(rgba):
    # 提取 RGBA 值
    r, g, b, a = rgba
    r, g, b, a = int(r*255), int(g*255), int(b*255), int(a*255)
    # 初始化最小距离和最佳匹配颜色名称
    min_distance = float('inf')
    best_match = None
    
    # 计算给定 RGBA 值与每个预定义颜色的距离
    for name, (cr, cg, cb, ca) in color_map.items():
        dist = distance.euclidean((r, g, b, a), (cr, cg, cb, ca))
        if dist < min_distance:
            min_distance = dist
            best_match = name
    
    return best_match


def set_font():
    # 必须写在with plt.xkcd()的里面，不然会报错
    font_types =[
        'Noto Sans CJK JP', 
        "Noto Serif CJK JP",
        "WenQuanYi Zen Hei",
        "AR PL UMing CN",
        "Long Cang",
        
        "Microsoft YaHei",
        "STXingKai",
        "STFangsong",
        "STKaiti",
        "STLiti",
        "STZhongsong"
    ]

    matplotlib.rcParams['font.family'] = random.choice(font_types)


def calculate_iou(bbox1, bbox2):
    x1_bbox1, y1_bbox1, x2_bbox1, y2_bbox1 = bbox1
    x1_bbox2, y1_bbox2, x2_bbox2, y2_bbox2 = bbox2

    x_intersection = max(0, min(x2_bbox1, x2_bbox2) - max(x1_bbox1, x1_bbox2))
    y_intersection = max(0, min(y2_bbox1, y2_bbox2) - max(y1_bbox1, y1_bbox2))
    intersection_area = x_intersection * y_intersection

    area_bbox1 = (x2_bbox1 - x1_bbox1) * (y2_bbox1 - y1_bbox1)
    area_bbox2 = (x2_bbox2 - x1_bbox2) * (y2_bbox2 - y1_bbox2)

    # import warnings
    # with warnings.catch_warnings(record=True) as warning_list:
    #     iou = intersection_area / (area_bbox1 + area_bbox2 - intersection_area)
    #     if warning_list:
    #         import pdb; pdb.set_trace()
            
    iou = intersection_area / (area_bbox1 + area_bbox2 - intersection_area)
    
    return iou



def judge_overlap(d: list):
    length = len(d)
    for i in range(length):
        for j in range(i+1, length):
            if calculate_iou(d[i]['bbox'], d[j]['bbox']) > 0.15:
                return "two bbox overlap"
            