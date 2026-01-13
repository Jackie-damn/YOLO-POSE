import os
import random
from PIL import Image, ImageDraw

# 圆环参数配置
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255),
    (128, 0, 128), (255, 165, 0), (0, 128, 128), (128, 128, 0)
]
BACKGROUNDS = [
    (255, 255, 255), (30, 30, 30), (200, 200, 200), (50, 100, 150), (100, 50, 150)
]

OUTPUT_DIR = 'rings_output'
IMG_SIZE = [(256, 256), (320, 320), (400, 400)]


def generate_ring(index):
    size = random.choice(IMG_SIZE)
    bg_color = random.choice(BACKGROUNDS)
    ring_color = random.choice(COLORS)
    thickness = random.randint(5, size[0] // 10)
    min_radius = thickness + 5
    max_radius = min(size[0], size[1]) // 2 - thickness - 5
    radius = random.randint(min_radius, max_radius)
    margin = radius + thickness + 2
    center_x = random.randint(margin, size[0] - margin)
    center_y = random.randint(margin, size[1] - margin)
    center = (center_x, center_y)
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    draw.ellipse([
        center[0] - radius - thickness,
        center[1] - radius - thickness,
        center[0] + radius + thickness,
        center[1] + radius + thickness
    ], fill=ring_color)
    draw.ellipse([
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius
    ], fill=bg_color)
    filename = os.path.join(OUTPUT_DIR, f'ring_{index:03d}.png')
    img.save(filename)
    # 生成YOLO标签（class_id x_center y_center width height，均归一化）
    class_id = 0
    x_center = center_x / size[0]
    y_center = center_y / size[1]
    bbox_width = (radius + thickness) * 2 / size[0]
    bbox_height = (radius + thickness) * 2 / size[1]
    yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n"
    label_filename = os.path.join(OUTPUT_DIR, f'ring_{index:03d}.txt')
    with open(label_filename, "w") as f:
        f.write(yolo_line)
    # 返回标签信息用于统计
    label = {
        "filename": filename,
        "center_x": center_x,
        "center_y": center_y,
        "radius": radius,
        "thickness": thickness,
        "ring_color": ring_color,
        "bg_color": bg_color,
        "img_size": size,
        "yolo_label": yolo_line.strip()
    }
    return label


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    num_images = 500
    labels = []
    for i in range(num_images):
        label = generate_ring(i)
        labels.append(label)
    # 保存所有标签到 json 文件
    import json
    with open(os.path.join(OUTPUT_DIR, "labels.json"), "w", encoding="utf-8") as f:
        json.dump(labels, f, ensure_ascii=False, indent=2)
    print(f"已生成 {num_images} 张圆环图片及YOLO标签数据，保存在 {OUTPUT_DIR} 文件夹。")


if __name__ == "__main__":
    main()