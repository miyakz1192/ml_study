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
1000イテレーション以降,0.002610 avgになっており、それ以上は下がらない。一旦ずっと下がらない傾向が見えた場合、下がらないらしい。

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

11/19 8:50より学習をスタート。しかし、しばらくして50~70iterations位で以下のエラー。::

 (next mAP calculation at 1000 iterations) ESC]2;70/6000: loss=-nan hours left=717.2^G
  70: -nan, -nan avg loss, 0.000000 rate, 332.178208 seconds, 4480 images, 717.177361 hours left
  realloc(): invalid old size

https://github.com/pjreddie/darknet/issues/1460
のページを見ると、configurationがおかしいのでダブルチェックせよとのこと。
さらに、以下のＵＲＬを見ろとのこと。
https://github.com/AlexeyAB/darknet
本家やん。

本家のページを見るとネットワークサイズが416 x 416に対して使っているcfgが合っていなかったので、それに合わせた。
それ以外はもう一回見返してみたけど特に変な所はなさそう。といっても、もともと指定していたネットワークサイズは32で割り切れるので問題ないと
おもったけど、。。::

  #width=608 #もともと
  #height=608 #もともと
  width=416
  height=416

11/21 00:08にds5を再スタート。
しかし、同じようなエラーでコケる。ネットワークサイズを416にしてもダメだし。

考察
------

1) tinyじゃないやつでやるとreallocでエラー。cfg間の差分は以下。本家の説明を見ていると以下の説明。
　Create file yolo-obj.cfg with the same content as in yolov4-custom.cfg (or copy yolov4-custom.cfg to yolo-obj.cfg) and:
  yolov4-custom.cfgをそのままcopyしてきて使っているのだけどなぁ。

　そして、実際の差分は以下。説明通りに設定したが、batchが異なるので、これを戻してみたらどうか。つまり、max_batchesを500500に、stepsを400000,450000に戻す。tinyの方で上手くiterationsは回っていたのでその値を逆に非tinyに輸入したらどうかという発想。::

 miyakz@lily2:~/git_repos/darknet$ diff -u cfg/yolov4-custom.cfg  ds5/yolov4-custom.cfg 
 --- cfg/yolov4-custom.cfg	2022-11-09 13:22:42.407693069 +0000
 +++ ds5/yolov4-custom.cfg	2022-11-20 15:02:56.971210638 +0000
 @@ -5,8 +5,10 @@
  # Training
  batch=64
  subdivisions=16
 -width=608
 -height=608
 +#width=608
 +#height=608
 +width=416
 +height=416
  channels=3
  momentum=0.949
  decay=0.0005
 @@ -17,9 +19,9 @@
  
  learning_rate=0.001
  burn_in=1000
 -max_batches = 500500
 +max_batches = 6000
  policy=steps
 -steps=400000,450000
 +steps=4800,5400
  scales=.1,.1
  
  #cutmix=1
 @@ -960,14 +962,14 @@
  size=1
  stride=1
  pad=1
 -filters=255
 +filters=18
  activation=linear
  
  
  [yolo]
  mask = 0,1,2
  anchors = 12, 16, 19, 36, 40, 28, 36, 75, 76, 55, 72, 146, 142, 110, 192, 243, 459, 401
 -classes=80
 +classes=1
  num=9
  jitter=.3
  ignore_thresh = .7
 @@ -1048,14 +1050,14 @@
  size=1
  stride=1
  pad=1
 -filters=255
 +filters=18
  activation=linear
  
  
  [yolo]
  mask = 3,4,5
  anchors = 12, 16, 19, 36, 40, 28, 36, 75, 76, 55, 72, 146, 142, 110, 192, 243, 459, 401
 -classes=80
 +classes=1
  num=9
  jitter=.3
  ignore_thresh = .7
 @@ -1136,14 +1138,14 @@
  size=1
  stride=1
  pad=1
 -filters=255
 +filters=18
  activation=linear
  
  
  [yolo]
  mask = 6,7,8
  anchors = 12, 16, 19, 36, 40, 28, 36, 75, 76, 55, 72, 146, 142, 110, 192, 243, 459, 401
 -classes=80
 +classes=1
  num=9
  jitter=.3
  ignore_thresh = .7
 miyakz@lily2:~/git_repos/darknet$ 

2) 1)が上手く行かない場合、yolo3にしてみる？ 

3) ds4で1000 iterationsを超えてもap値が0であった。依然としてやはり、学習データのバリエーションが足りないのかも


3)以降については、そもそも、reallocでコケる問題を先に解消する必要あり優先度は低め。


ds5の再実行
===========

まずはmax_batchesを500500に、stepsを400000,450000に戻すという、tinyで採用されていたパラメータ値を使ってやってみることにする。
11/21 23:00ころからスタート一時間くらいで同じエラー

再考察&実行
-------------

yolov4-custom.cfgじゃなくて、yolov4.cfgをベースにしてみては、、、と思う。
これで再度リトライしたい。

11/22 00:30位にスタート::
  miyakz@lily2:~/git_repos/darknet$ ./train_ds.sh ds5 big_not_customcfg

結果は同じエラー

再考察
-------

といいうことで、yolov4でやることは尽くした感じがある。
yolov2でやってみる
https://github.com/AlexeyAB/darknet/tree/47c7af1cea5bbdedf1184963355e6418cb8b1b4f#how-to-train-to-detect-your-custom-objects

ds5へのyolov2の組み込み(作業ログ)
======================================

