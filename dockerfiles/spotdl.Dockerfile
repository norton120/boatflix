ARG SPOTDL_VERSION=latest
FROM spotdl/spotify-downloader:${SPOTDL_VERSION}
CMD ["web", "--host", "0.0.0.0", "--port", "5050"]
