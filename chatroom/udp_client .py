import threading
import socket
import json
import os
import time
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

GTW=datetime.timezone(datetime.timedelta(hours=8))  # 設定所在時區 ( 台灣是 GMT+8 )
MAX_BYTES = 65535
server_addr = ('127.0.0.1',6000) # Remote server address
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # 建立一個UDP socket

def showtime():# 建立不斷改變文字變數的函式
    now = datetime.datetime.now(tz=GTW).strftime('%a %H:%M:%S\n %Y/%m/%d')
    TWtime.set(now)
    window.after(1000,showtime)

def confirm():#開新視窗
    boxselection=box.get()
    #text_message.insert('end', boxselection)
    if boxselection=='幫我選擇':
        global x1,x2,x3,x4 
        x1=0
        x2=0
        x4=0
        x3=0
        text_message.insert('end', '你已開啟選擇障礙選擇器\n')
        def callback():#確認關閉視窗
            a=messagebox.askquestion("詢問：","確定要關閉吗？") # yes或no
            if a=='yes':
                Swindow.destroy() # 返回值為yes就退出
                text_message.insert('end', '你已關閉選擇障礙選擇器\n')
        
        def che(): # Checkbutton command函式
            global x1,x2,x3,x4
            if check1.get()==1: #第一個框打勾x1設1，否則設0
                x1=1
            else:
                x1=0
            if check2.get()==1: 
                x2=1
            else:
                x2=0
            if check3.get()==1: 
                x3=1
            else:
                x3=0
            if check4.get()==1: 
                x4=1
            else:
                x4=0
        def start():
            global x1,x2,x3,x4
            rand=[]
            if ((x1==0)and (x2==0) and(x3==0) and(x4==0)): 
                rand.append('error')
            if x1==1:  #第一個框打勾時，a1text加進rand[]
                a1text=a1.get()#str
                rand.append(a1text)
            if x2==1: 
                a2text=a2.get()
                rand.append(a2text)
            if x3==1: 
                a3text=a3.get()
                rand.append(a3text)
            if x4==1: 
                a4text=a4.get()
                rand.append(a4text)
            
            msgdict =   {
                            "type": 7,
                            "nickname": nickname,
                            "message": rand
                        }
            msgdata = json.dumps(msgdict).encode('utf-8')
            print(msgdata)
            sock.sendto(msgdata, server_addr)     

        Swindow = tk.Toplevel(window)
        Swindow.title('選擇障礙') 
        Swindow.minsize(width=280, height=280)
        Swindow.protocol("WM_DELETE_WINDOW",callback)
        Swindow.resizable('False','False')#固定視窗是否可移動
        Che_frame=tk.Frame(Swindow,width=50,height=250)#放勾選框的地方
        Sel_frame=tk.Frame(Swindow,width=280,height=250)#放輸入選項的地方

        Che_frame.grid(row=0,column=0,pady=0)
        Sel_frame.grid(row=0,column=1,pady=6)

        #Checkbutton(勾選框) 設定
        check1=tk.IntVar()
        C1=tk.Checkbutton(Che_frame,variable=check1,onvalue=1,offvalue=0,command=che)
        check2=tk.IntVar()
        C2=tk.Checkbutton(Che_frame,variable=check2,onvalue=1,offvalue=0,command=che)
        check3=tk.IntVar()
        C3=tk.Checkbutton(Che_frame,variable=check3,onvalue=1,offvalue=0,command=che)
        check4=tk.IntVar()
        C4=tk.Checkbutton(Che_frame,variable=check4,onvalue=1,offvalue=0,command=che)

        C1.grid(row=0,column=0,padx=3,pady=19)
        C2.grid(row=1,column=0,padx=3,pady=0)
        C3.grid(row=2,column=0,padx=3,pady=19)
        C4.grid(row=3,column=0,padx=3,pady=0)


        label=tk.Label(Sel_frame,width=30,text='請打勾且將選項分別填入並按開始')
        label.grid(row=0,column=0,pady=5)

        a1=tk.StringVar()# 選擇框1
        a1.set('')
        a1_entry=tk.Entry(Sel_frame,width=30,textvariable=a1)
        a1_entry.grid(row=1,column=0,pady=5,ipady=7)

        a2=tk.StringVar()# 選擇框2
        a2.set('')
        a2_entry=tk.Entry(Sel_frame,width=30,textvariable=a2)
        a2_entry.grid(row=2,column=0,pady=5,ipady=7)

        a3=tk.StringVar()# 選擇框3
        a3.set('')
        a3_entry=tk.Entry(Sel_frame,width=30,textvariable=a3)
        a3_entry.grid(row=3,column=0,pady=5,ipady=7)

        a4=tk.StringVar()# 選擇框4
        a4.set('')
        a4_entry=tk.Entry(Sel_frame,width=30,textvariable=a4)
        a4_entry.grid(row=4,column=0,pady=5,ipady=7)

        btn_start=tk.Button(Swindow,width=15,text='Start',command=start)# 選擇框開始按鈕
        btn_start.grid(row=5,column=1,pady=10)
        
    elif boxselection=='收尋':
        def callback():#確認關閉視窗
            a=messagebox.askquestion("詢問：","確定要關閉嗎？")
            if a=='yes':
                Fwindow.destroy() # 返回值為yes就退出
                text_message.tag_remove("found","1.0",'end')
        def mySearch():#收尋
            text_message.tag_remove("found","1.0",'end')
            start = "1.0"
            key = entry.get()

            if (len(key.strip()) == 0):
                return
            while True:
                pos = text_message.search(key,start,'end')
                # print("pos= ",pos) # pos=  3.0  pos=  4.0  pos=     
                if (pos == ""):
                    break
                text_message.tag_add("found",pos,"%s+%dc" %(pos,len(key)))
                start = "%s+%dc" % (pos,len(key))
                # print("start= ",start) # start=  3.0+3c  start=  4.0+3c
        
        Fwindow = tk.Toplevel(window)
        Fwindow.title('尋找') 
        Fwindow.minsize(width=200, height=150)
        Fwindow.protocol("WM_DELETE_WINDOW",callback)
        entry = tk.Entry(Fwindow) 
        entry.grid(row=0,column=0,padx=5) 

        btn = tk.Button(Fwindow,text="Find",command=mySearch)
        btn.grid(row=0,column=1,padx=5,pady=5)
        text_message.tag_configure("found", background="yellow")

