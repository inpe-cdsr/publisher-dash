# publisher-dash

Dash application to plot graphs related to INPE-CDSR project.


## Installation

### Requirements

Make sure you have the following libraries installed:

- [`Python 3`](https://www.python.org/)

Install [`pyenv`](https://github.com/pyenv/pyenv#basic-github-checkout) and [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv#installing-as-a-pyenv-plugin). After that, install Python 3.7.4 using pyenv:

```
$ pyenv install 3.8.5
```

Create a Python environment with the Python version above through pyenv-virtualenv and activate it:

```
$ pyenv virtualenv 3.8.5 inpe_cdsr_publisher_dash && \
    pyenv activate inpe_cdsr_publisher_dash
```

Install the requirements:

```
$ pip install -r requirements.txt
```


## Run the application

Run the application:

```
$ pyenv activate inpe_cdsr_publisher_dash && \
    set -a && source environment.env && set +a && \
    python main.py
```


### Running with Docker

Build image (development or production):

```
$ docker build -t inpe-cdsr-publish-dash -f Dockerfile . --no-cache
$ docker build -t registry.dpi.inpe.br/cdsr/publish-dash:0.0.1 -f Dockerfile . --no-cache
```

Push image to registry:

```
$ docker push registry.dpi.inpe.br/cdsr/publish-dash:0.0.1
```
