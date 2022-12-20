=============================================
pytorchの練習
=============================================

以下のサイトを見ながら練習をしてみる。

参考URL
========

1) https://www.alpha.co.jp/blog/202207_01
2) https://tips-memo.com/pytorch-dataset
3) https://venoda.hatenablog.com/entry/2020/10/11/221117#31-%E3%83%87%E3%83%BC%E3%82%BF%E6%BA%96%E5%82%99
4) https://rightcode.co.jp/blog/information-technology/torch-optim-optimizer-compare-and-verify-update-process-and-performance-of-optimization-methods
5) http://cedro3.com/ai/pytorch-ssd-bccd/

X) https://github.com/miyakz1192/ml_study.git

最初の最初
===========

一番最初(1)のURLを見ながら実施してみると簡単にできた。
ただし、認識精度はだいぶ悪いようすで、転移学習、ファインチューニングなどの方法が必要とのこと。
しかし、このトライは白黒の様子で、本当はカラーでやりたい。


次に(2)、カラー
=====================

2)のURLがカラーの様子。
こちらを参考にやると、まずは、closeのモデルは作れそうな予感がする。
data augmentationも実施してくれるということで素晴らしい。。。。

X)に2)のコードをコピペしたものがあるfirst.py。

これは約5種位の犬の画像識別をするサンプルプログラムなのだが、
エポックを回してみると、全然正答率が低い感じ。

けども、darknetよりも確実に結果が出そうではある。

プログラムも非常に見通しが良いので、犬の画像をcloseに置き換えれば、closeの
学習過程が簡単にできそうである。darknetよりもずっと簡単そうだ。。。。

あとは4)などを試してみて、正答率が上がるかどうか、、、というところか。::

  Epoch 30/30
  -------------
  train Loss: 1.5886 Acc: 0.2845
  valid Loss: 1.5903 Acc: 0.3051
  a@pytorch:~/ml_study/pytorch/color$ 

次に(5)のSSDというやつ(大成功)
===============================

ここに乗っているレポジトリを参考にcloseデータを学習させたところ、非常に良い結果が
得られた。数時間の学習でゲーム画像内のcloseデータもちゃんと認識できた！
(darknetで悩んでいた数週間は一体何だったのだという位にあっさり行った)

