import copy
import math
import random

import numpy as np

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

def modify_number_visually(number):
    
    """更改单个数字，可以是int,float或str，更改数字单个位数希望能与原数据更像

    Args:
        number (_type_): 原数字

    Returns:
        modified_number_str: 改后数字，不改变数据类型
    """
    if isinstance(number, (int, np.integer)):
        number_str = str(number)
    elif isinstance(number, (float, np.float64)):
        number_str = str(number)
    else:
        number_str = number

    if number_str.replace('.', '', 1).isdigit():  # 处理数字或浮点数字符串
        num_digits = len(number_str)
        
        # 随机选择一个位数进行修改
        digit_to_modify = np.random.randint(num_digits)
        
        # 确保修改后的数字与原数字不同
        new_digit = number_str[digit_to_modify]
        while new_digit == number_str[digit_to_modify]:
            if number_str[digit_to_modify] == '.':
                new_digit = '.'
                break
            else:
                new_digit = str(np.random.randint(0, 10))
        
        # 构造修改后的数字
        modified_number_str = (
            number_str[:digit_to_modify] + new_digit + number_str[digit_to_modify+1:]
        )
        
        # 保持原类型
        if isinstance(number, (float, np.float64)):
            return float(modified_number_str)
        elif isinstance(number, (int, np.integer)):
            return int(modified_number_str)
        else:
            return modified_number_str
    else:  # 处理包含汉字的字符串
        num_chars = len(number_str)
        
        # 随机选择一个字符进行修改
        char_to_modify = np.random.randint(num_chars)
        
        # 随机选择一个汉字
        new_char = number_str[char_to_modify]
        while new_char == number_str[char_to_modify]:
            new_char = chr(random.randint(0x4e00, 0x9fff))
        
        # 构造修改后的字符串
        modified_number_str = (
            number_str[:char_to_modify] + new_char + number_str[char_to_modify+1:]
        )
        
        return modified_number_str

def random_change_number(dataframe, p):
    """随机选dataframe中的数字进行更改，构造dpo的负样本数据

    Args:
        dataframe (numpy dataframe): 输出的gt数据
        p (_type_): 以一定的概率选择数字进行修改
    """
    # 
    df = copy.deepcopy(dataframe)
    # 遍历DataFrame中的每一个元素，根据概率进行修改
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if np.random.rand() < p:
                df.iat[i, j] = modify_number_visually(df.iat[i, j])
    return df