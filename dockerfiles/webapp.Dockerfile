FROM python:3.12
COPY ./webapp /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD streamlit run main.py