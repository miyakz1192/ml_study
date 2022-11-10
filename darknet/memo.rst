================================================
darknetの構築メモ
================================================

環境
=====

lily2(環境情報)::

  miyakz@lily2:~$ cat /etc/issue
  Ubuntu 20.04.5 LTS \n \l
  
  miyakz@lily2:~$ uname -a
  Linux lily2 5.4.0-131-generic #147-Ubuntu SMP Fri Oct 14 17:07:22 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux
  miyakz@lily2:~$ 
  
構築
=====

以下のコマンドでcloneしてきてmakeするだけ。コンパイルは正常に終了する。::

  git clone https://github.com/AlexeyAB/darknet
  cd darknet/
  vim Makefile 

Makefileの先頭は以下。OPENMPを1にすることで環境のCPUをフル活用するので1にする::

  GPU=0
  CUDNN=0
  CUDNN_HALF=0
  OPENCV=0
  AVX=0
  OPENMP=1
  LIBSO=0
  ZED_CAMERA=0
  ZED_CAMERA_v2_8=0

あとは、makeコマンドを叩くだけ::

  make

検出の実行
===========

以下のコマンドを実行するのみ。::

  ./darknet detect cfg/yolov3.cfg yolov3.weights data/eagle.jpg

predictions.jpgというファイルができるので、適当に開いて確認する

学習データの用意
===================

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
  
  4 directories, 18 files
  miyakz@lily2:~/git_repos/darknet$ 

学習に必要なデータはtrainとvalidディレクトリに配置する。学習したい画像とそこをポイントしたファイルをそれぞれ配置する。
画像ごとにtxtを用意する。

また、他に、学習に関するファイルは以下（a.zipとかfirst.yamlとか入っているけど、これは今回は特に使わない)::

  miyakz@lily2:~/git_repos/darknet/ds1$ cat obj.data 
  classes = 1
  train  = ./ds1/train.txt
  valid  = ./ds1/valid.txt
  names =  ./ds1/obj.names
  backup = ./ds1/backup
  miyakz@lily2:~/git_repos/darknet/ds1$ cat obj.names 
  close
  miyakz@lily2:~/git_repos/darknet/ds1$ cat train.txt 
  ./ds1/train/Screenshot_2022-10-21-00-19-35-30_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds1/train/Screenshot_2022-10-21-00-21-51-38_56bd83b73c18fa95b476c6c0f96c6836.jpg
  miyakz@lily2:~/git_repos/darknet/ds1$ cat valid.txt 
  ./ds1/valid/Screenshot_2022-10-21-00-23-35-12_56bd83b73c18fa95b476c6c0f96c6836.jpg
  ./ds1/valid/Screenshot_2022-10-21-00-25-42-95_56bd83b73c18fa95b476c6c0f96c6836.jpg
  miyakz@lily2:~/git_repos/darknet/ds1$ 
  

学習の実行
===========

本家のURLを参考にしながら、tinyを使っていく。こちらのほうが精度が比較的悪くなるものの、
学習時間が短く済むそうな::

  https://github.com/AlexeyAB/darknet#how-to-train-tiny-yolo-to-detect-your-custom-objects

tinyのモデルをダウンロードして、darknetを実行するのみ。::

  wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.conv.29
  ./darknet detector train ds1/obj.data ds1/yolov4-tiny-custom.cfg ds1/yolov4-tiny.conv.29