ここのコードは信頼できるので、このコードをちゃんとforkしてclose検出(その他ゲームに現れる記号）を
認識させる学習フレームワーク基盤として発展させてい行きたい。

とりあえず、どのへんの座標を検出出来たのか出力できないので、
その機能を付けたい。

この辺の一連の話をjupyter notebookでビジュアルに振り返られるようにしておいておきたい。

なお、ゲーム画像を認識させる場合は、ゲーム画像は1080 x 2080位と大きいので、closeを含む画像を
416 x 416として抜き出してそれをjpgで保存して、入力させてやる必要がある。

しかし、検出時間は1秒位なので、416 x 416に分割されたとしても数回の作業で済むので
全く問題ない。

考察
-----

ゲーム画像についてはあまり成績は良くない。
概ね、1080 x 2400のため認識率が良くないと思われる::

  a@pytorch:~/close_ssd$ python3 first.py ./data/Screenshot_2022-11-11-00-31-27-10_56bd83b73c18fa95b476c6c0f96c6836.jpg

赤ちゃんの画像。closeは正しく認識されない。::

  a@pytorch:~/close_ssd$ python3 first.py ./data/Screenshot_2022-11-11-00-32-36-53_56bd83b73c18fa95b476c6c0f96c6836.jpg

井上尚弥の画像も同じう。

次に認識が失敗した画像を400 x 400くらいにすると見事認識した。
井上尚弥、赤ちゃんのほうも同じく。

したがって、ゲーム画像を認識させる場合には 400 x 400位の画像にしたほうが良いというコトがわかった。

トライ
=======

撮りためたゲーム画像をサンプルとして試してみる。
その前に手動で400 x 400を切り抜くのは大変なので、それを自動化するプログラムを組むことにする。


NGリスト
-----------


以下のファイルが正しくcloseが認識されない
file==> data/lu_Screenshot_2022-10-21-00-23-35-12_56bd83b73c18fa95b476c6c0f96c6836.jpg
ベーシックなcloseだが、全体が白のバックに薄い灰色の●　の中に白いバッテンが書かれているもの。
全く検出しない。

hit enter file==> data/lu_Screenshot_2022-11-11-00-41-06-93_56bd83b73c18fa95b476c6c0f96c6836.jpg
本当のcloseがそもそも含まれない画像。しかし、漢字をcloseとご検出してしまっている。
漢字が多いと確かに、closeのバッテン(クロス)が含まれるので、ここを誤検出している。
漢字は厄介だ。。。

hit enter file==> data/person.jpg
こちらは偶然混じった、darknetのサンプルファイル。理由はよくわからんけど、長靴の所とかを誤検出してしまっている。

hit enter file==> data/ru_Screenshot_2022-11-11-00-37-18-58_56bd83b73c18fa95b476c6c0f96c6836.jpg
本当のcloseがそもそも含まれない画像。宣伝のゲームの中にcloseと誤検出されるものが混じってしまっている。

hit enter file==> data/ru_Screenshot_2022-11-11-00-41-06-93_56bd83b73c18fa95b476c6c0f96c6836.jpg
本当のcloseが含まれる画像。カタカナのジを誤検出。また、本当のcloseは認識せず。全体背景が白をベースとした薄い青に、その上に薄いグレーに白い文字でバッテン。薄いグレーの中に横棒も混じってしまっているこのパターンは認識が難しい様子。

hit enter file==> data/lu_Screenshot_2022-12-05-20-23-33-26_56bd83b73c18fa95b476c6c0f96c6836.jpg
ゲーム画像を誤検出。見た感じバッテンの要素は全然なさそうだが、、、

hit enter file==> data/lu_Screenshot_2022-12-07-16-09-56-86_56bd83b73c18fa95b476c6c0f96c6836.jpg
漢字を誤検出

hit enter file==> data/lu_Screenshot_2022-12-08-18-32-13-36_56bd83b73c18fa95b476c6c0f96c6836.jpg
誤検出。ただし、0.6と低い数値だが。

hit enter file==> data/lu_Screenshot_2022-12-08-18-33-56-71_56bd83b73c18fa95b476c6c0f96c6836.jpg
漢字を誤検出。白色のバッテンを検出しないのはエライのだが、「残」を0.95とかなり高い確率で誤検出。

hit enter file==> data/lu_Screenshot_2022-12-08-23-17-20-54_56bd83b73c18fa95b476c6c0f96c6836.jpg
漢字「者」を0.84で高い誤検出

hit enter file==> data/lu_Screenshot_2022-12-09-00-20-49-28_56bd83b73c18fa95b476c6c0f96c6836.jpg
ゲーム中の顔？を0.95位で高い誤検出

hit enter file==> data/lu_Screenshot_2022-12-10-10-17-54-32_56bd83b73c18fa95b476c6c0f96c6836.jpg
なんと、">>"を0.95で誤検出。(これはこれで良い結果ではあるのだが。。。。？微妙！＿！＿！？)~

hit enter file==> data/ru_Screenshot_2022-12-05-20-05-24-88_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> data/ru_Screenshot_2022-12-08-18-31-56-89_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> data/ru_Screenshot_2022-12-08-18-27-03-36_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> data/ru_Screenshot_2022-12-08-18-32-03-84_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> data/ru_Screenshot_2022-12-08-18-32-13-36_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> data/ru_Screenshot_2022-12-08-23-19-13-78_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> data/ru_Screenshot_2022-12-09-00-20-49-28_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> data/ru_Screenshot_2022-12-08-23-17-20-54_56bd83b73c18fa95b476c6c0f96c6836.jpg
本当のcloseが含まれる画像。本当のcloseは認識せず。全体背景が白やほかの色（例：黄色など）をベースとした薄い青(あるいは灰色)に、その上に薄いグレーに白い文字でバッテン。薄いグレーの中に別の背景も混じっている画像(漢字も含む)。

hit enter file==> data/ru_Screenshot_2022-12-08-18-33-56-71_56bd83b73c18fa95b476c6c0f96c6836.jpg
充電の電池記号を0.86で誤検出。なんで。。。

hit enter file==> data/ru_Screenshot_2022-12-10-10-17-54-32_56bd83b73c18fa95b476c6c0f96c6836.jpg
closeは無いのだが、他の麻雀牌とか背景っぽいものをご認識してしまっている0.7位

グレー
-----------

hit enter file==> data/lu_Screenshot_2022-11-11-00-34-25-48_56bd83b73c18fa95b476c6c0f96c6836.jpg
本物のclose以外にも誤検出されているものがあるが、本当のcloseが1.00で検出されており、これはこれで正しい。
hit enter file==> data/lu_Screenshot_2022-11-11-00-39-39-59_56bd83b73c18fa95b476c6c0f96c6836.jpg


そもそもテストターゲットとしてcloseが400 x 400の中になかった
----------------------------------------------------------------

以下はcloseが存在しなかったがＮＧまたはＯＫの片割れの画像のため問題なし。

file==> data/lu_Screenshot_2022-10-21-00-21-51-38_56bd83b73c18fa95b476c6c0f96c6836.jpg
file==> data/lu_Screenshot_2022-10-21-00-21-51-38_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> data/lu_Screenshot_2022-10-21-00-25-42-95_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> data/lu_Screenshot_2022-11-11-00-32-36-53_56bd83b73c18fa95b476c6c0f96c6836.jpg

hit enter file==> data/ru_Screenshot_2022-10-21-00-23-35-12_56bd83b73c18fa95b476c6c0f96c6836.jpg
→　上記でNGとして検出されている画像の右上画像のため問題なし。
hit enter file==> data/ru_Screenshot_2022-11-11-00-31-27-10_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> data/ru_Screenshot_2022-11-11-00-34-25-48_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> data/ru_Screenshot_2022-11-11-00-35-14-37_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> data/ru_Screenshot_2022-11-11-00-35-55-52_56bd83b73c18fa95b476c6c0f96c6836.jpg

hit enter file==> data/ru_Screenshot_2022-11-11-00-47-07-72_56bd83b73c18fa95b476c6c0f96c6836.jpg

注目
------

hit enter file==> data/ru_Screenshot_2022-12-06-10-22-56-12_56bd83b73c18fa95b476c6c0f96c6836.jpg
別の背景が写り込んでいるのだが、closeを0.96で高く認識出来ている。
背景が写り込んでいるが、その上に濃いめの黒で塗られており（透けている）、その上に白地の×。
これは学習したclose記号そのもののパターン。


hit enter file==> data/ru_Screenshot_2022-12-07-16-09-56-86_56bd83b73c18fa95b476c6c0f96c6836.jpg
背景や漢字も混ざっているが、正しくcloseを認識0.98。やはり、すこし濃い目の黒がベースにある（背景や漢字が透けているが）。

hit enter file==> data/ru_Screenshot_2022-12-08-18-26-54-47_56bd83b73c18fa95b476c6c0f96c6836.jpg
0.64で認識。やはり、すこし濃い目の黒がベースにある

hit enter file==> data/ru_Screenshot_2022-12-08-23-30-31-53_56bd83b73c18fa95b476c6c0f96c6836.jpg
すごく小さいサイズのバッテンも（背景が黒で白のcloseであれば）、検出(0.94)できた。

考察
=====

現状、以下の学習が足りていない

1) 全体白地で、薄いグレーの上に白のclose（薄いグレーは透けている）
2) 様々な背景の上に、薄いグレーのベースがあり、その上に白のclose（薄いグレーは透けている）
3) ">>"を同じように学習させる

