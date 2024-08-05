
from labelformats.utils import *


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
    splitsign = True
    for i in range(len(legendlist)):
        if datalist[i] > max_num:
            max_id = i
            max_num = datalist[i]

        if datalist[i] > threshold:
            if splitsign:
                opt.append([legendlist[i]])
            else:
                opt[-1].append(legendlist[i])
            splitsign = False
        else:
            splitsign = True
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
    for idx, valuelist in enumerate(opt):
        if len(valuelist) == 1:
            if valuelist[0] == legendlist[max_id]:
                continue
            text += valuelist[0] 
        else:
            text += f"从{valuelist[0]}到{valuelist[-1]}"
        if idx < len(opt)-1:
            if idx == len(opt)-2 and len(opt[-1]) == 1 and opt[-1][0] == legendlist[max_id]:
                # 防止下一个是最后一个值，正好还等于最小值导致轮空，多出一个顿号的情况
                continue
            text +=  "、"
    if text == "":
        return max_text
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
    splitsign = True
    for i in range(len(legendlist)):
        if datalist[i] < min_num:
            min_id = i
            min_num = datalist[i]
        if datalist[i] < threshold:
            if splitsign:
                opt.append([legendlist[i]])
            else:
                opt[-1].append(legendlist[i])
            splitsign = False
        else:
            splitsign = True

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

    for idx, valuelist in enumerate(opt):
        if len(valuelist) == 1:
            if valuelist[0] == legendlist[min_id]:
                continue
            text += valuelist[0] 
        else:
            text += f"从{valuelist[0]}到{valuelist[-1]}"
        if idx < len(opt)-1:
            if idx == len(opt)-2 and len(opt[-1]) == 1 and opt[-1][0] == legendlist[min_id]:
                # 防止下一个是最后一个值，正好还等于最小值导致轮空，多出一个顿号的情况
                continue
            text +=  "、"
    if text == "":
        return min_text
    
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
        

