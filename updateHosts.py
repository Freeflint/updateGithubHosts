from __future__ import print_function
from requests import get
import ctypes, sys
import PySimpleGUI as sg


host_url = "http://hosts.gitcdn.top/hosts.txt"
hosts_path = "C:\Windows\System32\drivers\etc\hosts"
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win32; x86) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68"
}
sg.theme("DarkAmber")
layout =[
    [sg.T("github host:"),sg.Input(host_url,key="-InputHost-",size=(40,1)),\
    sg.B("更新",key="-Bupdate-") ]
    
]
wd = sg.Window("github加速 v0.01",font=("宋体",12),layout = layout)

def updateHost1(hosturl=host_url):
    result = get(url=hosturl,headers=headers)
    if result.status_code == 200:
        with open(hosts_path,mode="r+",encoding="utf-8") as f:
            tmp = f.read()
            
            s1= result.text.split("\n")
            
            s = "# fetch-github-hosts begin"
            r = tmp.find(s)
            
            if r < 0:
                f.close()
                #f.seek(0,2) #移到尾部
                with open(hosts_path,mode="w+") as fr:
                    fr.write(tmp + "\n"+ result.text)
                    fr.close()
                    return "hosts写入完成！\n"+ s1[-5][1:]
            #更新
            elif r > 0:
                f.seek(r+len(s)-3,0) #从头偏移到上次写入位置进行覆盖
                f.write("\n" + result.text)
                return "hosts更新完成！\n" + s1[-5][1:]
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    while True:
        event,values = wd.read()
        if event is None:
            wd.close()
            break
        if event == "-Bupdate-":
            r = updateHost1(values["-InputHost-"])
            sg.popup(r)
else:
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        else:#in python2.x
            ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)






