===============================================
GPUパススルーの設定メモ
===============================================

VMホスト
========

OSバージョン
--------------

以下の通り。::

  miyakz@lily2:~/nvidia_gpu_exp$ cat /etc/issue
  Ubuntu 20.04.5 LTS \n \l
  
  miyakz@lily2:~/nvidia_gpu_exp$ 

NVIDIAドライバの状況
-------------------------

最低限、NVIDIAのドライバをインストールし、CUDA関連は入っていない。::

  miyakz@lily2:~/nvidia_gpu_exp$ sudo ubuntu-drivers list
  nvidia-driver-470, (kernel modules provided by linux-modules-nvidia-470-generic)
  nvidia-driver-450-server, (kernel modules provided by linux-modules-nvidia-450-server-generic)
  nvidia-driver-470-server, (kernel modules provided by linux-modules-nvidia-470-server-generic)
  nvidia-driver-418-server, (kernel modules provided by linux-modules-nvidia-418-server-generic)
  nvidia-driver-390, (kernel modules provided by linux-modules-nvidia-390-generic)
  miyakz@lily2:~/nvidia_gpu_exp$ 
  

  miyakz@lily2:~/nvidia_gpu_exp$ apt list --installed | grep -i nvidia
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  libnvidia-cfg1-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,auto-removable]
  libnvidia-common-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 all [installed,auto-removable]
  libnvidia-compute-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-decode-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,auto-removable]
  libnvidia-encode-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,auto-removable]
  libnvidia-extra-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,auto-removable]
  libnvidia-fbc1-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,auto-removable]
  libnvidia-gl-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,auto-removable]
  libnvidia-ifr1-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,auto-removable]
  libnvidia-ml-dev/focal,now 10.1.243-3 amd64 [installed,auto-removable]
  xserver-xorg-video-nvidia-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,auto-removable]
  miyakz@lily2:~/nvidia_gpu_exp$ apt list --installed | grep -i cuda
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  libcudart10.1/focal,now 10.1.243-3 amd64 [installed,auto-removable]
  miyakz@lily2:~/nvidia_gpu_exp$ 

IOMMUの状況/AMD-Vi(仮想化支援)の設定状況
-------------------------------------------

IOMMU/AMI-Viは設定済み。::

  miyakz@lily2:~/nvidia_gpu_exp$ cat /var/log/syslog| grep -i iommu | head 
  Nov  1 13:12:53 lily2 kernel: [    0.196012] iommu: Default domain type: Translated 
  Nov  1 13:12:53 lily2 kernel: [    0.333619] pci 0000:00:00.2: AMD-Vi: IOMMU performance counters supported
  Nov  1 13:12:53 lily2 kernel: [    0.333929] pci 0000:00:01.0: Adding to iommu group 0
  Nov  1 13:12:53 lily2 kernel: [    0.333956] pci 0000:00:01.2: Adding to iommu group 0
  Nov  1 13:12:53 lily2 kernel: [    0.334059] pci 0000:00:02.0: Adding to iommu group 1
  Nov  1 13:12:53 lily2 kernel: [    0.334213] pci 0000:00:03.0: Adding to iommu group 2
  Nov  1 13:12:53 lily2 kernel: [    0.334239] pci 0000:00:03.1: Adding to iommu group 2
  Nov  1 13:12:53 lily2 kernel: [    0.334377] pci 0000:00:04.0: Adding to iommu group 3
  Nov  1 13:12:53 lily2 kernel: [    0.334481] pci 0000:00:05.0: Adding to iommu group 4
  Nov  1 13:12:53 lily2 kernel: [    0.334627] pci 0000:00:07.0: Adding to iommu group 5
  miyakz@lily2:~/nvidia_gpu_exp$ 
  
  
  miyakz@lily2:~/nvidia_gpu_exp$ cat /boot/config-5.4.0-1* | egrep -i "vfio|iommu"
  CONFIG_GART_IOMMU=y
  CONFIG_CALGARY_IOMMU=y
  CONFIG_CALGARY_IOMMU_ENABLED_BY_DEFAULT=y
  CONFIG_KVM_VFIO=y
  CONFIG_VFIO_IOMMU_TYPE1=y
  CONFIG_VFIO_VIRQFD=y
  CONFIG_VFIO=y
  CONFIG_VFIO_NOIOMMU=y
  CONFIG_VFIO_PCI=y
  CONFIG_VFIO_PCI_VGA=y
  CONFIG_VFIO_PCI_MMAP=y
  CONFIG_VFIO_PCI_INTX=y
  CONFIG_VFIO_PCI_IGD=y
  CONFIG_VFIO_MDEV=m
  CONFIG_VFIO_MDEV_DEVICE=m
  CONFIG_IOMMU_IOVA=y
  CONFIG_IOMMU_API=y
  CONFIG_IOMMU_SUPPORT=y
  # Generic IOMMU Pagetable Support
  # end of Generic IOMMU Pagetable Support
  # CONFIG_IOMMU_DEBUGFS is not set
  # CONFIG_IOMMU_DEFAULT_PASSTHROUGH is not set
  CONFIG_AMD_IOMMU=y
  CONFIG_AMD_IOMMU_V2=m
  CONFIG_INTEL_IOMMU=y
  CONFIG_INTEL_IOMMU_SVM=y
  # CONFIG_INTEL_IOMMU_DEFAULT_ON is not set
  CONFIG_INTEL_IOMMU_FLOPPY_WA=y
  CONFIG_HYPERV_IOMMU=y
  CONFIG_IOMMU_HELPER=y
  # CONFIG_SAMPLE_VFIO_MDEV_MTTY is not set
  # CONFIG_SAMPLE_VFIO_MDEV_MDPY is not set
  # CONFIG_SAMPLE_VFIO_MDEV_MDPY_FB is not set
  # CONFIG_SAMPLE_VFIO_MDEV_MBOCHS is not set
  # CONFIG_IOMMU_DEBUG is not set
  CONFIG_GART_IOMMU=y
  CONFIG_CALGARY_IOMMU=y
  CONFIG_CALGARY_IOMMU_ENABLED_BY_DEFAULT=y
  CONFIG_KVM_VFIO=y
  CONFIG_VFIO_IOMMU_TYPE1=y
  CONFIG_VFIO_VIRQFD=y
  CONFIG_VFIO=y
  CONFIG_VFIO_NOIOMMU=y
  CONFIG_VFIO_PCI=y
  CONFIG_VFIO_PCI_VGA=y
  CONFIG_VFIO_PCI_MMAP=y
  CONFIG_VFIO_PCI_INTX=y
  CONFIG_VFIO_PCI_IGD=y
  CONFIG_VFIO_MDEV=m
  CONFIG_VFIO_MDEV_DEVICE=m
  CONFIG_IOMMU_IOVA=y
  CONFIG_IOMMU_API=y
  CONFIG_IOMMU_SUPPORT=y
  # Generic IOMMU Pagetable Support
  # end of Generic IOMMU Pagetable Support
  # CONFIG_IOMMU_DEBUGFS is not set
  # CONFIG_IOMMU_DEFAULT_PASSTHROUGH is not set
  CONFIG_AMD_IOMMU=y
  CONFIG_AMD_IOMMU_V2=m
  CONFIG_INTEL_IOMMU=y
  CONFIG_INTEL_IOMMU_SVM=y
  # CONFIG_INTEL_IOMMU_DEFAULT_ON is not set
  CONFIG_INTEL_IOMMU_FLOPPY_WA=y
  CONFIG_HYPERV_IOMMU=y
  CONFIG_IOMMU_HELPER=y
  # CONFIG_SAMPLE_VFIO_MDEV_MTTY is not set
  # CONFIG_SAMPLE_VFIO_MDEV_MDPY is not set
  # CONFIG_SAMPLE_VFIO_MDEV_MDPY_FB is not set
  # CONFIG_SAMPLE_VFIO_MDEV_MBOCHS is not set
  # CONFIG_IOMMU_DEBUG is not set
  miyakz@lily2:~/nvidia_gpu_exp$ 


