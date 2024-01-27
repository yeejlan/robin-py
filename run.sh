uvicorn main:app --host 0.0.0.0 --port 9000 --no-access-log

#uvicorn main:app --host 0.0.0.0 --port 9000 --reload --log-config uvicorn.json --no-access-log


# install packages
# pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

#list installed packages
pip3 list

#redis instance
#docker run -p 6379:6379 redis/redis-stack:latest