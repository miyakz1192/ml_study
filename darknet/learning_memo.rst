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


結果と考察
------------

11/17 22:33現在、3446 iteration時点でap値が0.4%、ロスが0.2位をぶらぶら。
実際に画像をdetectさせてみると、::

  miyakz@lily2:~/git_repos/darknet$ ./check_screen_shot.sh ds4 best
  (snip)
  close: 31%
  close: 31%
  close: 32%
  close: 35%
  close: 31%
  close: 28%
  close: 53%
  close: 27%
  close: 35%
  close: 38%
  close: 64%
  close: 78%
  close: 47%
  close: 40%
  close: 29%
  close: 34%
  close: 34%
  close: 82%
  close: 83%
  close: 40%
  close: 25%
  close: 25%
  close: 54%
  close: 76%
  close: 37%
  close: 34%
  close: 66%
  close: 33%
  close: 43%
  close: 49%
  close: 33%
  close: 57%
  close: 50%
  close: 24%
  close: 52%
  close: 45%
  close: 31%
  close: 63%
  close: 55%
  close: 32%
  close: 68%
  close: 63%
  close: 34%
  close: 71%
  close: 66%
  close: 33%
  close: 66%
  close: 59%
  close: 29%
  close: 60%
  close: 55%
  close: 26%
  close: 27%
  close: 60%
  close: 52%
  close: 54%
  close: 46%
  close: 42%
  close: 52%
  close: 35%
  close: 41%
  close: 34%
  close: 33%
  close: 60%
  close: 24%
  close: 41%
  close: 34%
  close: 24%
  close: 32%
  close: 27%
  close: 33%
  miyakz@lily2:~/git_repos/darknet$ 


実際、ゲーム画像に対してcloseを「検出」はしているのだが、もちろん、誤検出しまくっている。

my_logs/nohup_ds3_20221116.logでは、iterationが1000でap = 80%くらいだったので、
これ以上、ds4のiterationを続けてもダメかと思う。そう思う理由は以下のメッセージが出ているため、
ds4での学習が上手く行っていないと考えた。ds3では同様のメッセージは出ていなかった。::

  miyakz@lily2:~/git_repos/darknet$ grep -rn Cannot nohup.out  | sort | uniq
  10737:Cannot load image 
  11562:Cannot load image 
  12387:Cannot load image 
  13228:Cannot load image 
  14061:Cannot load image 
  14890:Cannot load image 
  15715:Cannot load image 
  16540:Cannot load image 
  17365:Cannot load image 
  18190:Cannot load image 
  19019:Cannot load image 
  19852:Cannot load image 
  20681:Cannot load image 
  21510:Cannot load image 
  22335:Cannot load image 
  23266:Cannot load image 
  24099:Cannot load image 
  24924:Cannot load image 
  25753:Cannot load image 
  8152:Cannot load image 
  9083:Cannot load image 
  9912:Cannot load image 
  miyakz@lily2:~/git_repos/darknet$ 

ほかにも以下。1000 iterationで初めてでて、以降、100 iterationごとに出るので、中々気づきにくい。::

   (next mAP calculation at 1000 iterations) ESC]2;1000/500200: loss=0.2 hours left=3631.7^G
   1000: 0.155323, 0.187253 avg loss, 0.002610 rate, 26.370815 seconds, 64000 images, 3631.749998 hours left
    ^M4^M8^M12^M16^M20^M24^M28^M32^M36^M40^M44^M48^M52^M56^M60^M64^M68^M72^M76^M80^M84^M88^M92^M96^M100^M104^M108^M112^M116^M120^M124^M128^M132^M136^M140
    ^M144^M148^M152^M156^M160^M164^M168^M172^M176^M180^M184^M188^M192^M196^M200^M204^M208^M212^M216^M220^M224^M228^M232^M236^M240^M244^M248^M252^M256^M260
    ^M264^M268^M272^M276^M280^M284^M288^M292^M296^M300^M304^M308^M312^M316^M320^M324^M328^M332^M336^M340^M344^M348^M352^M356^M360^M364^M368^M372^M376^M380
    ^M384^M388^M392^M396^M400^M404
     calculation mAP (mean average precision)...
     Detection layer: 30 - type = 28 
     Detection layer: 37 - type = 28 
    Cannot load image 
    ^M408Label file name is too short:  
    Can't open label file. (This can be normal only if you use MSCOCO):  
    