人間がcloseを認識出来ないようなものはゲーム画像としては出してこない。

1)のパターンのゲームの画像をvalidデータとしてannotationしたうえで学習させる必要があると思われる

トライ2
==========

NGリストの以下の8つのファイルを新たにtrain/valに分けて訓練開始::

  hit enter file==> data/ru_Screenshot_2022-12-05-20-05-24-88_56bd83b73c18fa95b476c6c0f96c6836.jpg
  hit enter file==> data/ru_Screenshot_2022-12-08-18-31-56-89_56bd83b73c18fa95b476c6c0f96c6836.jpg
  hit enter file==> data/ru_Screenshot_2022-12-08-18-27-03-36_56bd83b73c18fa95b476c6c0f96c6836.jpg
  hit enter file==> data/ru_Screenshot_2022-12-08-18-32-03-84_56bd83b73c18fa95b476c6c0f96c6836.jpg
  hit enter file==> data/ru_Screenshot_2022-12-08-18-32-13-36_56bd83b73c18fa95b476c6c0f96c6836.jpg
  hit enter file==> data/ru_Screenshot_2022-12-08-23-19-13-78_56bd83b73c18fa95b476c6c0f96c6836.jpg
  hit enter file==> data/ru_Screenshot_2022-12-09-00-20-49-28_56bd83b73c18fa95b476c6c0f96c6836.jpg
  hit enter file==> data/ru_Screenshot_2022-12-08-23-17-20-54_56bd83b73c18fa95b476c6c0f96c6836.jpg