以下のように実施。::

  miyakz@lily2:~/git_repos/darknet$ cp cfg/yolov2-voc.cfg ds5/
  miyakz@lily2:~/git_repos/darknet$ 

  miyakz@lily2:~/git_repos/darknet$ diff -u cfg/yolov2-voc.cfg ds5/yolov2-voc.cfg 
  --- cfg/yolov2-voc.cfg	2022-11-09 13:22:42.407693069 +0000
  +++ ds5/yolov2-voc.cfg	2022-11-22 10:16:00.284410102 +0000
  @@ -1,7 +1,7 @@
   [net]
   # Testing
  -batch=1
  -subdivisions=1
  +batch=64
  +subdivisions=8
   # Training
   # batch=64
   # subdivisions=8
  @@ -234,14 +234,14 @@
   size=1
   stride=1
   pad=1
  -filters=125
  +filters=30
   activation=linear
   
   
   [region]
   anchors =  1.3221, 1.73145, 3.19275, 4.00944, 5.05587, 8.09892, 9.47112, 4.84053, 11.2364, 10.0071
   bias_match=1
  -classes=20
  +classes=1
   coords=4
   num=5
   softmax=1
  miyakz@lily2:~/git_repos/darknet$ 
  
  
  miyakz@lily2:~/git_repos/darknet$ cat train_ds_yolov2.sh 
  
  ddir=$1
  kind=$2
  
  if [ $# -ne 2 ]; then
  	echo "ERROR: data dir name is req, tiny or big, or big_not_customcfg"
  	exit 1
  fi
  
  
  set -x
  
  if [ ${kind} == "tiny" ];then
    echo "ERROR"
  elif [  ${kind} == "big" ];then
    echo "big"
    nohup ./darknet detector train ${ddir}/obj.data ${ddir}/yolov2-voc.cfg ${ddir}/darknet19_448.conv.23 -dont_show -mjpeg_port 8090 -map &
  elif [  ${kind} == "big_not_customcfg" ];then
    echo "ERROR"
  else
    echo "ERROR: no such option"
    exit 2
  fi
  
  
  
  miyakz@lily2:~/git_repos/darknet$ 
  

11/22 19:20よりスタート結果、avgがnanになる結果はかわらず。
my_logs/nohup_ds5_yolov2.log。
同じようなパラメータでtinyだったらnanにならなかったことを思い出す。
精度は期待できないが、yolov2のtinyでやってみる。::
  
  miyakz@lily2:~/git_repos/darknet$ diff -u cfg/yolov2-tiny-voc.cfg ds5/yolov2-tiny-voc.cfg 
  --- cfg/yolov2-tiny-voc.cfg	2022-11-09 13:22:42.407693069 +0000
  +++ ds5/yolov2-tiny-voc.cfg	2022-11-22 13:15:07.529157461 +0000
  @@ -1,7 +1,7 @@
   [net]
   # Testing
  -batch=1
  -subdivisions=1
  +batch=64
  +subdivisions=8
   # Training
   # batch=64
   # subdivisions=2
  @@ -115,13 +115,13 @@
   size=1
   stride=1
   pad=1
  -filters=125
  +filters=30
   activation=linear
   
   [region]
   anchors = 1.08,1.19,  3.42,4.41,  6.63,11.38,  9.42,5.11,  16.62,10.52
   bias_match=1
  -classes=20
  +classes=1
   coords=4
   num=5
   softmax=1
  miyakz@lily2:~/git_repos/darknet$ 

やっぱりだめ。yolov2でもだめだった。::

   69: -nan, -nan avg loss, 0.000100 rate, 39.914736 seconds, 4416 images, 421.417908 hours left
   known client: 4, sent = 181230, must be sent outlen = 181230
    MJPEG-stream sent. 
   Loaded: 0.000022 seconds
   Region Avg IOU: 0.000000, Class: nan, Obj: -nan, No Obj: -nan, Avg Recall: 0.000000,  count: 3
   Region Avg IOU: 0.000000, Class: nan, Obj: -nan, No Obj: -nan, Avg Recall: 0.000000,  count: 4
   Region Avg IOU: 0.000000, Class: nan, Obj: -nan, No Obj: -nan, Avg Recall: 0.000000,  count: 3
   Region Avg IOU: 0.000000, Class: nan, Obj: -nan, No Obj: -nan, Avg Recall: 0.000000,  count: 2
   Region Avg IOU: 0.000000, Class: nan, Obj: -nan, No Obj: -nan, Avg Recall: 0.000000,  count: 3
   Region Avg IOU: -nan, Class: -nan, Obj: -nan, No Obj: -nan, Avg Recall: -nan,  count: 0
   Region Avg IOU: 0.000000, Class: nan, Obj: -nan, No Obj: -nan, Avg Recall: 0.000000,  count: 2
   Region Avg IOU: 0.000000, Class: nan, Obj: -nan, No Obj: -nan, Avg Recall: 0.000000,  count: 1
   
    (next mAP calculation at 100 iterations) ESC]2;70/40200: loss=-nan hours left=421.7^G
    70: -nan, -nan avg loss, 0.000100 rate, 39.945466 seconds, 4480 images, 421.653232 hours left
   known client: 4, sent = 181242, must be sent outlen = 181242
   realloc(): invalid old size

結果はmy_logs/nohup_ds5_invalid_realloc_yolov2.log。
ds5でyolov4のtinyをちょっと試しにやってみる。。。::

  cp ds4/yolov4-tiny-custom.cfg  ds5/
  cp ds4/yolov4-tiny.conv.29 ds5/

iterationsが88まで行っているがreallocエラーでコケることは無い。


考察
-----

まず、ds4のtinyの時の考察を再掲する。tinyの時のゲーム画像のcloseを認識するものの誤検出が激しく、

1) validの不具合は解消したにもかかわらず事象は改善しなかった

2) ds4で1000 iterationsを超えてもap値が0であった。依然としてやはり、学習データのバリエーションが足りないのかも

3) 誤検出は依然として多い

4) tinyのままである。tinyじゃないと上手くいくかもしれない。

ということで、まず、tiny以外でやろうと思って、ds5にてtiny以外を試したのだが、

  yolov4のnon tinyでreallocエラー

  yolov2のnon tinyでreallocエラー

