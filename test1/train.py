import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import cv2, os, json

IMG_SIZE = 96

# ====== 数据集类 ======
class RingDataset(Dataset):
    def __init__(self, img_dir, label_file):
        self.img_dir = img_dir
        self.labels = json.load(open(label_file))
        self.files = list(self.labels.keys())

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        fname = self.files[idx]
        img = cv2.imread(os.path.join(self.img_dir, fname), cv2.IMREAD_GRAYSCALE)
        img = img.astype("float32") / 255.0
        img = torch.tensor(img).unsqueeze(0)  # [1, H, W]
        label = self.labels[fname]
        target = torch.tensor([label["cx"], label["cy"], label["r"]], dtype=torch.float32)
        return img, target

# ====== 模型结构 ======
class RingNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2)
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 12 * 12, 128), nn.ReLU(),
            nn.Linear(128, 3), nn.Sigmoid()  # 输出 cx, cy, r ∈ [0,1]
        )

    def forward(self, x):
        return self.fc(self.conv(x))

# ====== 训练 ======
dataset = RingDataset("ring_dataset/images", "ring_dataset/labels.json")
loader = DataLoader(dataset, batch_size=32, shuffle=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = RingNet().to(device)
opt = optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()

for epoch in range(10):  # 训练 10 轮
    total_loss = 0
    for imgs, targets in loader:
        imgs, targets = imgs.to(device), targets.to(device)
        preds = model(imgs)
        loss = loss_fn(preds, targets)
        opt.zero_grad()
        loss.backward()
        opt.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss {total_loss/len(loader):.4f}")

torch.save(model.state_dict(), "ring_model.pth")