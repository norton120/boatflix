FROM ghcr.io/dtcooper/raspberrypi-os:python3.12-bullseye
COPY ./host /boatflix
ENV PYTHONPATH=/boatflix
RUN pip install -r /boatflix/requirements/development-requirements.txt
