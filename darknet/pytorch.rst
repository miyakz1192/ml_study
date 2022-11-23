===================================================
pytorchで物体検出
===================================================

以下のサイトを参考にしながら、物体検出とトレーニングにチャレンジしてみる
http://cedro3.com/ai/pytorch-ssd-bccd/


守・破・理ということで、まずは写経してみる

環境情報
===========

OS::

 a@pytorch:~$ cat /etc/issue
 Ubuntu 20.04.1 LTS \n \l
 a@pytorch:~$ 


環境セットアップ
====================

まず、GPUが使えない環境だと単にpip3 install torchじゃダメ
https://tekenuko.hatenablog.com/entry/2018/01/26/103024
を見て、pytorchのwebサイトに行き、CPUを選択して、ダウンロードURLを得る。
最終的には以下のコマンド。::

  sudo apt update
  sudo apt install python3-pip
  sudo apt-get install libgl1-mesa-dev
  pip3 install numpy
  pip3 install opencv-python
  pip3 install matplotlib
  pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu


※ yolov7がGPU必須だと思って動かなくてdarknetを試したけど、この方法であれば、yolov7も動くんじゃないの？ 

コードのセットアップ
=========================

学習用のデータもすべて公開されているので大変ありがたい::

  # github からコードをコピー
  git clone https://github.com/cedro3/pytorch_ssd.git
  cd pytorch_ssd
  # 学習済みパラメータをダウンロード
  wget -P weights https://s3.amazonaws.com/amdegroot-models/ssd300_mAP_77.43_v2.pth

detectしてみる
===================

しかし、以下のエラー::

  a@pytorch:~/pytorch_ssd$ python3 first.py 
  Traceback (most recent call last):
    File "first.py", line 18, in <module>
      torch.set_default_tensor_type('torch.cuda.FloatTensor')  
    File "/home/a/.local/lib/python3.8/site-packages/torch/__init__.py", line 322, in set_default_tensor_type
      _C._set_default_tensor_type(t)
  TypeError: type torch.cuda.FloatTensor not available. Torch not compiled with CUDA enabled.
  a@pytorch:~/pytorch_ssd$ 

  a@pytorch:~/pytorch_ssd$ python3 
  Python 3.8.10 (default, Jun 22 2022, 20:18:18) 
  [GCC 9.4.0] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import torch
  >>> torch.cuda.is_available() 
  False
  >>> torch.set_default_tensor_type('torch.cuda.FloatTensor')  
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/a/.local/lib/python3.8/site-packages/torch/__init__.py", line 322, in set_default_tensor_type
      _C._set_default_tensor_type(t)
  TypeError: type torch.cuda.FloatTensor not available. Torch not compiled with CUDA enabled.
  >>> 


https://pytorch.org/docs/stable/tensors.html
を見るとCPUの場合はCPU tensorというのがあるらしい。
torch.FloatTensorに修正

https://niwakomablog.com/matplotllib-figure-show-errorhandling/
あと、この環境だとmatplot libが表示しれくれない(jupyterでないので)、savefigを使う

保存されたjpg画像を見ると、ちゃんとdetectまでは行けた!


  
  


