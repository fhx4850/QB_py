import socket
from urls import url_path
from QB.rout.url import UrlRouting
import QB.settings as settings


class _ServerResponce:
    def __init__(self, request):
        self.responce = None
        self._URLS = UrlRouting.URLS
        self._create_response(request)

    def get_responce(self):
        return self.responce

    def set_responce(self, responce):
        self.responce = responce

    def _create_response(self, request):
        """The method collects all the necessary data to respond to the user."""
        request = request.decode('utf-8')
        method, url, file_path = self._get_request_string(request)
        header, code = self._create_headers(method, url)
        body = self._create_body(code, url)
        if file_path and file_path != 'resources':
            file = self._render_file(file_path)
            self.set_responce(file)
        else:
            self.set_responce((header + body).encode())

    def _get_request_string(self, request):
        """Splits the string data of the client request into (method, url, file_path)."""
        parsed = request.split(' ')
        # Web request method.
        method = parsed[0]
        # Request addres
        url = parsed[1]
        file_path = None
        if url.find('.') != -1:
            path = settings.RESOURCEDIR + str(url).partition(settings.RESOURCEDIR)[2]
            file_path = self._find_file(path)

        return method, url, file_path

    def _create_headers(self, method, url):
        """Create headers for the response."""
        if not method == 'GET':
            return 'HTTP/1.1 405 Method not allowed\n\n', 405

        if not url in self._URLS:
            return 'HTTP/1.1 404 Not found\n\n', 404

        return 'HTTP/1.1 200 OK\n\n', 200

    def _create_body(self, code, url):
        """Creates a request body by calling the passed function in url."""
        if code == 404:
            return '<h1>404</h1><p>Not found</p>'
        elif code == 405:
            return '<h1>405</h1><p>Method not allowed</p>'
        else:
            return self._URLS[url]()

    def _render_file(self, file_path):
        """Processing files for transmission in response."""
        with open(file_path, 'rb') as file:
            response = file.read()

        header = 'HTTP/1.1 200 OK\n'

        # Determining the file extension.
        if file_path.endswith(".jpg"):
            mimetype = 'image/jpg'
        elif file_path.endswith(".css"):
            mimetype = 'text/css'
        else:
            mimetype = 'text/html'

        header += 'Content-Type: ' + str(mimetype) + '\n\n'

        final_response = header.encode('utf-8')
        final_response += response

        return final_response

    def _find_file(self, path):
        myfile = path.lstrip('/')
        return myfile


class IpTcpServer:
    """Server implementation."""

    def __init__(self, ip: str, port: int):
        self._serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._serv_socket.bind((ip, port))
        UrlRouting(url_path)
        self._URLS = UrlRouting.URLS
        self.dd = ""

    def run(self):
        self._serv_listen()

    def _serv_listen(self):
        self._serv_socket.listen()
        while True:
            client, addr = self._serv_socket.accept()
            self._client_thread(client)

    def output_request_log(self, request):
        request_url = request.decode('utf-8')
        print(str(request_url).splitlines()[0])

    def _client_thread(self, client):
        """Processing client requests."""
        while True:
            request = client.recv(4048)
            sr = _ServerResponce(request)
            response = sr.get_responce()
            client.send(response)
            client.close()
            break
        self.output_request_log(request)