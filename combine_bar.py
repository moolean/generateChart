import random
import warnings
from matplotlib import pyplot as plt
import numpy as np
from basedrawer import drawer, timer_decorator
import utils
import os
import random
import warnings
import matplotlib, matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import sensetool
import matplotlib.ticker as mticker
from labelformats.base_bar_opt import *
from datagenerater import *
import logging
import matplotlib.image as mpimg


# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [Process: %(process)d]"
# )

class bardrawer(drawer):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # 基础设定，直接复制
        self.weights = ['ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black']
        self.sizes = ['small', 'medium', 'large']
        self.styles = ["normal", "italic", "oblique"]
        self.variants = ["normal", "small-caps"]
        self.stretchs = ['ultra-condensed', 'extra-condensed', 'condensed', 'semi-condensed', 'normal', 'semi-expanded', 'expanded', 'extra-expanded', 'ultra-expanded']
        self.hatchs =['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']
        self.linestyles = ['-', '--', '-.', ':', '']
        self.linewidths = list(range(1, 6))
        self.units = ["", "", "", "", "", "", "", "", "", ""]
        self.alphas =  [num / 10 for num in range(5, 11)]

    # @timer_decorator
    def datagenerater(self, *args, **kwargs):
        # 如需修改数据格式参考原代码datagenerater.py，新代码写在此处
        return generate_multigroup_1d_data(*args, **kwargs)
    
    # @timer_decorator
    def chartdrawer(self, input_dict):

        # 直接复制
        config_dict, chart_data, csv_file, background_imgs, data_root, cnt = (
            input_dict['config_dict'], input_dict['chart_data'],
            input_dict['csv_file'], input_dict['background_imgs'],
            input_dict['data_root'], input_dict['cnt']
        )

        chart_title, legend_title, x_label, y_label, x_unit, y_unit, xticklabel_list, legend_list, data, datatype = (
            chart_data['chart_title'], chart_data['legend_title'], chart_data['x_label'], chart_data['y_label'],
            chart_data['x_unit'], chart_data['y_unit'], chart_data['xticklabel_list'],
            chart_data['legend_list'], chart_data['data'], chart_data["data_type"]
        )

        utils.set_font()

        hatchs =['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']
        linestyles = ['-', '--', '-.', ':', '']
        linewidths = list(range(1, 6))
        # cmap = matplotlib.colormaps['viridis']
        # colors = [cmap(i) for i in range(cmap.N)]
        colors, colorNames = utils.get_diff_color(len(data))
        alphas =  [num / 10 for num in range(5, 11)]
        units = ["", "", "", "", "", "", "", "", "", ""]
        unit = random.choice(units)
        weights = ['ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black']
        sizes = ['small', 'medium', 'large']
        styles = ["normal", "italic", "oblique"]
        variants = ["normal", "small-caps"]
        stretchs = ['ultra-condensed', 'extra-condensed', 'condensed', 'semi-condensed', 'normal', 'semi-expanded', 'expanded', 'extra-expanded', 'ultra-expanded']
        bar_vertical = random.choice([1,0])
        barWidth = 0.3
        # 设置是否用百分比显示数据
        if datatype in ["percentage","percentage_sum1"] and random.random() < 0.5:
            percentFormat = True
        else:
            percentFormat = False
        # 根据xticklabel_list数量控制图长度
        fig_width = 5 + len(xticklabel_list) * 0.5
        fig_height = 6 + len(data) * 0.5
        if bar_vertical:
            fig = plt.figure(figsize=(fig_width, fig_height), dpi=random.choice(range(240, 360)))
        else:
            
            fig = plt.figure(figsize=(fig_height, fig_width), dpi=random.choice(range(240, 360)))
        title_text = plt.title(chart_title)

        y_text = []
    
        r1 = np.arange(len(xticklabel_list))

        if bar_vertical:
            plt.xticks(r1, xticklabel_list)
        
            # 随机设置xticker倾斜度
            if random.random() < 0.1 or len(xticklabel_list) > 8:
                plt.xticks(rotation = random.choice([num for num in range(40, 70)]))
            plt.yticks([])
        else:
            plt.yticks(r1, xticklabel_list)
            plt.xticks([])
        
        bottom_data = []
        bars = []
        for i, y_data in enumerate(data):
            offset = (i - (len(data) - 1) / 2) * barWidth  # 计算偏移量
            
            linewidth = random.choice(linewidths)
            color = colors[i]
            colorNames[i][1] = legend_list[i]
            if random.random() < 0.1:
                hatch = random.choice(hatchs)
            else:
                hatch = None
            linestyle = random.choice(linestyles)
            alpha = random.choice(alphas)
        
            if not bottom_data:
                bottom_data = [0 for _ in range(len(xticklabel_list))]
            else:
                bottom_data = [x + max(data[i-1])*1.2 for x in bottom_data]
            if bar_vertical:
                # 正常水平画表
                bars.append(plt.bar(
                    r1, y_data, 
                    bottom=bottom_data,
                    width=barWidth, 
                    hatch=hatch, 
                    color=color, 
                    linewidth=linewidth,
                    linestyle=linestyle, alpha=alpha, label=legend_list[i]
                    ))
            else:
                # y_data = list(reversed(y_data))
                # 纵向画表
                bars.append(plt.barh(
                    r1, y_data, 
                    left=bottom_data,
                    height=barWidth, 
                    hatch=hatch, 
                    color=color, 
                    linewidth=linewidth,
                    linestyle=linestyle, alpha=alpha, label=legend_list[i]
                    ))


            weight = random.choice(weights)
            stretch = random.choice(stretchs)
            size = random.choice(sizes)
            style = random.choice(styles)
            variant = random.choice(variants)
            color = random.choice(colors)
    
            
            for index, position in enumerate(bottom_data):
                position = position + y_data[index]
                if not percentFormat:
                    format = f"{y_data[index]} {unit}"
                else:
                    format = '{:.0%}'.format(y_data[index])
                
                if bar_vertical:
                    tmp = plt.text(index, position, format, 
                            ha='center', va='bottom',
                            weight=weight, stretch=stretch, size=size, style=style, variant=variant
                            )
                else:
                    tmp = plt.text(position, index, format, 
                        ha='left', va='center',
                        weight=weight, stretch=stretch, size=size, style=style, variant=variant
                        )
                y_text.append(tmp)

        r2 = []
        last = 0
        for i in range(len(data)):
            h = last + max(data[i])*1.2/2
            last += max(data[i])
            r2.append(h)
        if bar_vertical:
            plt.yticks(r2, legend_list)
        else:
            plt.xticks(r2, legend_list)

        ax = plt.gca()
        # x轴
        # 去掉上面和右边的表框   
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        with warnings.catch_warnings(record=True) as warning_list:
            plt.tight_layout()
            if warning_list:
                for warning in warning_list:
                    print(warning)
                plt.close()
                return "error"
        new_ax = plt.gcf().add_axes([0, 0, 1, 1])
        bg_img_path = random.choice(background_imgs)
        bg_img = mpimg.imread(bg_img_path)
        new_ax.imshow(bg_img, alpha=random.uniform(0.1, 0.2), aspect='auto')
        new_ax.axis('off')

        with warnings.catch_warnings(record=True) as warning_list:
            plt.draw()
            if warning_list:
                for warning in warning_list:
                    print(warning)
                plt.close()
                return "error"
        #endregion ====== 画图 ======

        # 格式化最终输出，并保存  (每个种类的图格式不一，需要自行更改，**写在此处或新建文件不要更改原代码**)
        opt_text_md = getmd(colorNames, csv_file, percentFormat, bar_vertical, reverse_colume=bar_vertical)
        opt_text_nonumber = getlongcaption_v2(colorNames, csv_file, percentFormat, bar_vertical)

        if self.usage == "md":
            result = opt_text_md
        elif self.usage == "nonumber":
            result = opt_text_nonumber
        self.savefiles(fig, cnt,"prompts/longcap_prompt.txt", csv_file, result)

        # print(result)
        

if __name__=="__main__":

    draw = bardrawer(chart_type = "combine_bar", # 一定要使用规定的type名称
                    usage = "md", # 设置合成label的类别，md的输出为markdown格式
                    xticklabel_num_range = [5, 20], # 类别的随机范围，图合成时在5-20个类别中随机
                    data_group_num_range = [1, 5], # 图例的随机范围
                    x_data_sign_options = ["+"], # 
                    pie_autotext_type_options=["original_data", "percentage"],
                    )
    
    # 生成图，num为生成数量，num_workers为并行进程数
    draw(num = 100, num_workers = 20)
    
