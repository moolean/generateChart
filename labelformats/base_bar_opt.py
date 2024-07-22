
from labelformats.utils import *
normal_prompt = [
    "这些数字没有明显的规律",
    "没有显著的模式可以在这些数值中找到",
    "这些数值似乎没有清晰的规律",
    "无法从这些数字中看出明显的规律",
    "数值中没有显现出任何规律性",
    "这些数字并不呈现出明显的规律",
    "在这些数值中看不到明显的模式",
    "这些数值没有表现出显著的规律",
    "没有发现这些数字有明显的规律",
    "无法在这些数值中识别出明确的规律",
]
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

def getOvervViewText_legend(x_list, datarange):
    # print("---------------")
    # print(x_list)
    # print("---------------")
    # print(legends)
    prompt = ""
    # print(datarange)
    gap = abs(max(x_list) - min(x_list))
    gapwhole = abs(datarange[1] - datarange[0])
    if gapwhole == 0:
        prompt += "此图例数据数值完全一致。"
        return prompt
    elif gap/ gapwhole > 0.5:
        largegap_prompt = [
            "此图例中，各类数据差异较为明显",
            "各类数值差距明显",
            "在这一图例中，各种数据之间存在显著的差异",
            "这个图例内的数据类型有着明显的不同",
            "此类数据呈现出显著的差异化特征",
            "该图例中，数据各项之间差别较为明显",
            "在这个图例里，各种数据的差异性很突出",
            "这一图例的数据差异性较为显著",
            "在这个图例下，各类数据显现出较大的差异",
            "此图例中的各类数据有着显著的不同",
            "该图例中的各种数据有着明显的差异"
        ]
        prompt += random.choice(largegap_prompt)
    elif gap / gapwhole < 0.15:
        smallgap_prompt = [
            "此图例中，数值接近",
            "在这个图例中，数值相近",
            "这个图例中的各类数据数值相似",
            "在这个图例下，数值之间的差距不大",
            "此图例中的数值彼此接近",
            "该图例里的数值基本上相同",
            "这里的数值大体一致",
            "在此图例内，各数值相差无几",
            "该图例中数值相差不多",
            "在这个图例里，数值非常接近",
            "此图例数据的数值接近"
        ]
        prompt += random.choice(smallgap_prompt)

        alllarge_prompt = [
            "各个类别在此图例都较大",
            "在各种类别中，这个图例都显得很突出。",
            "这一图例在不同类别里都很大",
            "各类别内的这个图例都非常显眼",
            "在各个分类中，这个图例都显得较大",
            "各个类别下的这一图例都显得较大",
            "这个图例在不同类别中都特别显眼",
            "在不同类别中，此图例都显得较大",
            "各种类别中的这个图例都非常突出",
            "在不同分类下，这个图例都显得较大",
                ]
        allsmall_prompt = [
           "此图例在不同类别中都较小",
            "图例在各种类别里都比较小",
            "这个图表的此图例在每个类别中都偏小",
            "各类别的此图例都显得相当小",
            "不同类别中的此图例都相对较小",
            "在各个类别中，这个图例都显得比较小",
            "这幅图的此图例在各类别之间都比较小",
            "此图例在不同的类别里都显得比较小",
            "每个类别里的此图例都很小",
            "此图例在所有的类别中都显得比较小",
        ]

        if min(x_list) > datarange[1] - gapwhole*0.25:
            prompt += "，" + random.choice(alllarge_prompt) 
        elif max(x_list) <  datarange[1] - gapwhole*0.75:
            prompt += "，" + random.choice(allsmall_prompt) 
    else:
        prompt += random.choice(normal_prompt)
    return prompt
        
