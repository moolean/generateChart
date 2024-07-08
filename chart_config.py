from dataclasses import dataclass, field, asdict
import json

import random
import numpy as np

@dataclass
class ChartConfig:
    chart_type: str
    style_type_options: list = field(default_factory=lambda: [
        "Solarize_Light2",
    ])
    mode_options: list = field(default_factory=lambda: ["standard", "xkcd"])
    decimal_places_options: list = field(default_factory=lambda: [0, 1, 2, 3])
    x_data_sign_options: list = field(default_factory=lambda: ["+", "-", "mixed"])

    xticklabel_num_range: list = None # for 1d chart
    data_point_num_range: list = None # for 2d chart
    data_group_num_range: list = None

    generate_fx_data_options: list = field(default_factory=lambda: [False])
    correlation_options: list = field(default_factory=lambda: ["no_correlation"])
    fx_options: list = None

    need_data_label_options: list = True
    pie_autotext_type_options: list = None

    seed: int = None


    def get_option_once(self):
        if self.seed:
            random.seed(self.seed)
            np.random.seed(self.seed)

        style_type = random.choice(self.style_type_options)
        mode = random.choice(self.mode_options)
        decimal_places = random.choice(self.decimal_places_options)
        x_data_sign = random.choice(self.x_data_sign_options)
        need_data_label = True

        pie_autotext_type = None
        if need_data_label and any(_ in self.chart_type for _ in ["pie", "ring"]):
            pie_autotext_type = random.choice(self.pie_autotext_type_options)

        
        """
            对于一维图表，必须给x轴刻度标签数以及数据的组数（legend数量）
            对于二维图表，必须给总的数据点数
        """
        if self.xticklabel_num_range:
            xticklabel_num = random.randint(*self.xticklabel_num_range)
            data_group_num = random.randint(*self.data_group_num_range)
            data_point_num = xticklabel_num * data_group_num
        else:
            xticklabel_num = 0
            data_point_num = random.randint(*self.data_point_num_range)
            if self.data_group_num_range:
                data_group_num = random.randint(*self.data_group_num_range)
            else:
                data_group_num_candidates = [1]
                for group_num in range(2, 5):
                    if data_point_num % group_num == 0:
                        data_group_num_candidates.append(group_num)
                data_group_num = random.choice(data_group_num_candidates)

        correlation = random.choice(self.correlation_options)
        generate_fx_data = random.choice(self.generate_fx_data_options)
        fx = None
        if generate_fx_data:
            assert self.fx_options, f"当需要生成带函数关系的图表时，必须提供具体的fx选项"
            fx = random.choice(self.fx_options)

            if any(fx == _ for _ in ['sin', 'cos']): # 如果是sin和cos函数，点数得多一点才能看出来
                data_point_num *= 7
                data_group_num = 1 # sin/cos函数的情况下，data group取1比较合适，不然有点奇怪
                correlation = "no_correlation" # sin/cos函数的xy之间一定没有相关性
                need_data_label = False # 点数太多了，没法做ocr
                decimal_places = random.choice([1, 2]) # 函数关系为sin/cos的时候必须得有小数，y轴范围太小

            if any(fx == _ for _ in ["ln", "sqrt"]):
                x_data_sign = "+"
            
            if any(fx == _ for _ in ["kx^2"]): # 如果x_data不是mixed，看不出是二次函数
                x_data_sign = "mixed"
            
            if self.chart_type == "two_dim_line_chart": # 二维折线图，如果有好几个组，不容易看出函数是什么
                data_group_num = 1
        
        if not fx:
            correlation = "no_correlation"


        return dict(
            chart_type=self.chart_type,
            style_type=style_type,
            mode=mode,
            decimal_places=decimal_places,
            x_data_sign=x_data_sign,

            xticklabel_num=xticklabel_num,
            data_point_num=data_point_num,
            data_group_num=data_group_num,

            need_data_label=need_data_label,     # 是否需要每一个数据点的标签
            pie_autotext_type=pie_autotext_type, # 饼图显示的是百分比还是原始数据

            generate_fx_data=generate_fx_data,
            fx=fx,                               # xy之间的函数关系
            correlation=correlation,             # xy之间是正相关还是负相关
        )


    def to_jsonstr(self):
        return json.dumps(asdict(self))