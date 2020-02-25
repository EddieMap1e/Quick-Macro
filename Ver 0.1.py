#Ver 0.1
from pynput import mouse
from pynput import keyboard
import time
import json

#全局鼠标控制器
my_mouse=mouse.Controller()

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

#获取鼠标监视器
def newMouseListener(file):
    #鼠标移动事件
    global start_time
    start_time=time.time()
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
        if button.name=='middle':
            return False
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

#执行录制操作
def executeRecord(file):
    line=file.readline()
    while line:
        cmd=json.loads(line)
        if cmd['type']=='mouse':
            if cmd['event']=='move':
                setMousePosition(cmd['posX'],cmd['posY'])
            elif cmd['event']=='click':
                if cmd['pressed']:
                    mousePress(cmd['button'])
                else :
                    mouseRelease(cmd['button'])
        time.sleep(cmd['delay'])
        line=file.readline()
    return True


if __name__ == '__main__':
    print('3s后进行录制,鼠标中键结束')
    time.sleep(3)
    f=open('测试录制记录.rec','w',encoding='utf-8')
    listener = newMouseListener(f)
    listener.start()
    while listener.is_alive():
        print('正在录制中...')
        time.sleep(3)
    listener.stop()
    f.close()
    print('录制完成!')
    time.sleep(5)
    print('开始回放')
    f=open('测试录制记录.rec','r',encoding='utf-8')
    executeRecord(f)
    f.close()

