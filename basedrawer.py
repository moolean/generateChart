import io
import json
import os
import time
import numpy as np
import pandas as pd
from PIL import Image
import jieba
import logging
from tqdm import tqdm
import matplotlib, matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor
import matplotlib.font_manager as fm
from pathlib import Path
import random
from datetime import datetime
import warnings
from matplotlib.font_manager import FontProperties
from utils.chart_config import ChartConfig
import copy
import math
import matplotlib.image as mpimg
from abc import ABC, abstractmethod
import sensetool
import functools
from typing import Literal

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [Process: %(process)d]"
# )

def timer_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

class drawer(ABC):
    def __init__(self,
                chart_type,
                usage,
                xticklabel_num_range = [5, 20],
                data_group_num_range = [1, 5],
                x_data_sign_options = ["+"],
                client = None):
        """初始化

        Args:
            chart_type (str): 生成图表的类型
            usage (str): 输出的数据格式 (md, nonumber)
        """
        # 解决字体问题：手动加入字体管理器
        # 指定字体路径
        font_path = "chartfonts"
        # 检查字体路径是否存在
        if os.path.isdir(font_path):
            for root, dirs, files in os.walk(font_path):
                for file in files:
                    if file.endswith('.ttf') or file.endswith('.ttc') or file.endswith('.TTF'):
                        fm.fontManager.addfont(os.path.join(root, file))

        # 刷新 Matplotlib 的字体缓存
        fm._load_fontmanager(try_read_cache=False)

        # 获取所有可用字体
        available_fonts = [f.name for f in fm.fontManager.ttflist]

        # 打印所有可用字体以供检查
        print("Available fonts:", available_fonts)
        # 设置环境变量，将自定义字体路径添加到MATPLOTLIBRC
        os.environ['MATPLOTLIBRC'] = font_path
        # 使用字体列表
        self.font_types =[
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

        # # 忽略 UserWarning 警告（遇到生僻字字体没有会弹出字体警告）
        # warnings.filterwarnings("ignore", category=UserWarning)
        matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号
        # 初始化使用的字库
        dict_file = jieba.get_dict_file()
        self.words = [line.decode("utf-8").split()[0] for line in dict_file.readlines()]

        self.chart_type = chart_type
        usage: Literal["md", "lp", "nonumber_lp","nonumber_md", "desc_qa", "reasoning_qa"]
        self.usage = usage
        self.data_root = os.path.join("opt", f"data_{self.chart_type}_{self.usage}")
        # # 生成图的config，每个图随机config
        self.config = ChartConfig(
                        chart_type=self.chart_type,
                        x_data_sign_options = x_data_sign_options,
                        xticklabel_num_range = xticklabel_num_range, #改成tuple试试 TODO
                        data_group_num_range = data_group_num_range
                    )
        # 初始化背景
        background_path = "background"
        self.background_imgs = []
        for file in os.listdir(background_path):
            fp = os.path.join(background_path, file)
            # img = mpimg.imread(fp) Note: Init里面读图片并行会出问题，只能存放地址，不知道为什么
            # Image.open(fp)
            self.background_imgs.append(fp)

        
        self.checker = sensetool.checker(client)
        sensetool.print_divider("Init")

    def __call__(self, *args, **kwargs):
        return self.generate(*args, **kwargs)
    
    @abstractmethod
    def datagenerater(self):
        """数据生成，必须重载
        """
        pass

    @abstractmethod
    def chartdrawer(self):
        """画图，必须重载
        """
        pass

    def _clearPath(self):
        """创建目录或删除上一次的所有数据，但保留目录结构

        Args:
            data_root (path): 数据集目录
        """
        sensetool.print_divider("Clear Path")
        os.makedirs(self.data_root, exist_ok=True)
        os.makedirs(os.path.join(self.data_root, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.data_root, "jsons"), exist_ok=True)
        os.makedirs(os.path.join(self.data_root, "csvs"), exist_ok=True)
        for dirpath, dirnames, filenames in os.walk(self.data_root):
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                os.remove(file_path)

    def set_font(self):
        # 必须写在with plt.xkcd()的里面，不然会报错
        matplotlib.rcParams['font.family'] = random.choice(self.font_types)

    # @timer_decorator
    def _generate_data_once(self, config_dict):
        """生成一个图的数据
        Returns:
            dict: 数据
        """
        templete = {
            "chart_type":"",
            "chart_title": "",
            "legend_title": "",
            "x_label": "",
            "y_label": "",
            "x_unit": "",
            "y_unit": "",

            "xticklabel_list": [],
            "legend_list": [],
            "data": [],
            "data2": []
        }
        chart_data = copy.deepcopy(templete)
        
        chart_data["chart_title"] = random.choice(self.words) if random.random() < 0.7 else ""
        chart_data['legend_title'] = random.choice(self.words) if random.random() < 0.5 else ""
        chart_data["x_label"] = random.choice(self.words) if random.random() < 0.5 else ""
        chart_data["y_label"] = random.choice(self.words) if random.random() < 0.5 else ""
        chart_data["x_unit"] = random.choice(self.words) if random.random() < 0.5 else ""
        chart_data["y_unit"] = random.choice(self.words) if random.random() < 0.5 else ""

        for _ in range(config_dict['xticklabel_num']):
            chart_data['xticklabel_list'].append(random.choice(self.words))
        for _ in range(config_dict['data_group_num']): # 每一个legend都是一组数据
            chart_data["legend_list"].append(random.choice(self.words)) # legend代表每个组的组名
        
        csv_file = pd.DataFrame()
        csv_file2 = pd.DataFrame()

        self.datagenerater(config_dict, chart_data, csv_file)
        
        input_dict = dict(
            config_dict=config_dict,
            chart_data=chart_data,
            csv_file=csv_file,
            background_imgs=self.background_imgs
        )

        return input_dict

    # @timer_decorator
    def _generateOneChart(self, cnt):
        """单次图表生成
        Args:
            cnt (_type_): _description_

        Returns:
            _type_: _description_
        """
        # 生成config，规定chart的样式
        config_dict = self.config.get_option_once()
        # plt.style.use(config_dict['style_type'])

        # 有可能因为中文字符画不出来，也有可能是数据标签有重合情况，需要重新生成
        for try_count in range(5):
            input_dict = dict(
                data_root=self.data_root,
                cnt=cnt,
                usage=self.usage,
            )
            # 随机生成数据
            data_dict = self._generate_data_once(config_dict) # {chart_data, csv_file, background_imgs}
            input_dict.update(data_dict)
            # 画图脚本
            
            if config_dict['mode'] == "xkcd":
                with plt.xkcd():
                    draw_func_ret = self.chartdrawer(input_dict)
            elif config_dict['mode'] == "standard":
                draw_func_ret = self.chartdrawer(input_dict)

            # 如果返回值是None，代表成功生成了图表，否则保留setting重新生成图表
            # 不保留setting的话，图表的分布会不均匀
            if not draw_func_ret:
                return False # 返回False表示没失败
        
        print("尝试5次仍然失败，放弃本次图表生成")
        # print(f"本次的setting为:\n{self.config}")
        return True

    def generate(self, num, num_workers):
        """生成数据，callable

        Args:
            num (_type_): 生成的数目
            num_workers (_type_): 并行进程数
        """
        self._clearPath()
        sensetool.print_divider(f"Start Generate ({num_workers})")

        all_data_list = [i for i in range(num)]

        # random.set_seed(threading.current_thread().ident % int(2 ** 16))
        with ProcessPoolExecutor(max_workers = num_workers) as executor:
            pbar = tqdm(num, delay=1)
            for notseccess in executor.map(self._generateOneChart, all_data_list):
                if notseccess:
                    # 有可能因为中文字符画不出来，也有可能是数据标签有重合情况，需要重新生成
                    all_data_list.append(len(all_data_list))
                else:
                    pbar.update()
        pbar.close()

        json_file_names = os.listdir(os.path.join(self.data_root, "jsons"))
        # 自动生成结果文件名
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y%m%d")
        usage = self.usage
        optJsonlName = os.path.join(self.data_root, f"{self.chart_type}_{formatted_date}_{usage}.jsonl")

        f = open(optJsonlName, "w")
        for json_fn in json_file_names:
            with open(os.path.join(self.data_root, "jsons", json_fn)) as json_f:
                f.write(json_f.readline() + "\n")
        f.close()

        fulljson = os.path.join(os.getcwd(), optJsonlName)
        fullimage = os.path.join(os.getcwd(), self.data_root)
        sensetool.startView(fulljson, fullimage, self.data_root)

        pathOverView = {"root": fullimage,
                        "annotation": fulljson,
                        "data_augment": False,
                        "repeat_time": 1,
                        "length": num}
        
        
        self.checker.checkfiles(pathOverView)

    def savefiles(self, fig, cnt, prompt_path, csv_file, result, reject=None):
        """保存文件

        Args:
            fig : 图
            cnt : 当前图表ID
            prompt_path : 使用prompt的文件路径
            csv_file : 数据
            result : 模型输出 gt
            reject : 负样本 gt，用于DPO训练，str｜None
        """
        # 随机缩放图像
        buf = io.BytesIO()
        fig.savefig(buf, format='jpg')
        buf.seek(0)
        img = Image.open(buf)
        
        # 选择一个随机的缩放因子
        scale_factor = random.uniform(0.3, 1.2)
        original_size = img.size  # (width, height)
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        resized_img = img.resize(new_size, Image.Resampling.NEAREST)

        prompt = random.choice(sensetool.gettxt_list(prompt_path))

        save_json = {
            "image": f"images/{self.chart_type}_{cnt}.jpg",
            "height": new_size[1],
            "width": new_size[0],
            "conversations": [{"from": "human", "value": f"<image>\n{prompt}"}, 
                            {"from": "gpt", "value": f"{result}"}],
            "reject": reject,
            }

        image_save_path = os.path.join(self.data_root, f"images/{self.chart_type}_{cnt}.jpg")
        resized_img.save(image_save_path)
        buf.close()
        plt.close()
        
        json_save_path = os.path.join(self.data_root, f"jsons/{self.chart_type}_{cnt}.json")
        with open(json_save_path, "w") as f:
            json.dump(save_json, f, ensure_ascii=False)

        csv_save_path = os.path.join(self.data_root, f"csvs/{self.chart_type}_{cnt}.csv")
        csv_file.to_csv(csv_save_path, index=0)

    def savefiles_qa(self, fig, cnt, prompt_list, csv_file, result_list, reject=None):
        """保存文件

        Args:
            fig : 图
            cnt : 当前图表ID
            prompt_path : 使用prompt的文件路径
            csv_file : 数据
            result : 模型输出 gt
            reject : 负样本 gt，用于DPO训练，str｜None
        """
        # 随机缩放图像
        buf = io.BytesIO()
        fig.savefig(buf, format='jpg')
        buf.seek(0)
        img = Image.open(buf)
        
        # 选择一个随机的缩放因子
        scale_factor = random.uniform(0.3, 1.2)
        original_size = img.size  # (width, height)
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        resized_img = img.resize(new_size, Image.Resampling.NEAREST)

        conversations = []
        for i in range(len(prompt_list)):
            conversations.append({"from": "human", "value": f"<image>\n{prompt_list[i]}"})
            conversations.append({"from": "gpt", "value": f"{result_list[i]}"})

        save_json = {
            "image": f"images/{self.chart_type}_{cnt}.jpg",
            "height": new_size[1],
            "width": new_size[0],
            "conversations": conversations,
            "reject": reject,
            }

        image_save_path = os.path.join(self.data_root, f"images/{self.chart_type}_{cnt}.jpg")
        resized_img.save(image_save_path)
        buf.close()
        plt.close()
        
        json_save_path = os.path.join(self.data_root, f"jsons/{self.chart_type}_{cnt}.json")
        with open(json_save_path, "w") as f:
            json.dump(save_json, f, ensure_ascii=False)

        csv_save_path = os.path.join(self.data_root, f"csvs/{self.chart_type}_{cnt}.csv")
        csv_file.to_csv(csv_save_path, index=0)