訓練コマンド::
  
  a@pytorch:~/close_ssd$ python3 learn.py 

トライ2の結果と考察
=========================

上記トライ２のデータのうち、以下の１つだけが、0.72だった。他は誤検出か検出せず。::

  a@pytorch:~/close_ssd$ python3 first.py VOCdevkit/BCCD/JPEGImages/ru_Screenshot_2022-12-05-20-05-24-88_56bd83b73c18fa95b476c6c0f96c6836.jpg

少しだけ進歩したと言える。以前のweights/good_backup/20221212/close_weight.pthでは確かに0.72もスコアが出ない(というか検出せず)。

この結果から、訓練データを増やしたり工夫すれば良さそうであることがわかる

トライ3準備
===========

gaaのmemo.rstから引き継いだ以下の課題にトライ。

1.文字を変にcloseと認識してしまう。

　i.逆に大量の文字を学習させれば良い。これでcloseとの区別がつくようになるはず。
2.○　の中にバッテンのタイプを認識できない

　i.このタイプのcloseを学習させる必要あり
3.背景が透けているバッテンが認識されない。

　i.data augmentationで学習データを大量に作る必要がありか。

まず、課題の1から。作戦としては、いろいろとありそう。検討したものをとりあえず列挙していくが。

1. フリーのフォントをトレーニング画像として学習する。

   1. ただしこの方法ではフォントデータの中身を調べる必要があるのでめんどくさそう

2. matplotlibでテキスト描画してsavefigでjpegとしてsaveしてやる(32 x 32画像くらいか?)

   1. matplotlib周りはいじってきたのでなんとかなるか？

【重要な気づき】
そろそろ、pytorch_ssdの仕組みの詳細を知る必要があるかもしれない。
今closeのannotationのxmlファイルには種別がWBCだったり、closeだったりマチマチになっており、
本当にこれ、正しく認識出来るのかがよくわからなくなっているため。

トライ３結果
===============

漢字や日本語は誤検出が多いがそれなりに検出出来るようにはなった。しかし、以下のような困った事態が発生した

使った重みは以下。::
  a@pytorch:~/pytorch_ssd$ sha256sum close_weight_0.6436714378563133.pth
  15ba29eab2f8162bb5663d07acb812986c06b063a2bc542974e6db43a93cb94e  close_weight_0.6436714378563133.pth
  a@pytorch:~/pytorch_ssd$ 