VFIOの状況
------------

まず、IOMMUを調べる。以下のスクリプト::

  miyakz@lily2:~/bin$ cat iommu.sh 
  #!/bin/bash
  shopt -s nullglob
  for d in /sys/kernel/iommu_groups/*/devices/*; do 
      n=${d#*/iommu_groups/*}; n=${n%%/*}
      printf 'IOMMU Group %s ' "$n"
      lspci -nns "${d##*/}"
  done;
  miyakz@lily2:~/bin$ 

うちの環境では、GPUとSOUNDが同一IOMMUに属しているので、この２つをセットでパススルーする必要がある。::

  miyakz@lily2:~/bin$ ./iommu.sh | grep -i nvidia
  IOMMU Group 2 07:00.0 VGA compatible controller [0300]: NVIDIA Corporation GK208B [GeForce GT 710] [10de:128b] (rev a1)
  IOMMU Group 2 07:00.1 Audio device [0403]: NVIDIA Corporation GK208 HDMI/DP Audio Controller [10de:0e0f] (rev a1)
  miyakz@lily2:~/bin$ 
  

[]でくくられた値を、GRUB_CMDLINE_LINUX_DEFAULTに設定する。[10de:128b]と[10de:0e0f] の部分。

grubの設定(/etc/default/grub)
----------------------------------

GRUB_CMDLINE_LINUX_DEFAULTに以下の設定を行う。::

  GRUB_CMDLINE_LINUX_DEFAULT="vfio-pci.ids=10de:128b,10de:0e0f video=vesafb:off,efifb:off pci=nommconf"

video=以降の設定は、システムで1つのGPUをホストとVMゲストで取り合うことになるので、VMホストにそれを譲るための設定。これをすると、ホストで画面表示ができなくなる。もっと良い方法が存在するらしいのだが、あまりにも高度なため、実施できなかった。将来的にチャレンジしたいと思う。

pci=nommconfはよくわからないけど設定。(よくない)

VFIOの状況の確認
------------------

以下の通り。::

  07:00.0 VGA compatible controller [0300]: NVIDIA Corporation GK208B [GeForce GT 710] [10de:128b] (rev a1) (prog-if 00 [VGA controller])
          Subsystem: ZOTAC International (MCO) Ltd. GK208B [GeForce GT 710] [19da:1422]
          Flags: bus master, fast devsel, latency 0, IRQ 104
          Memory at f6000000 (32-bit, non-prefetchable) [size=16M]
          Memory at e8000000 (64-bit, prefetchable) [size=128M]
          Memory at f0000000 (64-bit, prefetchable) [size=32M]
          I/O ports at e000 [size=128]
          Expansion ROM at 000c0000 [disabled] [size=128K]
          Capabilities: <access denied>
          Kernel driver in use: vfio-pci
          Kernel modules: nvidiafb, nouveau
  
  07:00.1 Audio device [0403]: NVIDIA Corporation GK208 HDMI/DP Audio Controller [10de:0e0f] (rev a1)
          Subsystem: ZOTAC International (MCO) Ltd. GK208 HDMI/DP Audio Controller [19da:1422]
          Flags: fast devsel, IRQ 105
          Memory at f7080000 (32-bit, non-prefetchable) [size=16K]
          Capabilities: <access denied>
          Kernel driver in use: vfio-pci
          Kernel modules: snd_hda_intel


VMゲスト
=========


ホストの設定が完了したら、一からVMを作成するのが良い。
（既存のVMにGPUパススルーすると上手くいかない可能性あり)

1. virt-managerでVMを作成する
2. その際、cpu modeをhost-passthroughに設定して、sockets,core,threadsを指定する。
3. また、hostのGPUを指定する(サウンドは任意)
4. virsh editで追加の設定をする。kvmのhidden、ioapic driverの設定
5. VMを起動するとnouveauでエラーがでるため、いちど、GPUデバイスをVMから抜いて再起動。
6. VMに以下の設定を施す。
nouveauをblacklistに追加して、カーネルに反映。::
  a@ubuntu:~$ cat /etc/modprobe.d/blacklist.conf | grep nou
  blacklist nouveau
  a@ubuntu:~$ 
  
  sudo update-initramfs -u

7. VMを再起動する
8. VMを停止して、virt-managerからホストのGPUを追加する。
9. VMを起動する
10. VMにNVIDIAのドライバをインストールする
 以下のコマンド::

  16  sudo apt install ubuntu-drivers-common
   17  ubuntu-drivers
   18  ubuntu-drivers list
   19  sudo ubuntu-drivers list
   20  sudo apt install nvidia-driver-470

11. VMを再起動
12. VMでNVIDIAデバイスＧＰＵの確認

以下。::
  a@ubuntu:~$ lspci  | grep -i nvi
  06:00.0 VGA compatible controller: NVIDIA Corporation GK208B [GeForce GT 710] (rev a1)
  a@ubuntu:~$ 

ただ、ここで、nvida-smiしてもデバイスが見つからないと言われる。


CUDAのインストール
--------------------

ここで、VMにCUDAやyoloをインストールして、実際に学習タスクが上手く行くかを確認する。


1) driverをインストールしてみる(上記でインストールしているので、不要かも)

