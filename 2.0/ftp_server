from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def create_ftp_server():
    ftp_root_directory = r'C:\Users\Billy\PycharmProjects\FTP SERVER\project_resource'
    # Create an instance of the DummyAuthorizer class for managing 'virtual' users
    authorizer = DummyAuthorizer()

    authorizer.add_user("admin", "admin", ftp_root_directory, perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    server_address = ('127.0.0.1', 22)

    server = FTPServer(server_address, handler)

    print("Starting FTP server on 127.0.0.1:22. Connect with username 'admin' and password 'admin'.")
    server.serve_forever()

if __name__ == "__main__":
    create_ftp_server()
