import socket
from monitor import check_port

def test_check_port_open():
    try:
        temp_server = socket.socket()
        temp_server.bind(("127.0.0.1",0))
        temp_server.listen()
        host, port = temp_server.getsockname()

        status = check_port(host, port)[0]
        assert "OPEN" == status

    finally:
        temp_server.close()

def test_check_port_Error():

    temp_server = socket.socket()
    temp_server.bind(("127.0.0.1",0))
    host, port = temp_server.getsockname()
    temp_server.close()

    status = check_port(host, port)[0]
    assert "ERROR" == status
