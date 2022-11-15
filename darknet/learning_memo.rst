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

参考：途中結果のチャートについて
-------------------------------------

https://kagglenote.com/ml-tips/yolov4-training/
学習の際にはオプションをつけることが可能です。

-map: mapも学習曲線に描画する。
-dont_show: 学習曲線をGUI上でリアルタイム表示しないためのもの。サーバー上で学習をしていてGUI環境でない場合はこのオプションをつける。
-mjpeg_port 8090: GUI環境がないがリアルタイムで学習曲線を確認したい場合これをつける。ポートにアクセスすることで学習曲線が確認可能となる。

mjpeg_portはopencvが必要？
https://linuxize.com/post/how-to-install-opencv-on-ubuntu-20-04/

sudo apt install libopencv-dev
して、MakefileでOPENCVを有効してmake。これをやらないと。http://localhost:8090でチャートが現れなかった。


途中結果
----------

1) 既存重みファイルを指定しないパターン
　→　うまくいかない。すべての画像に対して生成されたweightファイルでdetectしたが一枚もdetectできず。
     my_logs/log_20221111に経過を記載(nohup.out)
     avgは2.69~2.80台をうろうろしており、この辺でもう良いかな感。

このため、既存重みファイルを指定するパターン、かつ、途中経過もグラフ表示しつつ、mapというものを試してみる。
あと、そもそもデータが足りないという話があるらしい。。。。データの水増しというのが必要そうな。
あと、1)だと学習がうまくいきずらいらしい。(転移学習をしたほうが良い)

https://teratail.com/questions/212736
こればっかりは試してみないとわかりませんが、数枚というのは少なすぎてうまくいかないと予想されます。
オーグメンテーションはある程度精度が出ているモデルをさらに精度をよくするのには有用ですが、元々数枚程度しかバリエーションないものを水増しして1000枚にしたところで難しいのではないかと思います。

Deep Learning は数千、数万のサンプルを使ってパラメータを調整するという仕組みのものなので、サンプルが用意できないのであれば、画像処理など別のアプローチを考えたほうがよいと思います。

ということだが、、、

2)　既存重みファイルを指定するパターンでGO(2022/11/12深夜開始)

途中結果2
----------------

既存重みファイルを指定するパターンだと、今の所、2022/11/13 00:09ほど。
avgは2.70台をウロウロ。パット見、下がり気味なので、放っておく。
適合は0。なんでだろう。試しに、1)の時と同様に途中経過のweightファイルで全画像に対してdetectしたが、一枚も上手く行かず。
はやり、データ数が足りないかな？

ただ、darknetはデータ拡張はデフォルトで実施しているとのことだが。
https://demura.net/robot/athome/15558.html

このページに記載のあるパラメータを幾つか確認してみたが、デフォルト設定なので、
大丈夫かと思った。

とりあえず、学習をさせながら以下のサイトを見つつ、データ水増しを実施する。
https://qiita.com/zumax/items/0727e329f3322897d3e7

あと、気づいたのだが、学習データをアノテーションするときに、
純粋に×マークより少し広い範囲まで含めてしまっているような気がする。
要するに、もう少し学習データを精度よくすれば良いのではないか。

また、mAPの計算の時に、
./ds2/Screenshot_2022-11-11-00-47-07-72_56bd83b73c18fa95b476c6c0f96c6836.txt
が見つかりませんみたいなメッセージが出ている。これ、もしかしたら、txtが誤って画像見たいに認識されていないかな。

valid.txtがバグっているわ。これがもしかしたら、学習に影響しているかも。::

  miyakz@lily2:~/git_repos/darknet/ds2$ cat valid.txt 
  ./ds2/Screenshot_2022-11-11-00-35-14-37_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds2/Screenshot_2022-11-11-00-35-55-52_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds2/Screenshot_2022-11-11-00-37-18-58_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds2/Screenshot_2022-11-11-00-39-39-59_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds2/Screenshot_2022-11-11-00-41-06-93_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds2/Screenshot_2022-11-11-00-47-07-72_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds2/Screenshot_2022-11-11-00-47-07-72_56bd83b73c18fa95b476c6c0f96c6836.txt
  miyakz@lily2:~/git_repos/darknet/ds2$ 
  
  trainは大丈夫の様子。
  miyakz@lily2:~/git_repos/darknet/ds2$ cat train.txt 
  ./ds2/Screenshot_2022-10-21-00-19-35-30_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds2/Screenshot_2022-10-21-00-21-51-38_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds2/Screenshot_2022-10-21-00-23-35-12_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds2/Screenshot_2022-10-21-00-25-42-95_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds2/Screenshot_2022-11-11-00-31-27-10_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds2/Screenshot_2022-11-11-00-32-36-53_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds2/Screenshot_2022-11-11-00-34-25-48_56bd83b73c18fa95b476c6c0f96c6836.jpg
  miyakz@lily2:~/git_repos/darknet/ds2$ 


