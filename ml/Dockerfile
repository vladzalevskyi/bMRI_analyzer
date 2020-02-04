FROM python:3.7

WORKDIR /ml_models

ADD . /ml_models

RUN pip install --upgrade cython
RUN pip install --upgrade numpy
RUN pip install fastapi uvicorn
RUN pip install -r requirements.txt

VOLUME ["/uploads"]
EXPOSE 5002

CMD ["uvicorn", "ml_app:app", "--reload", "--host",  "0.0.0.0", "--port" , "5002"]