こんな感じ。::

  a@ubuntu:~$ sudo ubuntu-drivers  list
  ERROR:root:could not open aplay -l
  Traceback (most recent call last):
    File "/usr/share/ubuntu-drivers-common/detect/sl-modem.py", line 35, in detect
      aplay = subprocess.Popen(
    File "/usr/lib/python3.8/subprocess.py", line 854, in __init__
      self._execute_child(args, executable, preexec_fn, close_fds,
    File "/usr/lib/python3.8/subprocess.py", line 1702, in _execute_child
      raise child_exception_type(errno_num, err_msg, err_filename)
  FileNotFoundError: [Errno 2] No such file or directory: 'aplay'
  nvidia-driver-470-server, (kernel modules provided by linux-modules-nvidia-470-server-generic)
  nvidia-driver-390, (kernel modules provided by linux-modules-nvidia-390-generic)
  nvidia-driver-418-server, (kernel modules provided by linux-modules-nvidia-418-server-generic)
  nvidia-driver-470, (kernel modules provided by linux-modules-nvidia-470-generic)
  nvidia-driver-450-server, (kernel modules provided by linux-modules-nvidia-450-server-generic)
  a@ubuntu:~$ 
  
  sudo apt-get install nvidia-driver-470-server

ただ、nvidia-smiではデバイスが無いと言われる。なんでだろう::

  a@ubuntu:~$ nvidia-smi 
  No devices were found
  a@ubuntu:~$ 

1) CUDAのインストール

以下のような感じ。::

  sudo apt install nvidia-cuda-toolkit

  a@ubuntu:~$ nvcc --version
  nvcc: NVIDIA (R) Cuda compiler driver
  Copyright (c) 2005-2019 NVIDIA Corporation
  Built on Sun_Jul_28_19:07:16_PDT_2019
  Cuda compilation tools, release 10.1, V10.1.243
  a@ubuntu:~$ nvidia-
  nvidia-bug-report.sh     nvidia-debugdump         nvidia-persistenced      nvidia-smi               
  nvidia-cuda-mps-control  nvidia-detector          nvidia-settings          nvidia-xconfig           
  nvidia-cuda-mps-server   nvidia-ngx-updater       nvidia-sleep.sh          

  
yoloc7の試行
----------------

デモ的な、馬の検出タスク。

やっぱり、CUDA/GPUが有効になっていないっぽい::

  a@ubuntu:~/yolov7$ python3 detect.py --source inference/images/horses.jpg --weights yolov7-e6e.pt --conf 0.25 --img-size 1280 --device 0
  Namespace(agnostic_nms=False, augment=False, classes=None, conf_thres=0.25, device='0', exist_ok=False, img_size=1280, iou_thres=0.45, name='exp', no_trace=False, nosave=False, project='runs/detect', save_conf=False, save_txt=False, source='inference/images/horses.jpg', update=False, view_img=False, weights=['yolov7-e6e.pt'])
  Traceback (most recent call last):
    File "detect.py", line 196, in <module>
      detect()
    File "detect.py", line 30, in detect
      device = select_device(opt.device)
    File "/home/a/yolov7/utils/torch_utils.py", line 71, in select_device
      assert torch.cuda.is_available(), f'CUDA unavailable, invalid device {device} requested'  # check availability
  AssertionError: CUDA unavailable, invalid device 0 requested
  a@ubuntu:~/yolov7$ python3 detect.py --source inference/images/horses.jpg --weights yolov7-e6e.pt --conf 0.25 --img-size 1280 
  Namespace(agnostic_nms=False, augment=False, classes=None, conf_thres=0.25, device='', exist_ok=False, img_size=1280, iou_thres=0.45, name='exp', no_trace=False, nosave=False, project='runs/detect', save_conf=False, save_txt=False, source='inference/images/horses.jpg', update=False, view_img=False, weights=['yolov7-e6e.pt'])
  YOLOR 🚀 v0.1-115-g072f76c torch 1.13.0+cu117 CPU
  
  Fusing layers... 
  Model Summary: 792 layers, 151687420 parameters, 817020 gradients
   Convert model to Traced-model... 
   traced_script_module saved! 
   model is traced! 
  
  /home/a/.local/lib/python3.8/site-packages/torch/functional.py:504: UserWarning: torch.meshgrid: in an upcoming release, it will be required to pass the indexing argument. (Triggered internally at ../aten/src/ATen/native/TensorShape.cpp:3190.)
    return _VF.meshgrid(tensors, **kwargs)  # type: ignore[attr-defined]
  5 horses, Done. (13159.0ms) Inference, (6.9ms) NMS
   The image with the result is saved in: runs/detect/exp3/horses.jpg
  Done. (13.215s)
  a@ubuntu:~/yolov7$ 


以前失敗した自分のタスクをやってみる。(学習タスク)
やっぱり、GPU関連でエラーになる::

  a@ubuntu:~/yolov7$ ./my_train3.sh 
  ++ python3 train_aux.py --workers 2 --batch-size 8 --data dataset/first/first.yaml --cfg cfg/training/yolov7-e6.yaml --weights yolov7-e6.pt --name yolov7-e6-first --hyp data/hyp.scratch.p6.yaml --epochs 300
  YOLOR 🚀 v0.1-115-g072f76c torch 1.13.0+cu117 CPU
  
  Namespace(adam=False, artifact_alias='latest', batch_size=8, bbox_interval=-1, bucket='', cache_images=False, cfg='cfg/training/yolov7-e6.yaml', data='dataset/first/first.yaml', device='', entity=None, epochs=300, evolve=False, exist_ok=False, global_rank=-1, hyp='data/hyp.scratch.p6.yaml', image_weights=False, img_size=[640, 640], label_smoothing=0.0, linear_lr=False, local_rank=-1, multi_scale=False, name='yolov7-e6-first', noautoanchor=False, nosave=False, notest=False, project='runs/train', quad=False, rect=False, resume=False, save_dir='runs/train/yolov7-e6-first5', save_period=-1, single_cls=False, sync_bn=False, total_batch_size=8, upload_dataset=False, v5_metric=False, weights='yolov7-e6.pt', workers=2, world_size=1)
  tensorboard: Start with 'tensorboard --logdir runs/train', view at http://localhost:6006/
  hyperparameters: lr0=0.01, lrf=0.2, momentum=0.937, weight_decay=0.0005, warmup_epochs=3.0, warmup_momentum=0.8, warmup_bias_lr=0.1, box=0.05, cls=0.3, cls_pw=1.0, obj=0.7, obj_pw=1.0, iou_t=0.2, anchor_t=4.0, fl_gamma=0.0, hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, degrees=0.0, translate=0.2, scale=0.9, shear=0.0, perspective=0.0, flipud=0.0, fliplr=0.5, mosaic=1.0, mixup=0.15, copy_paste=0.0, paste_in=0.15, loss_ota=1
  Traceback (most recent call last):
    File "train_aux.py", line 612, in <module>
      train(hyp, opt, device, tb_writer)
    File "train_aux.py", line 71, in train
      run_id = torch.load(weights).get('wandb_id') if weights.endswith('.pt') and os.path.isfile(weights) else None
    File "/home/a/.local/lib/python3.8/site-packages/torch/serialization.py", line 789, in load
      return _load(opened_zipfile, map_location, pickle_module, **pickle_load_args)
    File "/home/a/.local/lib/python3.8/site-packages/torch/serialization.py", line 1131, in _load
      result = unpickler.load()
    File "/home/a/.local/lib/python3.8/site-packages/torch/serialization.py", line 1101, in persistent_load
      load_tensor(dtype, nbytes, key, _maybe_decode_ascii(location))
    File "/home/a/.local/lib/python3.8/site-packages/torch/serialization.py", line 1083, in load_tensor
      wrap_storage=restore_location(storage, location),
    File "/home/a/.local/lib/python3.8/site-packages/torch/serialization.py", line 215, in default_restore_location
      result = fn(storage, location)
    File "/home/a/.local/lib/python3.8/site-packages/torch/serialization.py", line 182, in _cuda_deserialize
      device = validate_cuda_device(location)
    File "/home/a/.local/lib/python3.8/site-packages/torch/serialization.py", line 166, in validate_cuda_device
      raise RuntimeError('Attempting to deserialize object on a CUDA '
  RuntimeError: Attempting to deserialize object on a CUDA device but torch.cuda.is_available() is False. If you are running on a CPU-only machine, please use torch.load with map_location=torch.device('cpu') to map your storages to the CPU.
  a@ubuntu:~/yolov7$ 



https://www.nvidia.co.jp/content/DriverDownload-March2009/confirmation.php?url=/XFree86/Linux-x86_64/390.25/NVIDIA-Linux-x86_64-390.25.run&lang=jp&type=TITAN
 
ubuntuインストールして、GPUをVMに挿したあと、VMを起動すると、nouveauドライバでエラーするので、これを抜いた後 
     
https://choni-waniwani.blogspot.com/2017/11/ubuntu16nouveau.html  
  

NVIDIAドライバをインストールしてみる
はじめから、VMをインストールしてみよう

以下、aというVMを作った。::

  a@a:~$ lspci | grep -i nvidia
  a@a:~$ lsmod | grep -i nvidia
  a@a:~$ 
  @a:~$ ip a 
  1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
      link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
      inet 127.0.0.1/8 scope host lo
         valid_lft forever preferred_lft forever
      inet6 ::1/128 scope host 
         valid_lft forever preferred_lft forever
  2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
      link/ether 52:54:00:32:20:df brd ff:ff:ff:ff:ff:ff
      inet 192.168.122.151/24 brd 192.168.122.255 scope global dynamic enp1s0
         valid_lft 3428sec preferred_lft 3428sec
      inet6 fe80::5054:ff:fe32:20df/64 scope link 
         valid_lft forever preferred_lft forever
  a@a:~$ 
  
  a@a:~$ sudo apt list --installed | grep -i nouveau
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  a@a:~$ sudo apt list --installed | grep -i nvidia
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  a@a:~$ 
  
  a@a:~$ cat /etc/modprobe.d/blacklist.conf | tail -1
  blacklist nouveau
  a@a:~$ 
  
  a@a:~$ cat /etc/default/grub | grep DEFA
  GRUB_DEFAULT=0
  GRUB_CMDLINE_LINUX_DEFAULT="maybe-ubiquity modprobe.blacklist=nouveau"
  a@a:~$ 
  

このタイミングでVMを停止して、GPUを追加して、再起動。::

  a@a:~$ lsmod | grep -i nvidia
  a@a:~$ lspci | grep -i nvidia
  03:00.0 VGA compatible controller: NVIDIA Corporation GK208B [GeForce GT 710] (rev a1)
  a@a:~$ 
  
  a@a:~$ sudo apt list --installed | grep -i nvidia
  [sudo] password for a: 
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  a@a:~$ sudo apt list --installed | grep -i nouveau 
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  a@a:~$ 

この状態でnvidiaの純正driverのインストールを試みる。

https://www.nvidia.co.jp/content/DriverDownload-March2009/confirmation.php?url=/XFree86/Linux-x86_64/390.25/NVIDIA-Linux-x86_64-390.25.run&lang=jp&type=TITAN
 

次はccのバージョンチェックとかうるさいこと言われずに、インストールが進んでいる。。。
しかし、エラーが発生してインストール中断。::

      CONFTEST: is_export_symbol_gpl_refcount_dec_and_test
       CC [M]  /tmp/selfgz5621/NVIDIA-Linux-x86_64-390.25/kernel/nvidia/nv-frontend.o
       In file included from /tmp/selfgz5621/NVIDIA-Linux-x86_64-390.25/kernel/common/inc/nv-linux.h:136,
                      from /tmp/selfgz5621/NVIDIA-Linux-x86_64-390.25/kernel/nvidia/nv-frontend.c:13:
       /tmp/selfgz5621/NVIDIA-Linux-x86_64-390.25/kernel/common/inc/nv-list-helpers.h:94:19: error: redefinition of ‘list_is_first’
        94 | static inline int list_is_first(const struct list_head *list,
           |                   ^~~~~~~~~~~~~
  
したがって、lily2で実績のある方法で、実施してみる。  

miyakz@lily2:~$ sudo apt-get install nvidia-driver-470-server
miyakz@lily2:~$ nvidia-smi
(ドライバ出力)

こんな感じ。::

  a@a:~$ sudo nvidia-smi 
  [sudo] password for a: 
  
  
  
  
  No devices were found
  a@a:~$ 
  
  @a:~$ lspci | grep -i nvidia
  03:00.0 VGA compatible controller: NVIDIA Corporation GK208B [GeForce GT 710] (rev a1)
  a@a:~$ 
  
だめでしたね。。。

サウンドデバイスも一緒だとどうなる？::

  a@a:~$ lspci | grep -i nvidia
  03:00.0 VGA compatible controller: NVIDIA Corporation GK208B [GeForce GT 710] (rev a1)
  06:00.0 Audio device: NVIDIA Corporation GK208 HDMI/DP Audio Controller (rev a1)
  a@a:~$ sudo nvidia-smi 
  [sudo] password for a: 
  No devices were found
  a@a:~$ 
  
  
  a@a:~$ sudo ubuntu-drivers devices
  ERROR:root:could not open aplay -l
  Traceback (most recent call last):
    File "/usr/share/ubuntu-drivers-common/detect/sl-modem.py", line 35, in detect
      aplay = subprocess.Popen(
    File "/usr/lib/python3.8/subprocess.py", line 858, in __init__
      self._execute_child(args, executable, preexec_fn, close_fds,
    File "/usr/lib/python3.8/subprocess.py", line 1704, in _execute_child
      raise child_exception_type(errno_num, err_msg, err_filename)
  FileNotFoundError: [Errno 2] No such file or directory: 'aplay'
  == /sys/devices/pci0000:00/0000:00:02.2/0000:03:00.0 ==
  modalias : pci:v000010DEd0000128Bsv000019DAsd00001422bc03sc00i00
  vendor   : NVIDIA Corporation
  model    : GK208B [GeForce GT 710]
  driver   : nvidia-driver-450-server - distro non-free
  driver   : nvidia-driver-470 - distro non-free recommended
  driver   : nvidia-driver-390 - distro non-free
  driver   : nvidia-driver-418-server - distro non-free
  driver   : nvidia-driver-470-server - distro non-free
  driver   : xserver-xorg-video-nouveau - distro free builtin
  
  a@a:~$ 
  
追加で以下いんすとるー::

   69  sudo apt install nvidia-driver-450-server -y

だめ。
全部入れてみる。::

  a@a:~$ sudo nvidia-smi 
  No devices were found
  a@a:~$ sudo nvidia-smi 
  No devices were found
  a@a:~$ apt list --installed | grep -i nvidia 
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  libnvidia-cfg1-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-common-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 all [installed,automatic]
  libnvidia-compute-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-decode-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-encode-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-extra-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-fbc1-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-gl-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-ifr1-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-compute-utils-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-dkms-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-driver-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed]
  nvidia-kernel-common-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-kernel-source-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-prime/focal-updates,now 0.8.16~0.20.04.2 all [installed,automatic]
  nvidia-settings/focal-updates,now 470.57.01-0ubuntu0.20.04.3 amd64 [installed,automatic]
  nvidia-utils-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  xserver-xorg-video-nvidia-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  a@a:~$ 
  
  a@a:~$ cat list 
  sudo apt install -y nvidia-driver-390
  sudo apt install -y nvidia-driver-418-server
  sudo apt install -y nvidia-driver-470-server
  sudo apt install -y nvidia-driver-450-server
  sudo apt install -y nvidia-driver-470
  a@a:~$ 

どうもインストールしたバージョンで上書きされるらしいので、１つ１つ、トライする必要がある。
トライが必要なドライバは、ubuntu-driverコマンドで表示された以下のものたち。::

  sudo apt install -y nvidia-driver-390
  sudo apt install -y nvidia-driver-418-server
  sudo apt install -y nvidia-driver-470-server
  sudo apt install -y nvidia-driver-450-server
  sudo apt install -y nvidia-driver-470 


アンインストールを効率的に実施するコマンドライン::
  apt list --installed | grep -i nvidia 
  sudo apt-get purge *nvidia*

1) nvidia-driver-470-server

lily2でもnvidia-smiした所、ドライババージョンが470になっているので、期待感大だが、、、::

  a@a:~$ ./check.sh 
  ++ sudo ls
  check.sh  list	NVIDIA-Linux-x86_64-390.25.run	nvidia_remove.sh
  ++ echo 'nvidia installed (device)'
  nvidia installed (device)
  ++ grep -i nvidia
  ++ sudo lspci
  03:00.0 VGA compatible controller: NVIDIA Corporation GK208B [GeForce GT 710] (rev a1)
  06:00.0 Audio device: NVIDIA Corporation GK208 HDMI/DP Audio Controller (rev a1)
  ++ echo 'nvidia smi'
  nvidia smi
  ++ sudo nvidia-smi
  sudo: nvidia-smi: command not found
  ++ echo 'nvidia driver stuff installed'
  nvidia driver stuff installed
  ++ grep -i nvidia
  ++ sudo apt list --installed
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  a@a:~$ 

  ドライバのインストール
  sudo apt install nvidia-driver-470-server

    a@a:~$ ./check.sh 
  ++ sudo ls
  [sudo] password for a: 
  check.sh  list	NVIDIA-Linux-x86_64-390.25.run	nvidia_remove.sh
  ++ echo 'nvidia installed (device)'
  nvidia installed (device)
  ++ grep -i nvidia
  ++ sudo lspci
  03:00.0 VGA compatible controller: NVIDIA Corporation GK208B [GeForce GT 710] (rev a1)
  06:00.0 Audio device: NVIDIA Corporation GK208 HDMI/DP Audio Controller (rev a1)
  ++ echo 'nvidia smi'
  nvidia smi
  ++ sudo nvidia-smi
  No devices were found
  ++ echo 'nvidia driver stuff installed'
  nvidia driver stuff installed
  ++ grep -i nvidia
  ++ sudo apt list --installed
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  libnvidia-cfg1-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-common-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 all [installed,automatic]
  libnvidia-compute-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-decode-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-encode-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-extra-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-fbc1-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-gl-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-ifr1-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-compute-utils-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-dkms-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-driver-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed]
  nvidia-kernel-common-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-kernel-source-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-utils-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  xserver-xorg-video-nvidia-470-server/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  a@a:~$ 

だめでした。

2) nvidia-driver-470 

クリーンであることをチェック::
  
  a@a:~$ ./check.sh 
  ++ sudo ls
  [sudo] password for a: 
  check.sh  list	NVIDIA-Linux-x86_64-390.25.run	nvidia_remove.sh
  ++ echo 'nvidia installed (device)'
  nvidia installed (device)
  ++ grep -i nvidia
  ++ sudo lspci
  03:00.0 VGA compatible controller: NVIDIA Corporation GK208B [GeForce GT 710] (rev a1)
  06:00.0 Audio device: NVIDIA Corporation GK208 HDMI/DP Audio Controller (rev a1)
  ++ echo 'nvidia smi'
  nvidia smi
  ++ sudo nvidia-smi
  sudo: nvidia-smi: command not found
  ++ echo 'nvidia driver stuff installed'
  nvidia driver stuff installed
  ++ grep -i nvidia
  ++ sudo apt list --installed
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  a@a:~$ 
  
  0 upgraded, 0 newly installed, 0 to remove and 92 not upgraded.
  ++ grep -i nvidia
  ++ sudo apt list --installed
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  a@a:~$ 
  
クリーンである。  

470-serverの時もそうだったけど、nvidia-smiの所でハングする。。。::

  a@a:~$ ./check.sh 
  ++ sudo ls
  [sudo] password for a: 
  check.sh  list	NVIDIA-Linux-x86_64-390.25.run	nvidia_remove.sh
  ++ echo 'nvidia installed (device)'
  nvidia installed (device)
  ++ grep -i nvidia
  ++ sudo lspci
  03:00.0 VGA compatible controller: NVIDIA Corporation GK208B [GeForce GT 710] (rev a1)
  06:00.0 Audio device: NVIDIA Corporation GK208 HDMI/DP Audio Controller (rev a1)
  ++ echo 'nvidia smi'
  nvidia smi
  ++ sudo nvidia-smi
  
  a@a:~$ sudo strace -p 1099
  [sudo] password for a: 
  strace: Process 1099 attached
  ppoll([{fd=-1}, {fd=6, events=POLLIN}], 2, NULL, NULL, 8
  
なにかをずっと待っとるらしい。  
強制再起動して、再び、check./shやっぱり、同じコマンドでハングする。
一度、lily2ごと再起動してみる。ＮＧ．．．::

  a@a:~$ ./check.sh 
  ++ sudo ls
  [sudo] password for a: 
  check.sh  list	NVIDIA-Linux-x86_64-390.25.run	nvidia_remove.sh
  ++ echo 'nvidia installed (device)'
  nvidia installed (device)
  ++ grep -i nvidia
  ++ sudo lspci
  03:00.0 VGA compatible controller: NVIDIA Corporation GK208B [GeForce GT 710] (rev a1)
  06:00.0 Audio device: NVIDIA Corporation GK208 HDMI/DP Audio Controller (rev a1)
  ++ echo 'nvidia smi'
  nvidia smi
  ++ sudo nvidia-smi
  No devices were found
  ++ echo 'nvidia driver stuff installed'
  nvidia driver stuff installed
  ++ grep -i nvidia
  ++ sudo apt list --installed
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  libnvidia-cfg1-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-common-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 all [installed,automatic]
  libnvidia-compute-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-decode-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-encode-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-extra-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-fbc1-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-gl-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-ifr1-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-compute-utils-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-dkms-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-driver-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed]
  nvidia-kernel-common-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-kernel-source-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-prime/focal-updates,now 0.8.16~0.20.04.2 all [installed,automatic]
  nvidia-settings/focal-updates,now 470.57.01-0ubuntu0.20.04.3 amd64 [installed,automatic]
  nvidia-utils-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  xserver-xorg-video-nvidia-470/focal-updates,focal-security,now 470.141.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  a@a:~$ 
  
3) nvidia-driver-450-server 

