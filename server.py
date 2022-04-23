# #소켓 통신을 위한 모듈  import
# import socket
# #통신을 위한 소켓 생성
# sock = socket.socket()
#
# #클라이언트가 연결할 주소(그리고 포트) 바인
# #port =  종단간 통신의 출입구(0~65535개)
# sock.bind(('127.0.0.1', 3000))
#
# # 클라이언트 연결 대기 모드
# # 파라미터값은 연결 큐의 최대 크기 (=한번에 입장 가능한 수)
# sock.listen(5)
#
# #이 라인에서 대기하면서 클라이언트 측의 연결 요청을 기다림
# # 연결이 되면 클라이언트 소켓과 주소를 반환
# client_sock, address = sock.accept()
#
# print(address,'에서 연결 요청')
#
# while True:
#     #최대 255길이의 데이터를 수신
#     data = client_sock.recv(255)
#     msg = data.decode(encoding='utf8')  #data가 바이너리 값이므로 utf8 형식으로 변환
#     print("client: ", msg)
#
#     msg = input("server: ")
#     client_sock.send(bytes(msg,encoding='utf8'))


import socket
# 스레드를 사용하기 위한 모듈
import threading
import time


class SockServer:
    def __init__(self, address, port ):
        #바인딩 할 주소와 포트
        self.address = address
        self.port = port

        #소켓 생성
        self.sock = socket.socket()

        #클라이언트 소켓 리스트
        self.clients = []

    def accept(self):
        #바인딩, 리슨
        self.sock.bind(
            (self.address, self.port)
        )
        self.sock.listen(5)
        while True:
            client_sock, address = self.sock.accept()
            client_sock.settimeout(0.01)    #
            self.clients.append(client_sock)
            print(address,"에서 연결")

    def send(self):

        while True:
            msg = input()
            for c in self.clients:
                try:
                   c.send(bytes(msg, encoding='utf8'))
                except socket.timeout:
                    continue



    #클라이턴트 소켓으로부터 데이터 수신

    def recv(self):
        while True:
            for c in self.clients:
                try:
                    data = c.recv(255)
                    msg = data.decode(encoding='utf8')
                    print(msg)
                except socket.timeout:
                    continue

    #통신 시작 함수
    def communicate(self):
        #각각의 스레드 생성
        t_accept = threading.Thread(target=self.accept, daemon = True)
        t_send = threading.Thread(target=self.send, daemon=True)
        t_recv = threading.Thread(target=self.recv,daemon=True)

        t_accept.start()
        t_send.start()
        t_recv.start()


        #프로그램 종료 방지
        while True:
            time.sleep(1000)

server = SockServer('127.0.0.1',3000)
server.communicate()