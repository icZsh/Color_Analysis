#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
im = Image.open("/Users/zhushenghua/Downloads/下载 2.png")
im2 = Image.new("RGB",im.size,0)
count = 0
for y in range(im.size[1]):
    for x in range(im.size[0]):
        pix = im.getpixel((x,y))
        if(pix[0] < 100 and pix[1] < 100 and pix[2] < 100):
            count = count + 1
            im2.putpixel((x,y),(255,255,255))
print(count)
im2.show()