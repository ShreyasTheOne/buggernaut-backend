![Buggernaut Logo](buggernaut_backend/media/assets/app_logo_with_name_white.png)

**Buggernaut bridges the gap between you and the users of your app, providing a way for them to report any bugs they find in it**

This is the repository for the **backend** application of Buggernaut. Click [here](https://github.com/shreyasdoda/buggernaut-frontend) to go to the backend repository.

# Setup instructions (for local server only):
- Clone this repository to a folder on your device.
- Run `pip install -r requirements.txt` (using Python version 3.6.9 in virtual environment).
- From root directory of project execute the following commands:
  - `cd configuration/`
  - `touch base.yml`
  - `cp base_stencil.yml base.yml`
  - Fill out correct values to the given fields. **NOTE: ALL VALUES ARE REQUIRED FOR THE APP TO WORK**
- In the root directory of the project run: 
  - `python manage.py makemigrations` to create tables in the database
  - `python manage.py migrate` to apply the newest database representation to the app
  - `python manage.py runserver` to... run the server! It will automatically start an ASGI/Channels version 2.4.0 development server at http://127.0.0.1:8000/
- Buggernaut allows you to associate tags with issues. You must populate the database with tags from http://127.0.0.1:8000/tags/ for them to show up at the frontend.
- You are ready to use the app! Bon testing :)