1. 本物ののcloseなのにja_charと誤認識してしまう
   hit enter file==> imgdata/lu_Screenshot_2022-11-11-00-34-25-48_56bd83b73c18fa95b476c6c0f96c6836.jpg
   ただ、こちらは、白地に黒色のバッテン。いままで、黒字に白色のバッテンを学習していたので、コントラストが逆。
   このタイプのバッテンは一度もinputしていない。なので、ja_charと判定されたか。


2. 本物のcloseだけどcloseと認識しない。

   hit enter file==> imgdata/ru_Screenshot_2022-10-21-00-19-35-30_56bd83b73c18fa95b476c6c0f96c6836.jpg
   ちょっと太字な黒地に白のバッテン、バッテンの足が少し短い感じの


あと、薄いグレー地に白色のバッテンは相変わらず認識してくれない。
hit enter file==> imgdata/ru_Screenshot_2022-11-11-00-41-06-93_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/ru_Screenshot_2022-12-05-20-05-24-88_56bd83b73c18fa95b476c6c0f96c6836.jpg
hit enter file==> imgdata/ru_Screenshot_2022-12-07-15-40-28-75_56bd83b73c18fa95b476c6c0f96c6836.jpg
このバッテンは人間でもわかりにくい感じがするが、見分けがつく。
これより薄いグレーにしたら、インアクティブなバッテンとの区別がつかなくなりそうでかなり微妙な路線。

hit enter file==> imgdata/ru_Screenshot_2022-12-07-16-09-56-86_56bd83b73c18fa95b476c6c0f96c6836.jpg
これは漢字を背景に、薄いグレーの上に白地のバッテンが重なったもの。
closeは認識しないが、ja_charは認識した例。

hit enter file==> imgdata/ru_Screenshot_2022-12-08-18-27-03-36_56bd83b73c18fa95b476c6c0f96c6836.jpg
closeもja_charも特に認識しない。

hit enter file==> imgdata/ru_Screenshot_2022-12-08-23-17-20-54_56bd83b73c18fa95b476c6c0f96c6836.jpg
本物のcloseはあるのだけど、やっぱり薄いグレー地に白色のバッテンは弱い。
代わりに変な所をcloseと認識(0.62)


hit enter file==> imgdata/ru_Screenshot_2022-12-09-00-20-49-28_56bd83b73c18fa95b476c6c0f96c6836.jpg
ただ、どういうことか、こちらの画像では薄いグレー地に白のバッテンは0.83で認識
hit enter file==> imgdata/lu_Screenshot_2022-10-21-00-23-35-12_56bd83b73c18fa95b476c6c0f96c6836.jpg
同上(0.84)

あとは、画像残っていたけど、力尽きた。時間あれば追加確認。

以下、最初のトライでＮＧが出た画像で今回のトライで認識されていいるNG(例：薄グレー地に白バッテンなど)を除いたものを確認。
結果、誤検出はなくなり、今回の重みはかなり進歩していることが確認できた。

hit enter file==> data/lu_Screenshot_2022-11-11-00-41-06-93_56bd83b73c18fa95b476c6c0f96c6836.jpg
最初のトライ：「本当のcloseがそもそも含まれない画像。しかし、漢字をcloseとご検出してしまっている。
漢字が多いと確かに、closeのバッテン(クロス)が含まれるので、ここを誤検出している。
漢字は厄介だ。。。」
　→　漢字をcloseと誤認識することはなくなった。ja_charを数文字検出

hit enter file==> data/ru_Screenshot_2022-11-11-00-37-18-58_56bd83b73c18fa95b476c6c0f96c6836.jpg
最初のトライ：本当のcloseがそもそも含まれない画像。宣伝のゲームの中にcloseと誤検出されるものが混じってしまっている。
　→　closeの誤認識はなくなった。

