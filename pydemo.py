from ctypes import *
import ctypes
import json
import pymem
import time


# 初始化管理端dll
dll = ctypes.windll.LoadLibrary("./WxHelp.dll")
# 全局客户端id
clientIdVal = 1
speech = []
config = {'ATT':False}

def Get_moduladdr(Game): # 读DLL模块基址
    modules = list(Game.list_modules()) # 列出exe的全部DLL模块
    for module in modules:
        if module.name == 'WeChatWin.dll':
            Moduladdr = module.lpBaseOfDll
            return Moduladdr


def updatevison():
    config['ATT'] = True
    try:
        Game = pymem.Pymem("WeChat.exe")  # 游戏进程
    except:
        print('请先启动微信')
        return False
    else:
        add = [0x22300E0,0x223D90C,0x223D9E8,0x2253E4C,0x2255AA4,0x22585D4]
        Char_Modlue = Get_moduladdr(Game) # 读DLL模块基址
        for i in add:
            time.sleep(1)
            Game.write_int(Char_Modlue + i,1661536786)
        print('最新版本注入成功')
        config['ATT'] = False


# 发送消息
def sendMsg(clientId, msgData):
    dll.sendHpSocketData(clientId, json.dumps(msgData).encode())


# 客户端加入回调
@WINFUNCTYPE(None, ctypes.c_int)
def clientAccept(clientId):
    global clientIdVal
    clientIdVal = clientId
    print('cid' + str(clientId))


@WINFUNCTYPE(None, ctypes.c_int32, ctypes.c_char_p, ctypes.c_int32)#收到消息回调
def callRecvHandler(type_int_clientId, type_char_add_msg, type_int_length):
    ctypes_msg = ctypes.string_at(type_char_add_msg)
    data = json.loads(ctypes_msg.decode('utf-8'))
    print('data',data)

@WINFUNCTYPE(None, ctypes.c_int)#客户端断开回调
def clientClose(type_int_clientId):
    print('cid:' + str(type_int_clientId) + '断开')


def dcri(openpath):#解密收到的图片
    savepath = f'd:/111.png'
    data = {"type": 11181,"data": { "src_file":openpath ,"dest_file":savepath}}
    sendMsg(clientIdVal,data)
    return savepath


while True:
    dd = input('指令')
    if dd == 'i':#注入到微信的进程pid
        dll.InjectWeChatPid(1111) #微信的进程pid
    elif dd == 'c':#设置回调函数
        dll.SetCB(clientAccept, callRecvHandler, clientClose)
    elif dd == 's':
        sendMsg(clientIdVal, {"type": 11132, "data": {"to_wxid": 'wxid', "content": '文本消息'}})
    elif dd == 'm':
        sendMsg(clientIdVal,{"type": 11136, "data": {"to_wxid": 'wxid', "file": '图片路径'}})
    elif dd == 'g':
        sendMsg(clientIdVal, {"type": 11139, "data": {"to_wxid": 'wxid', "file": 'gif路径'}})
    elif dd == 'up':
        updatevison()#过旧版本限制登录
    elif dd == 'b':
        break