ということで、なぜか、tiny以外だとダメである。なぜだろう。

5) ここでふと思ったのだが、まず、確実に成功する方法でカスタムデータの学習を試してみることで自身をつけるのはどうだろう。

https://www.koi.mashykom.com/pytorch_3.html

6) あと、本家のページにも以下のヒントがある。これを活かしてみるのはどうだろう

https://github.com/AlexeyAB/darknet#how-to-improve-object-detection

・ネットワークのレゾリューションを上げる416 x 416から上に

・-show_imgsを付けて試してみる。  

・1 classごとに2000枚はほしいとのこと(現在のcloseは200枚程度)

・小さい画像だとストライドを調整したほうがよい。16 x 16が案内されているが、今回のcloseは 32 x  32。ストライドを調整しても良いのではないか。

7) yolov3のtinyで学習を進めてみる(記事tinyが怪しい点?いや、怪しくない点？を参照)

以下記事(tinyが怪しい点?いや、怪しくない点？)によって、yolov3のtinyなら大丈夫そうというコトがわかった。
かつ、今までの実績ベースでいくと、tinyなら学習がエラーせずに進む様子(1勝1敗、、、yolov4 tiny win , yolov2 tiny lose)。
かつ、いままで試したのはyolo2/4であって、yolov3は試してない。
ということで、ds5の再学習をyolov3のtinyで実施してみると、改善が期待できるのでは？
ためしにやってみる。

ds5の再学習
==============

yolov3のtinyで学習をすすめる。::

  miyakz@lily2:~/git_repos/darknet$ diff -u cfg/yolov3-tiny.cfg ds5/yolov3-tiny.cfg 
  --- cfg/yolov3-tiny.cfg	2022-11-09 13:22:42.407693069 +0000
  +++ ds5/yolov3-tiny.cfg	2022-11-22 17:09:46.956371282 +0000
  @@ -1,7 +1,7 @@
   [net]
   # Testing
  -batch=1
  -subdivisions=1
  +batch=64
  +subdivisions=16
   # Training
   # batch=64
   # subdivisions=2
  @@ -124,7 +124,7 @@
   size=1
   stride=1
   pad=1
  -filters=255
  +filters=18
   activation=linear
   
   
  @@ -132,7 +132,7 @@
   [yolo]
   mask = 3,4,5
   anchors = 10,14,  23,27,  37,58,  81,82,  135,169,  344,319
  -classes=80
  +classes=1
   num=6
   jitter=.3
   ignore_thresh = .7
  @@ -168,13 +168,13 @@
   size=1
   stride=1
   pad=1
  -filters=255
  +filters=18
   activation=linear
   
   [yolo]
   mask = 0,1,2
   anchors = 10,14,  23,27,  37,58,  81,82,  135,169,  344,319
  -classes=80
  +classes=1
   num=6
   jitter=.3
   ignore_thresh = .7
  miyakz@lily2:~/git_repos/darknet$ 

11/23 02:16より開始

早々とlose。reallocのいつものエラー::

  miyakz@lily2:~/git_repos/darknet$  grep avg nohup.out 
  avg_outputs = 324846 
  avg_outputs = 324846 
   1: 556.005249, 556.005249 avg loss, 0.000000 rate, 40.257556 seconds, 64 images, -1.000000 hours left
   2: 555.796509, 555.984375 avg loss, 0.000000 rate, 40.023119 seconds, 128 images, 5602.339534 hours left
   3: 556.233582, 556.009277 avg loss, 0.000000 rate, 40.137928 seconds, 192 images, 5601.925925 hours left
   4: 555.829895, 555.991333 avg loss, 0.000000 rate, 40.028085 seconds, 256 images, 5601.675859 hours left
   5: 556.016968, 555.993896 avg loss, 0.000000 rate, 40.083506 seconds, 320 images, 5601.275543 hours left
   6: 556.002319, 555.994751 avg loss, 0.000000 rate, 40.055308 seconds, 384 images, 5600.956159 hours left
   7: 555.905579, 555.985840 avg loss, 0.000000 rate, 40.106618 seconds, 448 images, 5600.600656 hours left
   8: -nan, -nan avg loss, 0.000000 rate, 40.373377 seconds, 512 images, 5600.319865 hours left
   9: -nan, -nan avg loss, 0.000000 rate, 41.320219 seconds, 576 images, 5600.412450 hours left
  miyakz@lily2:~/git_repos/darknet$ 


考察
-------
  
1) ds4で1000 iterationsを超えてもap値が0であった。依然としてやはり、学習データのバリエーションが足りないのかも

2) 誤検出は依然として多い(closeを検出するが誤検出多し)

3) tinyのままである。tinyじゃないと上手くいくかもしれない。

4) ここでふと思ったのだが、まず、確実に成功する方法でカスタムデータの学習を試してみることで自身をつけるのはどうだろう。

https://www.koi.mashykom.com/pytorch_3.html

5) あと、本家のページにも以下のヒントがある。これを活かしてみるのはどうだろう

https://github.com/AlexeyAB/darknet#how-to-improve-object-detection

・ネットワークのレゾリューションを上げる416 x 416から上に

・-show_imgsを付けて試してみる。  

・1 classごとに2000枚はほしいとのこと(現在のcloseは200枚程度)

・小さい画像だとストライドを調整したほうがよい。16 x 16が案内されているが、今回のcloseは 32 x  32。ストライドを調整しても良いのではないか。

6) yolov3 tinyで試した時、subdivisionsを16に設定。yolov4-tiny-customのほうが1となっており、数値に差が有り、気になる。

んー。かなりわからない状態になってきた。いままで学習がエラーせずに進むのはyolov4のtiny customしかない状況。他の代替手段が無いため、5)を試してみるしか無い状況。ds5の再実行を試してダメなら、4)をやってみよう。4)がもし上手く行くのならば、4)の成功をベースに白血球のデータをcloseに差し替えていけば学習が上手く行くはず（こっちのほうが近道か？）