クリーンチェク::

  a@a:~$ ./check.sh 
  ++ sudo ls
  check.sh  list	NVIDIA-Linux-x86_64-390.25.run	nvidia_remove.sh
  ++ echo 'nvidia installed (device)'
  nvidia installed (device)
  ++ grep -i nvidia
  ++ sudo lspci
  03:00.0 VGA compatible controller: NVIDIA Corporation GK208B [GeForce GT 710] (rev a1)
  06:00.0 Audio device: NVIDIA Corporation GK208 HDMI/DP Audio Controller (rev a1)
  ++ echo 'nvidia smi'
  nvidia smi
  ++ sudo nvidia-smi
  sudo: nvidia-smi: command not found
  ++ echo 'nvidia driver stuff installed'
  nvidia driver stuff installed
  ++ grep -i nvidia
  ++ sudo apt list --installed
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  a@a:~$ 

  nvidia-driver-450-serverのインストール

  VMをreboot。この後、lily2も一緒に起動しなくなった。
  /etc/modprobe.d/blacklist.confにblacklist vfioとして起動してきた。

そして、やっと見えるようになった。。。けど、なんか怪しい動作だな。。。。
これで良いのか。。。？::

  a@a:~$ ./check.sh 
  ++ sudo ls
  [sudo] password for a: 
  check.sh  list	NVIDIA-Linux-x86_64-390.25.run	nvidia_remove.sh
  ++ echo 'nvidia installed (device)'
  nvidia installed (device)
  ++ grep -i nvidia
  ++ sudo lspci
  03:00.0 VGA compatible controller: NVIDIA Corporation GK208B [GeForce GT 710] (rev a1)
  06:00.0 Audio device: NVIDIA Corporation GK208 HDMI/DP Audio Controller (rev a1)
  ++ echo 'nvidia smi'
  nvidia smi
  ++ sudo nvidia-smi
  Thu Nov  3 16:43:11 2022       
  +-----------------------------------------------------------------------------+
  | NVIDIA-SMI 450.203.03   Driver Version: 450.203.03   CUDA Version: 11.0     |
  |-------------------------------+----------------------+----------------------+
  | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
  | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
  |                               |                      |               MIG M. |
  |===============================+======================+======================|
  |   0  GeForce GT 710      Off  | 00000000:03:00.0 N/A |                  N/A |
  | 40%   34C    P8    N/A /  N/A |      5MiB /  2002MiB |     N/A      Default |
  |                               |                      |                  N/A |
  +-------------------------------+----------------------+----------------------+
                                                                                 
  +-----------------------------------------------------------------------------+
  | Processes:                                                                  |
  |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
  |        ID   ID                                                   Usage      |
  |=============================================================================|
  |  No running processes found                                                 |
  +-----------------------------------------------------------------------------+
  ++ echo 'nvidia driver stuff installed'
  nvidia driver stuff installed
  ++ grep -i nvidia
  ++ sudo apt list --installed
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  libnvidia-cfg1-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-common-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 all [installed,automatic]
  libnvidia-compute-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-decode-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-encode-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-extra-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-fbc1-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-gl-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  libnvidia-ifr1-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-compute-utils-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-dkms-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-driver-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed]
  nvidia-kernel-common-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-kernel-source-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  nvidia-utils-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  xserver-xorg-video-nvidia-450-server/focal-updates,focal-security,now 450.203.03-0ubuntu0.20.04.1 amd64 [installed,automatic]
  a@a:~$ 


