FROM python:3.8
WORKDIR /app
COPY . /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
ENV MYCUISINE_ENV mycuisine-env
CMD ["python", "run.py"]
