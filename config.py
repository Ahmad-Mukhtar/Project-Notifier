import time

from win10toast import ToastNotifier

IDS = ['996364628025274386', '1031626738982436864', '1031626732309299200', '996364628025274382', '1031626782284431360',
       '1031626776085250048', '1031626773660942336', '1031626762999021568', '996364628021080069', '1031626731394940928'
    , '996364628025274380', '996364628025274381', '1031626741679374336']
JOB_TYPE = ["Python", "Flask","Django", "Java", 'Spring Boot', 'Saas',
            'React', 'Nodejs', 'Unity', 'Desktop Application',
            'C#', 'C++', 'golang']


def show_notification(title, message, duration):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, None, duration)
    time.sleep(2)