　んー。やっぱり、あやしい。nvidia-smiがデバイス無いというタイミングあり。奇跡的なのか？
  以下のようなメッセージも出たりする::
  ++ sudo nvidia-smi
  Unable to determine the device handle for GPU 0000:03:00.0: GPU is lost.  Reboot the system to recover this GPU

  
VMとlily2のubuntuのバージョンが微妙に違うため、おそらく、nvidiaのドライバのバージョンも異なったのだと判断する。
このあと、cudaのインストール。

だが、nvidia-smiでデバイスが無い、とか、上記のエラー。上記のエラーを解消しようとしてＶＭをrebootすると、lily2ごとrebootしてしまうとか、
意味不明な状態が続いて、危ない（そもそも２回GPUがnvidia-smiで見えたのが奇跡的？）なので、VMでGPUを利用する試みは
残念ながら諦めるとするか？

最後に残された道は、VMのubuntuのバージョンを最新にすることか。最新は22.10。これで試してみて、なおも同じ状況であれば、
一旦VMでの利用は諦めよう。

まぁ、一旦lily2ごとshutdownした後起動すると見えるようになるかもしれんし。。。

A) Ubuntuのapt upgradedしてみる

upgraded前::

  a@a:~$ cat /etc/issue
  Ubuntu 20.04.1 LTS \n \l
  
  a@a:~$ 
  
