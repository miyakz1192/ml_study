# ライブラリの読み込み
import os
import sys
from PIL import Image

import torch
import torch.utils.data as data
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import transforms

import matplotlib.pyplot as plt

def make_filepath_list():
    """
    学習データ、検証データそれぞれのファイルへのパスを格納したリストを返す

    Returns
    -------
    train_file_list: list
        学習データファイルへのパスを格納したリスト
    valid_file_list: list
        検証データファイルへのパスを格納したリスト
    """
    train_file_list = []
    valid_file_list = []

    for top_dir in os.listdir('./Images/'):
        file_dir = os.path.join('./Images/', top_dir)
        file_list = os.listdir(file_dir)

        # 各犬種ごとに8割を学習データ、2割を検証データとする
        num_data = len(file_list)
        num_split = int(num_data * 0.8)

        train_file_list += [os.path.join('./Images', top_dir, file).replace('\\', '/') for file in file_list[:num_split]]
        valid_file_list += [os.path.join('./Images', top_dir, file).replace('\\', '/') for file in file_list[num_split:]]

    return train_file_list, valid_file_list


class ImageTransform(object):
    """
    入力画像の前処理クラス
    画像のサイズをリサイズする
    
    Attributes
    ----------
    resize: int
        リサイズ先の画像の大きさ
    mean: (R, G, B)
        各色チャンネルの平均値
    std: (R, G, B)
        各色チャンネルの標準偏差
    """
    def __init__(self, resize, mean, std):
        self.data_trasnform = {
            'train': transforms.Compose([
                # データオーグメンテーション
                transforms.RandomHorizontalFlip(),
                # 画像をresize×resizeの大きさに統一する
                transforms.Resize((resize, resize)),
                # Tensor型に変換する
                transforms.ToTensor(),
                # 色情報の標準化をする
                transforms.Normalize(mean, std)
            ]),
            'valid': transforms.Compose([
                # 画像をresize×resizeの大きさに統一する
                transforms.Resize((resize, resize)),
                # Tensor型に変換する
                transforms.ToTensor(),
                # 色情報の標準化をする
                transforms.Normalize(mean, std)
            ])
        }
    
    def __call__(self, img, phase='train'):
        return self.data_trasnform[phase](img)

class DogDataset(data.Dataset):
    """
    犬種のDataseクラス。
    PyTorchのDatasetクラスを継承させる。
    
    Attrbutes
    ---------
    file_list: list
        画像のファイルパスを格納したリスト
    classes: list
        犬種のラベル名
    transform: object
        前処理クラスのインスタンス
    phase: 'train' or 'valid'
        学習か検証化を設定
    """
    def __init__(self, file_list, classes, transform=None, phase='train'):
        self.file_list = file_list
        self.transform = transform
        self.classes = classes
        self.phase = phase
    
    def __len__(self):
        """
        画像の枚数を返す
        """
        return len(self.file_list)
    
    def __getitem__(self, index):
        """
        前処理した画像データのTensor形式のデータとラベルを取得
        """
        # 指定したindexの画像を読み込む
        img_path = self.file_list[index]
        img = Image.open(img_path)
        
        # 画像の前処理を実施
        img_transformed = self.transform(img, self.phase)
        
        # 画像ラベルをファイル名から抜き出す
        label = self.file_list[index].split('/')[2][10:]
        
        # ラベル名を数値に変換
        label = self.classes.index(label)
        
        return img_transformed, label

class Net(nn.Module):
    
    def __init__(self):
        super(Net, self).__init__()
        
        self.conv1_1 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, padding=1)
        self.conv1_2 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv2_1 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
        self.conv2_2 = nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.fc1 = nn.Linear(in_features=128 * 75 * 75, out_features=128)
        self.fc2 = nn.Linear(in_features=128, out_features=5)
        #self.fc2 = nn.Linear(in_features=128, out_features=120)
    
    def forward(self, x):
        x = F.relu(self.conv1_1(x))
        x = F.relu(self.conv1_2(x))
        x = self.pool1(x)
        
        x = F.relu(self.conv2_1(x))
        x = F.relu(self.conv2_2(x))
        x = self.pool2(x)

        x = x.view(-1, 128 * 75 * 75)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.softmax(x, dim=1)
        
        return x


