from twisted.internet import protocol, reactor
import names

# 터미널 컬러 코드
COLORS = [
    '\033[31m',
    '\033[32m',
    '\033[33m',
    '\033[34m',
    '\033[35m',
    '\033[36m',
    '\033[37m',
    '\033[4m'
]
transports = set()
users = set()
class Chat(protocol.Protocol) :
    # 사용자가 서버에 속하면 connected 메세지 출력
    def connectionMade(self) :
        name = names.get_first_name()
        color = COLORS[len(users)%len(COLORS)]
        users.add(name)
        
        #사용자가 접속하면 transport(클라이언트) 추가
        transports.add(self.transport)

        # 클라이언트가 연결되면 connected 메세지를 클라이언트에 전송
        self.transport.write('connected    '.encode())
        # 이름을 부여
        self.transport.write(f'{color}{name}\033[0m'.encode())
        
    # 사용자가 서버에 메시지를 보내면 실행 -- 사용자 메세지(data) 출력
    def dataReceived(self, data) :
        for t in transports :
            if self.transport is not t :
                t.write(data)
        #사용자의 데이터를 받아옴
        print(data.decode('utf-8'))

# 통신 프로토콜 정의
class ChatFactory(protocol.Factory) :
    def buildProtocol(self, addr) :
        return Chat()

print('Server started!!')
# TCP 8000번 포트 listen~

reactor.listenTCP(8000, ChatFactory())
reactor.run()