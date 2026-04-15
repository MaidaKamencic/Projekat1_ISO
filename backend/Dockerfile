FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt
COPY app.py /app/app.py
EXPOSE 5000
CMD ["python", "/app/app.py"]