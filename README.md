# URL Shortener Service

```text
db    db d8888b. db             .d8888. db   db  .d88b.  d8888b. d888888b d88888b d8888b.
88    88 88  `8D 88             88'  YP 88   88 .8P  Y8. 88  `8D `~~88~~' 88'     88  `8D
88    88 88oobY' 88             `8bo.   88ooo88 88    88 88oobY'    88    88ooooo 88oobY'
88    88 88`8b   88      C8888D   `Y8b. 88~~~88 88    88 88`8b      88    88~~~~~ 88`8b  
88b  d88 88 `88. 88booo.        db   8D 88   88 `8b  d8' 88 `88.    88    88.     88 `88.
~Y8888P' 88   YD Y88888P        `8888Y' YP   YP  `Y88P'  88   YD    YP    Y88888P 88   YD

```

## TODO:

* [x] Add Makefile.
* [x] Add Prometheus metrics.
* [x] Make SQL Engine singlethon.
* [ ] Add Dockerfile.
* [ ] Add unittests.
* [x] Create upload a file endpoint.
  * [x] Implement MinIO.
  * [x] Update DB class.
* [ ] Add validation functions.
  * [ ] For URLs.
  * [ ] Is expired?
* [x] Run another thread for delete expired urls.
* [ ] Add CI / CD file on GitHub.
  * [ ] Add workflow automations.
* [x] Change response between browser and curl.

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

   ```bash
   git clone https://github.com/uysalserkan/url-shorter.git
   cd url-shortener
    ```

2. Install dependencies

   ```bash
   conda env create -n url-shorter --file conda_env.yaml
   ```

3. Run application

   ```bash
   uvicorn app:app --port 25250
   ```

# License

This project is licensed under the [Apache License](LICENSE).
