# Color_Analysis

Please refer to the **color_analysis.py** as the final version for color recognition. The color recognition consiss of two parts: getting images' colors in RGB color formats and translating them to colors in words. After I obtain the RGB colors, I basically used a K-means-like alogrithm to calculate the distance between my input color(in RGB format) to the color map I've predefined. Whichever color in the color map the input color is the closet, we pick that color for the input color.
The result would be a RGB color and its corresponding name, e.g. (255,0 ,0) red
