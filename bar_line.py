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
from adjustText import adjust_text

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

        chart_title, legend_title, x_label, y_label, x_unit, y_unit, xticklabel_list, legend_list, data, data2, datatype = (
            chart_data['chart_title'], chart_data['legend_title'], chart_data['x_label'], chart_data['y_label'],
            chart_data['x_unit'], chart_data['y_unit'], chart_data['xticklabel_list'],
            chart_data['legend_list'], chart_data['data'], chart_data['data2'], chart_data["data_type"]
        )
        

        utils.set_font()

        # 画图
        markers = ['.', 'o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']
        fillstyles = ['full']
        # cmap = mpl.colormaps['viridis']
        # colors = [cmap(i) for i in range(cmap.N)]
        colors, colorNames = utils.get_diff_color(len(data)+len(data2))
        alphas = [num / 10 for num in range(7, 11)]
        linestyles = ['-', '--', '-.', ':']
        linewidths = list(range(1, 3))

        # 各种字体的格式
        # vert_types = ["center", "top", "bottom", "baseline", "center_baseline"]
        # hori_types = ["center", "right", "left"]
        weights = ['ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black']
        sizes = range(8, 12, 1)
        styles = ["normal", "italic", "oblique"]
        variants = ["normal", "small-caps"]
        stretchs = ['ultra-condensed', 'extra-condensed', 'condensed', 'semi-condensed', 'normal', 'semi-expanded', 'expanded', 'extra-expanded', 'ultra-expanded']
        units = ["", "", "", "", "", "", "", "", "", ""]
        # 设置是否用百分比显示数据
        if datatype=="percentage" and random.random() < 0.5:
            percentFormat = True
        else:
            percentFormat = False
        # 根据xticklabel_list数量控制图长度
        fig_width = 5 + len(xticklabel_list) * 0.3 + len(data)*2
        fig = plt.figure(figsize=(fig_width, np.random.uniform(4, 6)), dpi=random.choice(range(240, 360)))
        unit = random.choice(units)

        title_text = plt.title(chart_title)
        if unit:
            y_label += f"(单位：{unit})"
        y_label_text = plt.ylabel(y_label)
        y_list = []
        
        height_range = max(max(group_data) for group_data in data) - min(min(group_data) for group_data in data)
        text_offset = height_range * 0.02  # 偏移量为权重范围的2%
        
        '''
        分别画每一组数据,画折线图
        '''
        for i, y_data in enumerate(data):
            line_idx = i
            marker = random.choice(markers)
            fillstyle = random.choice(fillstyles)
            color = colors[i]
            # colorNames.append([utils.rgba_to_ch(color), legend_list[i]])
            colorNames[i][1] = legend_list[i]
            alpha = random.choice(alphas)
            linestyle = random.choice(linestyles)
            linewidth = random.choice(linewidths)
            if random.random() < 0.2:
                if random.random() < 0.5:
                    y_data[0] = None
                    csv_file[legend_list[i]][0] = ''
                else:
                    y_data[-1] = None
                    csv_file[legend_list[i]][len(xticklabel_list)-1] = ''
                
            plt.plot(xticklabel_list, y_data, marker=marker, fillstyle=fillstyle, color=color, alpha=alpha, linestyle=linestyle, linewidth=linewidth, label=legend_list[i])


            color = random.choice(colors)

            # ha = random.choice(hori_types)
            # va = random.choice(vert_types)

            weight = random.choice(weights)
            stretch = random.choice(stretchs)
            size = random.choice(sizes)
            style = random.choice(styles)
            variant = random.choice(variants)

            for i, value in enumerate(y_data):
                if value:
                    if not percentFormat:
                        format = str(value)+unit
                    else:
                        format = '{:.0%}'.format(value)
                    text = plt.text(
                        xticklabel_list[i], value + text_offset, format,
                        ha='center', va='bottom',
                        color=color,
                        weight=weight, stretch=stretch, size=size, style=style, variant=variant
                        )
                    text.set_path_effects([]) # 避免plt.xkcd()的影响

                # y_list.append(text)

        '''
        分别画每一组数据,画柱状图
        '''

        # ax2 = ax1.twinx()
        barWidth = 0.2
        r1 = np.arange(len(xticklabel_list))
        hatchs =['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']

        for i, y_data2 in enumerate(data2):
        
            offset = (i - (len(data2) - 1) / 2) * barWidth  # 计算偏移量

            linewidth = random.choice(linewidths)
            color = colors[len(data)+i]
            colorNames[len(data)+i][1] = legend_list[len(data)+i]
            if random.random() < 0.1:
                hatch = random.choice(hatchs)
            else:
                hatch = None
            linestyle = random.choice(linestyles)
            alpha = random.choice(alphas)

            plt.bar(
                r1 + offset, y_data2, width=barWidth, 
                hatch=hatch, 
                color=color, 
                linewidth=linewidth,
                linestyle=linestyle, alpha=alpha, label=legend_list[len(data)+i]
                )

            weight = random.choice(weights)
            stretch = random.choice(stretchs)
            size = random.choice(sizes)
            style = random.choice(styles)
            variant = random.choice(variants)
            color = random.choice(colors)

            
            for index, value in enumerate(y_data2):
                if value:
                    if not percentFormat:
                        format = str(value)+unit
                    else:
                        format = '{:.0%}'.format(value)
                    tmp = plt.text(index + offset, value, format, 
                            ha='center', va='bottom',
                            weight=weight, stretch=stretch, size=size, style=style, variant=variant
                            )
                # y_text.append(tmp)

        # 随机设置xticker倾斜度
        # try:
        #     if random.random() < 0.1 or len(xticklabel_list)>12:
        #         plt.xticks(rotation = random.choice([num for num in range(40, 70)]))
        # except:
        #     print("11111")
        
        locs = [1, 2, 3, 4]
        loc = random.choice(locs)
        legend = plt.legend(title=legend_title, loc=loc, bbox_to_anchor=(1, 0, 0.3, 1))
        
        ax = plt.gca()
        # # 随机将横轴放在0的位置
        # if random.random() < 0.4:
        #     ax.spines['top'].set_visible(False)
        #     ax.spines['right'].set_visible(False)
        #     ax.axhline(y=0, color='black', linewidth=0.8)
        #     # 设置 x 轴的刻度标签在横轴附近
        #     ax.xaxis.set_ticks_position('bottom')

        #     # 调整 x 轴标签的位置
        #     ax.spines['bottom'].set_position(('data', 0))

        # log数据设置对应刻度
        if datatype == "log":
            ax.set_yscale('symlog')
        # 百分比数据设置对应刻度
        if percentFormat:
            ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
            # print("percent")
            # ax.set_yscale('logit')

        # 随机去掉上面和右边的表框   
        if random.randint(0, 1): 
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        
        with warnings.catch_warnings(record=True) as warning_list:
            plt.tight_layout()
            if warning_list:
                # for warning in warning_list:
                #     print(warning)
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
                # for warning in warning_list:
                #     print(warning)
                plt.close()
                return "error"

        #endregion ====== 画图 ======

        # 格式化最终输出，并保存  (每个种类的图格式不一，需要自行更改，**写在此处或新建文件不要更改原代码**)
        result = getmd(colorNames, csv_file, percentFormat)
        # opt_text_nonumber = getlongcaption_v2(colorNames, csv_file, percentFormat)

        self.savefiles(fig, cnt,"prompts/longcap_prompt.txt", csv_file, result)

        # print(result)
        

if __name__=="__main__":

    draw = bardrawer(chart_type = "bar_line", # 一定要使用规定的type名称
                    usage = "md", # 设置合成label的类别，md的输出为markdown格式
                    xticklabel_num_range = [5, 20], # 类别的随机范围，图合成时在5-20个类别中随机
                    data_group_num_range = [1, 5], # 图例的随机范围
                    x_data_sign_options = ["+"], # 
                    pie_autotext_type_options=["original_data", "percentage"],
                    )
    
    # 生成图，num为生成数量，num_workers为并行进程数
    draw(num = 100, num_workers = 20)
    
