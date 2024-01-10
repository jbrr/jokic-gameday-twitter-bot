FROM public.ecr.aws/lambda/python:3.12

COPY function.py requirements.txt .env ./
COPY assets ./assets

RUN pip install -r requirements.txt

CMD ["function.handler"]