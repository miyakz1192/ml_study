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
  
  




XMLダンプ
-----------

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
  





