import socket
import select
import sys
# 서버에 접속한다.
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000)) #localhost : 127.0.0.1 

name = None

#무한루프로 서버로부터 메세지를 기다림
while True :
    # 소켓에서 메시지를 읽을 수 있을 때 까지 대기
    # 엔터칠때까지 기다림
    read , write , fail = select.select((s, sys.stdin), () , ())
    # 메세지가 도착하면 소켓에서 4096 바이트를 읽는다.
    for desc in read :
        #서버에서 온 메세지라면
        if desc == s:
            data = s.recv(4096)
            # 바이트 -> 문자열 출력
            print(data.decode())

            if name is None :
                name = data.decode()
                s.send(f'{name} is connected!!'.encode())

        #사용자가 입력한거라면     
        else :
            #사용자가 입력한 문자열을 읽어서
            msg = desc.readline()
            msg = msg.replace('\n' , '')
            s.send(f'{name} {msg}'.encode())