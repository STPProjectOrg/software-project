FROM python:3.10
EXPOSE 8000
WORKDIR /app 
COPY app/requirements.txt /app
#RUN pip install --upgrade pip
RUN pip install -r app/requirements.txt
COPY . /app 
ENTRYPOINT ["python3"] 
CMD ["app/manage.py", "runserver", "139.144.176.245:8000"]

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
CMD ["app/manage.py", "runserver", "139.144.176.245:8000"]