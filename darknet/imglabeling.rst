========================================
image labelingサーバの構築
========================================

参考URL
==========

https://medium.com/analytics-vidhya/object-detection-with-yolo-aa2dfab21d56

このサイトを参照して作業を実施した


作業
=====

labelImgをダウンロードしてくる::

  git clone https://github.com/tzutalin/labelImg.git

インストール作業::
  sudo apt update
  cd labelImg/
  sudo apt install pyqt5-dev-tools
  sudo apt install pip
  sudo pip3 install -r requirements/requirements-linux-python3.txt
  sudo pip3 install -r requirements/requirements-linux-python3.txt
  make qt5py3

labelImgディレクトリに移動して、以下のコマンドを実行する::

  python3 labelImg.py

参考URLがわかりやすいが、PASCAL VOCフォーマットを選び、OpenDirで画像が入ったディレクトリをOpenするとNext Imageをポンポン押して作業が進捗するので、やりやすい。Create RectBoxを選択して、label "close"の箇所を選択していく。

次にyoloフォーマットへの変換。上記のラベル付作業が終わると、画像が配置されている同じ場所にxmlファイルが生成されるので、これをyoloに合わせた軽しいに合わせるとのことで、以下のツールを更にDL::

  git clone https://ElencheZetetique@bitbucket.org/ElencheZetetique/rtod.git
  cd rtod/
  sudo pip3 install -r requirements.txt 

先ほどの画像(xml込)が入っているディレクトリに移動して(ここでは、labelImg/tempとしている)、
変換作業を行う。

  cd labelImg/temp/
  python3 /home/a/rtod/Tools/prepare.py -s ./ -yf 25 -cpy "./ds2/"

あとは、jpgとtxtが複数生成される。txtは画像の中の学習してほしい部分画像の座標を示すので、画像とセットで扱う必要がある。
この複数のjpg/txtの組を今度は、lily2(学習マシン）に移動する。

ds2を以下の構成は、learning_memo.rstに譲る。





