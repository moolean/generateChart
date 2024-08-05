import argparse
import random
import warnings
from matplotlib import pyplot as plt
import numpy as np
from basedrawer import drawer, timer_decorator
import utils.utils as utils
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
        | xticklabel_list[0]                | data[0][0]     | ...... | ......                                   |
        | ......                            | ......         | ...... | ......                                   |
        | xticklabel_list[xticklabel_num-1] | ......         | ...... | data[data_group_num-1][xticklabel_num-1] |

        datatype 为数据的范围或格式，在datagenerater中定义，保持数据生成格式和展示格式的同步
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
        # 根据xticklabel_list数量控制图长度
        if bar_vertical:
            fig_width = 5 + len(xticklabel_list) * 0.3 + len(data)*2
            fig = plt.figure(figsize=(fig_width, np.random.uniform(8, 10)), dpi=random.choice(range(240, 360)))
        else:
            fig_width = 5 + len(xticklabel_list) * 0.3 + len(data)*2
            fig = plt.figure(figsize=(np.random.uniform(8, 10), fig_width), dpi=random.choice(range(240, 360)))
        title_text = plt.title(chart_title)

        if unit:
            y_label += f"(单位：{unit})"
        y_label_text = plt.ylabel(y_label)
        y_text = []
        
        r1 = np.arange(len(xticklabel_list))
        
        if bar_vertical:
            plt.xticks(r1, xticklabel_list)
            # 随机设置xticker倾斜度
            if random.random() < 0.1 or len(xticklabel_list) > 8:
                plt.xticks(rotation = random.choice([num for num in range(40, 70)]))
            # 随机隐藏y轴
            if random.random() < 0.1 and "nonumber" not in usage:
                plt.yticks([])
        else:
            plt.yticks(r1, xticklabel_list)
            # 随机隐藏x轴
            if random.random() < 0.1 and "nonumber" not in usage:
                plt.xticks([])
        
        for i, y_data in enumerate(data):
            offset = (i - (len(data) - 1) / 2) * barWidth  # 计算偏移量
            
            linewidth = random.choice(self.linewidths)
            color = colors[i]
            colorNames[i][1] = legend_list[i]
            if random.random() < 0.1:
                hatch = random.choice(self.hatchs)
            else:
                hatch = None
            linestyle = random.choice(self.linestyles)
            alpha = random.choice(self.alphas)
        
            if bar_vertical:
                # 正常水平画表
                plt.bar(
                    r1 + offset, data[i], width=barWidth, 
                    hatch=hatch, 
                    color=color, 
                    linewidth=linewidth,
                    linestyle=linestyle, alpha=alpha, label=legend_list[i]
                    )
            else:
                # 纵向画表
                plt.barh(
                    r1 + offset, data[i], height=barWidth, 
                    hatch=hatch, 
                    color=color, 
                    linewidth=linewidth,
                    linestyle=linestyle, alpha=alpha, label=legend_list[i]
                    )

            weight = random.choice(self.weights)
            stretch = random.choice(self.stretchs)
            size = random.choice(self.sizes)
            style = random.choice(self.styles)
            variant = random.choice(self.variants)
            color = random.choice(colors)
    
            if "nonumber" not in usage:
                for index, value in enumerate(y_data):
                    if not percentFormat:
                        format = str(value)+unit
                    else:
                        format = '{:.0%}'.format(value)

                    if bar_vertical:
                        tmp = plt.text(index + offset, value, format, 
                                ha='center', va='bottom',
                                weight=weight, stretch=stretch, size=size, style=style, variant=variant
                                )
                    else:
                        tmp = plt.text(value, index + offset, format, 
                            ha='left', va='center',
                            weight=weight, stretch=stretch, size=size, style=style, variant=variant
                            )
                    y_text.append(tmp)
                
        locs = [1, 2, 3, 4]
        loc = random.choice(locs)
        # , bbox_to_anchor=(1, 0, 0.3, 1)
        legend = plt.legend(title=legend_title, loc=0)

        ax = plt.gca()
        # x轴
        # 随机去掉上面和右边的表框   
        if random.randint(0, 1): 
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        if datatype == "log":
            if bar_vertical:
                ax.set_yscale('symlog')
            else:
                ax.set_xscale('symlog')

        # 百分比数据设置对应刻度
        if percentFormat:
            if bar_vertical:
                ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
            else:
                ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))

        with warnings.catch_warnings(record=True) as warning_list:
            # plt.tight_layout()
            if warning_list:
                for warning in warning_list:
                    print(warning)
                plt.close()
                return "error"
            
        # 设置背景图
        new_ax = plt.gcf().add_axes([0, 0, 1, 1])
        bg_img_path = random.choice(background_imgs)
        bg_img = mpimg.imread(bg_img_path)
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
        
        """ 
        格式化最终输出，并保存  (每个种类的图格式不一，需要自行更改，** 写在此处或在labelformats/新建文件 不要更改原代码 **)
        每个图需要四种数据：
        usage: Literal["md", "lp", "nonumber_lp","nonumber_md", "desc_qa", "reasoning_qa"]
            有数字图：
                1. 直接转markdown （模型默认行为）
                2. longcaption描述 （目前不需要）
                3. 描述性QA
                4. 推理性QA （pending）
            无数字图：
                1. longcaption描述 （模型默认行为）
                2. 估计其中数字转markdown
                3. 描述性QA
                4. 推理性QA（pending）
        prompt 自行选择
            默认使用无md的提问，
            对应无数字强行估计md时使用带md的提问
        """
        
        if "qa" in self.usage:
            # 多轮qa 数据
            prompt_list, result_list = get_qa(colorNames, csv_file, percentFormat, bar_vertical)
            prompt = "prompts/markdown_prompt.txt"
            reject = None # 为了dpo准备的负例，暂不需要
            self.savefiles_qa(fig, cnt, prompt_list, csv_file, result_list, reject=reject)
        
        else:
            prompt = "prompts/longcap_detail_prompt.txt"
            reject = None
            if self.usage == "md":
                # 转md
                result = getmd(colorNames, csv_file, percentFormat, bar_vertical)
                # reject = getmd_reject(colorNames, csv_file, 0.2,percentFormat, bar_vertical)
            elif self.usage == "nonumber_lp":
                # 无数字longcaption
                result = getlongcaption_v2(colorNames, csv_file, percentFormat, bar_vertical)
            elif self.usage == "nonumber_md":
                # 无数字转估计md
                result = getmd_nonumber(colorNames, csv_file, percentFormat, bar_vertical)
                prompt = "prompts/markdown_prompt.txt"
    
            self.savefiles(fig, cnt, prompt, csv_file, result, reject=reject)

        # print(result)
        

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="This is a description of the program.")

    parser.add_argument("--num", type=int, default=100, help="生成的数量，测试时默认生成100个看效果，大批量生成时直接写在代码中生成100k不需要管")
    parser.add_argument("--workers", type=int, default=10, help="并行数，测试时默认10进程并行，大批量生成时m集群8卡有112个核使用112个进程跑，写在代码中不需要更改")

    args = parser.parse_args()

    draw = bardrawer(chart_type = "base_bar", # 一定要使用规定的type名称
                    usage = "md", # 设置合成label的类别，md的输出为markdown格式
                    xticklabel_num_range = [5, 20], # 类别的随机范围，图合成时在5-20个类别中随机
                    data_group_num_range = [1, 5], # 图例的随机范围
                    x_data_sign_options = ["mixed"], # 生成数据的正负，( + | - | mixed )
                    )
    
    # 生成图，num为生成数量，num_workers为并行进程数
    draw(num = args.num, num_workers = args.workers)
    