ds5再実行
==========

ネットワークのレゾリューションを上げる。832 x 832にする

ストライドの調整。すでに1,2の値になっている::
  miyakz@lily2:~/git_repos/darknet$ grep stride= ds5/yolov4-tiny-custom.cfg  | sort | uniq
  stride=1
  stride=2
  miyakz@lily2:~/git_repos/darknet$ 
  
layersの値はcfgファイル上、負の値に設定されており、よくわからなく、調整を避けた。

11/23 02:35より学習開始。

結果と考察
---------------

結果はＮＧ。::

   layer   filters  size/strd(dil)      input                output
   0 conv     32       3 x 3/ 2    832 x 832 x   3 ->  416 x 416 x  32 0.299 BF
   (snip)
    (next mAP calculation at 1000 iterations) ESC]2;285/500200: loss=-nan hours left=14394.2^G
    285: -nan, -nan avg loss, 0.000017 rate, 102.712098 seconds, 18240 images, 14394.152970 hours left


結果はmy_logs/nohup_ds5_nan.log

再掲

【効果があるかもしれない施策】

1) ds4で1000 iterationsを超えてもap値が0であった。依然としてやはり、学習データのバリエーションが足りないのかも

2) 誤検出は依然として多い(closeを検出するが誤検出多し)

4) ここでふと思ったのだが、まず、確実に成功する方法でカスタムデータの学習を試してみることで自身をつけるのはどうだろう。

https://www.koi.mashykom.com/pytorch_3.html

6) yolov3 tinyで試した時、subdivisionsを16に設定。yolov4-tiny-customのほうが1となっており、数値に差が有り、気になる。


【すでに試して効果がなかった施策】

3) tinyのままである。tinyじゃないと上手くいくかもしれない。 →　これは意味なし。

5) あと、本家のページにも以下のヒントがある。これを活かしてみるのはどうだろう
https://github.com/AlexeyAB/darknet#how-to-improve-object-detection
やったことネットワークのレゾリューションを832 x 832、subdivisionsは1のまま


ここでやっぱり残りの（多分、本当にラストの）施策は4)だと思う。

Mashykomの実行
===================

https://www.koi.mashykom.com/pytorch_3.html
のサイトのYOLOv4-Darknetモデルの学習の所を参照して試す。

まず、https://github.com/mashyko/darknet
にcfgまで置かれているので、レポジトリごとcloneしてくる。
と思ったら、不幸なことに存在しない。。。。

cfgファイルの作り方はここが参考になるかも。
https://qiita.com/taichinakabeppu/items/e4d38f19c4041b9f4fc3

darknet/cfg/yolov4-custom.cfgを持ってきて書き換えると書いてある。
cfgは以下。::

  miyakz@lily2:~/git_repos/darknet$ diff -u cfg/yolov4-custom.cfg  blood/yolov4-custom.cfg 
  --- cfg/yolov4-custom.cfg	2022-11-09 13:22:42.407693069 +0000
  +++ blood/yolov4-custom.cfg	2022-11-23 02:22:58.453319909 +0000
  @@ -5,8 +5,8 @@
   # Training
   batch=64
   subdivisions=16
  -width=608
  -height=608
  +width=416
  +height=416
   channels=3
   momentum=0.949
   decay=0.0005
  @@ -17,9 +17,9 @@
   
   learning_rate=0.001
   burn_in=1000
  -max_batches = 500500
  +max_batches = 6000
   policy=steps
  -steps=400000,450000
  +steps=4800,5400
   scales=.1,.1
   
   #cutmix=1
  @@ -960,14 +960,14 @@
   size=1
   stride=1
   pad=1
  -filters=255
  +filters=24
   activation=linear
   
   
   [yolo]
   mask = 0,1,2
   anchors = 12, 16, 19, 36, 40, 28, 36, 75, 76, 55, 72, 146, 142, 110, 192, 243, 459, 401
  -classes=80
  +classes=3
   num=9
   jitter=.3
   ignore_thresh = .7
  @@ -1048,14 +1048,14 @@
   size=1
   stride=1
   pad=1
  -filters=255
  +filters=24
   activation=linear
   
   
   [yolo]
   mask = 3,4,5
   anchors = 12, 16, 19, 36, 40, 28, 36, 75, 76, 55, 72, 146, 142, 110, 192, 243, 459, 401
  -classes=80
  +classes=3
   num=9
   jitter=.3
   ignore_thresh = .7
  @@ -1136,14 +1136,14 @@
   size=1
   stride=1
   pad=1
  -filters=255
  +filters=24
   activation=linear
   
   
   [yolo]
   mask = 6,7,8
   anchors = 12, 16, 19, 36, 40, 28, 36, 75, 76, 55, 72, 146, 142, 110, 192, 243, 459, 401
  -classes=80
  +classes=3
   num=9
   jitter=.3
   ignore_thresh = .7
  miyakz@lily2:~/git_repos/darknet$ 
 
11/23 11:26より学習開始。
これで上手く行けば良いが、上手く行かない場合なにか根本的な所でミスがあると思っている。 

結果はＮＧ。やっぱり、根本的な所がへんだなぁ。::

 (next mAP calculation at 1000 iterations) ESC]2;30/6000: loss=-nan hours left=939.4^G
  30: -nan, -nan avg loss, 0.000000 rate, 328.933514 seconds, 1920 images, 939.408316 hours left
  realloc(): invalid old size

cfgファイルなどは改めて内容を確認したが問題は特になさそう。


考察(blood)
-----------------

web上の記事では(cfgファイルの内容は不明だが)すでに成功しているだろう事例だけに、今までとかなり事情が異なる。
reallocエラーの前にnanが出現することが特徴的であり、nanがreallocエラーを引き起こしていると想定して、
nanに関するissueが乗っている記事を探したら結構あった。

