FROM python:3.7

WORKDIR /ml_models

ADD . /ml_models

RUN pip install --upgrade cython
RUN pip install --upgrade numpy

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "ml_app.py"]
