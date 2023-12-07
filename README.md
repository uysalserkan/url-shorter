# URL Shortener Service

![URL Shortener Logo](imgs/url_shorter_logo.png)

## TODO:

* [x] Add Makefile.
  * [ ] Add workflow automations.
* [ ] Add Dockerfile.
* [ ] Add unittests.
* [x] Create upload a file endpoint.
  * [x] Implement MinIO.
  * [x] Update DB class.
* [ ] Add validation functions.
  * [ ] For URLs.
* [ ] Run another thread for delete expired urls.
* [ ] Add CI / CD file on GitHub.

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
- SQLAlchemy (for database interaction)
- MinIO (for object storage)
- Dynaconf (for configs)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/uysalserkan/url-shorter.git
   cd url-shortener
    ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Run application

   ```bash
   uvicorn app:app --port 25250
   ```

# License

This project is licensed under the [Apache License](LICENSE).