https://github.com/pjreddie/darknet/issues/622
　→　内容はよくわからない。結局ここに投稿している皆さんも解決方法が良くわからないそうだ。

https://github.com/pjreddie/darknet/issues/690
　→　上記よりも少し詳しいヒントが乗っている。

カウント= 0の場合、Nan値が返され、YOLOレイヤーに画像が渡されなくなります
だから、その時はYoloレイヤーのマスクを変更するだけです（私の理解）
私の場合、yolov3-tiny.config から最後のレイヤーのマスクを変更するだけです。
マスク = 0、1、2
に
マスク = 1、2、3
（これは私がランダムに行うもので、私にとってはうまくいきます）
ありがとう
　→　理由はよくわからないけど効くこともあるらしい。ランダムに行うというのが気になるが。。


My issue was solved when I changed my anchors according to my dataset by using
darknet.exe detector calc_anchors data/obj.data -num_of_clusters <number_of _anchors(9 is used for original yolo)> -width <your_width> -height <your_height>
　→　全く良くわからなんい。



@ztilottama : I used batch=64 and subdivisions=16, but it can be specific to your task. With single image SGD was diverging.


https://teratail.com/questions/303594
default config(batch=1, subdivisions=1) is just for test, uncomment Training batch=64 subdivisions=8 to train. correct me if i'm wrong


https://teratail.com/questions/242322
以下の変更を行うことで解決できました。

cfgファイルの設定を変更
learning_rate = 0.001　→　0.0001

学習率が変化する設定を最適に調整しないと、学習が発散するようです。


上記URLからポイントされている記事
https://touch-sp.hatenablog.com/entry/2017/09/21/182622

https://stackoverflow.com/questions/60158549/getting-nan-during-darknet-training-what-am-i-doing-wrong
幾つか記事はあるが、learning_rateの減少設定がある。

https://weekendproject9.hatenablog.com/entry/2018/04/30/205622
上手く行かなければ、batch,subdivisionsを1,1にするのが案内されている。
また、「＊学習過程で "-nan" が出てくるが学習における82,94,108のどれかで数字が出ていれば学習が進んでいる」

https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects
nanはavgフィールドに現れると学習が悪い方向に進んでいるが、そうでなければ特に問題はないということ。上記ＵＲＬも同じ記事がある。

https://github.com/pjreddie/darknet/issues/1460
reallocエラーに関する記事がそもそも少ないのだが、やはり、nanが原因の様子。

他の記事だと
https://teratail.com/questions/113758
reallocに渡すポインタはあらかじめmalloc/calloc/reallocされたものか、さもなくばNULLじゃないといけないんですよー。
https://linuxjm.osdn.jp/html/LDP_man-pages/man3/malloc.3.html

ということで、そもそものプログラミングの問題があるのかもしれない。だが、avgでnanが出ている事自体、学習が進んでいない（悪い状態）なので、
これを解決することがやはり、再優先課題かと。


https://anton0825.hatenablog.com/entry/2018/03/16/000000
「学習途中で出力される評価指標がnanになることがあるが正常らしい。評価指標の計算式的に仕方ないのかも？ずっとnanが続くようだとだめだけど、学習データの中に物体のlabelが一つも含まれないような場合ではnanになるのは正常らしい。」
とのことでこのＵＲＬの記事中にもあるように、nanがあるけど、avgフィールドにnanが無いため学習としては正常ということか。

https://stackoverflow.com/questions/37232782/nan-loss-when-training-regression-network
「出力が無制限であるため、ニューラル ネットワークを使用した回帰は機能しにくいため、勾配の爆発の問題が特に発生しやすくなります (nans の原因となる可能性があります)。

歴史的に、勾配爆発の 1 つの重要な解決策は学習率を下げることでしたが、Adam のようなパラメーターごとの適応学習率アルゴリズムの出現により、優れたパフォーマンスを得るために学習率を設定する必要がなくなりました。あなたがニューラル ネットワークのマニアで、学習スケジュールを調整する方法を知っていない限り、SGD を勢いで使用する理由はほとんどありません。

試してみることができる可能性のあるいくつかのことを次に示します。

変位値正規化または z スコアリングによって出力を正規化します。厳密に言うと、データセット全体ではなく、トレーニング データに対してこの変換を計算します。たとえば、変位値の正規化では、サンプルがトレーニング セットの 60 パーセンタイルにある場合、値は 0.6 になります。 (また、0 パーセンタイルが -0.5 で 100 パーセンタイルが +0.5 になるように、正規化された分位値を 0.5 だけシフトすることもできます)。

ドロップアウト率を上げるか、重みに L1 および L2 ペナルティを追加して、正則化を追加します。 L1正則化は機能選択に似ています。機能の数を5に減らすとパフォーマンスが向上するとおっしゃっていたので、L1もそうかもしれません。

それでも問題が解決しない場合は、ネットワークのサイズを縮小してください。これはパフォーマンスに悪影響を与える可能性があるため、常に最良のアイデアとは限りませんが、あなたのケースでは、入力機能 (35) に対して多数の第 1 層ニューロン (1024) があるため、役立つ場合があります。

バッチ サイズを 32 から 128 に増やします。128 はかなり標準的な値であり、最適化の安定性を向上させる可能性があります。」