print("====validating working process each classes defined following====")

# 画像データへのファイルパスを格納したリストを取得する
train_file_list, valid_file_list = make_filepath_list()

print('train data num, 学習データ数 : ', len(train_file_list))
# 先頭3件だけ表示
print(train_file_list[:3])

print('valid data num, 検証データ数 : ', len(valid_file_list))
# 先頭3件だけ表示
print(valid_file_list[:3])


# 動作確認
img = Image.open('./Images/n02085620-Chihuahua/n02085620_199.jpg')

# リサイズ先の画像サイズ
resize = 300

# 今回は簡易的に(0.5, 0.5, 0.5)で標準化
mean = (0.5, 0.5, 0.5)
std = (0.5, 0.5, 0.5)

transform = ImageTransform(resize, mean, std)
img_transformed = transform(img, 'train')

#plt.imshow(img)
#plt.show()

#plt.imshow(img_transformed.numpy().transpose((1, 2, 0)))
#plt.show()
plt.savefig("test.jpg")

print("====MAIN====")

# 動作確認
# クラス名
dog_classes = [
    'Chihuahua',  'Shih-Tzu',
    'borzoi', 'Great_Dane', 'pug'
]
#dog_classes = [
#    'Chihuahua',
#    'Japanese_spaniel',
#    'Maltese_dog',
#    'Pekinese',
#    'Shih-Tzu',
#    'Blenheim_spaniel',
#    'papillon',
#    'toy_terrier',
#    'Rhodesian_ridgeback',
#    'Afghan_hound',
#    'basset',
#    'beagle',
#    'bloodhound',
#    'bluetick',
#    'black-and-tan_coonhound',
#    'Walker_hound',
#    'English_foxhound',
#    'redbone',
#    'borzoi',
#    'Irish_wolfhound',
#    'Italian_greyhound',
#    'whippet',
#    'Ibizan_hound',
#    'Norwegian_elkhound',
#    'otterhound',
#    'Saluki',
#    'Scottish_deerhound',
#    'Weimaraner',
#    'Staffordshire_bullterrier',
#    'American_Staffordshire_terrier',
#    'Bedlington_terrier',
#    'Border_terrier',
#    'Kerry_blue_terrier',
#    'Irish_terrier',
#    'Norfolk_terrier',
#    'Norwich_terrier',
#    'Yorkshire_terrier',
#    'wire-haired_fox_terrier',
#    'Lakeland_terrier',
#    'Sealyham_terrier',
#    'Airedale',
#    'cairn',
#    'Australian_terrier',
#    'Dandie_Dinmont',
#    'Boston_bull',
#    'miniature_schnauzer',
#    'giant_schnauzer',
#    'standard_schnauzer',
#    'Scotch_terrier',
#    'Tibetan_terrier',
#    'silky_terrier',
#    'soft-coated_wheaten_terrier',
#    'West_Highland_white_terrier',
#    'Lhasa',
#    'flat-coated_retriever',
#    'curly-coated_retriever',
#    'golden_retriever',
#    'Labrador_retriever',
#    'Chesapeake_Bay_retriever',
#    'German_short-haired_pointer',
#    'vizsla',
#    'English_setter',
#    'Irish_setter',
#    'Gordon_setter',
#    'Brittany_spaniel',
#    'clumber',
#    'English_springer',
#    'Welsh_springer_spaniel',
#    'cocker_spaniel',
#    'Sussex_spaniel',
#    'Irish_water_spaniel',
#    'kuvasz',
#    'schipperke',
#    'groenendael',
#    'malinois',
#    'briard',
#    'kelpie',
#    'komondor',
#    'Old_English_sheepdog',
#    'Shetland_sheepdog',
#    'collie',
#    'Border_collie',
#    'Bouvier_des_Flandres',
#    'Rottweiler',
#    'German_shepherd',
#    'Doberman',
#    'miniature_pinscher',
#    'Greater_Swiss_Mountain_dog',
#    'Bernese_mountain_dog',
#    'Appenzeller',
#    'EntleBucher',
#    'boxer',
#    'bull_mastiff',
#    'Tibetan_mastiff',
#    'French_bulldog',
#    'Great_Dane',
#    'Saint_Bernard',
#    'Eskimo_dog',
#    'malamute',
#    'Siberian_husky',
#    'affenpinscher',
#    'basenji',
#    'pug',
#    'Leonberg',
#    'Newfoundland',
#    'Great_Pyrenees',
#    'Samoyed',
#    'Pomeranian',
#    'chow',
#    'keeshond',
#    'Brabancon_griffon',
#    'Pembroke',
#    'Cardigan',
#    'toy_poodle',
#    'miniature_poodle',
#    'standard_poodle',
#    'Mexican_hairless',
#    'dingo',
#    'dhole',
#    'African_hunting_dog',
#]

