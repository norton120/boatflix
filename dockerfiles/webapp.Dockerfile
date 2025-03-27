FROM python:3.12
ARG ENVIRONMENT=production
ENV PYTHONPATH=/app
COPY ./webapp /app/webapp
WORKDIR /app
RUN pip install -r /app/webapp/requirements/${ENVIRONMENT}-requirements.txt
CMD ["uvicorn", "webapp.app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]