→　調整するべきは、学習率(効果が無いかもしれない？）、ネットワークサイズの縮小？


https://discuss.tensorflow.org/t/getting-nan-for-loss/4826
斜め読みしかできていないが、layerを接続する際にデータを正規化していない場合に、nan現象が発生しやすいとのこと。
(たしかに、ある程度の値の範囲で正規化されていれば、nanのような問題は発生しなきがする。しかし、ここはdarknetのプログラミング領域なので、
ちょっと手がだしにくい)

https://github.com/AlexeyAB/darknet
本家だと、If you get a Nan, then for some datasets better to decrease learning rate, for 4 GPUs set learning_rate = 0,00065 (i.e. learning_rate = 0.00261 / GPUs). In this case also increase 4x times burn_in = in your cfg-file. I.e. use burn_in = 4000 instead of 1000.
ただし、こちらはマルチＧＰＵの場合だ。ＣＰＵの場合はどうなのか？？
srcを見ているとburn_inはgpu関連によく出てくるパラーメタのようなので、burn_inの調整はCPUの場合にとって関係性がかなり低いと思われる。


http://cedro3.com/ai/pytorch-ssd-bccd/
この記事を見ると、完全コピペだけど、pytorchで物体検出のtrainingや検出もできちゃうんじゃないか？
という気になってしまう。darknetでさんざんやって上手く行かない場合、こちらの挑戦してしまうというのも最終的な手かもしれない。


【まとめ】
nanを避けるための設定

1) yoloレイヤのマスクを変更する(0,1,2 → 1,2,3) 

2) アンカーの設定を変更する(よくわからないが)

3) batchやsubdivisionsを調整する(タスクによるとのことだが)

4) learning_rateの変更(0.001 to 0.0001)

5) batchとsubdivisionsを1に変更する。

6) ネットワークサイズを縮小する

7) バッチサイズを増やす


まず、5でやってみている。
だけど、別記事によれば、逆で64,8に設定するべきとも読める。
けどもまぁ、試しに1,1でやってみる。

blood再実行
===============

batch=64, subdivisions=8(16から8に変更)は、nanが発生する(my_logs/nohup_blood_realloc_error2.log)。
batchとsubdivisionsを1にしてみると、どうか？

A) batch,subdivisions=1　→　NG(my_logs/nohup_blood_realloc_error3.log)
B) learning_rate=0.0001 and A) →  NG(my_logs/nohup_blood_realloc_error4.log)
C) batch,subdivisions=64,16 and learning_rate=0.0001 →　NG my_logs/nohup_blood_realloc_error5.log
D) network size = 160(width,height) ※  416 x 416から変更 and learning_rate=0.0001 →　 NG(my_logs/nohup_blood_realloc_error6.log)
E) 最後のyoloレイヤのマスクを6,7,8から7,8,9に変更 NG(error7)

learning_rateをもっと低くしてみるのも良いかも？？？あとはネットワークサイズの縮小やmask変更？くらいかしか残されていない。
あと、これで上手く行かなかったら、yolov4 tinyでもう一回学習が回るか（回った結果、誤検出が多い重みが生成されてしまうが)？

あと、お試しのサーバ再起動？？14日間連続稼働しているのも何か悪影響合ったりして(本当か？なんだそれ？？)

んー。一応、ds4 tinyで上手く言った時も本当に大丈夫なのかな、、、と思ってds4 tinyを学習開始

→　上手く言っている(my_logs/nohup_ds4.log)

考察
------

もはや、yolov4 tinyしか学習が上手く行かないので、脇目を振らず、ds4を中心にyolov4 tinyで
学習を改善するしか無いのではないか。

11/24 20:43学習開始

ds6の計画
=============

ds4からcopyしてds6を作る。違う所はtrain.txtが200に対してvalidが400程度。
この数値を逆転する。すなわち、train.txtとvalid.txtを入れ替えて学習をトライしてみる。

しかし、avgが下がらないし、ap値も0のままで、、、my_logs/nohup_ds6.log

考察
-----

特に変わらず。1000 iterationsでap=0。なんでだ。

1) trainデータの数が足りていない(1000位は必要？）

2) trainデータがいい加減。明らかにcloseじゃない図形も含まれてしまっている

3) 画像サイズが大きすぎる。yoloでは416 x 416が標準らしいので、trainとvalidもそれに合わせる。ゲーム画像は416 x 416のパターンに分割してしまう。ゲーム画像の下半分は不要なので、上半分だけを抽出して416 x 416の画像を複数つくる

4) yolov4 tinyしか学習が回らないため、yolov4 tinyを使うしか無い

5) bloodをyolov4 tinyで回してみる(学習が1634 iterationsまで回っているds6のconfig/weightをbloodで利用する)


blood by yolov4 tiny
======================

ds6で1634も回ったyolov4 tinyのcfg/weightを使えば学習が絶対に上手く行くはず。
11/25 21:44学習開始!
yolov4 tiny以外では60iterations未満でnanになっていたが、現在293 iterations回っている所をみると、
上手く学習が進みそうな気配がある.

11/26 1:49現在、539 iterations回っており、avgも順調に下がっているので良い感じかもしれない。

結局約5000 iterations位回ったが途中でavgがnanになり、"mean average precision (mAP@0.50) = 0.281002, or 28.10 % "
を最高値として叩きだしたが学習が途中で頓挫した結果になった(my_logs/nohup_blood_mAP_0_28.txt)。

考察(blood by yolov4 tiny)
-----------------------------

1) やはり、学習が回るのはyolov4 tinyくらしかないのでは

2) yolov4 tinyでも約2000 iterationsくらいまでは好調だった。つまり、2000 iterations位で良いmAP値が出せればＯＫ
   (ds3は1000 iterationsくらいでmAPが80%位だった)

4) bloodが416 x 416なので、この画像がベストサイズなのではないか。

ds7の計画
===========

tranデータの水増しを優先しすぎて、あきらかにcloseの形をしていないものが多く有り、
こういった間違ったデータは精度に多大なる影響があるとのこと(annotationがミスっていると
まずいtrainデータになるとのこと)のため、改めてtrainデータの再生成を行う。

まずは、手始めに単純な基本的なcloseを作り、それを数百パターンにaugumentationする。
それを416 x 416画像にして(32 x 32画像のcloseを(0,0)に配置して、残りの余白を白にする)

