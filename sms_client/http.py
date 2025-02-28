from typing import Dict, Any

class HttpRequest:
    """Класс для представления HTTP-запроса."""
    def __init__(self, method: str, path: str, headers: Dict[str, str], body: bytes):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        """Преобразует запрос в байты."""
        headers = '\r\n'.join([f'{k}: {v}' for k, v in self.headers.items()])
        
        request_line = f'{self.method} {self.path} HTTP/1.1\r\n'
        
        return f'{request_line}{headers}\r\n\r\n'.encode() + self.body


class HttpResponse:
    """Класс для представления HTTP-ответа."""
    def __init__(self, status_code: int, headers: Dict[str, str], body: bytes):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    @classmethod
    def from_bytes(cls, data: bytes) -> 'HttpResponse':
        """Создает объект ответа из байтов."""
        parts = data.split(b'\r\n\r\n', 1)

        header_part = parts[0].decode() if parts else ''
        body = parts[1] if len(parts) > 1 else b''

        headers_lines = header_part.split('\r\n')
        status_line = headers_lines[0] if headers_lines else ''
        status_code = int(status_line.split(' ')[1]) if status_line else 0
        headers = {}

        for line in headers_lines[1:]:
            if line.strip():
                key, value = line.split(': ', 1)
                headers[key] = value
        
        return cls(status_code, headers, body)