import random
import warnings
from matplotlib import pyplot as plt
import numpy as np
from basedrawer import drawer, timer_decorator
from utils import utils
import os
import random
import warnings
import matplotlib, matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import sensetool
import matplotlib.ticker as mticker
from labelformats.base_bar_opt import *
from utils.datagenerater import *
import logging
import matplotlib.image as mpimg
from matplotlib.patches import ConnectionPatch
import pandas as pd
from matplotlib.colors import to_rgba


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
        其中pie统一表示为大图，bar表示为小图
        """
        # 设置字体
        utils.set_font() 
        # 获取颜色
        colors, colorNames = get_non_black_colors(len(data))
        # 设定单位
        unit = random.choice(self.units)

        #region ======== 画图 ========
        bar_vertical = 0
        bar_left = random.choice([1,0])
        
        if random.random()<0.25:
            is_percent_pie = True
            is_percent_bar = True
        elif random.random()<0.5:
            is_percent_pie = False
            is_percent_bar = True
        elif random.random()<0.75:
            is_percent_pie = True
            is_percent_bar = False
        else:
            is_percent_pie = False
            is_percent_bar = False

        percent = random.choice([random.uniform(100,10000),random.uniform(100,100000)])
        if not is_percent_bar:
            for i in range(1):
                for j in range(1,len(legend_list)):
                    data[j][i] = round(data[j][i]*percent, 1)
                    csv_file.loc[i, csv_file.columns[j+1]] = data[j][i]
        
        if not is_percent_pie:
            for i in range(len(xticklabel_list)):
                for j in range(1):
                    data[j][i] = round(data[j][i]*percent, 1)
                    csv_file.loc[i, csv_file.columns[j+1]] = data[j][i]
        
        # 为了生成柱状小图
        grid = plt.GridSpec(nrows=5, ncols=2, wspace=0.2, hspace=0.2)
        
        if bar_vertical:
            fig = plt.figure(figsize = (np.random.uniform(8, 11), np.random.uniform(5, 8)), dpi=random.choice(range(240, 360)))
        else:
            fig = plt.figure(figsize = (np.random.uniform(9, 12), np.random.uniform(4, 7)), dpi=random.choice(range(240, 360)))  

        if bar_left:
            ax1 = plt.subplot(grid[:, 1])      
            ax2 = plt.subplot(grid[1:4, 0])
        else:
            ax1 = plt.subplot(grid[:, 0])      
            ax2 = plt.subplot(grid[1:4, 1])  

        # # big bar parameters
        overall_ratios = data[0]
        overall_ratios_new = np.array(overall_ratios) / sum(overall_ratios)
        colors, colorNames = get_non_black_colors(len(overall_ratios))
        bottom = 1
        width = np.random.uniform(1, 3)
        index = random.choice(range(len(overall_ratios)))
        bc_list = []
        for j, (height_new, height, label) in enumerate(reversed([*zip(overall_ratios_new, overall_ratios, xticklabel_list)])):
            bottom -= height_new
            bc = ax1.bar(0, height_new, width, bottom=bottom, color=colors[j], label=label)
            if is_percent_pie:
                ax1.bar_label(bc, labels=[f"{height:.1%}"], label_type='center')
            else:
                ax1.bar_label(bc, labels=[f"{height:.1f}"], label_type='center')
            # ax2.bar_label(bc, labels=[f"{label}"], label_type='edge')
            
            # 使用annotate函数添加文字标签
            for rect in bc:
                height = rect.get_height()
                ax1.annotate(
                    label,  # 标签文本
                    xy=(rect.get_x() - rect.get_width(), rect.get_y() + height / 2),  # 标签的位置
                    xytext=(5, 0),  # 偏移位置
                    textcoords="offset points",  # 使用偏移位置
                    ha='left', va='center',  # 水平对齐和垂直对齐
                    fontsize=10, color='black'
                )

                if j == index:
                    if bar_left:
                        x_bar = rect.get_x()
                    else:
                        x_bar = rect.get_x()+rect.get_width()
                    y_bar = rect.get_y()
                    y_bar_2 = rect.get_y()+rect.get_height()
                    label_ax2 = label

            bc_list.append(bc)

        ax1.axis('off')
        ax1.set_xlim(- 2.5 * width, 2.5 * width)
        
       
        age_ratios = []
        age_labels = legend_list[1:]
        for bar_i in range(len(age_labels)):
            age_ratios.append(data[bar_i+1][0])
        if not bar_vertical:
            if bar_left:
                sorted_data = sorted(zip(age_ratios, age_labels), reverse=True)
                age_ratios, age_labels = zip(*sorted_data)
            else:
                sorted_data = sorted(zip(age_ratios, age_labels), reverse=False)
                age_ratios, age_labels = zip(*sorted_data)
        age_ratios_new = np.array(age_ratios) / sum(age_ratios)
        colors1, colorNames1 = get_non_black_colors(len(age_ratios))
        
        bottom = 1
        width = np.random.uniform(1, 3)

        needLabel = random.random()
        bc_list2 = []
        if bar_vertical:
        # Adding from the top matches the legend.
            for j, (height_new, height, label) in enumerate(reversed([*zip(age_ratios_new, age_ratios, age_labels)])):
                bottom -= height_new
                bc = ax2.bar(0, height_new, width, bottom=bottom, color=colors1[j], label=label)
                if is_percent_bar:
                    ax2.bar_label(bc, labels=[f"{height:.1%}"], label_type='center')
                else:
                    ax2.bar_label(bc, labels=[f"{height:.1f}"], label_type='center')
                # ax2.bar_label(bc, labels=[f"{label}"], label_type='edge')
                
                # 使用annotate函数添加文字标签
                if needLabel > 0.3:
                    for rect in bc:
                        height = rect.get_height()
                        ax2.annotate(
                            label,  # 标签文本
                            xy=(rect.get_x() + rect.get_width(), rect.get_y() + height / 2),  # 标签的位置
                            xytext=(5, 0),  # 偏移位置
                            textcoords="offset points",  # 使用偏移位置
                            ha='left', va='center',  # 水平对齐和垂直对齐
                            fontsize=10, color='black'
                        )
                
                for rect in bc:
                    if j == 0:
                        if bar_left:
                            rect_x = rect.get_x()+rect.get_width()
                        else:
                            rect_x = rect.get_x()
                bc_list2.append(bc)

        else:
            y_pos = range(len(age_ratios))  # X 轴位置
            spacing_factor = random.uniform(1.2,1.5)
            y_pos = [pos * spacing_factor for pos in y_pos]
            width_tmp = np.random.uniform(0.9, 1) 
            for j, (height_new, height, label) in enumerate(reversed([*zip(age_ratios_new, age_ratios, age_labels)])):
                bc = ax2.bar(y_pos[j]-width_tmp*0.5*len(age_ratios), height_new, width=width_tmp, color=colors1[j], label=label)
                # bc = ax2.bar(y_pos[j]+width_tmp, height_new, width=width_tmp, color=colors1[j], label=label)
                if is_percent_bar:
                    ax2.bar_label(bc, labels=[f"{height:.1%}"], label_type='center')
                else:
                    ax2.bar_label(bc, labels=[f"{height:.1f}"], label_type='center')
                ax2.bar_label(bc, labels=[f"{label}"], label_type='edge')

                for rect in bc:
                    if bar_left and j == len(age_ratios)-1:
                        rect_x = rect.get_x()+rect.get_width()
                    elif j==0:
                        rect_x = rect.get_x()
                bc_list2.append(bc)


        ax2.set_title(label_ax2)
        if bar_left:
            if needLabel < 0.7:
                if needLabel<0.35:
                    ax2.legend(bc_list2, age_labels[::-1], loc='center left', bbox_to_anchor=(-0.2, 0), fontsize='medium')
                else:
                    ax2.legend(bc_list2, age_labels[::-1], loc='center left', bbox_to_anchor=(-0.2, 1), fontsize='medium')
            elif needLabel > 0.9:
                ax1.legend(bc_list, xticklabel_list[::-1], loc='center right', bbox_to_anchor=(0, 0), fontsize='medium')
        else:
            if needLabel < 0.7:
                if needLabel<0.35:
                    ax2.legend(bc_list2, age_labels[::-1], loc='center right', bbox_to_anchor=(1.3, 0), fontsize='medium')
                else:
                    ax2.legend(bc_list2, age_labels[::-1], loc='center right', bbox_to_anchor=(1.3, 1), fontsize='medium')
            elif needLabel > 0.9:
                ax1.legend(bc_list, xticklabel_list[::-1], loc='center right', bbox_to_anchor=(0.2, 0), fontsize='medium')
        ax2.axis('off')
        ax2.set_xlim(- 2.5 * width, 2.5 * width)
        # ax2.set_ylim(0.9, 1)

        if bar_vertical:
            bar_height = sum(age_ratios_new)
        else:
            if bar_left:
                bar_height = age_ratios_new[0]
            else:
                bar_height = age_ratios_new[-1]
        # draw top connecting line 
        # if bar_left     
        con = ConnectionPatch(xyA=(rect_x , bar_height), coordsA=ax2.transData,
                            xyB=(x_bar, y_bar_2), coordsB=ax1.transData)
        con.set_color([0, 0, 0])
        linewidth = np.random.uniform(1, 5)
        con.set_linewidth(linewidth)
        ax2.add_artist(con)

        # draw bottom connecting line
        con = ConnectionPatch(xyA=(rect_x , 0), coordsA=ax2.transData,
                            xyB=(x_bar, y_bar), coordsB=ax1.transData)
        con.set_color([0, 0, 0])
        ax2.add_artist(con)
        con.set_linewidth(linewidth)

        plt.tight_layout()
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
        opt_text_md = getmd_bar(colorNames, colorNames1, csv_file, xticklabel_list[::-1], age_labels[::-1], label_ax2, is_percent_pie, is_percent_bar, bar_vertical, bar_left)
        # opt_text_nonumber = getlongcaption_bar(colorNames, csv_file, percentFormat, bar_vertical)

        if self.usage == "md":
            result = opt_text_md
        # elif self.usage == "nonumber":
        #     result = opt_text_nonumber
        self.savefiles(fig, cnt,"prompts/markdown_prompt.txt", csv_file, result)

        # print(result)

def getmd_bar(colorNames, colorNames1, csv_file, xticklabel_list, legend_list, label_ax2, is_percent_pie, is_percent_bar, bar_vertical, bar_left):
    opt_text_md = f"这是两张柱状图的组合，大柱状图共有{len(colorNames)}组数据，"
    pie = csv_file.iloc[:, :2].iloc[::-1]
    bar = csv_file.loc[:0,:].iloc[:, 2:]
    bar = pd.melt(bar,var_name='类别',value_name='百分比').iloc[::-1].reset_index(drop=True)
    if not bar_vertical:
        if bar_left:
            bar = bar.sort_values(by='百分比', ascending=True).reset_index(drop=True)
        else:
            bar = bar.sort_values(by='百分比', ascending=False).reset_index(drop=True)
    pie.columns = ['类别', '百分比']
    # if is_percent:
    #     bar = bar.map(modify_value)
    #     pie = pie.map(modify_value)
    if is_percent_pie:
        pie = pie.map(modify_value)
    if is_percent_bar:
        bar = bar.map(modify_value)
    md_pie = pie.to_markdown(index=False)
    md_bar = bar.to_markdown(index=False)
    # md = csv_file.to_markdown(index=False)

    for i in colorNames:
        opt_text_md += f"其中{i[0]}代表{xticklabel_list[i[1]]}，"
    opt_text_md += f"该图对应的markdown格式如下：\n```markdown\n{md_pie}\n```"
    opt_text_md += f"\n\n小柱状图表示的是大柱状图{label_ax2}区域的细分，共有{len(colorNames1)}组数据，"
    for i in colorNames1:
        opt_text_md += f"其中{i[0]}代表{legend_list[i[1]]}，"
    opt_text_md += f"该图对应的markdown格式如下：\n```markdown\n{md_bar}\n```"
    return opt_text_md

def modify_value(x):
        #修改dataframe中的值,变成百分数表示
        if type(x) != str:
            return '{:.1%}'.format(x)
        else:
            return x

def get_non_black_colors(n):
    while True:
        colors, colorNames = utils.get_diff_color(n)
        colors_rgba = [to_rgba(c) for c in colors]
        if not any(np.all(np.isclose(c, [0, 0, 0, 1])) for c in colors_rgba):
            return colors, colorNames
            
def generate_barofpie_1d_data(config_dict, chart_data, csv_file):
    """
    大柱状图，小柱状图:
    | legend_title                      | legend_list[0] | ...... | legend_list[data_group_num-1]            |
    | --------------------------------- | -------------- | ------ | ---------------------------------------- |
    | xticklabel_list[0]                | data[0][0]     | ...... | data[data_group_num-1][0]                |
    | ......                            |   ......       |  nan   |            nan                           |
    | xticklabel_list[xticklabel_num-1] |   ......       |        |                                          |
    第一列为pie的数据，第一行后面为bar的数据
    大柱状图选择最小值作为小柱状图的表示区域
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
        total_now = 0
        for j in range(len(chart_data["data"][0])):
            total += chart_data["data"][0][j]
        for j in range(len(chart_data["data"][0])):
            if j==len(chart_data["data"][0])-1:
                chart_data["data"][0][j] = 1-total_now
            else:
                chart_data["data"][0][j] = round(chart_data["data"][0][j]/total, 3)
                total_now += chart_data["data"][0][j]
            if chart_data["data"][0][j] < min:
                min = chart_data["data"][0][j]
                min_index = j
        csv_file[chart_data["legend_list"][0]] = chart_data["data"][0]
        chart_data["min_index"] = min_index

    if chart_data["data_type"] == "percentage_sum1":
        #修改数据为百分比格式，每行的数据之和也要为1，跳过第一列
        for i in range(len(chart_data["data"][0])):
            total = 0
            total_now = 0
            for j in range(1,len(chart_data["data"])):
                total += chart_data["data"][j][i]
            for j in range(1,len(chart_data["data"])):
                if j==len(chart_data["data"])-1:
                    chart_data["data"][j][i] = 1-total_now
                else:
                    chart_data["data"][j][i] = round(chart_data["data"][j][i]/total, 3)
                    total_now += chart_data["data"][j][i]
        for j in range(1,len(chart_data["data"])):
            csv_file.loc[0, chart_data["legend_list"][j]] = chart_data["data"][j][0]

    csv_file.columns = [col_name if col_name != "" else '' for col_name in csv_file.columns]
        

if __name__=="__main__":

    draw = bardrawer(chart_type = "bar_of_bar_horizontal", # 一定要使用规定的type名称
                    usage = "md", # 设置合成label的类别，md的输出为markdown格式
                    xticklabel_num_range = [2, 7], # 类别的随机范围，图合成时在5-20个类别中随机
                    data_group_num_range = [3, 6], # 图例的随机范围
                    x_data_sign_options = ["+"], 
                    )
    
    # 生成图，num为生成数量，num_workers为并行进程数
    draw(num = 100, num_workers = 5,)
    