# リサイズ先の画像サイズ
resize = 300

# 今回は簡易的に(0.5, 0.5, 0.5)で標準化
mean = (0.5, 0.5, 0.5)
std = (0.5, 0.5, 0.5)

# Datasetの作成
train_dataset = DogDataset(
    file_list=train_file_list, classes=dog_classes,
    transform=ImageTransform(resize, mean, std),
    phase='train'
)

valid_dataset = DogDataset(
    file_list=valid_file_list, classes=dog_classes,
    transform=ImageTransform(resize, mean, std),
    phase='valid'
)

index = 0
print(train_dataset.__getitem__(index)[0].size())
print(train_dataset.__getitem__(index)[1])


# バッチサイズの指定
batch_size = 64

# DataLoaderを作成
train_dataloader = data.DataLoader(
    train_dataset, batch_size=batch_size, shuffle=True)

valid_dataloader = data.DataLoader(
    valid_dataset, batch_size=32, shuffle=False)

# 辞書にまとめる
dataloaders_dict = {
    'train': train_dataloader, 
    'valid': valid_dataloader
}

# 動作確認
# イテレータに変換
batch_iterator = iter(dataloaders_dict['train'])

# 1番目の要素を取り出す
inputs, labels = next(batch_iterator)

print(inputs.size())
print(labels)

net = Net()
print(net)

criterion = nn.CrossEntropyLoss()
#optimizer = optim.SGD(net.parameters(), lr=0.01)
#以下に取り替えてみる
optimizer = optim.Adam(net.parameters(), lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0, amsgrad=False)

# エポック数
#num_epochs = 30
num_epochs = 300

for epoch in range(num_epochs):
    print('Epoch {}/{}'.format(epoch+1, num_epochs))
    print('-------------')
    sys.stdout.flush()
    
    for phase in ['train', 'valid']:
        
        if phase == 'train':
            # モデルを訓練モードに設定
            net.train()
        else:
            # モデルを推論モードに設定
            net.eval()
        
        # 損失和
        epoch_loss = 0.0
        # 正解数
        epoch_corrects = 0
        
        # DataLoaderからデータをバッチごとに取り出す
        for inputs, labels in dataloaders_dict[phase]:
            
            # optimizerの初期化
            optimizer.zero_grad()
            
            # 学習時のみ勾配を計算させる設定にする
            with torch.set_grad_enabled(phase == 'train'):
                outputs = net(inputs)
                
                # 損失を計算
                loss = criterion(outputs, labels)
                
                # ラベルを予測
                _, preds = torch.max(outputs, 1)
                
                # 訓練時はバックプロパゲーション
                if phase == 'train':
                    # 逆伝搬の計算
                    loss.backward()
                    # パラメータの更新
                    optimizer.step()
                
                # イテレーション結果の計算
                # lossの合計を更新
                # PyTorchの仕様上各バッチ内での平均のlossが計算される。
                # データ数を掛けることで平均から合計に変換をしている。
                # 損失和は「全データの損失/データ数」で計算されるため、
                # 平均のままだと損失和を求めることができないため。
                epoch_loss += loss.item() * inputs.size(0)
                
                # 正解数の合計を更新
                epoch_corrects += torch.sum(preds == labels.data)

        # epochごとのlossと正解率を表示
        epoch_loss = epoch_loss / len(dataloaders_dict[phase].dataset)
        epoch_acc = epoch_corrects.double() / len(dataloaders_dict[phase].dataset)

        print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))
        sys.stdout.flush()

# 予測用のダミーデータ
x = torch.randn([1, 3, 300, 300])
preds = net(x)


#===================================================