ds3の時のエラー。これが唯一。txtでデータ形式が間違っていただけなので、学習には根本的な影響は無いと判断。::
  miyakz@lily2:~/git_repos/darknet$ grep Cannot my_logs/nohup_ds3_20221116.log  | sort | uniq
  Cannot load image ./ds3/close_data/Screenshot_2022-11-11-00-47-07-72_56bd83b73c18fa95b476c6c0f96c6836.txt
  miyakz@lily2:~/git_repos/darknet$ 


ds4のデータで個別にdetector mapをしてみるとエラーが再現。::
  miyakz@lily2:~/git_repos/darknet$ ./darknet detector map  ./ds4/obj.data ./ds4/yolov4-tiny-custom.cfg ./ds4/backup/yolov4-tiny-custom_best.weights
  (snip)
  [yolo] params: iou loss: ciou (4), iou_norm: 0.07, obj_norm: 1.00, cls_norm: 1.00, delta_norm: 1.00, scale_x_y: 1.05
  nms_kind: greedynms (1), beta = 0.600000 
  Total BFLOPS 6.787 
  avg_outputs = 299663 
  Loading weights from ./ds4/backup/yolov4-tiny-custom_best.weights...
   seen 64, trained: 172 K-images (2 Kilo-batches_64) 
  Done! Loaded 38 layers from weights-file 
  
   calculation mAP (mean average precision)...
   Detection layer: 30 - type = 28 
   Detection layer: 37 - type = 28 
  404Cannot load image 
  408Label file name is too short:  
  Can't open label file. (This can be normal only if you use MSCOCO):  
  
   detections_count = 24830, unique_truth_count = 407  
  class_id = 0, name = close, ap = 0.36%   	 (TP = 57, FP = 5055) 
  
   for conf_thresh = 0.25, precision = 0.01, recall = 0.14, F1-score = 0.02 
   for conf_thresh = 0.25, TP = 57, FP = 5055, FN = 350, average IoU = 0.56 % 
  
   IoU threshold = 50 %, used Area-Under-Curve for each unique Recall 
   mean average precision (mAP@0.50) = 0.003634, or 0.36 % 
  Total Detection Time: 236 Seconds
  
  Set -points flag:
   `-points 101` for MS COCO 
   `-points 11` for PascalVOC 2007 (uncomment `difficult` in voc.data) 
   `-points 0` (AUC) for ImageNet, PascalVOC 2010-2012, your custom dataset
  miyakz@lily2:~/git_repos/darknet$ 

valid.txtに空白を見つける::

  miyakz@lily2:~/git_repos/darknet$ cat ds4/valid.txt | tail -2
  ./ds4/close_data/Screenshot_2022-11-11-00-47-07-72_56bd83b73c18fa95b476c6c0f96c6836.jpg
  
  miyakz@lily2:~/git_repos/darknet$ 

もっかい実施してみる。::

  [yolo] params: iou loss: ciou (4), iou_norm: 0.07, obj_norm: 1.00, cls_norm: 1.00, delta_norm: 1.00, scale_x_y: 1.05
  nms_kind: greedynms (1), beta = 0.600000 
  Total BFLOPS 6.787 
  avg_outputs = 299663 
  Loading weights from ./ds4/backup/yolov4-tiny-custom_best.weights...
   seen 64, trained: 172 K-images (2 Kilo-batches_64) 
  Done! Loaded 38 layers from weights-file 
  
   calculation mAP (mean average precision)...
   Detection layer: 30 - type = 28 
   Detection layer: 37 - type = 28 
  408
   detections_count = 23728, unique_truth_count = 407  
  class_id = 0, name = close, ap = 0.44%   	 (TP = 57, FP = 4608) 
  
   for conf_thresh = 0.25, precision = 0.01, recall = 0.14, F1-score = 0.02 
   for conf_thresh = 0.25, TP = 57, FP = 4608, FN = 350, average IoU = 0.62 % 
  
   IoU threshold = 50 %, used Area-Under-Curve for each unique Recall 
   mean average precision (mAP@0.50) = 0.004385, or 0.44 % 
  Total Detection Time: 235 Seconds
  
  Set -points flag:
   `-points 101` for MS COCO 
   `-points 11` for PascalVOC 2007 (uncomment `difficult` in voc.data) 
   `-points 0` (AUC) for ImageNet, PascalVOC 2010-2012, your custom dataset
  miyakz@lily2:~/git_repos/darknet$ 

