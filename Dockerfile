FROM python:3.12-alpine
WORKDIR /app
COPY index.html yapim.html server.py ./
CMD ["python", "server.py"]
