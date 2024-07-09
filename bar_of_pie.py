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
from optformat import *
from datagenerater import *
import logging
import matplotlib.image as mpimg
from matplotlib.patches import ConnectionPatch
import pandas as pd


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
        # return generate_multigroup_1d_data(*args, **kwargs)
        return generate_barofpie_1d_data(*args, **kwargs)
        # return generate_singlegroup_1d_data(*args, **kwargs)
    
    # @timer_decorator
    def chartdrawer(self, input_dict):

        # 直接复制
        config_dict, chart_data, csv_file, background_imgs, data_root, cnt, usage = (
            input_dict['config_dict'], input_dict['chart_data'],
            input_dict['csv_file'], input_dict['background_imgs'],
            input_dict['data_root'], input_dict['cnt'],  input_dict['usage']
        )

        chart_title, legend_title, x_label, y_label, x_unit, y_unit, xticklabel_list, legend_list, data, datatype = (
            chart_data['chart_title'], chart_data['legend_title'], chart_data['x_label'], chart_data['y_label'],
            chart_data['x_unit'], chart_data['y_unit'], chart_data['xticklabel_list'],
            chart_data['legend_list'], chart_data['data'], chart_data["data_type"]
        )
        """
        csv_file 格式:
        | legend_title                      | legend_list[0] | ...... | legend_list[data_group_num-1]            |
        | --------------------------------- | -------------- | ------ | ---------------------------------------- |
        | xticklabel_list[0]                | data[0][0]     | ...... | data[0][data_group_num-1]                |
        | ......                            |   ......       |        |                                          |
        | xticklabel_list[xticklabel_num-1] |   ......       |        |                                          |
        第一列为pie的数据，第一行后面为bar的数据
        """
        # 设置字体
        utils.set_font() 
        # 获取颜色
        colors, colorNames = utils.get_diff_color(len(data))
        # 设定单位
        unit = random.choice(self.units)

        #region ======== 画图 ========
        bar_vertical = random.choice([1,0])
        barWidth = 0.2
        # 设置是否用百分比显示数据
        if datatype == "percentage" and random.random() < 0.5:
            percentFormat = True
        else:
            percentFormat = False

        weight = random.choice(self.weights)
        stretch = random.choice(self.stretchs)
        size = random.choice(self.sizes)
        style = random.choice(self.styles)
        variant = random.choice(self.variants)
        color = random.choice(colors)

        # make figure and assign axis objects
        # fig_width = 5 + len(xticklabel_list) * 0.3 + len(data)*2
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(np.random.uniform(7, 14), np.random.uniform(5, 10)), dpi=random.choice(range(240, 360)))
        fig.subplots_adjust(wspace=0)

        # pie chart parameters
        overall_ratios = data[0]
        # labels = ['Approve', 'Disapprove', 'Undecided']
        # explode = [0.1, 0, 0]
        explode = [0] * len(overall_ratios)
        explode[0] = 0.1
        # rotate so that first wedge is split by the x-axis
        angle = -180 * overall_ratios[0]
        colors, colorNames = utils.get_diff_color(len(overall_ratios))
        wedges, *_ = ax1.pie(overall_ratios, autopct='%1.1f%%', startangle=angle,
                            labels=xticklabel_list, explode=explode, colors=colors)

        # bar chart parameters
        # age_ratios = [.33, .54, .07, .06]
        # age_labels = ['Under 35', '35-49', '50-65', 'Over 65']
        age_ratios = []
        age_labels = legend_list[1:]
        for bar_i in range(len(age_labels)):
            age_ratios.append(data[bar_i+1][0])
        
        bottom = 1
        # width = .2
        width = random.choice(range(1,3))

        # Adding from the top matches the legend.
        for j, (height, label) in enumerate(reversed([*zip(age_ratios, age_labels)])):
            bottom -= height
            bc = ax2.bar(0, height, width, bottom=bottom, color=color, label=label,
                        alpha=min(0.1 + 0.25 * j, 1.0))
            ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')

        ax2.set_title(xticklabel_list[0])
        ax2.legend()
        ax2.axis('off')
        ax2.set_xlim(- 2.5 * width, 2.5 * width)

        # use ConnectionPatch to draw lines between the two plots
        theta1, theta2 = wedges[0].theta1, wedges[0].theta2
        center, r = wedges[0].center, wedges[0].r
        bar_height = sum(age_ratios)

        # draw top connecting line
        x = r * np.cos(np.pi / 180 * theta2) + center[0]
        y = r * np.sin(np.pi / 180 * theta2) + center[1]
        con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                            xyB=(x, y), coordsB=ax1.transData)
        con.set_color([0, 0, 0])
        con.set_linewidth(4)
        ax2.add_artist(con)

        # draw bottom connecting line
        x = r * np.cos(np.pi / 180 * theta1) + center[0]
        y = r * np.sin(np.pi / 180 * theta1) + center[1]
        con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                            xyB=(x, y), coordsB=ax1.transData)
        con.set_color([0, 0, 0])
        ax2.add_artist(con)
        con.set_linewidth(4)

        plt.show()

        with warnings.catch_warnings(record=True) as warning_list:
            # plt.tight_layout()
            if warning_list:
                for warning in warning_list:
                    print(warning)
                plt.close()
                return "error"
        # 设置背景图
        new_ax = plt.gcf().add_axes([0, 0, 1, 1])
        new_ax.imshow(mpimg.imread(random.choice(background_imgs)), alpha=random.uniform(0.1, 0.2), aspect='auto')
        new_ax.axis('off')

        with warnings.catch_warnings(record=True) as warning_list:
            plt.draw()
            if warning_list:
                for warning in warning_list:
                    print(warning)
                plt.close()
                return "error"
        #endregion ====== 画图 ======

        # 格式化最终输出，并保存  
        opt_text_md = getmd_bar(colorNames, csv_file, xticklabel_list, legend_list)
        opt_text_nonumber = getlongcaption_bar(colorNames, csv_file, percentFormat, bar_vertical)

        if self.usage == "md":
            result = opt_text_md
        elif self.usage == "nonumber":
            result = opt_text_nonumber
        self.savefiles(fig, cnt,"prompts/markdown_prompt.txt", csv_file, result)

        # print(result)

