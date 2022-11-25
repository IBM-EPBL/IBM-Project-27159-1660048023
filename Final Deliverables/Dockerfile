FROM python:3.10.6

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]