ds2結果
========

上手く行かなかった。9000イテレーションを迎えた時点でmAPが0かつ、ロスが2.7から下がらないため。
my_logs/ds2_logs.txtとds2/result.jpegに結果を格納。

./check_sample.sh ds2の結果、画像を全部確認したが全く予測が０.


気づきまとめ(1)
================

1)  valid.txtがバグっている(txt)が混入している

2)  iterationが9000まで行っていない(とはいえどもmAPは0のままだが)

3) そもそもアノテーション箇所が間違っている

4) 学習データ数が足りない(100からがスタート、通常は数千)

5) 既存重みファイルを指定するのが良いみたい

6) 学習データのアノテーションが適当(ちゃらんぽらんだった)


とりあえず、ds2はいろいろとおかしい所が満載かもしれないが、
とりあえず、9000イテレーションまでを迎えてみて、どうなのか？を確認してみる

いくらiterationが90000行ったとしてもmAPが0で、ロスも下がらないようであれば、ダメ。
mAPの値をとにかく出さないとダメらしい。

特に6)については、アノテーションの矩形を指定するときに、正しく×マークを指定していなかったかもしれない。

ds3の実行
===============

ds2をコピーしてきて、ds3を創る。

まず、valid.txtを直す。
正しく×を選択した×単一の画像(約32×32の画像,close1.jpg)を元に、とにかくdarknetが動作するのかを確認してみる。
とりあえず、動作している。
data augumentationを使って訓練データや検証データを水増し(594個)。
以下の状況でとりあえず、1晩位放置して、mAPの値に変化がでるかを観察してみる。

1) valid.txtを修正(txtの混在を修正)
2) アノテーション箇所が間違っているのを修正(0 0.5 0.5 1.0 1.0)※　つまり画像全体
3) trainデータは200個。validは394個
4) 既存重みファイルを指定

まずは、1000 iterationの時のmAP値!

なお、単に×画像をいろいろと拡大、縮小、回転、明るさなどを変えた画像を大量に入れた(train=200,valid=394)。
その他、validデータとして、ゲームの画像を入れた。

結果と考察
------------

2881イテレーションを経過した時点での状況。

「半分」上手く行った。
まず、学習用、検証用に自分で作った×画像については学習できたし、正しく検出出来た様子。
学習中に(2881イテレーション)、0.05 avg/mAP=94.86%となりかなりいい感じになっている。
しかし、validデータ中に含まれるゲーム画像中の×については全く検出しない。
data augumentationかましたデータの世界だとＯＫだけど、現実のゲーム画像では全然ヒットしないという悲しい結果に。
ただ、自分自身が指定したパターンでの学習と検証が確認でき、Darknetでの画像認識の実現性がこれで少し確認はできたので、
少しは進歩したと思って良い。

以下、考察。

1) trainデータ中のゲーム画像の×のバリエーションが不足しているのではないか。しかし、これはたくさんのサンプル画像を用意する必要があり、かなりの手間ではある。しかし、100~200画像位ならなんとか努力の範囲かもしれない

2) 9000イテレーションは回してみる(11/15時点では2991イテレーションのため、もう２日位は回してみる)

3) 画像のサイズの不一致が起きている？学習と検証用にdata augumentationして作った画像のサイズは32×32でかなり小さい。それに対して、ゲーム用の画像は1080×2400のサイズになっているため。この心配を検証するために、1080×2400の画像ファイルを編集し、100%近く検出できる×画像を直接埋め込んで見る。それを、11/15時点で出来た重みファイルを用いて検出できるかを確認する。検出できるなら問題なさそうだし、検出できないなら、画像サイズの不一致がまずいのかもしれないという予測になる。
  結果はNG。./ds3/close_data/close1.jpgそのものは89%の確率でcloseと識別できるが、./ds3/close_data/close1.jpgが混じったScreenshot_test.jpg(1080×2400)は検出できなかった。なんでだろう。


