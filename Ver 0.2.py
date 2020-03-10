#Ver 0.2
from pynput import mouse
from pynput import keyboard
import time
import json

#全局鼠标控制器
my_mouse=mouse.Controller()
#全局键盘控制器
my_keyboard=keyboard.Controller()
#系统显示设置中的缩放倍率 会影响到鼠标获取的xy坐标映射 (如笔记本默认是1.25倍)
display_X=1.0

#鼠标连点 可设置点击次数和延迟
def mouseClick(type:str='left',times:int=1,delay:float=0.1):
    for _ in range(times):
        if _!=0 :
            time.sleep(delay)
        if type == 'left':
            my_mouse.click(mouse.Button.left)
        elif type == 'right':
            my_mouse.click(mouse.Button.right)
        elif type == 'middle':
            my_mouse.click(mouse.Button.middle)
        else :
            return False
    return True

#持续按住鼠标 可设置持续的时间
def keepMousePress(type:str='left',seconds:float=0.1):
    if type == 'left':
        my_mouse.press(mouse.Button.left)
        time.sleep(seconds)
        my_mouse.release(mouse.Button.left)
    elif type == 'right':
        my_mouse.press(mouse.Button.right)
        time.sleep(seconds)
        my_mouse.release(mouse.Button.right)
    elif type == 'middle':
        my_mouse.press(mouse.Button.middle)
        time.sleep(seconds)
        my_mouse.release(mouse.Button.middle)
    else :
        return False
    return True

#按住鼠标
def mousePress(type:str='left'):
    if type=='left':
        my_mouse.press(mouse.Button.left)
    elif type=='right':
        my_mouse.press(mouse.Button.right)
    elif type=='middle':
        my_mouse.press(mouse.Button.middle)
    else :
        return False
    return True

#松开鼠标
def mouseRelease(type:str='left'):
    if type=='left':
        my_mouse.release(mouse.Button.left)
    elif type=='right':
        my_mouse.release(mouse.Button.right)
    elif type=='middle':
        my_mouse.release(mouse.Button.middle)
    else :
        return False
    return True

#鼠标滚动
def mouseScroll(dx,dy):
    my_mouse.scroll(dx,dy)
    return True

#鼠标向下滚动
def mouseScrollDown(dy:int):
    my_mouse.scroll(0,-dy)
    return True

#鼠标向上滚动
def mouseScrollUp(dy:int):
    my_mouse.scroll(0,dy)
    return True

#设置鼠标的位置 (瞬时移动)
def setMousePosition(x:int,y:int):
    my_mouse.position=(x,y)
    return True

#移动位置 相对于当前位置的 (瞬时移动)
def moveMouse(dx:int,dy:int):
    my_mouse.move(dx,dy)
    return True

#获取鼠标监视器 (参数为录制保存的文件实例)
def newMouseListener(file):
    global start_time
    start_time=time.time()
    #鼠标移动事件
    def on_move(x,y):
        global start_time
        record={}
        record['type']='mouse'
        record['event']='move'
        record['posX']=x
        record['posY']=y
        end_time=time.time()
        delay=end_time-start_time
        record['delay']=delay
        start_time=end_time
        file.writelines(json.dumps(record)+'\n')
        file.flush()
    #鼠标点击事件
    def on_click(x,y,button,pressed):
        global start_time
        record={}
        record['type']='mouse'
        record['event']='click'
        record['posX']=x
        record['posY']=y
        record['button']=button.name
        record['pressed']=pressed
        end_time=time.time()
        delay=end_time-start_time
        record['delay']=delay
        start_time=end_time
        file.writelines(json.dumps(record)+'\n')
        file.flush()
    #鼠标滚动事件
    def on_scroll(x,y,dx,dy):
        global start_time
        record={}
        record['type']='mouse'
        record['event']='scroll'
        record['posX']=x
        record['posY']=y
        record['dx']=dx
        record['dy']=dy
        end_time=time.time()
        delay=end_time-start_time
        record['delay']=delay
        start_time=end_time
        file.writelines(json.dumps(record)+'\n')
        file.flush()
    return mouse.Listener(on_move=on_move,on_click=on_click,on_scroll=on_scroll)

#键盘按下按键 (参数需要为VK值)
def keyPress(key_code):
    my_keyboard.press(keyboard.KeyCode.from_vk(key_code))
    return True

#键盘松开按键 (参数需要为VK值)
def keyRelease(key_code):
    my_keyboard.release(keyboard.KeyCode.from_vk(key_code))
    return True

#持续按键 可设置持续时间 (模拟连续时间间隔)
def keepKeyPress(key_code,seconds:float,delay=0.02):
    t=time.time()
    while time.time()-t<seconds:
        keyPress(key_code)
        time.sleep(delay)
    keyRelease(key_code)
    return True

#连续模拟打字 字母及数字有效 空格有效 回车应用\n转义 string中含有无法键入的字符将出错
def typeString(string:str):
    my_keyboard.type(string)
    return True

#获取键盘监视器 参数为录制保存的文件实例
def newKeyboardListener(file):
    global start_time
    start_time=time.time()
    #键盘按下事件
    def on_press(key):
        #F12键结束
        if key == keyboard.Key.f12:
            return False
        global start_time
        record={}
        record['type']='keyboard'
        record['event']='press'
        end_time=time.time()
        delay=end_time-start_time
        record['delay']=delay
        start_time=end_time
        try:
            record['key_code']=key.vk
        except AttributeError:
            record['key_code']=key.value.vk
        finally:
            file.writelines(json.dumps(record)+'\n')
            file.flush()
    #键盘释放事件
    def on_release(key):
        global start_time
        record={}
        record['type']='keyboard'
        record['event']='release'
        end_time=time.time()
        delay=end_time-start_time
        record['delay']=delay
        start_time=end_time
        try:
            record['key_code']=key.vk
        except AttributeError:
            record['key_code']=key.value.vk
        finally:
            file.writelines(json.dumps(record)+'\n')
            file.flush()
    return keyboard.Listener(on_press=on_press,on_release=on_release)

#执行录制操作
def executeRecord(file):
    line=file.readline()
    while line:
        cmd=json.loads(line)
        #鼠标事件
        if cmd['type']=='mouse':
            if cmd['event']=='move':
                setMousePosition(cmd['posX']/display_X,cmd['posY']/display_X)
            elif cmd['event']=='click':
                if cmd['pressed']:
                    mousePress(cmd['button'])
                else :
                    mouseRelease(cmd['button'])
        #键盘事件
        elif cmd['type']=='keyboard':
            if cmd['event']=='press':
                keyPress(cmd['key_code'])
            elif cmd['event']=='release':
                keyRelease(cmd['key_code'])
        time.sleep(cmd['delay'])
        line=file.readline()
    return True


if __name__ == '__main__':
    #修改倍率
    display_X=1.25
    f = open('我的脚本1.rec','w',encoding='utf-8')
    x=newKeyboardListener(f)
    y=newMouseListener(f)
    print('开始录制 F12结束')
    x.start()
    y.start()
    while(x.is_alive()):
        i=1
    y.stop()
    f.close()
    print(y.is_alive())
    print('录制完成')
    f = open('我的脚本1.rec','r',encoding='utf-8')
    time.sleep(3)
    print('开始回放')
    executeRecord(f)

    
    