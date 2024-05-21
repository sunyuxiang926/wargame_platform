import math
from PIL import Image, ImageDraw

# 定义图像大小和背景色
width, height = 58, 58
background_color = (0, 0, 0, 0)  # 透明背景，RGBA格式

# 计算渐变色的起始颜色和终止颜色
start_color0 = (173, 216, 230, 255) # 淡蓝色
end_color0 = (245, 245, 220, 255) # 米色

start_color1 = end_color0
end_color1 = (184, 134, 11, 255) # 土黄色

start_color2 = end_color1
end_color2 = (144, 238, 144, 255) # 浅绿色

start_color3 = end_color2
end_color3 = (0, 100, 0, 255) # 深绿色

start_color4 = end_color3
end_color4 = (255, 255, 153, 255) # 深黄色
# (255, 255, 153, 255)

start_color5 = end_color4
end_color5 = (255, 165, 0, 255) # 橙色

start_color6 = end_color5
end_color6 = (255, 0, 0, 255) # 红色

start_color7 = end_color6
end_color7 = (128, 0, 128, 255) # 紫色

start_color8 = end_color7
end_color8 = (0, 0, 128, 255) # 深蓝色

start_color9 = end_color8
end_color9 = (173, 216, 230, 255) # 青色


offset = 4000

# 计算渐变步长
step = 1
num = 10
# 生成num张渐变色图像
for i in range(0, num, step):
    # 计算当前图像的颜色
    current_color = tuple(int(start + (end - start) * i / num) for start, end in zip(start_color0, end_color0))

    # 创建透明图像对象和绘图对象
    image = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 计算正六边形的顶点坐标
    center_x, center_y = width // 2, height // 2
    side_length = min(width, height) // 2 + 5 # 正六边形的边长，减1是为了避免边界溢出
    hexagon = []
    for j in range(6):
        angle = 2 * math.pi * j / 6  + math.radians(30)# 计算角度
        x = center_x + side_length * 0.866 * math.cos(angle)  # 0.866 为正六边形内切圆半径与边长之比
        y = center_y + side_length * 0.866 * math.sin(angle)
        hexagon.append((x, y))

    # 绘制正六边形
    draw.polygon(hexagon, fill=current_color)

    # 保存图像为PNG文件
    file_name = f"dixing{i*10 + offset}.png"
    image.save(file_name, 'PNG')

# 生成num张渐变色图像
for i in range(0, num, step):
    # 计算当前图像的颜色
    current_color = tuple(int(start + (end - start) * i / num) for start, end in zip(start_color1, end_color1))

    # 创建透明图像对象和绘图对象
    image = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 计算正六边形的顶点坐标
    center_x, center_y = width // 2, height // 2
    side_length = min(width, height) // 2 + 5 # 正六边形的边长，减1是为了避免边界溢出
    hexagon = []
    for j in range(6):
        angle = 2 * math.pi * j / 6 + math.radians(30)# 计算角度
        x = center_x + side_length * 0.866 * math.cos(angle)  # 0.866 为正六边形内切圆半径与边长之比
        y = center_y + side_length * 0.866 * math.sin(angle)
        hexagon.append((x, y))

    # 绘制正六边形
    draw.polygon(hexagon, fill=current_color)

    # 保存图像为PNG文件
    file_name = f"dixing{(i+num)*10 + offset}.png"
    image.save(file_name, 'PNG')

# 生成num张渐变色图像
for i in range(0, num, step):
    # 计算当前图像的颜色
    current_color = tuple(int(start + (end - start) * i / num) for start, end in zip(start_color2, end_color2))

    # 创建透明图像对象和绘图对象
    image = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 计算正六边形的顶点坐标
    center_x, center_y = width // 2, height // 2
    side_length = min(width, height) // 2 + 5 # 正六边形的边长，减1是为了避免边界溢出
    hexagon = []
    for j in range(6):
        angle = 2 * math.pi * j / 6 + math.radians(30)# 计算角度
        x = center_x + side_length * 0.866 * math.cos(angle)  # 0.866 为正六边形内切圆半径与边长之比
        y = center_y + side_length * 0.866 * math.sin(angle)
        hexagon.append((x, y))

    # 绘制正六边形
    draw.polygon(hexagon, fill=current_color)

    # 保存图像为PNG文件
    file_name = f"dixing{(i+num*2)*10 + offset}.png"
    image.save(file_name, 'PNG')

# 生成num张渐变色图像
for i in range(0, num, step):
    # 计算当前图像的颜色
    current_color = tuple(int(start + (end - start) * i / num) for start, end in zip(start_color3, end_color3))

    # 创建透明图像对象和绘图对象
    image = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 计算正六边形的顶点坐标
    center_x, center_y = width // 2, height // 2
    side_length = min(width, height) // 2 + 5 # 正六边形的边长，减1是为了避免边界溢出
    hexagon = []
    for j in range(6):
        angle = 2 * math.pi * j / 6 + math.radians(30)# 计算角度
        x = center_x + side_length * 0.866 * math.cos(angle)  # 0.866 为正六边形内切圆半径与边长之比
        y = center_y + side_length * 0.866 * math.sin(angle)
        hexagon.append((x, y))

    # 绘制正六边形
    draw.polygon(hexagon, fill=current_color)

    # 保存图像为PNG文件
    file_name = f"dixing{(i+num*3)*10 + offset}.png"
    image.save(file_name, 'PNG')

