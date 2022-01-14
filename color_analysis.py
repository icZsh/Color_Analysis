#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import colorsys
from io import BytesIO
import pickle
import numpy as np
import requests as req
from PIL import Image
from os import path
import os
# get file parent path
current_path = path.dirname(__file__)
parent_path = os.path.dirname(current_path)

color_map = {
    'black':(0,41,0,36,0,33),
    'gray':(180,220,180,220,180,220),
    'white':(240,255,240,255,240,255),
    'red':(150,255,0,75,0,75),
    'pink':(245,255,100,200,180,210),
    'brown':(135,200,50,150,0,100),
    'orange':(235,255,140,185,0,50),
    'yellow':(225,255,200,255,0,50),
    'green':(0,100,128,255,0,100),
    'cyan':(0,50,140,200,140,200),
    'blue':(0,100,0,150,200,255),
    'light blue':(135,175,220,255,220,255),
    'light purple':(215,235,170,200,215,235),
    'light green':(100,150,200,250,140,180),
    'purple':(128,160,0,75,130,220),
    'pastel':(240,255,220,230,175,200),
}



def get_dominant_color(image):
    # convert image format
    image = image.convert('RGBA')
    # generate thumbnails
    image.thumbnail((200, 200))
    max_score = 0
    dominant_color = None
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # skip pure black
        if a == 0:
            continue
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        if y > 0.9:
            continue
        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    return dominant_color


def get_RGB(url):
    response = req.get(url)
    rgb=get_dominant_color(Image.open(BytesIO(response.content)))
    RGB_list=[]
    for i in range(3):
        RGB_list.append(rgb[i])

    RGB_array=np.array([RGB_list])
    return RGB_array

def RGB_to_Hex(rgb):
    color = '#'
    for i in rgb:
        num = int(i)
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return color


def get_more_data_list(r_start,r_end, g_start,g_end,b_start,b_end):
    data_list = []
    step = 4
    for tmp_r in range(r_start,r_end,step):
        for tmp_g in range(g_start,g_end,step):
            for tmp_b in range(b_start,b_end,step):
                data_list.append([tmp_r,tmp_g,tmp_b])
    return data_list



def getColorList(color_map):
    data_list = []
    color_data_list = []
    for key in color_map.keys():
        start_r, start_g, start_b, end_r, end_g, end_b = color_map[key]
        tmp_data = get_more_data_list(start_r, start_g, start_b, end_r, end_g, end_b)
        data_list.extend(tmp_data)
        color_data_list.extend([key for i in range(len(tmp_data))])
    return data_list,color_data_list



def get_distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))


def find_color(RGB_array, color_dict):
    #     color_dict = getColorList()
    distance2 = np.sqrt(255 ** 2 + 255 ** 2 + 255 ** 2)
    color2 = ''
    #     safe_distance = 15
    for color in color_dict:
        for sub in range(len(color_dict[color])):
            distance = get_distance(RGB_array, color_dict[color][sub])
            #             if distance <= safe_distance:
            #                 return color
            if distance < distance2:
                distance2 = distance
                color2 = color
    return color2


def load_color_pickle():
    with open(f"{current_path}/config/color.pickle", 'rb') as f:
        new_color_dict = pickle.load(f)
    return new_color_dict
