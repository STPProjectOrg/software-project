FROM python:3.10
EXPOSE 8000
WORKDIR /app 
COPY requirements.txt /app
#RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app 
ENTRYPOINT ["python3"] 
CMD ["app/manage.py", "runserver", "0.0.0.0:8000"]

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
CMD ["app/manage.py", "runserver", "0.0.0.0:8000"]