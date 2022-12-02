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
  





