FROM python:3.10-slim
RUN mkdir "code"
COPY . ./code
WORKDIR /code
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 8090
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090"]