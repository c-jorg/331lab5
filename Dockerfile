FROM python:3
COPY mathservice.py .
EXPOSE 8080
CMD ["python", "./mathservice.py"]  