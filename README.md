# Django_HMS
This is a Django Hotel Management System

##Steps to get started with the software
 1. Clone the repo or download code in zip file
 2. Open the folder in a code editor like VSCode, it will look like this - 
         ![Configuring virtual environment](https://github.com/Darshan4114/Django_HMS/blob/main/readme_images/django_hms_open_in_vscode.png)
    - TIP: Create a virtual environment
      > *Run these commands in the Django_HMS folder through the vscode terminal/ command prompt/ powershell* 
         ![Configuring virtual environment](https://github.com/Darshan4114/Django_HMS/blob/main/readme_images/django_hms_config_commands.png)

 3. Run `pip install -r requirements.txt` to install all the libraries from "requirements.txt". You can see the last command in the image above :point_up_2:
 4. After the `pip install -r requirements.txt` is done it will look something like this-
         ![Configuring virtual environment](https://github.com/Darshan4114/Django_HMS/blob/main/readme_images/django_hms_pip_install_done.png)
         
 5. Create a .env file in your "HMS" folder.
         ![Configuring virtual environment](https://github.com/Darshan4114/Django_HMS/blob/main/readme_images/django_hms_create_dotenv_file.png)   
  *Now since we are using environment variables from the beginning here, so that the application remains flexible and you can deploy easily without much HARD code to change
 
6. Make migrations and migrate.
   *Run these commands*
   ```python
   python manage.py makemigrations
   python manage.py migrate
   ```
   Result will look like - 
         ![Configuring virtual environment](https://github.com/Darshan4114/Django_HMS/blob/main/readme_images/django_hms_create_dotenv_file.png) 
7. Now run either one of the following commands to start the development server.
   ```python
   python manage.py runserver
   django r
   ```

> Now you should have the server running on - http://127.0.0.1:8000/

## Create super user and create Rooms
1. Now you need to create a superuser to access the admin panel. Run one of the following commands - 
    ```python
    python manage.py createsuperuser
    django csu
    ```
2. Open admin panel: http://127.0.0.1:8000/admin
3. Create Room Categories and Rooms
4. Start using the app! You can use the Stripe features by creating a stripe account and putting in the client id and secret environment variables.
5. Cheers! Thats all there is to it

**Thanks for using my repository, if you find any bugs, you can raise an issue. If you would like to help me make it better, I will very much appreciate your PR. Thank you :)**
