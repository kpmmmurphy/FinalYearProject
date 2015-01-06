import socket
import time

#UDP_IP = "192.168.52.2"
#UDP_PORT = 5005
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007


test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
test_socket.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    print sock.recv(10240)

last_time = 0
running = True
while running:
    try:
        current_time = time.time()
        if(current_time > last_time + 2):
            last_time = current_time
            test_socket.connect(("192.168.52.1", 80))
            test_socket.sendto("WHOOP", (UDP_IP, UDP_PORT))
            print("sent")

    except Exception:
        running = False
        test_socket.close()
        raise
test_socket.close()