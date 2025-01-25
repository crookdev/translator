FROM python:3.12

WORKDIR /code

COPY ./api/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Related to the on-premise service setup
COPY ./on-prem-service-setup/api-cognitive-services/download_hf_models.py /code/download_hf_models.py
RUN python3 ./download_hf_models.py

COPY ./api/app /code/app

EXPOSE 80

# Run the application
CMD ["fastapi", "run", "app/main.py", "--port", "80"]