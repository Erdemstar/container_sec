# Container Security

In this repository, there is a django-based web application that I developed for container security. On the basis of the application, there are 3 endpoints that will perform Dockerfile bestpractice scanning, Image scanning and Dockerfile bestpractice and image scanning at the same time. You can trigger them manually or via a tool that sends API/HTTP requests. In addition, the results are produced in json format and easy to parse.

# Setup


### Image Scan (grype)
Since scanning Docker Image is a different concept in itself, **anchor/grype**,which is known in the Open source world, is used here. Below is the link to install. You can check the relevant steps and perform a healthy installation.

https://github.com/anchore/grype#installation

**Note**: After installation, run **grype** from the terminal and check if there is a problem.

### Celery Settings 
The application also uses celery to perform asynchronous task management. If you want to change the relevant celery settings, you can touch the constants starting with CELERY from the Settings.py section of the application.

### Flower Settings 
A module called Flower is used to see Celery's work in the web application. This module shows the tasks that Celery has done on the Web. If you want to change the relevant flower settings, you can touch the constants starting with FLOWER from the Settings.py section of the application.

### Broker Settings
Celery needs brokers during operation. Redis is used in this project. Redis was not installed on the main host during development and used as a Docker container.

    docker run -d --name redis -p 6379:6379 redis:latest

**Note** : If you want to use a different broker or port, you must define this change as "CELERY_BROKER_URL", "CELERY_RESULT_BACKEND" in Settings.
 

### App Settings 
You will see the settings.py file in the container_sec/container_sec section in the directory where you downloaded the application codes. At the bottom of this file, some constant values used by the application are defined. Some of these fields are already given above with default values for parts.

| Field | Explanation |
|--|--|
| APP_BASE_PATH | The folder path of the application in the operating system |
| APP_FILE_UPLOAD_PATH | File upload file path used by the application itself |
| APP_DOCKERFILE_PATH | File path where the application keeps Dockerfiles |
| APP_IMAGESCAN_PATH | File path where the application stores the Image Scan result |
| APP_HTTP_URL | The part where the HTTP host and port information of the application is given |
| APP_DOCKERFILE_HTTP_URL | HTTP Endpoint on the Dockerfile side of the application |
| APP_IMAGE_SCANNER_HTTP_URL | HTTP Endpoint on the ImageScan side of the application |
|||
| CELERY_BROKER_URL | Broker information that Celery will use |
| CELERY_RESULT_BACKEND | Backend information where Celery will record the results |
|||
| FLOWER_HTTP_URL | HOST and Port information where Flower application is running |
| FLOWER_API_TASK_HTTP_URL | Flower Task API Endpoint part |

### Dependency Settings
 The library information used by the application is in the requirements.txt. You can install using the command below.
 
    pip3 install -r requirements.txt

**Note**: I use [virtualenv](https://virtualenv.pypa.io/en/latest/) to avoid any problems while installing the dependencies of this and similar projects.

# Run
After the above settings are made, the application is ready to run. You can run the application by following the steps below.

### Redis
If you haven't installed redis yet, it will be quickly installed in the Docker environment using the command below and then run.

    docker run -d --name redis -p 6379:6379 redis:latest

### Celery
The celery will stand up when the following command is run by switching to the container_sec folder from the folder where the codes are located.

    celery -A container_sec.celery worker --loglevel=INFO

### Flower
The flower will stand up when the following command is run by switching to the container_sec folder from the folder where the codes are located.

    celery -A container_sec flower --port=5555

### App
If there is no problem in the above steps, all we have to do is to remove the Django application. For this, it will be sufficient to switch to the container_sec folder from the folder where the codes are located and run the following command.

    python3 manage.py runserver

# PoC
[![Container_Security_Application.gif](https://s9.gifyu.com/images/Container_Security_Application.gif)](https://gifyu.com/image/SmECA)

I took a screen recording to show you how your app works. You can access it via the [link](www.youtube.com/watch?v=Q3AzFpCBPZM).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)