def send_message(): # 傳送輸入文字
        msgtext = text_text.get('0.0','end')
        print(msgtext)

        # 判讀是否為指令 (最前兩個字元與最後兩個字元都是"%%")
        if msgtext[:2] == '%%' and msgtext[7:9] == '%%':
            if msgtext[2:7] == 'Leave': # 若為離開聊天室的指令
                # 建立Leave Request訊息的dict物件
                msgdict = {
                    "type": 11,
                    "nickname": nickname
                }
                msgdata = json.dumps(msgdict).encode('utf-8')
                print(msgdata)
                sock.sendto(msgdata, server_addr) # 送到Server
        else:
            # 建立Message Request訊息的dict物件
            msgdict = {
                "type": 4,
                "nickname": nickname,
                "message": msgtext
            }
        # 轉成JSON字串，再轉成bytes
        msgdata = json.dumps(msgdict).encode('utf-8')
        print(msgdata)
        sock.sendto(msgdata, server_addr)
        # 如果送出的是Leave Request，則結束程式
        if (msgdict['type']==11):
            print("Leave") # 除錯用
            os._exit(0)

        now_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        text_message.insert('end',now_time+'\n')#傳送時間
        text_message.insert('end','我: ' + text_text.get('0.0','end'))#訊息內容
        text_text.delete('0.0','end')

def cancel():# 取消輸入文字
    text_text.delete('0.0','end')

def get_msg():
    #print('執行緒get_msg開始')
    global s
    while True:
        try:
            data, address = sock.recvfrom(MAX_BYTES)
            msgdict = json.loads(data.decode('utf-8'))
            # 依照type欄位的值做對應的動作
            if msgdict['type'] == 3:
                welcome = '歡迎 '+ msgdict['nickname']+' 加入聊天室' 
                print(welcome)
                text_message.insert('end',welcome+'\n' )
                listbox.insert('end',msgdict['nickname'])###
            ## Message Response(5)：這是之前Message Request的回應訊息
            if msgdict['type'] == 5:
                # 不需做任何處理
                print('Get Message Response from server.') # 除錯用
                pass 
            ## Message Transfer(6)：這是其他Client所發布的訊息
            if msgdict['type'] == 6:
                print('Get Message Transfer from server.') # 除錯用
                # 以「nickname: message content」的格式印出
                print(msgdict['nickname'] + ': ' + msgdict['message'])
                now_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                text_message.insert('end',now_time + '\n' + msgdict['nickname'] + ': ' + msgdict['message'])
            if msgdict['type'] == 8:     #server傳回來選擇rand()的值
                    print(msgdict['message'])
                    text_message.insert('end',"為您選擇的是:"+ msgdict['message']+'\n' )
            if msgdict['type'] == 12:    #某client離開
                bye = msgdict['nickname']+' 離開聊天室' 
                text_message.insert('end',bye+'\n' )
                print(bye)
            if msgdict['type'] == 10:    #目前用戶有誰
                msgdict["message"].insert(0,'-----目前用戶-----')
                #print(msgdict["message"])##list
                vlist.set(msgdict["message"])
        except:
            break


nickname = input('請輸入你留言時的綽號/別名：') # 請使用者輸入他的nickname
 # 準備Enter Request訊息的dict物件
msgdict = {
    "type": 1,
    "nickname": nickname
}
 # 轉成JSON字串，再轉成bytes
