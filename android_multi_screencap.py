import os
import time

############################################################
# android multi screencap by python 
# 产品经理和开发工程师经常要从android设备上大量一次性截图。
# 以前的方式一般是，安装一个手机管家，或adb指令截图。但是麻烦在于，每次都要手工输入命令及给图片命名
# 
# 现在有一个更优雅的方式，使用USB线连接设备后，保证有adb安装，本脚本自动帮你命名
#
# run time python3.5.4
# Stephen Zhu
############################################################

f = os.popen(r"adb devices", "r")
shuchu = f.read()
f.close()
#print(shuchu)  # cmd输出结果

# 输出结果字符串处理
s = shuchu.split("\n")   # 切割换行
new = [x for x in s if x != '']  # 去掉空''
#print(new)

# 可能有多个手机设备
devices = []  # 获取设备名称
for i in new:
    dev = i.split('\tdevice')
    if len(dev)>=2:
        devices.append(dev[0])

if not devices:
    print("android phone is not connected 手机没连上")
    exit
else:
    print("find android devices 当前已经连接的手机设备:%s"%str(devices))


j=0
for curr in devices:
    j=j+1
    print(str(j)+'\t'+curr);
devcount = len(devices)

#f1 = os.popen(r"adb connect", "r")
if devcount!=1:
    s1 = input("please select your device 请选择连接的设备:")
    s1int = int(s1)
    while( s1int>devcount or s1int<1 ):
        print("input number error, retry 输入号码错误,请重新选择")
        s1 = input("please select your device 请选择连接的设备:")
        s1int = int(s1)

    print("you have selected the device number 您选择的设备号码是" + str(s1int))
    selected_dev = devices[s1int-1]
else:
    #唯一连接的adb设备
    selected_dev = devices[0]

    #流水号,用于区分同一秒的截图，以免文件名重复造成覆盖
    serial = 0
while True:
    serial = serial+1    
    userinput = input("\n-------------------------------------------------------------------------"
        "\nPress enter to capture a picture on android and pull to PC, or input your filename to save as you want"
        "\n按回车键立即android截图并自动命名保存， 或输入自定义文件名回车, 输入exit退出"+ "\n")
    len1 = len(userinput)
    #print('your input is:' + userinput)
    if 'exit' in userinput:
        exit("sorry, exit")
    filename = ''
    if len1==0:
        filename = time.strftime("%Y%m%d_%H%M%S", time.localtime()) + "_" + str(serial).zfill(4) +".png"
    else:
        print('your input is: ' + userinput)
        if ".png" not in userinput or '.PNG' not in userinput:
            filename = userinput + ".png"
        else:
            filename = userinput + ".png"

    f10 = os.popen("adb -s "+selected_dev + " shell screencap -p " + "/sdcard/tmpscreen.png")
    out10 = f10.read()
    print(out10)
    f10.close()

    f11 = os.popen("adb -s "+selected_dev + " pull /sdcard/tmpscreen.png " + "./" + filename)
    out11 = f11.read()
    f11.close()

    print(
        "already saved to file:"  + filename + "\n"
    "\n已保存为文件" + filename + "\n\n")

#the end