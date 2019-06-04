FROM python:3.7-slim
WORKDIR /flaskr-tdd
COPY . /flaskr-tdd
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