def getOvervViewText_legend(trend):
    if trend == "up":
        prompt = random.choice([
            "数据显示上升趋势。",
            "数据显示增长趋势。",
            "数据呈现增长态势。",
            "数据有上升的倾向。",
            "数据显示出上升的趋势。",
            "数据呈现出上升趋势。",
            "数据表现出上升趋势。",
            "数据呈上升态势。",
            "数据呈现出增长的趋势。",
            "数据显示出增长趋势。",
            "数据有增长的趋势。",
            "数据表现出增长的趋势。",
            "数据处于上升状态。",
            "数据在持续上升。",
            "数据呈现上升状态。",
            "数据显示上升态势。",
            "数据展现出上升的趋势。"
        ])
    elif trend == "down":
            prompt = random.choice([
            "数据呈下降趋势。",
            "数据显示下降的趋势。",
            "数据显示出下降的趋势。",
            "数据正在呈现下降趋势。",
            "数据呈现出下降的趋势。",
            "数据表明有下降趋势。",
            "数据显示出数据下降的趋势。",
            "数据呈现出下滑的趋势。",
            "数据表明下降趋势。",
            "数据的趋势是下降的。",
            "数据显现出下降的趋势。",
            "数据表现为下降趋势。",
            "数据表现出下降的趋势。",
            "数据趋势是下降的。",
            "数据展现出下降趋势。",
            "数据反映出下降的趋势。",
            "数据显示了下降的趋势。",
            "数据呈现下行趋势。",
            "数据反映了下降趋势。",
            "数据表明趋势在下降。"
        ])
    elif trend == "random_flat":
            prompt = random.choice([
            "数据走势平稳。",
            "数据走势保持平坦。",
            "数据保持平稳状态。",
            "数据走势平稳。",
            "数据走势平坦。",
            "数据走势没有波动，保持平稳。",
            "数据没有变化趋势，走势相当平坦。",
            "数据既无增长也无下降，走势平稳。",
            "数据趋势不变，保持平坦的走势。",
            "数据走势保持平稳。",
            "数据走势平稳。",
            "数据既无上升也无下降的趋势，走势平坦。",
            "数据走势平稳，没有上升或下降的趋势。",
            "数据走势平坦。",
            "数据走势平稳。",
            "数据既不呈现上升也不呈现下降，走势保持平稳。",
            "数据无升降趋势，走势保持平坦。",
            "数据走势平稳。",
            "数据没有上升或下降的动向，走势平坦。",
        ])
    elif trend == "random_fluctuate":
            prompt = random.choice([
            "数据波动剧烈。",
            "数据波动很大。",
            "数据波动幅度较大。",
            "数据波动很大。",
            "数据没有表现出增长或减少的趋势，且波动很明显。",
            "数据不呈现上升或下降的趋势，并且波动性强。",
            "数据波动巨大。",
            "数据波动性大。",
            "数据波动幅度较大。",
            "数据波动显著。",
            "数据波动显著。",
            "数据波动较大。",
            "数据波动幅度较大。",
            "数据没有趋势性变化，波动却很大。",
            "数据不呈现上升或下降的趋势，并且波动幅度大。",
            "数据没有明显的变化趋势，但波动很大。",
            "数据波动却很剧烈。",
            "数据波动显著。"
        ])
    elif trend == "up2down":
            prompt = random.choice([
                "数据走势先升后降。",
                "数据先升后降。",
                "数据趋势先增加再减少。",
                "数据先上升然后下降。",
                "数据曲线先上扬后下跌。",
                "数据变化先增后减。",
                "数据走向先涨后跌。",
                "数据先涨然后降。",
                "数据趋势先高后低。",
                "数据先上升后回落。",
                "数据趋势先上升然后下降。",
                "数据波动先涨后落。",
                "数据先攀升后回落。",
                "数据趋势先爬升后下降。",
                "数据先高涨然后回落。",
                "数据曲线先上升后跌落。",
                "数据变化先上涨然后下降。",
                "数据趋势先上扬后回落。",
                "数据走势先升高后回落。",
                "数据曲线先升然后降。"
        ])
    elif trend == "down2up":
            prompt = random.choice([
            "数据趋势先降后升。",
            "数据的变化趋势是先减少再增加。",
            "数据先下跌，然后回升。",
            "数据先下降，之后上扬。",
            "数据呈现出先减少后增多的趋势。",
            "数据走势先减后增。",
            "数据趋势表现为先下降再上升。",
            "数据先是下滑，然后反弹。",
            "数据先有下降，随后上升。",
            "数据变化显示出先下降再回升的模式。",
            "数据呈现出先下跌后上涨的趋势。",
            "数据变化先是下降，接着上升。",
            "数据表现为先减少，后增加。",
            "数据显示出先下降后增加的趋势。",
            "数据先降低，后升高。",
            "数据走势显示出先下降然后上升。",
            "数据先降，后升。",
            "数据趋势显示出先下滑然后回升。",
            "数据的变化模式是先下降后上升。",
            "数据显示出先减少，接着增长的趋势。"
        ])
    # elif trend == "periodic":
    #         prompt = random.choice([
    #         "数据呈现周期性变化",
    #         "数据具有周期性的趋势",
    #         "数据展示出周期性的模式",
    #         "数据呈现出周期性波动",
    #         "数据表现出周期性趋势",
    #         "数据具有周期性波动",
    #         "数据显示出周期性变化",
    #         "数据体现了周期性趋势",
    #         "数据呈现周期性特征",
    #         "数据展现出周期性变化",
    #         "数据有周期性的趋势",
    #         "数据显示周期性波动",
    #         "数据具有周期性的模式",
    #         "数据展现周期性趋势",
    #         "数据表现出周期性的特征",
    #         "数据呈现周期性模式",
    #         "数据显示出周期性特征",
    #         "数据具有周期性变化",
    #         "数据体现周期性变化",
    #         "数据展现出周期性波动"
    #     ])
    # elif trend == "none":
    #         prompt = random.choice([
    #         "数据没有明显的趋势或规律",
    #         "数据中看不出明显的趋势",
    #         "数据没有显示出显著的规律",
    #         "从数据中看不出特定的趋势",
    #         "数据没有呈现出明显的模式",
    #         "数据缺乏明显的趋势性",
    #         "数据中没有发现显著的规律",
    #         "数据没有显示出明确的趋势",
    #         "数据没有呈现出任何显著的规律",
    #         "从数据中无法看出明显的趋势",
    #         "数据中没有出现明显的模式",
    #         "数据没有展示出明显的趋势",
    #         "数据中没有显现出特定的规律",
    #         "从数据中看不出明确的趋势",
    #         "数据中未能表现出显著的趋势",
    #         "数据没有表现出任何明显的规律",
    #         "数据中没有显示出明确的模式",
    #         "数据没有显示出显著的趋势",
    #         "数据没有体现出明显的规律",
    #         "数据中未能看出显著的趋势"
        # ])
    else:
        raise ValueError
    return prompt


