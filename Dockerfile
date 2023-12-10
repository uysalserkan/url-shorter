FROM condaforge/mambaforge
#FROM debian:bullseye-slim
LABEL authors="serkan.uysal"

#RUN apt-get update && apt-get install wget -y
#RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /opt/miniconda-installer.sh
#RUN bash /opt/miniconda-installer.sh -b
WORKDIR /

COPY models/ models/
COPY controller/ controller/
COPY app.py .
COPY engines.py .
COPY config.py .
COPY conda_env.yaml environment.yaml
COPY *.toml .

RUN conda --version
RUN conda env update --name base --file environment.yaml
RUN conda install --name base -c conda-forge uvicorn -y

CMD ["uvicorn", "app:app", "--port", "80"]