from PIL import Image, ImageDraw

path='/home/cory/Pictures/医疗/康/DICOM/中山大学附属第八医院/png/202404300862/T2Map_anatomical'

# 定义每行每列的图片数量
num_rows = 2
num_cols = 6
# 每张图片的宽度和高度
image_width = 384
image_height = 384
# 每个宫格之间的间隔大小
padding = 10
# 背景色
background_color = (255, 255, 255)  # 白色

# 创建一个空白的拼接图像
total_width = num_cols * image_width + (num_cols - 1) * padding
total_height = num_rows * image_height + (num_rows - 1) * padding
combined_image = Image.new('RGB', (total_width, total_height), background_color)

# 读取所有的图片并逐个粘贴到拼接图像中
for i in range(num_rows):
    for j in range(num_cols):
        idx = i * num_cols + j  # 计算图片索引
        try:
            # 假设图片文件名为image_0.png, image_1.png, ..., image_29.png
            image_path = f'{path}/{idx}.png'
            img = Image.open(image_path)
            combined_image.paste(img, (j * (image_width + padding), i * (image_height + padding)))
        except IOError:
            pass  # 处理找不到图片的情况

# 保存拼接后的图片
combined_image.save('combined_image.png')

# 显示拼接后的图片
combined_image.show()