hit enter file==> data/lu_Screenshot_2022-12-05-20-23-33-26_56bd83b73c18fa95b476c6c0f96c6836.jpg
最初のトライ：ゲーム画像を誤検出。見た感じバッテンの要素は全然なさそうだが、、、
　→　誤検出はなくなった。

hit enter file==> data/lu_Screenshot_2022-12-07-16-09-56-86_56bd83b73c18fa95b476c6c0f96c6836.jpg
最初のトライ：漢字を誤検出
　→　誤検出はなくなった。ja_charを数文字検出

hit enter file==> data/lu_Screenshot_2022-12-08-18-32-13-36_56bd83b73c18fa95b476c6c0f96c6836.jpg
最初のトライ： 誤検出。ただし、0.6と低い数値だが。
　→　closeの誤検出はなくなった。ja_charを２文字検出。ただし、いずれも誤検出。closeの誤検出はなくなったので良しとする。

hit enter file==> data/lu_Screenshot_2022-12-08-18-33-56-71_56bd83b73c18fa95b476c6c0f96c6836.jpg
 最初のトライ：   漢字を誤検出。白色のバッテンを検出しないのはエライのだが、「残」を0.95とかなり高い確率で誤検出。
　→　closeの誤検出はなくなった。ja_charを正しく検出。

hit enter file==> data/lu_Screenshot_2022-12-08-23-17-20-54_56bd83b73c18fa95b476c6c0f96c6836.jpg
 最初のトライ： 漢字「者」を0.84で高い誤検出
 →　誤検出はなくなった

hit enter file==> data/lu_Screenshot_2022-12-09-00-20-49-28_56bd83b73c18fa95b476c6c0f96c6836.jpg
 最初のトライ： ゲーム中の顔？を0.95位で高い誤検出
　→　誤検出はなくなった。

hit enter file==> data/ru_Screenshot_2022-12-08-18-33-56-71_56bd83b73c18fa95b476c6c0f96c6836.jpg
  最初のトライ： 充電の電池記号を0.86で誤検出。なんで。。。
　→　誤検出はなくなった。

hit enter file==> data/ru_Screenshot_2022-12-10-10-17-54-32_56bd83b73c18fa95b476c6c0f96c6836.jpg
  最初のトライ： closeは無いのだが、他の麻雀牌とか背景っぽいものをご認識してしまっている0.7位
　→　誤検出はなくなった。


トライ3の考察
==============

上手く認識しないバッテンに傾向あり。以下の施策が効果あがりそうな気配。

1. 白地に黒色のバッテン

2. ちょっと太字な黒地に白のバッテン、バッテンの足が少し短い感じの

3. 薄いグレー地に白色のバッテン

あとは、ja_charのパターンをもっと増やせば(現在1000文字)、認識精度が上がるかもしれない。なので、

4. ja_charデータのさらなる追加(目安+1000?)

ubuntuへのipaフォントのインストール
---------------------------------------

このＵＲＬが非常にありがたいか。

https://ubuntu.perlzemi.com/blog/20200906132441.html

以下の感じ。::

  sudo apt install -y fonts-ipafont
  fontのキャッシュを更新しましょう。
  
  fc-cache -fv
  フォントがインストールされたか確認しましょう。
  
  fc-list | grep -i ipa

けど結局japanize motplotlibを使って上手く表示はできるようになった。


japanize-matplotlib
-----------------------

https://pypi.org/project/japanize-matplotlib/

以下。::

  pip install japanize-matplotlib
  
  import matplotlib.pyplot as plt
  import japanize_matplotlib
  
  plt.plot([1, 2, 3, 4])
  plt.xlabel('簡単なグラフ')
  plt.show()

青空文庫からデータを取得して文字列一覧を試しに生成してみる
------------------------------------------------------------

このURLがありがたい。

https://qiita.com/y_itoh/items/fa04c1e2f3df2e807d61

コードはそのまま使わせてもらった。

トライ3
=========

1000文字の日本語データを用意して学習を開始。
  





