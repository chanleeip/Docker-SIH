FROM python:3.11-alpine
WORKDIR /backend
COPY . .
RUN pip install -r requirement.txt
EXPOSE 5000
CMD [ "python","app.py" ]