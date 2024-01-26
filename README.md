**OVERVIEW**  
In this hotel management system, it's an all in one web app with user side and admin interface.  
The user interface is for normal hotel customers where customers can book,reserve rooms and read interesting and educative blogs  
about hotels and travel.
The admin interface is for specific hotel staff responsible for confirming reservations and allocating rooms.  
Digital receipts are issued as a confirmation of online payment through MTN momo, Airtel money or VISA.  

SETTING UP A DJANGO PROJECT IN DOCKER ON WSL2 FOR DEVELOPMENT.  
**Prerequisites:**
  - [Docker for desktop](https://www.docker.com/products/docker-desktop/)
  - [Vs code text editor](https://visualstudio.microsoft.com/downloads/)
  - [WSL2](https://www.windowscentral.com/how-install-wsl2-windows-10)
    
**STEPS:**
 1. Open Ubuntu on your system.
 2. Run: `sudo apt update && sudo apt upgrade` to update the package lists and upgrade installed packages to their latest versions.
 3. Create a folder to setup your development: `mkdir <your_project_name>`
 4. Navigate to this folder: `cd <your_project_name>`
 5. Assuming python and pip are already installed, run `python3 -m venv <name_for_virtual_environment>` to create a virtual environment for your project. You can find more information about setting up a development environment in wsl2 [here](https://learn.microsoft.com/en-us/windows/wsl/setup/environment).
 6. Run `python3 --version` and `pip3 --version` to check the respective versions of python and pip.
 7. If they aren't up to date, run `pip3 install --upgrade pip` to upgrade pip to the latest version and visit [here](https://docs.python-guide.org/starting/install3/linux/) for a comprehensive guide of how to install python on your machine.
 8. If all is set, activate your virtual environment by running the command: `source <name_for_virtual_environment>/bin/activate`
 9. Lastly, run; `code .` to open Vs code text editor. Note the `.` at the end. The basic setup is now done. It's time to create relevant files within our project.
 10. Within Vs code, press ~Ctrl+Shift+`~ to open your terminal.
 11. Run: `source <name_for_virtual_environment>/bin/activate` to activate your virtual environment.
 12. Install Django by running: `pip install Django`.
 13. Within your root directory, create a file named `Dockerfile`. Note that this file has got no extension.
 14. Populate `Dockerfile` with the following code:
     ```python
     # The image you are going to inherit your Dockerfile from
     FROM python:3.10.12
     # Necessary, so Docker doesn't buffer the output and that you can see the output 
     # of your application (e.g., Django logs) in real-time.
     ENV PYTHONUNBUFFERED 1
     # Make a directory in your Docker image, which you can use to store your source code
     RUN mkdir /hms
     # Set the /hms directory as the working directory
     WORKDIR /hms
     # Copies from your local machine's current directory to the HMS folder 
     # in the Docker image
     COPY . .
     # Copy the requirements.txt file adjacent to the Dockerfile 
     # to your Docker image
     COPY ./requirements.txt /requirements.txt
     # Install the requirements.txt file in Docker image
     RUN pip install -r /requirements.txt
     # Create a non-system user with a home directory
     RUN adduser --disabled-password --gecos "" user
     USER user
     ```
15. In the same directory, create a file `requirements.txt` and run the command: `pip freeze > requirements.txt`
16. Create a new file called `docker-compose.yml`. This should contain all the commands to run our docker containers.Populate it with the following basic code:
    ```python
    # Verion of docker-compose to use 
    version: "3.8"

    services:
     app:
       build:
        context: . #Sets the directory for docker-compose to build.

    # Maps port on the local machine to port on Docker image
    ports:
      - "8000:8000"
      
    volumes: 
    # Copy changes made to the project to your image in real-time.
      - .:/hms
    # Handles the command used to run the project in the Docker container.
    command: sh -c "python manage.py runserver 0.0.0.0:8000" 
    ```
17. The docker files settings are now ready and it's time to build our first Docker Image. Run: `docker-compose run --rm app django-admin startproject core .`
18. In the above command, the syntax is: `docker-compose run --rm <service_name> <desired_command_instruction>`.
19. **Note**:
   If you’re starting a new project, it’s highly recommended to set up a custom user model, even if the default User model is sufficient for you.    
   This model behaves identically to the default user model, but you’ll be able to customize it in the future if the need arises.
    [Vist](https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project) the Official Django documentation for reference
21. Build the Image and run the container by running: `docker-compose build` and then `docker-compose run`
22. **Important**: If you want to view container ID, stop or delete docker image, run the following commands respectively; `docker ps -a`, `docker stop`, `docker rm <container_id>`.
23. Navigate to `localhost:8000` and you will see the django welcome page. Our project is now setup successfully annd it's time to run commands for setting up new apps, and folders:
    `docker-compose run --rm app python3 manage.py startapp app1` , ` docker-compose run --rm app python3 manage.py makemigrations` and `docker-compose run --rm app python3 manage.py migrate`.

