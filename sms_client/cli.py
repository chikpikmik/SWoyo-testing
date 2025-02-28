import argparse
import logging
import json
import base64
import asyncio
from urllib.parse import urlparse
from typing import Dict

from .config import load_config
from .http import HttpRequest
from .client import send_request

def setup_logging():
    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

async def main():
    setup_logging()

    parser = argparse.ArgumentParser(description='Отправка СМС через API')
    parser.add_argument('--sender', required=True, help='Номер отправителя')
    parser.add_argument('--recipient', required=True, help='Номер получателя')
    parser.add_argument('--message', required=True, help='Текст сообщения')
    args = parser.parse_args()

    logging.info(f'Аргументы: sender={args.sender}, recipient={args.recipient}, message={args.message}')

    try:
        config = load_config()
        server_url = config['server_url']
        username = config['username']
        password = config['password']



        body = json.dumps({
            'sender':    args.sender,
            'recipient': args.recipient,
            'message':   args.message
        }).encode('utf-8')

        basic_auth = base64.b64encode(f'{username}:{password}'.encode()).decode() #dGVzdDp0ZXN0
        parsed_url = urlparse(server_url)
        host = parsed_url.hostname
        port = parsed_url.port or 80

        headers = {
            'Host': f'{host}:{port}',
            'Content-Type': 'application/json',
            'Authorization': f'Basic {basic_auth}',
            'Content-Length': str(len(body))
        }

        request = HttpRequest('POST', '/send_sms', headers, body)
        response = await send_request(host, port, request)

        print(f'Код ответа: {response.status_code}')
        print(f'Тело ответа: {response.body.decode()}')

        logging.info(f'Ответ: код={response.status_code}, тело={response.body.decode()}')
    
    except Exception as e:
        logging.error(f'Ошибка: {str(e)}')
        print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    asyncio.run(main())