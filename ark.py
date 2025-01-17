﻿import os
import sys
import pyautogui as auto
import time
import keyboard
import configparser
from PIL import Image


'''属性设置'''
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
Apath = config.get('main', 'Apath')  # 模拟器图片位置
pausetime = int(config.get('main', 'pausetime'))  # 点击间隔
ip = config.get('main', 'ip')  # 模拟器端口ip地址
c = config.get('main', 'c')  # 图片识别率
Is = config.get('main', 'Is')  # 默认分辨率为1280*720

map = ('S4-1.png', '4-8.png', '7-15.png', '1-7.png', 'R8-7.png')
'''函数部分'''
# 从模拟器上截图并返回图片
def screenshot():
    os.system(f"adb shell screencap -p {Apath}/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png")


# 得到当前分辨率
def getT_is():
    filename = 'screenshot.png'
    try:
        os.remove(filename)
    except:
        pass
    screenshot()
    try:
        global hx
        global hy
        global True_image_size
        img = Image.open(filename)
        True_image_size = img.size
        maxSize = max(True_image_size)
        minSize = min(True_image_size)
        hx = maxSize//2
        hy = minSize//2
        return hx, hy, True_image_size
    except:
        print('abd连接失败，请打开模拟器后重试')
        sys.exit(0)


# 触摸输入
def tap(x, y):  # 点击坐标 x，y
    print(f'点击坐标 {x} {y}')
    os.system(f'adb shell input tap {x} {y}')

# 勾选代理指挥
def check():
    p = auto.locate(f'./picture/{Is}/uncheck.png', 'screenshot.png', confidence=c)
    if p != None:
        x, y = auto.center(p)
        tap(x, y)
        time.sleep(pausetime)


# 对图片进行多次选择分析
def touchlist(imglist, pausetime, stage, start=None):
    if stage == 'battling':
        screenshot()
        while True:
            if time.time() - start > 300:
                tap(hx, hy)
                time.sleep(pausetime)
                tap(hx, hy)
                time.sleep(pausetime)
                return None
            for img_name in imglist:
                if auto.locate(f'./picture/{Is}/{img_name}','screenshot.png', confidence=c) == None:
                    print('战斗进行中...')
                    screenshot()
                    time.sleep(pausetime)
                else:
                    print('战斗结束，退出战斗...')
                    return None 
    else:
        while True:
            screenshot()
            check()
            for img_name in imglist:
                p = auto.locate(f'./picture/{Is}/{img_name}', 'screenshot.png', confidence=c)
                if stage == 'start' and p != None:  # 开始阶段
                    if img_name == 'start_battle_1.png' or img_name == 'start_battle_2.png': # 点击开始战斗按钮
                        x, y = auto.center(p)
                        tap(x, y)
                        time.sleep(pausetime)
                        print('开始行动')
                        break
                    elif img_name == 'os.png':  # 点击op按钮
                        x, y = auto.center(p)
                        tap(x, y)
                        time.sleep(pausetime)
                        print('开始战斗')						
                        return None
                    elif img_name == 'lzbz.png': # 点击碎石                   
                        x, y = auto.center(p)
                        tap(x, y)
                        print('碎石 准备开始战斗')
                        time.sleep(pausetime)
                        break
                    elif img_name in map:
                        x, y = auto.center(p)
                        tap(x, y)
                        print(img_name)
                        time.sleep(pausetime)
                        break
                elif stage == 'end' and p != None :  # 结束阶段
                    if img_name == 'confidence.png' or img_name == 'confidence_1.png':  # 点击结算画面
                        x, y = auto.center(p)
                        tap(x, y)
                        time.sleep(pausetime)
                        print('战斗结束')						
                        return None
                    elif img_name == 'defeat.png' or img_name == 'jm.png':# 任务失败 和 剿灭作战
                        tap(hx, hy)
                        time.sleep(pausetime)
                        tap(hx, hy)
                        time.sleep(pausetime)
                        print('任务失败')						
                        return None
                    elif img_name == 'recover.png' or img_name == '400.png' or img_name == 'login.png' or img_name == 'terminal.png' : # 升级
                        x, y = auto.center(p)
                        tap(x, y)
                        time.sleep(pausetime)
                        print('掉线 '+ img_name)
                        break
                    elif img_name == 'last.png':# 重进
                        tap(hx, hy)
                        time.sleep(pausetime)
                        tap(hx, hy)
                        time.sleep(pausetime)
                        print('掉线 '+ img_name)
                        return None

def battle(times):
    i = 0
    n = int(times)
    while i < n:
        i += 1
        start = time.time()
        print(f'--------第{i}次战斗开始--------')
        touchlist(('start_battle_1.png','start_battle_2.png','os.png', 'lzbz.png') + map, pausetime, 'start')
        touchlist(('confidence.png', 'confidence_1.png', 'defeat.png','jm.png','recover.png', '400.png', 'login.png', 'terminal.png', 'last.png', '0.png'),6,'battling', start=start)
        touchlist(("confidence.png", 'confidence_1.png', 'defeat.png','jm.png','recover.png', '400.png', 'login.png', 'terminal.png', 'last.png', '0.png'), pausetime, 'end')
        print(f"---------第{i}次战斗结束--------")
        time.sleep(pausetime)
        screenshot()
        while auto.locate(f'./picture/{Is}/start_battle_1.png','screenshot.png', confidence=c) == None and auto.locate(f'./picture/{Is}/start_battle_2.png','screenshot.png', confidence=c) == None:
            screenshot()
            print('等待开始按钮...')
            time.sleep(1)
            p = auto.locate(f'./picture/{Is}/last.png', 'screenshot.png', confidence=c)
            if p != None:
                x, y = auto.center(p)
                tap(x, y)
                time.sleep(1)
            if time.time() - start > 180:
                tap(hx, hy)
                time.sleep(pausetime)
        end = time.time()
        if end - start < 30:
            i -= 1





'''初始化部分'''
print("欢迎使用明日方舟自定义挂机程序\n-------------------按下Enter键开始-------------------\n")
os.system('pause')
print("\n--------初始化中--------\n")
os.system(f'adb connect {ip}')
getT_is()
print(f'配置图片分辨率:{Is}\n当前实际分辨率:{True_image_size} 中心值:({hx},{hy})\n点击间隔:{pausetime}\n图片识别率:{c}')
print('\n--------初始化成功--------\n请选择模式 F1无限模式 F2自定义次数')


'''主代码部分'''
key = keyboard.read_key(suppress=False)
if key == "f1":
    os.system('pause')
    battle(99999)
elif key == "f2":
    os.system('pause')
    while True:
        try:
            times = input("请输入次数")
            battle(times)
            break
        except e:
            print(e)
            print('请输入正确的值')
