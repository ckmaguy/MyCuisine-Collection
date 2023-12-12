FROM python:3.8
WORKDIR /app
COPY . /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV=production
ENV FLASK_APP=run.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