def getOvervViewText_xticker(x_list, datarange):
    # print("---------------")
    # print(x_list)
    # print("---------------")
    # print(legends)
    prompt = ""
    # print(datarange)
    gap = abs(max(x_list) - min(x_list))
    gapwhole = abs(datarange[1] - datarange[0])
    if gapwhole == 0:
        prompt += "此类别数据数值完全一致"
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
        prompt += random.choice(largegap_prompt)
    elif gap / gapwhole < 0.15:
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
        prompt += random.choice(smallgap_prompt)

        alllarge_prompt = [
            "各个图例中的此类别都较大",
            "在各种图例中，这个类别显得很突出。",
            "这一类别在不同图例里都很大",
            "各图例都非常显眼",
            "在各个图例中，这个类别都显得较大",
            "各个图例下的这一类别都显得较大",
            "这个类别在不同图例中都特别显眼",
            "在不同图例中，此类别都显得较大",
            "各种图例中的这个类别都非常突出",
            "在不同图例下，这个类别都显得较大",
                ]
        allsmall_prompt = [
           "此类别在不同图例中都较小",
            "在各图例里都比较小",
            "这个图表的此类别在每个图例中都偏小",
            "各图例的此类别都显得相当小",
            "不同图例中的此类别都相对较小",
            "在各个图例中，这个类别都显得比较小",
            "这幅图的此图例在各图例之间都比较小",
            "此类别在不同的图例里都显得比较小",
            "每个图例里的此类别都很小",
            "此类别在所有的图例中都显得比较小",
        ]

        if min(x_list) > datarange[1] - gapwhole*0.25:
            prompt += "," + random.choice(alllarge_prompt) 
        elif max(x_list) <  datarange[1] - gapwhole*0.75:
            prompt += "," + random.choice(allsmall_prompt) 
    else:
        prompt += random.choice(normal_prompt)
    return prompt


def legendtext(xlist: list, nums: list):
    pass

def getlargest(legendlist, datalist, threshold):
    """获取最大值并输出prompt

    Args:
        legendlist (): 类别列表
        datalist (): 对应的数列表
        threshold (): 判断阈值，高于阈值输出
    """
    opt = []
    max_id = 0
    max_num = -10000000
    for i in range(len(legendlist)):
        if datalist[i] > max_num:
            max_id = i
            max_num = datalist[i]

        if datalist[i] > threshold:
            opt.append(legendlist[i])

    max_text = f"{legendlist[max_id]}在该类最高"

    text = ""
    prompt = [
        "其中{}较高",
        "{}的数值偏高",
        "{}的指标较高",
        "这里的{}数据较高",
        "{}的值比较高",
        "表中{}各项也属于高值",
        "{}的数值较高",
    ]
    if opt == [] or len(opt) == 1:
        return max_text
    opt.remove(legendlist[max_id])
    for value in opt[:-1]:
        text += value + " 、"
    text += opt[-1]

    return  max_text + "，" + random.choice(prompt).format(text)

def getsmallest(legendlist, datalist, threshold):
    """获取最大值并输出prompt

    Args:
        legendlist (): 类别列表
        datalist (): 对应的数列表
        threshold (): 判断阈值，高于阈值输出
    """
    opt = []
    min_id = 0
    min_num = 10000000
    for i in range(len(legendlist)):
        if datalist[i] < min_num:
            min_id = i
            min_num = datalist[i]
        if datalist[i] < threshold:
            opt.append(legendlist[i])

    min_text = f"{legendlist[min_id]}在该类最低"
    text = ""
    prompt = [
        "其中{}较低",
        "{}的数值偏小",
        "{}的指标较低",
        "这里的{}数据很低",
        "{}的值比较小",
        "表中{}各项属于低值",
        "{}的数值较低",
    ]
    if opt == [] or len(opt) == 1:
        return min_text
    
    opt.remove(legendlist[min_id])
    for value in opt[:-1]:
        text += value + " 、"
    text += opt[-1]
    
    return min_text + "，" + random.choice(prompt).format(text)

def getLargeOrSmallText(legendlist, datalist, largeThresold, smallThresold):
    gl = getlargest(legendlist, datalist, largeThresold)
    gs = getsmallest(legendlist, datalist, smallThresold)
    if gl != "":
        if gs != "":
            return f"{gl}，{gs}。\n"
        else:
            return f"{gl}。\n"
    else:
        if gs != "":
            return f"{gs}。\n"
        else:
            return f"\n"
        
def modify_value(x):
    """
    修改dataframe中的值,变成百分数表示
    """
    if type(x) != str:
        return '{:.0%}'.format(x)
    else:
        return x
    
