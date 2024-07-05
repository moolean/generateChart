import math
import random

# 根据输入数字的数量级来确定四舍五入的范围。例如，24 四舍五入到 10 的倍数，345 四舍五入到 100 的倍数，8020 四舍五入到 1000 的倍数。
def round_down_to_nearest(number):

    negtive = False
    if number < 0:
        number = abs(number)
        negtive = True

    if number < 10:
        scale = 1
    else:
        scale = int(10 ** (len(str(int(number))) - 1) / 2)
    
    # Floor the number to the nearest scale
    if number < 1:
        number *= 100
        scale = 5
        rounded_number = round(number/scale) * scale
        rounded_number = round(rounded_number/100,2)
    else:
        rounded_number = round(number / scale) * scale

    if negtive:
        rounded_number = -rounded_number
    return rounded_number

def round_to_nearest_up(number):
    # Determine the scale for rounding based on the number of digits
    if number == 0:
        return 0
    negtive = False
    if number < 0:
        number = abs(number)
        negtive = True

    if number < 10:
        scale = 1
    else:
        scale = 10 ** (len(str(int(number))) - 1)
    
    # Round the number to the nearest scale
 
    if number < 1:
        if negtive:
            rounded_number = 0
        else:
            rounded_number = 1
    else:
        if negtive:

            rounded_number = -math.floor(number / scale) * scale
        else:
            rounded_number = round(number / scale) * scale
    return rounded_number

def round_to_nearest_down(number):
    # Determine the scale for rounding based on the number of digits
    if number == 0:
        return 0
    negtive = False
    if number < 0:
        number = abs(number)
        negtive = True

    if number < 10:
        scale = 1
    else:
        scale = 10 ** (len(str(int(number))) - 1)
    if number < 1:
        if negtive:
            rounded_number = 1
        else:
            rounded_number = 0
    else:
        # Round the number to the nearest scale
        if negtive:
            rounded_number = -round(number / scale) * scale

        else:
            rounded_number = math.floor(number / scale) * scale

    return rounded_number


def getRoundText(y_text, x_value):

    x_value_round = round_down_to_nearest(x_value)

    prompt_list = [
        "\"{}\"的数据大约为{}",
        "\"{}\"的数据大约接近{}",
        "\"{}\"的数据大约在{}左右",
        "\"{}\"在{}左右",
        "\"{}\"的值接近{}",
        "\"{}\"接近{}",
        "\"{}\"大约在{}",
        "\"{}\"是{}",
        "\"{}\"的值接近{}",
        "\"{}\"的值为{}",
    ]
    return random.choice(prompt_list).format(y_text, x_value_round)

def getCompareText(y_text, x_list, datarange, legends):
    # print("---------------")
    # print(x_list)
    # print("---------------")
    # print(legends)
    prompt_list = []
    gap = abs(max(x_list) - min(x_list))
    gapwhole = abs(datarange[1] - datarange[0])
    if gapwhole == 0:
        prompt_list.append("此类别数据数值一致")
    elif gap/ gapwhole > 0.5:
        largegap_prompt = [
            "此类别中，各类数据差异较为明显",
            "各类别数值差距明显",
            "在这一类别中，各种数据之间存在显著的差异",
            "这个类别内的数据类型有着明显的不同",
            "此类数据呈现出显著的差异化特征",
            "该类别中，数据各项之间差别较为明显",
            "在这个类别里，各种数据的差异性很突出",
            "这一类的数据差异性较为显著",
            "在这个类别下，各类数据显现出较大的差异",
            "此类别中的各类数据有着显著的不同",
            "该类别中的各种数据有着明显的差异"
        ]
        prompt_list.append(random.choice(largegap_prompt))
    elif gap/ gapwhole < 0.1:
        smallgap_prompt = [
            "此类別中，数值接近",
            "在这个类别中，数值相近",
            "这个类别中的各类数据数值相似",
            "在这个分类下，数值之间的差距不大",
            "此类别中的数值彼此接近",
            "该类别里的数值基本上相同",
            "这里的数值大体一致",
            "在此类别内，各数值相差无几",
            "该分类中数值相差不多",
            "在这个类别里，数值非常接近",
            "此类别数据的数值接近"
        ]
        prompt_list.append(random.choice(smallgap_prompt))
    
    prompt_list.append(f"“{legends[x_list.index(min(x_list))]}”的数据数值最低")
    prompt_list.append(f"“{legends[x_list.index(max(x_list))]}”的数据数值最高")

    return random.choice(prompt_list)