それだけの世界でtrain/validで学習できるかをyolov4 tinyで試してみる。
学習データの再生成を実施する

改善点

1) closeの移動や回転の具合が大きすぎてcloseの図形になっていなかったためパラメタを調整。変化率を抑えた
2) 移動や回転時に補完方法がnearlestになっておりcloseの図形が崩れたのでconstantを指定して周りに同調した

一応、画像はできた(990画像)。どうせなので画像を生成したあとの定形作業は自動化したい。
(blood by yolov4 tinyの学習進行状態などをみつつ。。。）

ds7はds6ベースにして学習をすすめる。以下の2 STEPに分けてやって見る

STEP1) ゲームの画像なしでdata_augmentationしたデータをtrainとvalidに分けて学習する。
　　　 もし、ここで良い結果が得られたら、yolov4 tinyで学習がすすめることが出来そうだ
       (mAP値を80%目標)とする


STEP2) もし、上記目標を達成できたら、今度は集めたゲーム画像を416 x 416に分けてvalidデータに追加する。

STEP1が上手く行かなかったら諦めて他のフレームワークを試してみることにする。

STEP1を11/27 23:52開始

STEP1が12/2 に14677 iterationsで停止。大体4日iterationsさせて、結果は65%だった。
やはり、nanになり、学習が停止

学習したデータ自体は良く検出するが(クラス数が1なので、確率値が低くても大丈夫),
ゲーム画像だと全くだめ。

file:///home/miyakz/git_repos/darknet/predictions.jpg

ということで、学習の正答率が上がらないため、darknetの試行はこれにて終了する。

考察
====

今回、darknetを使ったことが良くない点だったかもしれない。
yolov4を使った物体検出ではなく、deep Learningとヒューリスティック観点、
および、通常の画像処理を組み合わせたアプローチを考える。

そもそも、ゲーム画像のバッテンマーク(close)を検出する目的で、yolov4の物体検出を
使おうとしたが全く上手くは行かなかった(せいぜい65%)。

一方で、物体検出ではない画像判別はゼロつくなどを中心にいくらでも理論やコードが
豊富にあると思う。

なので、枯れた画像判別をベースにして、ゲーム画像をある単位のピクセル幅でずらしながら、
32 x 32の画像を抽出して、それを画像判別のDL器にかけていくと、非常に計算量は
多くなるがバッテンを判別できるようになるのではないか。という新しいアイデア。

これをやってみることにする。


tinyが怪しい点?いや、怪しくない点？
---------------------------------------

以下で実行してみたら、ありえない結果になり、かつ、コマンドが復帰しない!::

  miyakz@lily2:~/git_repos/darknet$ ./darknet detect cfg/yolov4-tiny.cfg org_weight/yolov4-tiny.conv.29 data/eagle.jpg 
   GPU isn't used 
  mini_batch = 1, batch = 1, time_steps = 1, train = 0 
  nms_kind: greedynms (1), beta = 0.600000 
  nms_kind: greedynms (1), beta = 0.600000 
  
   seen 64, trained: 0 K-images (0 Kilo-batches_64) 
   Detection layer: 30 - type = 28 
   Detection layer: 37 - type = 28 
  data/eagle.jpg: Predicted in 154.500000 milli-seconds.
  bus: 100%
  fire hydrant: 100%
  bench: 100%
  cat: 100%
  horse: 100%
  sheep: 100%
  cow: 100%
  elephant: 100%
  bear: 100%
  zebra: 100%

ここで中断.
しかし、以下のURLの通り実施してみると、tinyの精度はちょっと悪いけど、ちゃんと検出する。yolov4のtinyが悪い？？？

https://pjreddie.com/darknet/yolo/

こんな感じ。::

  wget https://pjreddie.com/media/files/yolov3-tiny.weights
  ./darknet detect cfg/yolov3-tiny.cfg org_weight/yolov3-tiny.weights data/dog.jpg
  ./darknet detect cfg/yolov3-tiny.cfg org_weight/yolov3-tiny.weights data/eagle.jpg 
  


ちょっと分析っぽい
---------------------

cfgファイルのwidth,heightを変えてもログの以下の表示は変わらない。::

  Resizing, random_coef = 1.40 
  
   608 x 608 
  Loaded: 0.500794 seconds

一体、この608 x 608はどこから来ているのだろう。多分ソース上、ここ。::

  detector.c:234:                printf("\n %d x %d  (batch = %d) \n", dim_w, dim_h, net.batch);
  detector.c:237:                printf("\n %d x %d \n", dim_w, dim_h);
  detector.c:331:                printf("Resizing to initial size: %d x %d ", init_w, init_h);

