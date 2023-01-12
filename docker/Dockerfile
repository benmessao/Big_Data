FROM python:3

WORKDIR /DOCKER

COPY app.py ./

RUN pip install pandas numpy plotly streamlit

COPY . .

CMD ["streamlit","run","app.py","--server.port=4000"]