しかし、サンプル中のdog.jpgやeagle.jpgなどは画像の大きさがそれぞれ違う。::

  miyakz@lily2:~/git_repos/darknet/data$ ls *jpg | while read line
  > do
  > file $line
  > done
  dog.jpg: JPEG image data, Exif standard: [TIFF image data, big-endian, direntries=10, description=                               , manufacturer=Canon, model=Canon PowerShot S95, orientation=upper-left, xresolution=192, yresolution=200, resolutionunit=2, software=Photos 1.0, datetime=2014:09:19 16:08:30], baseline, precision 8, 768x576, components 3
  eagle.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=9, manufacturer=PENTAX             , model=PENTAX K-5         , orientation=upper-left, xresolution=162, yresolution=170, resolutionunit=2, software=Photos 1.0, datetime=2013:07:19 21:57:42], baseline, precision 8, 773x512, components 3
  giraffe.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 300x300, segment length 16, baseline, precision 8, 500x500, components 3
  horses.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=9, manufacturer=PENTAX             , model=PENTAX K-5         , orientation=upper-left, xresolution=162, yresolution=170, resolutionunit=2, software=Photos 1.0, datetime=2013:04:13 15:02:50], baseline, precision 8, 773x512, components 3
  person.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=9, manufacturer=PENTAX             , model=PENTAX K-5         , orientation=upper-left, xresolution=162, yresolution=170, resolutionunit=2, software=Photos 1.0, datetime=2013:04:13 14:59:36], baseline, precision 8, 640x424, components 3
  rizard.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 800x500, components 3
  scream.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=6, orientation=upper-left, xresolution=86, yresolution=94, resolutionunit=2, software=Paint.NET v3.5.5], baseline, precision 8, 352x448, components 3
  miyakz@lily2:~/git_repos/darknet/data$ 


ただ、これらファイルは画像のサイズはマチマチではあるが、大体３桁×３桁のサイズに対して、今回のds3はtrain/validともに32×32であり、Screenshot系は1080×2400と100倍以上のサイズの差はある。これが今回のNGにつながっているかどうかはわからない。。。

しかし、なんか、変な感じはする。ネットワークのサイズがそもそも、416 x 416 になっていること、および、close1.txtで0.5 0.5 1.0 1.0で画像全体の比率を指定している中たりからすると、32 x 32の画像では「検出してほしいサイズの」closeになっているが、416 x 416のサイズで解釈された時に416 x 416全体を目一杯使ったcloseに「ひきのばされて」いないか？::

   layer   filters  size/strd(dil)      input                output
   0 conv     32       3 x 3/ 2    416 x 416 x   3 ->  208 x 208 x  32 0.075 BF

まさに、close1.jpgの×を1080 x 2400に引き伸ばした画像を作成して、ds3のbestの重みで学習させた所、closeとして認識された。
これが、ゲーム画像(1080 x 2400)に埋め込まれた32 x 32サイズのcloseマークを検出できなかった原因だ！::

  temp/Screenshot_test3_long.jpg: Predicted in 510.126000 milli-seconds.
  close: 70%


その後の検証として、train/validデータをやはり、1080 x 2400で用意して、サイズとしては32 x 32のcloseを作る。32 x 32の画像のもと、data augumentationでバリエーションを作り、それを1080 x 2400の空画像（背景が白）に、キッチり32 x 32のサイズとしてcloseを埋め込んだ上で、正しい比率をannotationの.txtファイルに指定すれば良いのだと思われる。


ds3を停止nohup_ds3_20221116.logに結果を記録

  
ds4の計画と実行
===================

32 x 32画像の1080 x 2400画像への埋め込み&data augumentationは最新のdata_augmentation.ipynbで対応。
そして、上記の考察を受けて、train/validデータを改めて用意する。::

  a@imglabeling:~/labelImg/temp_for_ds4$ cat 0.txt 
  0 0.015278 0.006875 0.028704 0.012917
  a@imglabeling:~/labelImg/temp_for_ds4$ 
  
  miyakz@lily2:~/git_repos/darknet$ ruby -e "puts 16.0/1080.0"
  0.014814814814814815
  miyakz@lily2:~/git_repos/darknet$ ruby -e "puts 16.0/2400.0"
  0.006666666666666667
  miyakz@lily2:~/git_repos/darknet$ ruby -e "puts 32.0/1080.0"
  0.02962962962962963
  miyakz@lily2:~/git_repos/darknet$ ruby -e "puts 32.0/2040.0"
  0.01568627450980392
  miyakz@lily2:~/git_repos/darknet$ 
  
大体合っているので、一応、0.txtのannotationデータをすべてのtrain/valid画像に対して使う::

  a@imglabeling:~/labelImg$ ./create_annotation_txt.sh temp_for_ds4/
  a@imglabeling:~/labelImg$ 

ds4をds3をベースに作り、学習開始(11/16 2:38)
