FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
VOLUME /etc/devops
ENTRYPOINT ["python3", "main.py", "--compose", "/etc/devops/docker-compose/docker-compose.yml", "--nginx", "/etc/devops/nginx/template-nginx.conf", "--out", "/etc/devops/nginx/nginx.conf", "--deny", "nginx", "ngen"]