import random
import warnings
from matplotlib import pyplot as plt
import numpy as np
from basedrawer import drawer, timer_decorator
import generateChart.utils.utils as utils
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
        return generate_singlegroup_1d_data(*args, **kwargs)
    
    # @timer_decorator
    def chartdrawer(self, input_dict):

        # 直接复制
        config_dict, chart_data, csv_file, background_imgs, data_root, cnt = (
            input_dict['config_dict'], input_dict['chart_data'],
            input_dict['csv_file'], input_dict['background_imgs'],
            input_dict['data_root'], input_dict['cnt']
        )

        chart_title, legend_title, x_label, y_label, x_unit, y_unit, xticklabel_list, legend_list, data = (
            chart_data['chart_title'], chart_data['legend_title'], chart_data['x_label'], chart_data['y_label'],
            chart_data['x_unit'], chart_data['y_unit'], chart_data['xticklabel_list'],
            chart_data['legend_list'], chart_data['data']
        )

        utils.set_font()

        explode = [0] * len(xticklabel_list)
        stratangles = list(range(360))
        shalows = [True, False]
        pct_decimal_places_options = [1,2,3]

        cmap = matplotlib.colormaps['viridis']
        # colors = [cmap(i) for i in range(cmap.N)]
        # color = [random.choice(colors) for _ in range(len(xticklabel_list))]
        color, colorNames = utils.get_diff_color(len(xticklabel_list))
        assert len(colorNames) >= len(xticklabel_list)
        for i in range(len(xticklabel_list)):
            colorNames[i][1] = xticklabel_list[i]
        #  = utils.generate_distinct_colors()
        #  = [[utils.rgba_to_ch(i), xticklabel_list[idx]] for idx,i in enumerate(color)]
        # 随机分离一块
        if random.randint(0, 4) == 0:
            idx = random.randint(0, len(xticklabel_list)-1)
            explode[idx] = 0.1
        stratangle = random.choice(stratangles)
        shalow = random.choice(shalows)
        pct_decimal_places = random.choice(pct_decimal_places_options)

        fig = plt.figure(figsize=(np.random.uniform(8, 10), np.random.uniform(4, 6)), dpi=random.choice(range(240, 360)))
        title_text = plt.title(chart_title)
        # 分三种类别：1.只有legend，扇形上不标 2. 只有扇形标，legend不标 3. 都有
        # 圆外围现实的类别标签按概率隐藏，但是不隐藏legend
        select_type = random.choice(['legend', 'title', 'all'])
        if select_type == 'legend':
            label_show = None
            showlegend = True
        elif select_type == 'title':
            label_show = xticklabel_list
            showlegend = False
        elif select_type == 'all':
            label_show = xticklabel_list
            showlegend = True


        pie_ret = plt.pie(
            data[0], labels=label_show,
            colors=color,
            autopct=f'%.{pct_decimal_places}f%%' if config_dict['need_data_label'] else None, 
            startangle=stratangle,    # 整体逆时针的旋转角度
            explode=explode,          # 每个wedge往外突出多少
            shadow=shalow,             # 是否有阴影，也可以传入一个字典控制阴影样式
            wedgeprops=dict(width=random.uniform(0.2, 0.6)) # 环形宽度是多少
        )
        
        wedges, texts = pie_ret[0], pie_ret[1]
        autotexts = pie_ret[2] if len(pie_ret) == 3 else None
        
        if config_dict['pie_autotext_type'] == "original_data":
            # 将百分比改回原有数字
            for i, autotext in enumerate(autotexts):
                autotext.set_text(str(data[0][i]))
        elif config_dict['pie_autotext_type'] == "percentage":
            csv_file[y_label] = [float(autotext.get_text()[:-1]) for autotext in autotexts]


        ax = plt.gca()
        locs = [1, 2, 3, 4] # 分别代表'upper right', 'upper left', 'lower left', 'lower right'
        loc = random.choice(locs)
        if showlegend:
            legend = ax.legend(
                wedges, xticklabel_list,
                title=x_label,
                loc=loc,                      # 图例的位置
                bbox_to_anchor=(1, 0, 0.3, 1) # 图例的坐标xywh，配合loc一起使用
            )
        
        with warnings.catch_warnings(record=True) as warning_list:
            plt.tight_layout()
            if warning_list:
                for warning in warning_list:
                    print(warning)
                plt.close()
                return "font error"
        
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
                return "font error"


        #endregion ====== 画图 ======

        # 格式化最终输出，并保存  (每个种类的图格式不一，需要自行更改，**写在此处或新建文件不要更改原代码**)
        result = getmd(colorNames, csv_file)
        # opt_text_nonumber = getlongcaption_v2(colorNames, csv_file, percentFormat)

        self.savefiles(fig, cnt,"prompts/longcap_prompt.txt", csv_file, result)

        # print(result)
        

if __name__=="__main__":

    draw = bardrawer(chart_type = "base_ring", # 一定要使用规定的type名称
                    usage = "md", # 设置合成label的类别，md的输出为markdown格式
                    xticklabel_num_range = [5, 20], # 类别的随机范围，图合成时在5-20个类别中随机
                    data_group_num_range = [1, 5], # 图例的随机范围
                    x_data_sign_options = ["+"], # 
                    pie_autotext_type_options=["original_data", "percentage"],
                    )
    
    # 生成图，num为生成数量，num_workers为并行进程数
    draw(num = 100, num_workers = 20)
    
