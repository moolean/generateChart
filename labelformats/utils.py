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