FROM python:3.10.7-slim-buster
WORKDIR /demoapp
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["python","./app.py"]
EXPOSE 5000