upgradedあと。::

  a@a:~$ cat /etc/issue
  Ubuntu 20.04.5 LTS \n \l
  
  a@a:~$ 





  
B) Ubuntuのversionを20.10にしてみる。

結局ダメでした。nouveauが変になるので、blacklistに入れて、450-serverを入れて、、、::

  a@a:~$ ./check.sh 
  ++ sudo ls
  [sudo] password for a: 
  check.sh  nvidia_remove.sh
  ++ echo 'nvidia installed (device)'
  nvidia installed (device)
  ++ sudo lspci
  ++ grep -i nvidia
  06:00.0 VGA compatible controller: NVIDIA Corporation GK208B [GeForce GT 710] (rev a1)
  ++ echo 'nvidia smi'
  nvidia smi
  ++ sudo nvidia-smi
  No devices were found
  ++ echo 'nvidia driver stuff installed'
  nvidia driver stuff installed
  ++ grep -i nvidia
  ++ sudo apt list --installed
  
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  
  libnvidia-cfg1-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  libnvidia-common-470/kinetic,now 470.141.03-0ubuntu1 all [installed,automatic]
  libnvidia-compute-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  libnvidia-decode-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  libnvidia-egl-wayland1/kinetic,now 1:1.1.10-1 amd64 [installed,automatic]
  libnvidia-encode-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  libnvidia-extra-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  libnvidia-fbc1-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  libnvidia-gl-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  libnvidia-ifr1-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  nvidia-compute-utils-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  nvidia-cuda-gdb/kinetic,now 11.5.114~11.5.2-1ubuntu1 amd64 [installed,auto-removable]
  nvidia-cuda-toolkit-doc/kinetic,now 11.5.2-1ubuntu1 all [installed,auto-removable]
  nvidia-dkms-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  nvidia-driver-450/kinetic,now 460.91.03-0ubuntu1 amd64 [installed]
  nvidia-driver-460/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  nvidia-driver-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  nvidia-kernel-common-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  nvidia-kernel-source-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  nvidia-prime/kinetic,now 0.8.17.1 all [installed,automatic]
  nvidia-settings/kinetic,now 510.47.03-0ubuntu1 amd64 [installed,automatic]
  nvidia-utils-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  xserver-xorg-video-nvidia-470/kinetic,now 470.141.03-0ubuntu1 amd64 [installed,automatic]
  ++ echo 'nvcc '
  nvcc 
  ++ nvcc --version
  ./check.sh: line 10: nvcc: command not found
  a@a:~$ cat /etc/issue
  Ubuntu 22.10 \n \l
  
  a@a:~$ 

