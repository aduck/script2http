FROM python:3.8.13-slim-buster
WORKDIR /app
COPY . .
RUN pip install -r requirement.txt
VOLUME ['/app/scripts']
EXPOSE 5000
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "main:app"]