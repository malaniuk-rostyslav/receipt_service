### Build and install packages
FROM python:3.8 as build-python

# Cleanup apt cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /server/

WORKDIR /server/
RUN pip install -r requirements.txt

### Final image
FROM python:3.8-slim

# Remove apt chache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=build-python /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/

RUN apt-get update -y
RUN apt-get install wget -y
RUN apt-get install build-essential -y
RUN apt-get install libpq-dev -y


# Copy scripts for starting project
COPY . /server/
WORKDIR /server/


EXPOSE 8003
ENV PYTHONPATH=.

CMD ["uvicorn", "backend.service.main:app", "--reload", "--host=0.0.0.0", "--port=8003"]