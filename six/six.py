import math
from PIL import Image, ImageDraw

# 定义图像大小和背景色
width, height = 58, 58
background_color = (0, 0, 0, 0)  # 透明背景，RGBA格式

# 定义渐变色的起始颜色和终止颜色
color1 = (255, 0, 0, 255)  # 红色，不透明度为255
color2 = (0, 0, 255, 255)  # 蓝色，不透明度为255
color3 = (0, 255, 0, 255)  # 绿色，不透明度为255

# 生成100张多种颜色渐变的图像
for i in range(0, 100):
    # 计算当前图像的颜色
    if i < 50:
        t = i / 99  # 根据渐变步数计算插值参数
        current_color = tuple(int((1 - t) * c1 + t * c2) for c1, c2 in zip(color1, color2))
    if i >= 50:
        t = i / 99  # 根据渐变步数计算插值参数
        current_color = tuple(int((1 - t) * c2 + t * c3) for c2, c3 in zip(color2, color3))

    # 创建透明图像对象和绘图对象
    image = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 计算正六边形的顶点坐标
    center_x, center_y = width // 2, height // 2
    side_length = min(width, height) // 2 - 1  # 正六边形的边长，减1是为了避免边界溢出
    hexagon = []
    for j in range(6):
        angle = 2 * math.pi * j / 6  # 计算角度
        x = center_x + side_length * 0.866 * math.cos(angle)  # 0.866 为正六边形内切圆半径与边长之比
        y = center_y + side_length * 0.866 * math.sin(angle)
        hexagon.append((x, y))

    # 绘制正六边形
    draw.polygon(hexagon, fill=current_color)

    # 保存图像为PNG文件
    file_name = f"dixing{i*10}.png"
    image.save(file_name, 'PNG')