detector.cによると以下。一発デバッグprintfでも仕込んでやれば何かわかるだろうな。::

    194     while (get_current_iteration(net) < net.max_batches) {
    195         if (l.random && count++ % 10 == 0) {
    196             float rand_coef = 1.4;
    197             if (l.random != 1.0) rand_coef = l.random;
    198             printf("Resizing, random_coef = %.2f \n", rand_coef);
    199             float random_val = rand_scale(rand_coef);    // *x or /x
    200             int dim_w = roundl(random_val*init_w / net.resize_step + 1) * net.resize_step;
    201             int dim_h = roundl(random_val*init_h / net.resize_step + 1) * net.resize_step;

多分、dim_wとdim_hを決めている式の右辺の乗算の左側が常に1に近くなり、かつ、net.resize_stepが608であれば、いつも、dim_wとdim_hは608になるのだろう。多分、そのような値にconfigurationされているように思える。resize_stepを決めているのは以下。configにresize_stepがなければデフォルトで32が入る気がする。::

  src/parser.c:1234:    net->resize_step = option_find_float_quiet(options, "resize_step", 32);

configではresize_stepは設定していないので、::

  miyakz@lily2:~/git_repos/darknet$ grep -rn resize_step ds5/*
  miyakz@lily2:~/git_repos/darknet$ 

dim_wとdim_hが608になるためには、右辺の乗算の左側が19になる必要がある。ところで、init_wはnet.wだ。::

  src/detector.c:120:    const int init_w = net.w;

んで、net.wを設定している箇所は::

  src/parser.c:1209:    net->w = option_find_int_quiet(options, "width",0);
  src/network.c:580:    net->w = w;

であるが、int resize_network関数でいろいろとwとhが更新されており、最終的にはoutput層のwとhになるらしい。
なので、ここで表示されているwとhは純粋にinputではないのかもしれない。たしかに、inputは変更後の416 x 416になっているため問題ないんだろうなぁ::

   layer   filters  size/strd(dil)      input                output
   0 conv     32       3 x 3/ 1    416 x 416 x   3 ->  416 x 416 x  32 0.299 BF

データ処理の手順の半自動化
==============================

やはり、バリエーションを増やすための作業の省力化をしたいものだ。
以下の手順で今の所実施している。

A)data_augmentationで自動生成したclose画像の処理とその自動化(./get_augmentation_data.sh)
---------------------------------------------------------------------------------------------

1) data_augmentationのサーバでjupyterを使ってtrain/valid画像を生成。こちらは画像を見ながらいろいろと試行錯誤しながら実施している(data_augmentationするコードの修正と仮生成したtrain/valid画像をいろいろと試行錯誤。このプロセスで生成された仮生成画像は、あくまで仮)

2) train/valid画像がよさ気だと思ったら、本生成 

3) この場でannotationのtxtも自動生成してしまう
   (data_augmentationした416 x 416の画像のアノテーションの位置は固定。)

4) 本生成したtrain/valid画像(annotationのtxtも込)をtar.gzで固める

なお、tar.gzのファイル名はdata_augmentation_close_img.tar.gz

A-1) data_augmentationした416 x 416画像のアノテーションtxtをつくる
-----------------------------------------------------------------------

滅多にやる必要はない。data_augmentationした画像の全体画素数を変更したら、
アノテーションtxtを再度生成する必要がある。

data_augmentationサーバからimglabelingサーバに画像を1つだけ送って、
imglabelingサーバでアノテーションを作る必要がある。以下、その手順。

まず、data_augmentationサーバにある416 x 416画像(座標0,0に32 x 32のclose画像が配置)のうち、任意の１つを
imagelabelingサーバに転送する。::

  scp 88.jpg a@192.168.122.237:/home/a/close_data/

次にimagelabelingサーバでimagelabelingツールを実行する::

  a@imglabeling:~/labelImg$ ./run.sh 

続けて得られた88.xml(VOC形式)。参考までに全体を乗せておく::

  @imglabeling:~/close_data$ cat 88.xml 
  <annotation>
  	<folder>close_data</folder>
  	<filename>88.jpg</filename>
  	<path>/home/a/close_data/88.jpg</path>
  	<source>
  		<database>Unknown</database>
  	</source>
  	<size>
  		<width>416</width>
  		<height>416</height>
  		<depth>1</depth>
  	</size>
  	<segmented>0</segmented>
  	<object>
  		<name>close</name>
  		<pose>Unspecified</pose>
  		<truncated>1</truncated>
  		<difficult>0</difficult>
  		<bndbox>
  			<xmin>1</xmin>
  			<ymin>1</ymin>
  			<xmax>32</xmax>
  			<ymax>32</ymax>
  		</bndbox>
  	</object>
  </annotation>
  a@imglabeling:~/close_data$ 


ツールのrectangle選択ではymaxが31になったが、後にvimで32に編集した.
txtに変換する::

  python3 /home/a/rtod/Tools/prepare.py -s ./ -yf 25 -cpy "./ds7/"

生成された88.txtを見てみる::

  a@imglabeling:~/close_data$ cat 88.txt 
  0 0.039663 0.039663 0.074519 0.074519
  a@imglabeling:~/close_data$ 

最初のエントリはラベルなので0(close)でＯＫ。
2番め：annotation対象の中心座標(x)を画像のwidthで割ったもの
3番め：annotation対象の中心座標(y)を画像のheightで割ったもの
4番目: annotation画像のwidthを画像のwidthで割ったもの
5番目: annotation画像のheightを画像のheightで割ったもの

計算結果は大体合っている。::

  a@imglabeling:~/close_data$ ruby -e "puts 16.0/416.0"
  0.038461538461538464
  a@imglabeling:~/close_data$ ruby -e "puts 16.0/416.0"
  0.038461538461538464
  a@imglabeling:~/close_data$ ruby -e "puts 32.0/416.0"
  0.07692307692307693
  a@imglabeling:~/close_data$ ruby -e "puts 32.0/416.0"
  0.07692307692307693
  a@imglabeling:~/close_data$ 

新しいデータで、data_augmentationサーバのcreate_annotation_txt.shの
データの箇所を変更する(template変数)。

A)の作業を再度実施する。具体的にはlily2で以下のシェルを実行するのみ。::
  ./get_augmentation_data.sh


B)キャプチャしたゲーム画像に関する処理
-----------------------------------------------------

以下の作業は完全に手作業で、今の所自動化はちょっとむずかしいか？？？

1) imglabelingサーバでラベリングする

2) ツールを使ってVOCからyolo形式に変換

3) tar.gzで固める

なお、tar.gzのファイル名はgame_screen_shots.tar.gz


C) 統合する
---------------

1) A)とB)のtar.gzをlily2に持って行き、dsX(Xは正の整数)のディレクトリに格納する

2) 解答してclose_dataに入る

3) ツールを実行して、train.txtとvalid.txtを作る

4) obj.dataの中のパスをdsXにしておく(一度やればＯＫ)




