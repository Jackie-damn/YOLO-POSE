# train.py
"""
YOLOv8 训练脚本（Ultralytics API）
适用于单类/多类的 YOLOv8 训练，带常用超参与训练后评估/导出步骤。
"""

from ultralytics import YOLO
import os
import argparse

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--data", type=str, default="data.yaml", help="path to data yaml")
    p.add_argument("--model", type=str, default="yolov8n.pt", help="pretrained backbone or custom weight")
    p.add_argument("--epochs", type=int, default=100)
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--batch", type=int, default=16)
    p.add_argument("--lr0", type=float, default=1e-3)
    p.add_argument("--project", type=str, default="runs/ring_train")
    p.add_argument("--name", type=str, default="exp")
    p.add_argument("--device", type=str, default="0")  # "cpu" 或 GPU id "0"
    p.add_argument("--save_every", type=int, default=10, help="save checkpoint every N epochs (optional)")
    return p.parse_args()

def main():
    args = parse_args()

    # Create project dir
    os.makedirs(args.project, exist_ok=True)

    # Load a model (预训练权重或自定义)
    model = YOLO(args.model)

    # Training
    # 你可以通过 augment 参数控制内置的 mosaic/mixup 等
    results = model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        lr=args.lr0,
        device=args.device,
        project=args.project,
        name=args.name,
        workers=8,
        # 可选项（内置超参微调）
        optimizer="SGD",            # 或 "Adam"
        momentum=0.937,
        weight_decay=5e-4,
        # augmentation controls
        augment=True,              # 开启默认增强 (mosaic, mixup等)
        cache=False,               # 是否把数据缓存到内存（大数据慎用）
        # 保存最好的权重（val mAP）
        save=True,
        # verbose training log 默认 True
    )

    # results 里含训练元数据
    print("训练完成，结果对象：", results)

    # 评估：直接用训练出的 best.pt（若存在）
    best_weights = os.path.join(args.project, args.name, "weights", "best.pt")
    if os.path.exists(best_weights):
        print("开始使用 best.pt 进行评估：", best_weights)
        eval_model = YOLO(best_weights)
        eval_model.val(data=args.data)  # 打印 mAP, precision, recall 等
    else:
        print("未找到 best.pt，跳过评估")

    # 导出模型（可选）：ONNX 和 TFLite
    # 若需要导出到其他格式，可取消注释下面一行
    # model.export(format=["onnx", "tflite"])  # 支持传入字符串或 list

if __name__ == "__main__":
    main()