※ VmのXMLを直していないのがちょっと気になる、

C) Fedora

全体の手順が乗っており、わかりやすい？

http://kikei.github.io/linux/2021/05/18/nvidia.html

https://blog.osakana.net/archives/11286

→　結局、470ドライバのカーネルモジュールビルドでこける（インストーラ失敗）

D) 他の方法

cuda-installで簡単という話。これはやってみたほうがよいかも？？

https://zenn.dev/190ikp/articles/how_to_install_nvidia_drivers

cuda-installでやると、やっぱりへんな状態に::

  a@a:~$ sudo nvidia-smi 
  NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver. Make sure that the latest NVIDIA driver is installed and running.
  
  a@a:~$ 
  
  [  138.080860] nvidia-nvlink: Nvlink Core is being initialized, major device number 236
  [  138.080867] NVRM: The NVIDIA GeForce GT 710 GPU installed in this system is
                 NVRM:  supported through the NVIDIA 470.xx Legacy drivers. Please
                 NVRM:  visit http://www.nvidia.com/object/unix.html for more
                 NVRM:  information.  The 520.61.05 NVIDIA driver will ignore
                 NVRM:  this GPU.  Continuing probe...
  [  138.083016] NVRM: No NVIDIA GPU found.
  [  138.083277] nvidia-nvlink: Unregistered Nvlink Core, major device number 236
  a@a:~$ 
  

やっぱりドライバ新しすぎるのかいな。
470に変えてもＮＧ．

E) 万策尽きた。VMへのGPUパススルーは諦めて、ホスト(lily2)でやる


参考：check.sh/nvidia_removeスクリプト
---------------------------------------

スクリプトは以下。::

  a@a:~$ cat check.sh 
  set -x
  sudo ls
  echo "nvidia installed (device)"
  sudo lspci | grep -i nvidia
  echo "nvidia smi"
  sudo nvidia-smi
  echo "nvidia driver stuff installed"
  sudo apt list --installed | grep -i nvidia
  echo "nvcc "
  nvcc --version
  a@a:~$ cat nvidia_remove.sh 
  set -x
  sudo apt list --installed | grep -i nvidia
  
  sudo apt-get purge "*nvidia*"
  
  sudo apt list --installed | grep -i nvidia
  
  a@a:~$ 
  


vmのXMLダンプ
---------------

以下の状況。ポイントは以下。

1. cpu modeをhost-passthroughに設定して、sockets,core,threadsを指定する
2. kvmのhidden属性をon
3. ioapic driver='kvm'に設定
4. 安全のために、ホスト起動時にVMを起動しない
5. ホストデバイスをGPUのみを選択

