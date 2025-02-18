FROM python:3.9-alpine

WORKDIR /felix-bernard-website/docker/

RUN python3 -m pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080

EXPOSE 8080

CMD ["python3", "main.py"]