data = json.dumps(msgdict).encode('utf-8')
sock.sendto(data, server_addr) # 將Enter Request送到Server
# 等待並接收Server傳回來的訊息，若為Enter Response則繼續下一步，否則繼續等待
is_entered = False
while not is_entered:
    try: # 擷取recvfrom()的例外狀況
        data, address = sock.recvfrom(MAX_BYTES)
        msgdict = json.loads(data.decode('utf-8'))
        if msgdict['type'] == 2:
            is_entered = True
            print('成功進入伺服器!!!')          
    except ConnectionResetError:  # 前一次的sendto()沒有送成功 (Server沒起來)
        # 印出重送提示訊息，5秒後重新傳送
        print('伺服器連線失敗，5秒後重試')
        for i in range(5):
            time.sleep(1)
            print('.', end='', flush=True)
        print()
        data = json.dumps(msgdict).encode('utf-8')
        sock.sendto(data, server_addr)

def callback():#確認是關閉
    a=messagebox.askquestion("詢問：","確定要離開吗？") # yes或no
    if a=='yes':
        window.destroy() # 返回值為yes就退出
        msgdict = {
                    "type": 11,
                    "nickname": nickname
                }
        msgdata = json.dumps(msgdict).encode('utf-8')
        print(msgdata)
        sock.sendto(msgdata, server_addr) # 送到Server
        print('程式結束') 
        os._exit(0)#程式結束

def user_list():
    msgdict = {
                "type": 9,
                "nickname": nickname
            }
    msgdata = json.dumps(msgdict).encode('utf-8')
    print(msgdata)
    sock.sendto(msgdata, server_addr) # 送到Server

get_msg_thread = threading.Thread(target=get_msg)
get_msg_thread.start()     

#Tk()建立 tkinter 視窗物件
window = tk.Tk() 
window.title('七嘴八舌')
window.protocol("WM_DELETE_WINDOW",callback)
window.resizable('False','False')#固定視窗是否可移動
TWtime=tk.StringVar()#台灣時間，使用在showtime

message_frame= tk.Frame(window,width=480,height=300)
text_frame   = tk.Frame(window,width=480,height=100)
send_frame   = tk.Frame(window,width=480,height=40 )
list_frame   = tk.Frame(window,width=130,height=300)
user_frame   = tk.Frame(window,width=130,height=100)
time_frame   = tk.Frame(window,width=130,height=40 )

message_frame.grid(row=0,column=0,padx=3,pady=6)
text_frame.grid   (row=1,column=0,padx=3,pady=6)
send_frame.grid   (row=2,column=0)
list_frame.grid   (row=0,column=2)
user_frame.grid   (row=1,column=2)
time_frame.grid   (row=2,column=2)

message_frame.grid_propagate(0)
text_frame   .grid_propagate(0)
send_frame   .grid_propagate(0)
list_frame   .grid_propagate(0)
user_frame   .grid_propagate(0)
time_frame   .grid_propagate(0)

###message_frame、text_frame
text_message=tk.Text(message_frame)
text_text=tk.Text(text_frame)

text_message.grid()
text_text.grid()
###send_frame
button_send=tk.Button(send_frame,font=('Arial',10),text='發送',command=send_message)
button_cancel=tk.Button(send_frame,font=('Arial',10),text='刪除',command=cancel)
label_space=tk.Label(send_frame)#空白
box=ttk.Combobox(send_frame,width=10,values=[' ','幫我選擇','收尋'])
btn_selection=tk.Button(send_frame,font=('Arial',10),text='確定',command=confirm)

button_send.grid(row=2,column=0,padx=4,pady=1,ipadx=15,ipady=4)
button_cancel.grid(row=2,column=1,padx=12,pady=1,ipadx=15,ipady=4)
label_space.grid(row=2,column=2,padx=65)
box.grid(row=2,column=3,padx=20)
btn_selection.grid(row=2,column=4)
###list_frame
vlist=tk.StringVar()
vlist.set('-----目前用戶-----')
#listbox滾輪
scrollbar1=tk.Scrollbar(list_frame)
scrollbar1.grid(row=0,column=1,sticky=tk.NS)

listbox=tk.Listbox(list_frame,yscrollcommand=scrollbar1.set,listvariable=vlist,width=15)
scrollbar1.config(command=listbox.yview)
listbox.grid(row=0,column=0,ipady=70)
###user_frame
button_list=tk.Button(user_frame,font=('Arial',10),text='更新用戶',width=8,command=user_list)
button_list.grid(row=0,column=0,padx=20,pady=30,ipady=7)
###time_frame
label_clock=tk.Label(time_frame,anchor='e',textvariable=TWtime)
label_clock.grid(row=0,column=0,padx=10)
#text_message滾輪
scrollbar=tk.Scrollbar(window,command=text_message.yview)
text_message.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0,column=1,sticky=tk.NS)

text_message.insert('end',"歡迎你("+nickname+")加入聊天室!!\n請輸入聊天訊息：\n")
showtime()#更新時間

window.mainloop()