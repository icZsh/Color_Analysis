#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import colorsys
from PIL import Image
import collections
import numpy as np
import pymysql
from tqdm import tqdm
import requests
from io import BytesIO
import pandas as pd

def get_image(url):
    response=requests.get(url)
    image=Image.open(BytesIO(response.content))
    return image

def get_dominant_color(image):
#颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')
#生成缩略图，减少计算量，减小cpu压力
    image.thumbnail((200, 200))
    max_score = 0
    dominant_color = None
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过纯黑色
        if a == 0:
            continue
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        # 忽略高亮色
        if y > 0.9:
            continue
        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = np.array([r, g, b])
    return dominant_color

# def RGB_to_Hex(rgb):
#     color = '#'
#     for i in rgb:
#         num = int(i)
#         # 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
#         color += str(hex(num))[-2:].replace('x', '0').upper()
#     return color

# def new_image(color,outfile):
#     new_image = Image.new("RGB", (90, 35), color)
#     new_image.save(outfile)

def get_more_data_list(r_start,r_end, g_start,g_end,b_start,b_end):
    data_list = []
    step = 4
    for tmp_r in range(r_start,r_end,step):
        for tmp_g in range(g_start,g_end,step):
            for tmp_b in range(b_start,b_end,step):
                data_list.append(np.array([
                    tmp_r,tmp_g,tmp_b
                ]))
    return data_list

def getColorList():
    dict = collections.defaultdict(list)

    # 黑色
    dict['black'] = get_more_data_list(0, 41, 0, 36, 0, 33)

    # 灰色
    dict['gray'] = get_more_data_list(180, 220, 180, 220, 180, 220)

    # 白色
    dict['white'] = get_more_data_list(240, 255, 240, 255, 240, 255)

    # 红色
    dict['red'] = get_more_data_list(150, 255, 0, 75, 0, 75)

    # 粉色
    dict['pink'] = get_more_data_list(245, 255, 100, 200, 180, 210)

    # 肉色
    dict['pastel'] = get_more_data_list(240, 255, 220, 230, 175, 200)

    # 棕色
    dict['brown'] = get_more_data_list(135, 200, 50, 150, 0, 100)

    # 浅棕色
    # dict['light brown']=get_more_data_list(200,225,150,200,140,180)

    # 红色2
    # dict['red2'] = get_more_data_list(0,10,43,255,46,255)

    # 橙色
    dict['orange'] = get_more_data_list(235, 255, 140, 185, 0, 50)

    # 黄色
    dict['yellow'] = get_more_data_list(225, 255, 200, 255, 0, 50)

    # 绿色
    dict['green'] = get_more_data_list(0, 100, 128, 255, 0, 100)

    # 浅绿
    dict['light green'] = get_more_data_list(100, 150, 200, 250, 140, 180)

    # 青色
    dict['cyan'] = get_more_data_list(0, 50, 140, 200, 140, 200)

    # 蓝色
    dict['blue'] = get_more_data_list(0, 100, 0, 150, 200, 255)

    # 浅蓝色
    dict['light blue'] = get_more_data_list(135, 175, 220, 255, 220, 255)

    # 紫色
    dict['purple'] = get_more_data_list(128, 160, 0, 75, 130, 220)

    # 浅紫色
    dict['light purple'] = get_more_data_list(215, 235, 170, 200, 215, 235)

    return dict

def get_distance(p1,p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

def get_color(result):
    distance2 = np.sqrt(255 ** 2 + 255 ** 2 + 255 ** 2)
    color2 = ''
    color_dict = getColorList()
    for color in color_dict:
        for sub in range(len(color_dict[color])):
            distance = get_distance(result,color_dict[color][sub])
            if distance < distance2:
                distance2 = distance
                color2 = color
    return color2

if __name__ == '__main__':
    #连接到服务器
    conn = pymysql.connect(
        host='rm-uf66010lgas9h78138o.mysql.rds.aliyuncs.com',
        port=3306,
        user='deploy',
        password='Genetsis2019@',
        db='martiderm_db',
        charset='utf8mb4'
    )
    sql = "select * from wechat_article_list"
    cursor = conn.cursor()
    cursor.execute(sql)
    data_result = pd.read_sql(sql, conn)

    #获取测试数据集
    cover_image = data_result['cover']
    cover_image.to_list()
    test_image=cover_image[0:100]

    color_list=[]
    for url in tqdm(test_image):
        image=get_image(url)
        result=get_dominant_color(image)
        color=get_color(result)
        color_list.append(color)



