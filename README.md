# Websocket message forward demo

Install packages

    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

Copy and edit env file

    cp .env.example .env

Start app

    uvicorn main:app --host 0.0.0.0 --port 9000 --no-access-log

Open "socket_client.html" in browser, input token, hit "connect"

    python generate_token.py

Send message

    python send_message_via_uid_cid.py
