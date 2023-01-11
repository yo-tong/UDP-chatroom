import socket
import json
import random
from threading import Thread
MAX_BYTES = 65535
my_port = 6000
client_list = [] # 存放Client資訊的清單

 # 創建一個socket，並bind在指定的address
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('0.0.0.0',my_port))
print('Listening at {}'.format(sock.getsockname()))
  # 處理來自Client訊息的無窮迴圈

if __name__ == '__main__': 
    print('伺服器已經開啟')
while(True): # 接收來自Client的訊息，取得訊息內容(data)與地址資訊(address)
    try:
        data, address = sock.recvfrom(MAX_BYTES)
    except ConnectionResetError:
        continue
    text = data.decode('utf-8')
    print('The client at {} says {!r}'.format(address, text))
    # 將訊息內容由JSON字串轉成dict物件
    message = json.loads(text)
     # 依照type欄位的值做對應的動作
    ## Enter Request (1)：有一個新的Client加入
    if message['type'] == 1:
        # 新建一個Client的dict物件來存放它的資訊
        new_client = {
            'nickname': message['nickname'],
            'address': address
        }
        print('Enter Request：', new_client) # 除錯用
         # 將新Client的dict物件加入list中
        client_list.append(new_client)
         # 送回Request Response訊息
        msgdict = {
            "type": 2,
            "nickname": message['nickname'],
            "isAllow":'yes'
        }
        data = json.dumps(msgdict).encode('utf-8')
        sock.sendto(data, address)
        print('Send back Enter Response to', address) # 除錯用

        msgdict = {
            "type":3,
            "nickname": message['nickname']
        }
        data = json.dumps(msgdict).encode('utf-8')
        for client in client_list:
            if client['address'] != address:
                sock.sendto(data, client['address']) 

 ## Message Request (4)：有一個Client送來聊天訊息
    elif message['type'] == 4:
         # 建立一個Message Response (5) 訊息，送回給來源Client
        msgdict = {
             "type": 5
        }
        data = json.dumps(msgdict).encode('utf-8')
        sock.sendto(data, address)
        print('Send back Message Response to', address) # 除錯用
         # 建立一個Message Transfer (6)訊息
        msgdict = {
             "type": 6,
             "nickname": message['nickname'], # 來源Client的綽號
             "message": message['message']  # 來源Client的聊天內容
        }
        data = json.dumps(msgdict).encode('utf-8')
        # 針對每一個在client_list中的每一個Client，
        # 轉送Message Transfer訊息給他們 (來源Client除外)
        for client in client_list:
            if client['address'] != address:
                sock.sendto(data, client['address']) 
                print('Transfer message to', client['address'] ) # 除錯用

    elif message['type'] == 7: 
        if(message['message']==["error"]):
            pass
        else:
            result=(random.choice(message['message']))
            msgdict = {
                "type": 8,
                "nickname": message['nickname'], # 來源Client的綽號
                "message": result  # 來源Client的聊天內容
            }   
            data = json.dumps(msgdict).encode('utf-8')
            sock.sendto(data, address)
            print(msgdict)
    elif message['type'] == 11:
          # 建立一個暫時的Client dict物件來存放要離開的client資訊
        new_client = {
                  'nickname': message['nickname'],
                  'address': address
                    }
        msgdict = {
            "type": 12,
            "nickname": message['nickname'], 
        }   
        print('Leave Request: ', new_client)
            # 若這個Client dict物件存在於client_list清單中，
            # 則將之從client_list中移除
        if  new_client in client_list:
            client_list.remove(new_client)
            data = json.dumps(msgdict).encode('utf-8')
            for client in client_list:
                if client['address'] != address:
                    sock.sendto(data, client['address']) 
            print('Leave Request: remove successfully') #除錯用
        else:
              print('Leave Request: remove failed')
              pass
    elif message['type'] == 9:
        user=[]
        for client in client_list:#在client_list的，client用戶加到user[]
            user.append(client['nickname']) 
        msgdict = {
                "type": 10,
                "nickname": message['nickname'], # 來源Client的綽號
                "message": user # 來源Client的內容
            } 
        data = json.dumps(msgdict).encode('utf-8')
        sock.sendto(data, address)
        print(msgdict)
 