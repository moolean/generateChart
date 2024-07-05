import random
import numpy as np


def round_number(num, decimal_places):
        # 数据小数点位数控制
        if decimal_places == 0:
            return round(num)
        else:
            return round(num, decimal_places)
    
def generate_random_numbers(total_count, decimal_places, x_data_sign, range_min = -10000, range_max = 10000, max_ratio = 100, base_num=None):
    
    
    if base_num == None:
        numbers = [np.random.uniform(range_min, range_max)]
    else:
        numbers = [base_num]
    while len(numbers) < total_count:
        next_num = np.random.uniform(range_min, range_max)
        if all(abs(next_num) / max(abs(num), 1) <= max_ratio and abs(num) / max(abs(next_num), 1) <= max_ratio for num in numbers):
            numbers.append(next_num)
    
    if x_data_sign == "+":

        return [round_number(abs(num), decimal_places) for num in numbers] 
    elif x_data_sign == "-":
        return [round_number(-abs(num), decimal_places) for num in numbers]
    elif x_data_sign == "mixed":
        return [round_number(num, decimal_places) for num in numbers] 


def generate_multigroup_1d_data(config_dict, chart_data, csv_file):
    """
    柱状图，一维折线图:
    | legend_title                      | legend_list[0] | ...... | legend_list[data_group_num-1]            |
    | --------------------------------- | -------------- | ------ | ---------------------------------------- |
    | xticklabel_list[0]                | data[0][0]     | ...... | ......                                   |
    | ......                            | ......         | ...... | ......                                   |
    | xticklabel_list[xticklabel_num-1] | ......         | ...... | data[data_group_num-1][xticklabel_num-1] |
    """
    data_type = random.choice(["percentage", "10000","100", "percentage_sum1"]) 
    chart_data["data_type"] = data_type
    if data_type == "10000":
        num_min = random.randint(-10000, 0)
        num_max = random.randint(0, 10000)
    elif data_type == "100":
        num_min = random.randint(-100, 0)
        num_max = random.randint(0, 100)
    elif data_type == "percentage":
        num_min = random.uniform(0, 0.2)
        num_max = random.uniform(0.2, 1)
        config_dict['decimal_places'] = 2
        config_dict['x_data_sign'] = "+"
    elif data_type == "percentage_sum1":
        # 要求不同组在同一个x坐标点之和为0
        num_min = 1
        num_max = 10000
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
        #修改数据为百分比格式，同一xticker数据之和为1，用2位小数表示
        for i in range(len(chart_data["data"][0])):
            total = 0
            for j in range(len(chart_data["data"])):
                total += chart_data["data"][j][i]
            for j in range(len(chart_data["data"])):
                chart_data["data"][j][i] = round(chart_data["data"][j][i]/total, 2)
        for j in range(len(chart_data["data"])):
            csv_file[chart_data["legend_list"][j]] = chart_data["data"][j]

    csv_file.columns = [col_name if col_name != "" else '' for col_name in csv_file.columns]


def generate_multigroup_1d_mix_data(config_dict, chart_data, csv_file, csv_file2):
    """
    柱状图和一维折线图合并
    柱状图，一维折线图:
    | legend_title                      | legend_list[0] | ...... | legend_list[data_group_num-1]            |
    | --------------------------------- | -------------- | ------ | ---------------------------------------- |
    | xticklabel_list[0]                | data[0][0]     | ...... | ......                                   |
    | ......                            | ......         | ...... | ......                                   |
    | xticklabel_list[xticklabel_num-1] | ......         | ...... | data[data_group_num-1][xticklabel_num-1] |

    data_type: percentage, 10000, 100
    """
    data_type = random.choice(["percentage", "10000","100", "log"]) 
    chart_data["data_type"] = data_type
    if data_type == "10000":
        num_min = random.randint(-10000, 0)
        num_max = random.randint(0, 10000)
    elif data_type == "100":
        num_min = random.randint(-100, 0)
        num_max = random.randint(0, 100)
    elif data_type == "percentage":
        num_min = random.uniform(0, 0.2)
        num_max = random.uniform(0.2, 1)
        config_dict['decimal_places'] = 2
        config_dict['x_data_sign'] = "+"
    elif data_type == "log":
        num_min = random.randint(-10000, 0)
        num_max = random.randint(0, 10000)
    # 一组数据拆分成两个图
    split = int(config_dict['data_group_num']/2)

 
    csv_file[chart_data['legend_title']] = chart_data['xticklabel_list']
    csv_file2[chart_data['legend_title']] = chart_data['xticklabel_list']

    # 为每个legend生成一组数据
    for i in range(config_dict['data_group_num']):
        if i<split:
            chart_data["data"].append(generate_random_numbers(
                config_dict['xticklabel_num'], config_dict['decimal_places'], config_dict['x_data_sign'], range_min = num_min, range_max = num_max)
            )
            csv_file[chart_data["legend_list"][i]] = chart_data["data"][i]
        else:
            chart_data["data2"].append(generate_random_numbers(
                config_dict['xticklabel_num'], config_dict['decimal_places'], config_dict['x_data_sign'], range_min = num_min, range_max = num_max)
            )
            csv_file2[chart_data["legend_list"][i]] = chart_data["data2"][i-split]
    
    csv_file.columns = [col_name if col_name != "" else '' for col_name in csv_file.columns]
    csv_file2.columns = [col_name if col_name != "" else '' for col_name in csv_file2.columns]

def generate_singlegroup_1d_data(config_dict, chart_data, csv_file):
    """
    饼图:
    | x_label                           | y_label                   |
    | --------------------------------- | ------------------------- |
    | xticklabel_list[0]                | data[0][0]                |
    | ......                            | ......                    |
    | xticklabel_list[xticklabel_num-1] | data[0][xticklabel_num-1] |
    """
    
    # 饼图图表中没有直角坐标系的y轴，y_label为空字符串
    # 但是csv文件中可以有列名，例如占比，比例等
    chart_data["y_label"] = "" 


    chart_data["data"].append(generate_random_numbers(
        config_dict['xticklabel_num'], config_dict['decimal_places'], config_dict['x_data_sign'], range_min=random.randint(-10000,0), range_max=random.randint(0,10000))
    )
    
    if chart_data['x_label']:
        pie_label = chart_data['x_label']
    else:
        pie_label = "-"
    csv_file[pie_label] = chart_data['xticklabel_list']
    csv_file[chart_data["y_label"]] = chart_data["data"][0]
    
    csv_file.columns = [col_name if col_name != "" or col_name!="-" else ' ' for col_name in csv_file.columns]
  