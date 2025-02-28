#import socket
import asyncio
from .http import HttpResponse

'''
def send_request(host: str, port: int, request) -> HttpResponse:
    """Отправляет HTTP-запрос через сокет и возвращает ответ."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.send(request.to_bytes())
        response_data = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response_data += chunk
        
        return HttpResponse.from_bytes(response_data)
'''

async def send_request(host: str, port: int, request) -> HttpResponse:
    """Асинхронно отправляет HTTP-запрос через сокет и возвращает ответ."""
    reader, writer = await asyncio.open_connection(host, port)

    try:
        writer.write(request.to_bytes())
        await writer.drain()

        response_data = b''
        while True:
            chunk = await reader.read(4096)
            if not chunk:
                break
            response_data += chunk

        return HttpResponse.from_bytes(response_data)
    
    finally:
        writer.close()
        await writer.wait_closed()