エラーを解消したところでap値にほとんど変化は無い。

ここで、少し考察。

1) valid.txtの不具合を解消して再度学習(valit.txt(train.txt)に画像のみを入れる。かつ、空行を入れない。)

2) ds3では1000 iterations位でap値が90%以上の好成績を出した。学習が上手く行っているかどうかを見るには、1000 iterations位で良いかもしれない。気になったら、そのタイミングで個別にdetect mapすれば良い。

3) 誤検出が多いのでやっぱり、学習データのバリエーションが足りない？（データ数のみでなく）  trainデータ中のゲーム画像の×のバリエーションが不足しているのではないか。しかし、これはたくさんのサンプル画像を用意する必要があり、かなりの手間ではある。しかし、100~200画像位ならなんとか努力の範囲かもしれない

4) tinyなのが悪い？昔、darknetを触り始めの頃に、普通にＤＬしてきたサンプルのweightとcfgを用いてbird/dogをdetectした所誤検出ばかりだったことを思い出した。しかし、tinyじゃない場合、非常に学習が遅いことも知っている。 

3)に関して、以下を思い出した。
オーグメンテーションはある程度精度が出ているモデルをさらに精度をよくするのには有用ですが、元々数枚程度しかバリエーションないものを水増しして1000枚にしたところで難しいのではないかと思います。
Deep Learning は数千、数万のサンプルを使ってパラメータを調整するという仕組みのものなので、サンプルが用意できないのであれば、画像処理など別のアプローチを考えたほうがよいと思います。

valid.txtの不具合を解消しもう一度、学習を実行する。
現時点でのログをmy_logs/nohup_ds4_20221117_2241.logに格納する。

まず、方針として1)の不具合を解消を実施し再度学習を進める。上手く行かない場合、tinyじゃないものに切り替える。それでも上手く行かない場合、やはり学習データが足りないと思われるので、バリエーションを増やしてみる。
  

ds4の再実行(valid.txtの不具合解消)
========================================

11/17 22:45開始〜11/18 20:53で、iterationsが2985回。::
  
   (next mAP calculation at 3000 iterations) 
   2985: 0.178416, 0.183888 avg loss, 0.002610 rate, 26.172093 seconds, 191040 images, 3701.297353 hours left
    v3 (iou loss, Normalizer: (iou: 0.07, obj: 1.00, cls: 1.00) Region 30 Avg (IOU: 0.000000), count: 1, class_loss = 0.000000, iou_loss = 0.000000, total_loss = 0.000000 
   v3 (iou loss, Normalizer: (iou: 0.07, obj: 1.00, cls: 1.00) Region 37 Avg (IOU: 0.152555), count: 27, class_loss = 0.386920, iou_loss = 1.759697, total_loss = 2.146617 
   total_bbox = 77221, rewritten_bbox = 0.000000 % 
   MJPEG-stream sent. 
   Loaded: 0.000039 seconds

apが0かつ、avgもこれ以上下がらないので、打ち切り。
my_logs/nohup_ds4_20221117-20221118.log


考察
---------

1) validの不具合は解消したにもかかわらず事象は改善しなかった

2) ds4で1000 iterationsを超えてもap値が0であった。依然としてやはり、学習データのバリエーションが足りないのかも

3) 誤検出は依然として多い

4) tinyのままである。tinyじゃないと上手くいくかもしれない。

このことから、2)と4)が怪しいポイントかと考えた。2)の学習バリエーションの増加は単純に結構な労力なので、とりあえず、4)を試してみる。

確かに、過去、素直にネットからDLしてきたtinyでdetectすると、かなり、サンプルのbirdやdogでさえ誤検出していた(tinyじゃないほうは誤検出せず)ので、4)はすこし、期待できる。ただし、学習時間は長くなるので、そこは覚悟


ds5の計画と実行
===================

ds5を作り、本家の以下にしたがい、cfgを修正した。
あとのobj.dataやtrain/validの画像データそのものはds4を継承している。

https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects

11/19 8:50より学習をスタート


データ処理の手順の半自動化
==============================

TOBE:やはり、バリエーションを増やすための作業の省力化をしたいものだ。