def modify_value(x):
        #修改dataframe中的值,变成百分数表示
        if type(x) != str:
            return '{:.0%}'.format(x)
        else:
            return x
def getmd(colorNames, csv_file, percentFormat=None, bar_vertical=True, ):
    opt_text_md = f"这是一张柱状图，共有{len(colorNames)}组数据，"
    if percentFormat:
        csv_file = csv_file.applymap(modify_value)
    # 保证输出表顺序和人顺序一样，由上到下由左到右
    if not bar_vertical:
        # 如果是纵排表，按行反转 DataFrame
        csv_file = csv_file.iloc[::-1].reset_index(drop=True)
    md = csv_file.to_markdown(index=False)

    for i in colorNames:
        opt_text_md += f"其中{i[0]}代表{i[1]}，"
    opt_text_md += f"该图对应的markdown格式如下：\n```markdown\n{md}\n```"

    return opt_text_md

def getlongcaption_bar(colorNames, csv_file, percentFormat=None, bar_vertical=True, ):

    opt_text_lc = f"这是一张柱状图，共有{len(colorNames)}组数据，"
    datarange = [round_to_nearest_down(csv_file.iloc[:, 1:].min().min()), round_to_nearest_up(csv_file.iloc[:, 1:].max().max())]
    opt_text_lc += "\n\n### 分析与描述：\n\n"
    if bar_vertical:
        opt_text_lc += f"- **Y轴**：Y轴代表数值尺度, 图中数据大体上范围从{datarange[0]}到{datarange[1]}\n"
        opt_text_lc += "- **X轴**：X轴代表不同的变量或类别,从左到右依次是：" 
        for value in csv_file.iloc[0:-1, 0]:
            opt_text_lc += value + " 、"
        opt_text_lc += csv_file.iloc[-1, 0] + " 。\n"
        opt_text_lc += "**颜色图例**：图表有一个图例，解释所用颜色与所代表的具体项：\n"
        for i in colorNames:
            opt_text_lc += f"- {i[0]}：{i[1]}\n"
    else:
        csv_file = csv_file.iloc[::-1].reset_index(drop=True)
        opt_text_lc += f"- **X轴**：X轴代表数值尺度, 范围从{datarange[0]}到{datarange[1]}\n"
        opt_text_lc += "- **Y轴**：Y轴代表不同的变量或类别,从上到下依次是：" 
        for value in csv_file.iloc[0:-1, 0]:
            opt_text_lc += value + " 、"
        opt_text_lc += csv_file.iloc[-1, 0] + " 。\n"
        opt_text_lc += "**颜色图例**：图表有一个图例，解释所用颜色与所代表的具体项：\n"
        for i in colorNames:
            opt_text_lc += f"- {i[0]}：{i[1]}\n"
        

    opt_text_lc += "\n### 数据分析\n\n"
    for i, row in csv_file.iterrows():
        
        y_text = row.iloc[0]
        datalist = row[1:].tolist()
        legendlist = csv_file.columns[1:].tolist()
    
        if len(datalist) == 1:
            opt_text_lc += f"{i+1}. **{y_text}**：{getRoundText(legendlist[0], datalist[0])}\n"
        else:
            opt_text_lc += f"{i+1}. **{y_text}**：{getCompareText(y_text, datalist, datarange, legendlist)}。其中，"
            for idx in range(len(datalist)):
                opt_text_lc +=f"{getRoundText(legendlist[idx], datalist[idx])}。"
            opt_text_lc += "\n"
   
    return opt_text_lc