def modify_value(x):
    """
    修改dataframe中的值,变成百分数表示
    """
    if type(x) != str:
        return '{:.0%}'.format(x)
    else:
        return x
    
def getmd(colorNames, csv_file, percentFormat=None, bar_vertical=True, reverse_colume=False, ):
    opt_text_md = f"这是一张折线图，共有{len(colorNames)}组数据，"
    if percentFormat:
        csv_file = csv_file.map(modify_value)
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

def getmd_nonumber(colorNames, csv_file, percentFormat=None, bar_vertical=True, reverse_colume=False, ):
    opt_text_md = f"这是一张折线图，共有{len(colorNames)}组数据，"
    # 无数字输出nonumber的md，每个值要估算，第一列是xticker不能改
    csv_file.iloc[:, 1:] = csv_file.iloc[:, 1:].map(round_down_to_nearest)

    if percentFormat:
        csv_file = csv_file.map(modify_value)
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


def getlongcaption_line(data_trend, colorNames, csv_file, percentFormat=None, bar_vertical=True, y_visible=True):
    # print(csv_file)
    opt_text_lc = f"这是一张折线图，共有{len(colorNames)}组数据，图中没有给出明确数字，只能给出估计值和大概趋势。"
    datarange = [round_to_nearest_down(csv_file.iloc[:, 1:].min().min()), round_to_nearest_up(csv_file.iloc[:, 1:].max().max())]
    largeThresold = datarange[0] + (datarange[1] - datarange[0])*0.70
    smallThresold = datarange[0] + (datarange[1] - datarange[0])*0.30
    opt_text_lc += "\n\n### 分析与描述：\n\n"
    xlist = [i for i in csv_file.iloc[0:-1, 0]]
    
    # 图例分析

    # csv_file = csv_file.iloc[::-1].reset_index(drop=True)
    if y_visible:
        # 看得见y轴数字
        opt_text_lc += f"- **Y轴**：Y轴代表数值尺度, 范围大概从{datarange[0]}到{datarange[1]}\n"
    else:
        opt_text_lc += f"- **Y轴**：Y轴代表数值尺度, 没有写具体范围\n"
    opt_text_lc += "- **X轴**：X轴代表不同的变量或类别,从左到右依次是：" 
    for value in xlist:
        opt_text_lc += value + " 、"
    opt_text_lc += csv_file.iloc[-1, 0] + " 。\n"
    xlist.append(csv_file.iloc[-1, 0])
    # print(xlist)
    opt_text_lc += f"**颜色图例**：图表有{len(colorNames)}个图例：\n"
    for idx, i in enumerate(colorNames):
        datalist = [i for i in csv_file.iloc[:, idx+1]]
        overtext = getOvervViewText_legend(data_trend[idx])
        opt_text_lc += f"- {i[1]}：{i[0]}, {overtext}" 
        if overtext == "此图例数据数值完全一致。":
            continue
        # print(datalist)
        opt_text_lc += f"{getLargeOrSmallText(xlist, datalist, largeThresold, smallThresold)}"
        # print(opt_text_lc)
    # print(csv_file)
        
    # # 数据分析
    # if len(colorNames) == 1:
    #     return opt_text_lc
    
    # opt_text_lc += "\n### 数据分析\n\n"
    # for i, row in csv_file.iterrows():
        
    #     y_text = row.iloc[0]
    #     datalist = row[1:].tolist()
    #     legendlist = csv_file.columns[1:].tolist()

    #     opt_text_lc += f"{i+1}. **{y_text}**：{getOvervViewText_xticker(datalist, datarange)}。"
    #     opt_text_lc += f"{getLargeOrSmallText(legendlist, datalist, largeThresold, smallThresold)}"

   
    return opt_text_lc