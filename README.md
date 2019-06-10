# Apli.ai
A Website to make hiring easy.

# How to Use

1. Python3
2. git clone https://gitlab.com/apliai.iitb/website.git
3. cd website
4. source env/bin/activate
5. pip install -r requirements.txt --ignore-installed
6. cd apliai
7. Create a Firebase service account with db on cloudfirestore save the generated jsonkey as serviceAccountKey.json in this folder
8. python manage.py runserver

# Structure

* env -> Virtualenv for the project.
* apliai -> Main Project.
* accounts -> App to handle user accounts.
* recruiter -> App to handle recruiter demands.
* campus -> App to handle campus demands.
* maintainer -> Main Admin side

# Improvements To be made

https://docs.google.com/spreadsheets/d/1_qbsjBP7NekRRNS54Q31qhrqQgx78UQvGW1PWXrJpZA/edit?usp=sharing

# Contributors

1. Work always in your respective branches and only create pull request when work needs to be verified.

# Git basic commands

* git clone `repo-link`
* git branch `branch-name`
* git checkout `branch-name`
* git add .
* git commit -m "some message for your work"
* git push origin `branch-name`