# 生成num张渐变色图像
for i in range(0, num, step):
    # 计算当前图像的颜色
    current_color = tuple(int(start + (end - start) * i / num) for start, end in zip(start_color4, end_color4))

    # 创建透明图像对象和绘图对象
    image = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 计算正六边形的顶点坐标
    center_x, center_y = width // 2, height // 2
    side_length = min(width, height) // 2 + 5 # 正六边形的边长，减1是为了避免边界溢出
    hexagon = []
    for j in range(6):
        angle = 2 * math.pi * j / 6 + math.radians(30)# 计算角度
        x = center_x + side_length * 0.866 * math.cos(angle)  # 0.866 为正六边形内切圆半径与边长之比
        y = center_y + side_length * 0.866 * math.sin(angle)
        hexagon.append((x, y))

    # 绘制正六边形
    draw.polygon(hexagon, fill=current_color)

    # 保存图像为PNG文件
    file_name = f"dixing{(i+num*4)*10 + offset}.png"
    image.save(file_name, 'PNG')

# 生成num张渐变色图像
for i in range(0, num, step):
    # 计算当前图像的颜色
    current_color = tuple(int(start + (end - start) * i / num) for start, end in zip(start_color5, end_color5))

    # 创建透明图像对象和绘图对象
    image = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 计算正六边形的顶点坐标
    center_x, center_y = width // 2, height // 2
    side_length = min(width, height) // 2 + 5 # 正六边形的边长，减1是为了避免边界溢出
    hexagon = []
    for j in range(6):
        angle = 2 * math.pi * j / 6 + math.radians(30)# 计算角度
        x = center_x + side_length * 0.866 * math.cos(angle)  # 0.866 为正六边形内切圆半径与边长之比
        y = center_y + side_length * 0.866 * math.sin(angle)
        hexagon.append((x, y))

    # 绘制正六边形
    draw.polygon(hexagon, fill=current_color)

    # 保存图像为PNG文件
    file_name = f"dixing{(i+num*5)*10 + offset}.png"
    image.save(file_name, 'PNG')

# 生成num张渐变色图像
for i in range(0, num, step):
    # 计算当前图像的颜色
    current_color = tuple(int(start + (end - start) * i / num) for start, end in zip(start_color6, end_color6))

    # 创建透明图像对象和绘图对象
    image = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 计算正六边形的顶点坐标
    center_x, center_y = width // 2, height // 2
    side_length = min(width, height) // 2 + 5 # 正六边形的边长，减1是为了避免边界溢出
    hexagon = []
    for j in range(6):
        angle = 2 * math.pi * j / 6 + math.radians(30)# 计算角度
        x = center_x + side_length * 0.866 * math.cos(angle)  # 0.866 为正六边形内切圆半径与边长之比
        y = center_y + side_length * 0.866 * math.sin(angle)
        hexagon.append((x, y))

    # 绘制正六边形
    draw.polygon(hexagon, fill=current_color)

    # 保存图像为PNG文件
    file_name = f"dixing{(i+num*6)*10 + offset}.png"
    image.save(file_name, 'PNG')

# 生成num张渐变色图像
for i in range(0, num, step):
    # 计算当前图像的颜色
    current_color = tuple(int(start + (end - start) * i / num) for start, end in zip(start_color7, end_color7))

    # 创建透明图像对象和绘图对象
    image = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 计算正六边形的顶点坐标
    center_x, center_y = width // 2, height // 2
    side_length = min(width, height) // 2 + 5 # 正六边形的边长，减1是为了避免边界溢出
    hexagon = []
    for j in range(6):
        angle = 2 * math.pi * j / 6 + math.radians(30)# 计算角度
        x = center_x + side_length * 0.866 * math.cos(angle)  # 0.866 为正六边形内切圆半径与边长之比
        y = center_y + side_length * 0.866 * math.sin(angle)
        hexagon.append((x, y))

    # 绘制正六边形
    draw.polygon(hexagon, fill=current_color)

    # 保存图像为PNG文件
    file_name = f"dixing{(i+num*7)*10 + offset}.png"
    image.save(file_name, 'PNG')

# 生成num张渐变色图像
for i in range(0, num, step):
    # 计算当前图像的颜色
    current_color = tuple(int(start + (end - start) * i / num) for start, end in zip(start_color8, end_color8))

    # 创建透明图像对象和绘图对象
    image = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 计算正六边形的顶点坐标
    center_x, center_y = width // 2, height // 2
    side_length = min(width, height) // 2 + 5 # 正六边形的边长，减1是为了避免边界溢出
    hexagon = []
    for j in range(6):
        angle = 2 * math.pi * j / 6 + math.radians(30)# 计算角度
        x = center_x + side_length * 0.866 * math.cos(angle)  # 0.866 为正六边形内切圆半径与边长之比
        y = center_y + side_length * 0.866 * math.sin(angle)
        hexagon.append((x, y))

    # 绘制正六边形
    draw.polygon(hexagon, fill=current_color)

    # 保存图像为PNG文件
    file_name = f"dixing{(i+num*8)*10 + offset}.png"
    image.save(file_name, 'PNG')

# 生成num张渐变色图像
for i in range(0, num, step):
    # 计算当前图像的颜色
    current_color = tuple(int(start + (end - start) * i / num) for start, end in zip(start_color9, end_color9))

    # 创建透明图像对象和绘图对象
    image = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 计算正六边形的顶点坐标
    center_x, center_y = width // 2, height // 2
    side_length = min(width, height) // 2 + 5 # 正六边形的边长，减1是为了避免边界溢出
    hexagon = []
    for j in range(6):
        angle = 2 * math.pi * j / 6 + math.radians(30)# 计算角度
        x = center_x + side_length * 0.866 * math.cos(angle)  # 0.866 为正六边形内切圆半径与边长之比
        y = center_y + side_length * 0.866 * math.sin(angle)
        hexagon.append((x, y))

    # 绘制正六边形
    draw.polygon(hexagon, fill=current_color)

    # 保存图像为PNG文件
    file_name = f"dixing{(i+num*9)*10 + offset}.png"
    image.save(file_name, 'PNG')