def getmd_bar(colorNames, csv_file, xticklabel_list, legend_list):
    opt_text_md = f"这是一张扇形图和柱状图的组合，共有{len(colorNames)}组数据，"
    csv_file = csv_file.map(modify_value)
    pie = csv_file.iloc[:, :2]
    bar = csv_file.loc[:0,:].iloc[:, 2:]
    bar = pd.melt(bar,var_name='类别',value_name='百分比').iloc[::-1]
    pie.columns = ['类别', '百分比']
    md_pie = pie.to_markdown(index=False)
    md_bar = bar.to_markdown(index=False)
    # md = csv_file.to_markdown(index=False)

    for i in colorNames:
        opt_text_md += f"其中{i[0]}代表{xticklabel_list[i[1]]}，"
    opt_text_md += f"该图对应的markdown格式如下：\n```markdown\n{md_pie}\n```"
    opt_text_md += f"\n\n柱状图表示的是扇形图{xticklabel_list[0]}区域的细分，"
    opt_text_md += f"该图对应的markdown格式如下：\n```markdown\n{md_bar}\n```"
    return opt_text_md

def generate_barofpie_1d_data(config_dict, chart_data, csv_file):
    """
    扇形图，柱状图:
    | legend_title                      | legend_list[0] | ...... | legend_list[data_group_num-1]            |
    | --------------------------------- | -------------- | ------ | ---------------------------------------- |
    | xticklabel_list[0]                | data[0][0]     | ...... | data[0][data_group_num-1]                |
    | ......                            |   ......       |  nan   |            nan                           |
    | xticklabel_list[xticklabel_num-1] |   ......       |        |                                          |
    第一列为pie的数据，第一行后面为bar的数据
    data[0][0]应该为第一列最小值
    """
    data_type = "percentage_sum1"
    chart_data["data_type"] = data_type
    if data_type == "percentage_sum1":
        # 要求不同组在同一个x坐标点之和为0
        num_min = 10
        num_max = 1000
        config_dict['decimal_places'] = 2
        config_dict['x_data_sign'] = "+"

    csv_file[chart_data['legend_title']] = chart_data['xticklabel_list']

     # 为每个legend生成一组数据
    for i in range(config_dict['data_group_num']):
        chart_data["data"].append(generate_random_numbers(
            config_dict['xticklabel_num'], config_dict['decimal_places'], config_dict['x_data_sign'],
            range_min=num_min, range_max=num_max)
        )
        csv_file[chart_data["legend_list"][i]] = chart_data["data"][i]

        
    if chart_data["data_type"] == "percentage_sum1":
        #修改数据为百分比格式，饼图的数据之和为1，即纵列，用2位小数表示
        # for i in range(len(chart_data["data"])):
        total = 0
        min = chart_data["data"][0][0]
        min_index = 0
        for j in range(len(chart_data["data"][0])):
            total += chart_data["data"][0][j]
        for j in range(len(chart_data["data"][0])):
            chart_data["data"][0][j] = round(chart_data["data"][0][j]/total, 2)
            if chart_data["data"][0][j] < min:
                min = chart_data["data"][0][j]
                min_index = j
        # 最小的放在data[0][0]
        tmp = chart_data["data"][0][0]
        chart_data["data"][0][0] = min
        chart_data["data"][0][j] = tmp
        # for j in range(len(chart_data["data"])):
        csv_file[chart_data["legend_list"][0]] = chart_data["data"][0]

    if chart_data["data_type"] == "percentage_sum1":
        #修改数据为百分比格式，每行的数据之和也要为1，跳过第一列
        for i in range(len(chart_data["data"][0])):
            total = 0
            for j in range(1,len(chart_data["data"])):
                total += chart_data["data"][j][i]
            for j in range(1,len(chart_data["data"])):
                chart_data["data"][j][i] = round(chart_data["data"][j][i]/total, 2)
        for j in range(len(chart_data["data"])):
            csv_file[chart_data["legend_list"][j]] = chart_data["data"][j]

    csv_file.columns = [col_name if col_name != "" else '' for col_name in csv_file.columns]
        

if __name__=="__main__":

    draw = bardrawer(chart_type = "bar_of_pie", # 一定要使用规定的type名称
                    usage = "md", # 设置合成label的类别，md的输出为markdown格式
                    xticklabel_num_range = [2, 8], # 类别的随机范围，图合成时在5-20个类别中随机
                    data_group_num_range = [3, 6], # 图例的随机范围
                    x_data_sign_options = ["+"], # 
                    pie_autotext_type_options=["original_data", "percentage"],
                    )
    
    # 生成图，num为生成数量，num_workers为并行进程数
    draw(num = 20, num_workers = 5,)
    
