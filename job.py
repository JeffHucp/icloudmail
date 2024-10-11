#此脚本用于自动注册icloud隐藏邮箱
#运行环境： macos 12.7.6
#by  JeffHu

import time
import datetime
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
import pyautogui
import sys
import subprocess

class auto_click_icloud_mail:

    def __init__(self):
        self.height_list = []
        self.pid_list = []
        self.x_list = []
        self.y_list = []

    def open_system_preferences(self):
        if sys.platform == 'darwin':  # macOS
            subprocess.run(['open', '/System/Library/PreferencePanes/AppleIDPrefPane.prefPane'])
        else:
            print("Cannot open system preferences on this platform.")

    def get_window_info_by_app_name(self):
        # 获取所有屏幕上的窗口信息
        window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
        for window in window_list:
            if window["kCGWindowOwnerName"] == "系统偏好设置":
                #系统偏好页的=679
                #appleid页的Height= 612
                # 电子邮件已达上限的Height=204
                self.height = window["kCGWindowBounds"]["Height"]
                self.x = window["kCGWindowBounds"]["X"]
                self.y = window["kCGWindowBounds"]["Y"]
                self.pid = window["kCGWindowOwnerPID"]
                self.height_list.append(int(self.height))
                self.x_list.append(int(self.x))
                self.y_list.append(int(self.y))
                self.pid_list.append(int(self.pid))
        return self.height_list, self.pid_list,self.x_list, self.y_list

    # 根据不同窗口的高度，做不同操作
    def do_thing(self):
        if 218 in self.height_list:
            print("已达到最大可创建邮件数量！")
        if 204 in self.height_list:
            time.sleep(3)
            print(str(datetime.datetime.now()) + " 已被限制，10分钟后再试！")
            self.index = self.height_list.index(204)
            self.pid = self.pid_list[self.index]
            subprocess.run(f'kill -9 {self.pid}',shell=True)
            time.sleep(600)
        elif 560 in self.height_list:
            self.index = self.height_list.index(560)
            self.x = self.x_list[self.index]
            self.y = self.y_list[self.index]
            pyautogui.click(self.x + 185,self.y + 310,interval=2)
            pyautogui.typewrite('a')
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(5)
            self.get_window_info_by_app_name()
            if 204 in self.height_list or 218 in self.height_list:
                self.do_thing()
            else:
                pyautogui.press('enter')
                time.sleep(5)
                global a
                a = 1
        elif 560 not in self.height_list and 537 in self.height_list:
            if a == 1:
                print(str(datetime.datetime.now()) + " 本次已注册完成！")
                time.sleep(5)
                self.a = 0
            else:
                print(str(datetime.datetime.now()) + " 注册中！")
                time.sleep(5)
            self.index = self.height_list.index(537)
            self.x = self.x_list[self.index]
            self.y = self.y_list[self.index]
            pyautogui.click(self.x + 32,self.y + 433,interval=3)
        elif 560 not in self.height_list and 612 in self.height_list:
            self.index = self.height_list.index(612)
            self.x = self.x_list[self.index]
            self.y = self.y_list[self.index]
            pyautogui.click(self.x + 590,self.y + 200,interval=2)
            print(str(datetime.datetime.now()) + " 进入邮箱注册页面")
            time.sleep(5)
        elif 560 not in self.height_list and self.height_list == []:
            print(str(datetime.datetime.now()) + " 打开appleid页面")
            time.sleep(2)
            self.open_system_preferences()
            time.sleep(10)

if __name__ == "__main__":
    a = 0
    while True:
        obj = auto_click_icloud_mail()
        obj.get_window_info_by_app_name()
        obj.do_thing()
