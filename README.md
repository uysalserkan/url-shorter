# URL Shortener Service

```text
db    db d8888b. db             .d8888. db   db  .d88b.  d8888b. d888888b d88888b d8888b.
88    88 88  `8D 88             88'  YP 88   88 .8P  Y8. 88  `8D `~~88~~' 88'     88  `8D
88    88 88oobY' 88             `8bo.   88ooo88 88    88 88oobY'    88    88ooooo 88oobY'
88    88 88`8b   88      C8888D   `Y8b. 88~~~88 88    88 88`8b      88    88~~~~~ 88`8b  
88b  d88 88 `88. 88booo.        db   8D 88   88 `8b  d8' 88 `88.    88    88.     88 `88.
~Y8888P' 88   YD Y88888P        `8888Y' YP   YP  `Y88P'  88   YD    YP    Y88888P 88   YD

```

![GitHub License](https://img.shields.io/github/license/uysalserkan/url-shorter)
![GitHub issues](https://img.shields.io/github/issues/uysalserkan/url-shorter)
![GitHub pull requests](https://img.shields.io/github/issues-pr/uysalserkan/url-shorter)
![GitHub Repo stars](https://img.shields.io/github/stars/uysalserkan/url-shorter)
![GitHub forks](https://img.shields.io/github/forks/uysalserkan/url-shorter)
![GitHub repo size](https://img.shields.io/github/repo-size/uysalserkan/url-shorter)


## TODO:

* [x] Add Makefile.
* [x] Add Prometheus metrics.
* [x] Make SQL Engine singlethon.
* [x] Add Dockerfile.
* [x] Change response between browser and curl.
* [x] Run another thread for delete expired urls.
* [x] Create upload a file endpoint.
  * [x] Implement MinIO.
  * [x] Update DB class.
* [x] Add validation functions.
  * [x] For URLs.
  * [x] Is expired?
  * [x] Delete files which not exist on DB.
* [ ] Add unittests.
* [ ] Add CI / CD file on GitHub.
    * [ ] Add workflow automations.
* [ ] Add delete after download/visit option.

## Introduction

The URL Shortener Service is a simple and efficient tool for shortening long URLs into concise and easy-to-share links. This service is designed to provide users with shortened URLs that redirect to the original long URLs.

## Features

- Shorten long URLs to generate compact and shareable links.
- Access detailed analytics and statistics for each shortened URL.
- Customize the shortened URL with a custom alias or keyword.
- Easy-to-use web interface and RESTful API for integration with other applications.

## Getting Started

### Prerequisites

- Python 3.x
- FastAPI (for the web application)
- Uvicorn
- SQLModel (for database interaction)
- MinIO (for object storage)
- Dynaconf (for configs)
- Prometheus (data collection)

### Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/uysalserkan/url-shorter.git
   cd url-shortener
    ```

2. Install dependencies

   ```shell
   conda env create -n url-shorter --file conda_env.yaml
   ```

3. Run application

   ```shell
   uvicorn app:app --port 25250
   ```

### Run Docker

1. ```shell
   docker build -t url-shorter .
   ```

2. ```bash
   # Install MinIO
   docker run -d \                                                        
    -p 9000:9000 \      
    -p 9090:9090 \
    --name minio \
    -v ~/minio/data:/data \
    -e "MINIO_ROOT_USER=minioadmin" \
    -e "MINIO_ROOT_PASSWORD=minioadmin" \
    quay.io/minio/minio server /data --console-address ":9090"
   ``` 

3. ```shell
   docker run -n url-shorter-container -p 80:80 --network host url-shorter
   ```

# License

This project is licensed under the [Apache License](LICENSE).
