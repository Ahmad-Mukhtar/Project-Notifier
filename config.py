import time

from win10toast import ToastNotifier

IDS = ['996364628025274386', '1031626732309299200']
JOB_TYPE = ["Python", "Django"]


def show_notification(title, message, duration):
    toaster = ToastNotifier()
    toaster.show_toast(title, message,None, duration)
    time.sleep(2)
