===========================================
データ水増し入門
===========================================

動機
=====

close(×：バッテンじるし)を学習するモデルをdarknetで構築しようとしているが、
サンプルデータが10数個くらいしか集めるコトができず、
そのせいか、darknetが学習をちっともしてくれない(mAPが常に0で、
ロスも0.28avgから下に一向に下がらず)。

学習データが少ないことがそもそもの原因と考え、
Data Augmentationを使ってデータを水増ししてみる。

まずは、学習を上手くすすめるためには1000枚程度の画像が必要とのことだが、
そもそも、自力でそんな枚数を集めるのはこんなんだ。。。

以下のサイトを参照に試してみるが、jupyterを使っていくらしい。
https://www.codexa.net/data_augmentation_python_keras/
https://qiita.com/zumax/items/0727e329f3322897d3e7

別環境にjupyterがあったのだが、そこを汚したくないので、
別途新しく創るコトにする。

環境構築
==========

OS
----

OS環境。::

 a@dataaug:~$ cat /etc/issue
 Ubuntu 20.04.1 LTS \n \l
 
 a@dataaug:~$ 


jupyter nodebookのインストール
---------------------------------

本家の情報を参考にインストールしてみる。

https://jupyter.org/install

以下のコマンドを実行する::

  sudo apt update
  sudo apt install pip

  pip install jupyterlab

  pip install markupsafe==2.0.1


以下を実行。::

  jupyter-lab --ip=0.0.0.0


data augmentationのためのパッケージの追加インストール
----------------------------------------------------------

以下を実行する。::

  pip install tensorflow
  pip install tensorflow-gpu

kerasをインストールします。::

  pip install keras

試しに動かしてみる
---------------------

以下のURLを参考にしながら。

https://qiita.com/zumax/items/0727e329f3322897d3e7


以下のコマンドでインストール::

  pip install Pillow
  pip install numpy
  pip install pandas
  pip install matplotlib
  pip install scipy
  
パンケーキ画像の表示
----------------------

コードなど::


  import keras.utils.image_utils as image
  import numpy as np
  import matplotlib.pyplot as plt
  
  
  #アップロードされた画像を読み込み
  img = image.load_img("./pancake.jpg", target_size=(640, 640))
  #画像をnumpy配列に変換する
  img = np.array(img)
  #表示画像のサイズを設定
  plt.figure(figsize = (10, 10))
  #軸を表示しない
  plt.xticks(color = "None")
  plt.yticks(color = "None")
  plt.tick_params(bottom = False, left = False)
  #表示
  plt.imshow(img)
  














