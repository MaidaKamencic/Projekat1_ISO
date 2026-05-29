FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt
COPY app.py /app/app.py
COPY wait_for_db.py /app/wait_for_db.py
EXPOSE 5000
CMD ["sh", "-c", "python /app/wait_for_db.py && python /app/app.py"]