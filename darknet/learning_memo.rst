=====================================
学習の記録
=====================================

ds1
=====

以下のような構造::

  miyakz@lily2:~/git_repos/darknet$ tree ds1/
  ds1/
  ├── a.zip
  ├── backup
  ├── first.yaml
  ├── obj.data
  ├── obj.names
  ├── obj_train_data
  ├── train
  │   ├── Screenshot_2022-10-21-00-19-35-30_56bd83b73c18fa95b476c6c0f96c6836.jpg
  │   ├── Screenshot_2022-10-21-00-19-35-30_56bd83b73c18fa95b476c6c0f96c6836.txt
  │   ├── Screenshot_2022-10-21-00-21-51-38_56bd83b73c18fa95b476c6c0f96c6836.jpg
  │   └── Screenshot_2022-10-21-00-21-51-38_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── train.txt
  ├── valid
  │   ├── Screenshot_2022-10-21-00-23-35-12_56bd83b73c18fa95b476c6c0f96c6836.jpg
  │   ├── Screenshot_2022-10-21-00-23-35-12_56bd83b73c18fa95b476c6c0f96c6836.txt
  │   ├── Screenshot_2022-10-21-00-25-42-95_56bd83b73c18fa95b476c6c0f96c6836.jpg
  │   └── Screenshot_2022-10-21-00-25-42-95_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── valid.txt
  ├── yolov4.conv.137
  ├── yolov4-custom.cfg
  ├── yolov4-tiny.conv.29
  └── yolov4-tiny-custom.cfg

結果
------

上手く行かなかった。avgが0.2程度でストップしてdetectしてみるけど、検出せず。

考察
----

本家ページを見ると、avgが0.2じゃなくて、もう１桁低い、0.02位でストップするらしい(小さなモデル)。
なのでもう少し学習を続けるべきではないか。あと、学習データを少しだけ増やしてみる。
あと、cfgの画像の高さと幅が実際の画像のサイズと異なることがわかった。再設定してみる。
(1040*2400)
classの数と、filterの数は調整するべきかも。
既存重みファイルを指定するパターンだと上手く行かない？それとも指定する？

ds2
=====

cfgファイルの画像の高さと幅を変更する(結局不要)
-------------------------------------------------

変更の必要は無いみたい。変更してしまうと、darknetが正しく動かなかった。


u don't have to resize it, because Darknet will do it instead of you!

It means you really don't need to do that and you can use different image sizes during your training. What you posted above is just network configuration. There should be full network definition as well. And the height and the width tell you what's the network resolution. And it also keeps aspect ratio, check e.

Darknet が代わりにサイズを変更するため、サイズを変更する必要はありません。

これは、実際にそれを行う必要がなく、トレーニング中にさまざまな画像サイズを使用できることを意味します。 上に投稿したのは単なるネットワーク構成です。 完全なネットワーク定義も必要です。 高さと幅から、ネットワークの解像度がわかります。 また、アスペクト比も保持されます。e を確認してください。

https://stackoverflow.com/questions/49450829/darknet-yolo-image-size


classの数と、filterの数は調整
-------------------------------------------------

https://medium.com/analytics-vidhya/object-detection-with-yolo-aa2dfab21d56

change [filters=255] to filters=(classes + 5)x3 in the 3 [convolutional] before each [yolo] layer, keep in mind that it only has to be the last [convolutional] before each of the [yolo] layers.
Source - https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects (item #1)

とのこと。

一箇所目.::

  [convolutional]
  size=1
  stride=1
  pad=1
  #filters=255
  filters=18
  activation=linear
  
  
  
  [yolo]
  mask = 3,4,5
  
２カ所目。::

  [convolutional]
  size=1
  stride=1
  pad=1
  #filters=255
  filters=18
  activation=linear
  
  [yolo]
  mask = 0,1,2
  
あとclassは文字列ベースでyoloレイヤで２箇所あったので、それぞれclass=1に修正。

学習データを追加、および、ds2の構成
-------------------------------------------

imglabeling.rstを参照。このツールを使って、データを生成した。ds2は以下の構成。
以前はvalid/trainディレクトリを生成していたが、のベタンのほうが管理しやすいことに気づいた::

  ds2
  ├── backup
  ├── obj.data
  ├── obj.names
  ├── Screenshot_2022-10-21-00-19-35-30_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ├── Screenshot_2022-10-21-00-19-35-30_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── Screenshot_2022-10-21-00-21-51-38_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ├── Screenshot_2022-10-21-00-21-51-38_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── Screenshot_2022-10-21-00-23-35-12_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ├── Screenshot_2022-10-21-00-23-35-12_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── Screenshot_2022-10-21-00-25-42-95_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ├── Screenshot_2022-10-21-00-25-42-95_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── Screenshot_2022-11-11-00-31-27-10_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ├── Screenshot_2022-11-11-00-31-27-10_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── Screenshot_2022-11-11-00-32-36-53_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ├── Screenshot_2022-11-11-00-32-36-53_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── Screenshot_2022-11-11-00-34-25-48_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ├── Screenshot_2022-11-11-00-34-25-48_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── Screenshot_2022-11-11-00-35-14-37_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ├── Screenshot_2022-11-11-00-35-14-37_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── Screenshot_2022-11-11-00-35-55-52_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ├── Screenshot_2022-11-11-00-35-55-52_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── Screenshot_2022-11-11-00-37-18-58_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ├── Screenshot_2022-11-11-00-37-18-58_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── Screenshot_2022-11-11-00-39-39-59_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ├── Screenshot_2022-11-11-00-39-39-59_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── Screenshot_2022-11-11-00-41-06-93_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ├── Screenshot_2022-11-11-00-41-06-93_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── Screenshot_2022-11-11-00-47-07-72_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ├── Screenshot_2022-11-11-00-47-07-72_56bd83b73c18fa95b476c6c0f96c6836.txt
  ├── train.txt
  ├── valid.txt
  ├── yolov4-tiny.conv.29
  └── yolov4-tiny-custom.cfg


既存重みファイルを指定するパターンだと上手く行かない？それとも指定する？
-----------------------------------------------------------------------------

指定するパターンと指定しないパターンで試してみる。

まずは、指定しないパターンでやってみる。