::

  miyakz@lily2:~/nvidia_gpu_exp$ virsh dumpxml  --domain GPUtest 
  <domain type='kvm' id='29'>
    <name>GPUtest</name>
    <uuid>cbadad08-f307-4d99-a3fb-77d5d785d8d0</uuid>
    <metadata>
      <libosinfo:libosinfo xmlns:libosinfo="http://libosinfo.org/xmlns/libvirt/domain/1.0">
        <libosinfo:os id="http://ubuntu.com/ubuntu/20.04"/>
      </libosinfo:libosinfo>
    </metadata>
    <memory unit='KiB'>4194304</memory>
    <currentMemory unit='KiB'>4194304</currentMemory>
    <vcpu placement='static'>1</vcpu>
    <resource>
      <partition>/machine</partition>
    </resource>
    <os>
      <type arch='x86_64' machine='pc-q35-4.2'>hvm</type>
      <bootmenu enable='no'/>
    </os>
    <features>
      <acpi/>
      <apic/>
      <kvm>
        <hidden state='on'/>
      </kvm>
      <vmport state='off'/>
      <ioapic driver='kvm'/>
    </features>
    <cpu mode='host-passthrough' check='none'>
      <topology sockets='1' cores='1' threads='1'/>
    </cpu>
    <clock offset='utc'>
      <timer name='rtc' tickpolicy='catchup'/>
      <timer name='pit' tickpolicy='delay'/>
      <timer name='hpet' present='no'/>
    </clock>
    <on_poweroff>destroy</on_poweroff>
    <on_reboot>restart</on_reboot>
    <on_crash>destroy</on_crash>
    <pm>
      <suspend-to-mem enabled='no'/>
      <suspend-to-disk enabled='no'/>
    </pm>
    <devices>
      <emulator>/usr/bin/qemu-system-x86_64</emulator>
      <disk type='file' device='disk'>
        <driver name='qemu' type='qcow2'/>
        <source file='/var/lib/libvirt/images/GPUtest.qcow2' index='2'/>
        <backingStore/>
        <target dev='vda' bus='virtio'/>
        <boot order='1'/>
        <alias name='virtio-disk0'/>
        <address type='pci' domain='0x0000' bus='0x03' slot='0x00' function='0x0'/>
      </disk>
      <disk type='file' device='cdrom'>
        <driver name='qemu' type='raw'/>
        <source file='/home/miyakz/cdimage/ubuntu-20.04.1-legacy-server-amd64.iso' index='1'/>
        <backingStore/>
        <target dev='sda' bus='sata'/>
        <readonly/>
        <alias name='sata0-0-0'/>
        <address type='drive' controller='0' bus='0' target='0' unit='0'/>
      </disk>
      <controller type='usb' index='0' model='ich9-ehci1'>
        <alias name='usb'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x1d' function='0x7'/>
      </controller>
      <controller type='usb' index='0' model='ich9-uhci1'>
        <alias name='usb'/>
        <master startport='0'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x1d' function='0x0' multifunction='on'/>
      </controller>
      <controller type='usb' index='0' model='ich9-uhci2'>
        <alias name='usb'/>
        <master startport='2'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x1d' function='0x1'/>
      </controller>
      <controller type='usb' index='0' model='ich9-uhci3'>
        <alias name='usb'/>
        <master startport='4'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x1d' function='0x2'/>
      </controller>
      <controller type='sata' index='0'>
        <alias name='ide'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x1f' function='0x2'/>
      </controller>
      <controller type='pci' index='0' model='pcie-root'>
        <alias name='pcie.0'/>
      </controller>
      <controller type='pci' index='1' model='pcie-root-port'>
        <model name='pcie-root-port'/>
        <target chassis='1' port='0x10'/>
        <alias name='pci.1'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0' multifunction='on'/>
      </controller>
      <controller type='pci' index='2' model='pcie-root-port'>
        <model name='pcie-root-port'/>
        <target chassis='2' port='0x11'/>
        <alias name='pci.2'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x1'/>
      </controller>
      <controller type='pci' index='3' model='pcie-root-port'>
        <model name='pcie-root-port'/>
        <target chassis='3' port='0x12'/>
        <alias name='pci.3'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x2'/>
      </controller>
      <controller type='pci' index='4' model='pcie-root-port'>
        <model name='pcie-root-port'/>
        <target chassis='4' port='0x13'/>
        <alias name='pci.4'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x3'/>
      </controller>
      <controller type='pci' index='5' model='pcie-root-port'>
        <model name='pcie-root-port'/>
        <target chassis='5' port='0x14'/>
        <alias name='pci.5'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x4'/>
      </controller>
      <controller type='pci' index='6' model='pcie-root-port'>
        <model name='pcie-root-port'/>
        <target chassis='6' port='0x15'/>
        <alias name='pci.6'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x5'/>
      </controller>
      <controller type='pci' index='7' model='pcie-root-port'>
        <model name='pcie-root-port'/>
        <target chassis='7' port='0x16'/>
        <alias name='pci.7'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x6'/>
      </controller>
      <controller type='virtio-serial' index='0'>
        <alias name='virtio-serial0'/>
        <address type='pci' domain='0x0000' bus='0x02' slot='0x00' function='0x0'/>
      </controller>
      <interface type='network'>
        <mac address='52:54:00:32:20:df'/>
        <source network='default' portid='8741442c-1a75-4ddf-930c-f94afd6aee4f' bridge='virbr0'/>
        <target dev='vnet4'/>
        <model type='virtio'/>
        <alias name='net0'/>
        <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
      </interface>
      <serial type='pty'>
        <source path='/dev/pts/4'/>
        <target type='isa-serial' port='0'>
          <model name='isa-serial'/>
        </target>
        <alias name='serial0'/>
      </serial>
      <console type='pty' tty='/dev/pts/4'>
        <source path='/dev/pts/4'/>
        <target type='serial' port='0'/>
        <alias name='serial0'/>
      </console>
      <channel type='unix'>
        <source mode='bind' path='/var/lib/libvirt/qemu/channel/target/domain-29-GPUtest/org.qemu.guest_agent.0'/>
        <target type='virtio' name='org.qemu.guest_agent.0' state='disconnected'/>
        <alias name='channel0'/>
        <address type='virtio-serial' controller='0' bus='0' port='1'/>
      </channel>
      <channel type='spicevmc'>
        <target type='virtio' name='com.redhat.spice.0' state='disconnected'/>
        <alias name='channel1'/>
        <address type='virtio-serial' controller='0' bus='0' port='2'/>
      </channel>
      <input type='tablet' bus='usb'>
        <alias name='input0'/>
        <address type='usb' bus='0' port='1'/>
      </input>
      <input type='mouse' bus='ps2'>
        <alias name='input1'/>
      </input>
      <input type='keyboard' bus='ps2'>
        <alias name='input2'/>
      </input>
      <graphics type='spice' port='5903' autoport='yes' listen='127.0.0.1'>
        <listen type='address' address='127.0.0.1'/>
        <image compression='off'/>
      </graphics>
      <sound model='ich9'>
        <alias name='sound0'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x1b' function='0x0'/>
      </sound>
      <video>
        <model type='qxl' ram='65536' vram='65536' vgamem='16384' heads='1' primary='yes'/>
        <alias name='video0'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x0'/>
      </video>
      <hostdev mode='subsystem' type='pci' managed='yes'>
        <driver name='vfio'/>
        <source>
          <address domain='0x0000' bus='0x07' slot='0x00' function='0x0'/>
        </source>
        <alias name='hostdev0'/>
        <address type='pci' domain='0x0000' bus='0x06' slot='0x00' function='0x0'/>
      </hostdev>
      <redirdev bus='usb' type='spicevmc'>
        <alias name='redir0'/>
        <address type='usb' bus='0' port='2'/>
      </redirdev>
      <redirdev bus='usb' type='spicevmc'>
        <alias name='redir1'/>
        <address type='usb' bus='0' port='3'/>
      </redirdev>
      <memballoon model='virtio'>
        <alias name='balloon0'/>
        <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
      </memballoon>
      <rng model='virtio'>
        <backend model='random'>/dev/urandom</backend>
        <alias name='rng0'/>
        <address type='pci' domain='0x0000' bus='0x05' slot='0x00' function='0x0'/>
      </rng>
    </devices>
    <seclabel type='dynamic' model='apparmor' relabel='yes'>
      <label>libvirt-cbadad08-f307-4d99-a3fb-77d5d785d8d0</label>
      <imagelabel>libvirt-cbadad08-f307-4d99-a3fb-77d5d785d8d0</imagelabel>
    </seclabel>
    <seclabel type='dynamic' model='dac' relabel='yes'>
      <label>+64055:+108</label>
      <imagelabel>+64055:+108</imagelabel>
    </seclabel>
  </domain>
  
  miyakz@lily2:~/nvidia_gpu_exp$ 
  