def getmd(colorNames, csv_file, percentFormat=None, bar_vertical=True, reverse_colume=False, ):
    opt_text_md = f"这是一张柱状图，共有{len(colorNames)}组数据，"
    if percentFormat:
        csv_file = csv_file.applymap(modify_value)
    # 保证输出表顺序和人顺序一样，由上到下由左到右
    if not bar_vertical:
        # 如果是纵排表，按行反转 DataFrame
        csv_file = csv_file.iloc[::-1].reset_index(drop=True)
    if reverse_colume:
        csv_file = csv_file.iloc[:, 0:1].join(csv_file.iloc[:, -1:0:-1].reset_index(drop=True))
    md = csv_file.to_markdown(index=False)

    for i in colorNames:
        opt_text_md += f"其中{i[0]}代表{i[1]}，"
    opt_text_md += f"该图对应的markdown格式如下：\n```markdown\n{md}\n```"

    return opt_text_md

def getlongcaption(colorNames, csv_file, percentFormat=None, bar_vertical=True, *args, **kwargs):

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


def getlongcaption_v2(colorNames, csv_file, percentFormat=None, bar_vertical=True, ):

    opt_text_lc = f"这是一张柱状图，共有{len(colorNames)}组数据，"
    datarange = [round_to_nearest_down(csv_file.iloc[:, 1:].min().min()), round_to_nearest_up(csv_file.iloc[:, 1:].max().max())]
    largeThresold = datarange[0] + (datarange[1] - datarange[0])*0.65
    smallThresold = datarange[0] + (datarange[1] - datarange[0])*0.35
    opt_text_lc += "\n\n### 分析与描述：\n\n"
    

    # 图例分析

    if bar_vertical:
        xlist = [i for i in csv_file.iloc[0:-1, 0]]
        opt_text_lc += f"- **Y轴**：Y轴代表数值尺度, 图中数据大体上范围从{datarange[0]}到{datarange[1]}\n"
        opt_text_lc += "- **X轴**：X轴代表不同的变量或类别,从左到右依次是：" 
        
        for value in xlist:
            opt_text_lc += value + " 、"
        opt_text_lc += csv_file.iloc[-1, 0] + " 。\n"

        opt_text_lc += f"**颜色图例**：图表有{len(colorNames)}个图例：\n"
        for idx, i in enumerate(colorNames):
            datalist = [i for i in csv_file.iloc[0:-1, idx+1]]
            overtext = getOvervViewText_legend(datalist, datarange)
            opt_text_lc += f"- {i[1]}：{i[0]}, {overtext}。"
            if overtext == "此图例数据数值完全一致。":
                continue
            opt_text_lc += f"{getLargeOrSmallText(xlist, datalist, largeThresold, smallThresold)}"
    else:
        csv_file = csv_file.iloc[::-1].reset_index(drop=True)
        xlist = [i for i in csv_file.iloc[0:-1, 0]]
        opt_text_lc += f"- **X轴**：X轴代表数值尺度, 范围从{datarange[0]}到{datarange[1]}\n"
        opt_text_lc += "- **Y轴**：Y轴代表不同的变量或类别,从上到下依次是：" 

        for value in xlist:
            opt_text_lc += value + " 、"
        opt_text_lc += csv_file.iloc[-1, 0] + " 。\n"

        opt_text_lc += f"**颜色图例**：图表有{len(colorNames)}个图例：\n"
        for idx, i in enumerate(colorNames):
            datalist = [i for i in csv_file.iloc[0:-1, idx+1]]
            overtext = getOvervViewText_legend(datalist, datarange)
            opt_text_lc += f"- {i[1]}：{i[0]}, {overtext}。" 
            if overtext == "此图例数据数值完全一致。":
                continue
            opt_text_lc += f"{getLargeOrSmallText(xlist, datalist, largeThresold, smallThresold)}"
        
    # 数据分析
    if len(colorNames) == 1:
        return opt_text_lc
    
    opt_text_lc += "\n### 数据分析\n\n"
    for i, row in csv_file.iterrows():
        
        y_text = row.iloc[0]
        datalist = row[1:].tolist()
        legendlist = csv_file.columns[1:].tolist()

        opt_text_lc += f"{i+1}. **{y_text}**：{getOvervViewText_xticker(datalist, datarange)}。"
        opt_text_lc += f"{getLargeOrSmallText(legendlist, datalist, largeThresold, smallThresold)}"

   
    return opt_text_lc