from QB.server.server import IpTcpServer
# from QB.cli.main_cli import MainCli

if __name__ == '__main__':
    serv = IpTcpServer('127.0.0.1', 8888)
    # MainCli._perform_action()
    serv.run()