# Installation

1. Install system dependencies

    ```bash
    sudo apt-get update
    sudo apt-get install -y python3-pip python3.7-venv texlive-base texlive-lang-german texlive-fonts-recommended texlive-latex-extra
    ```

2. Install python-dependencies in virtual environment

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    ```

# Development

1. Install additional dependencies after you installed the dependencies listed in [Installation](#installation)

    ```bash
    sudo apt-get install -y gettext
    python3 -m pip install -r requirements_dev.txt
    ```

2. Create the SQLite-database by running the following command inside the project directory:

    ```bash
    python3 manage.py migrate
    ```

3. Create an admin-account by running the following command inside the project directory:

    ```bash
    python3 manage.py createsuperuser
    ```

    Note that this doesn't set the `fist_name`, thus the `username` is shown on the website. If you want your `fist_name` to be shown instead, you have to add your fist name in the admin interface.

4. Start the local webserver

    ```bash
    python3 manage.py runserver
    ```

    You can now visist http://localhost:8000/ in your browser

## pre-commit

Code quality is ensured via various tools bundled in [`pre-commit`](https://github.com/pre-commit/pre-commit/).

You can install `pre-commit`, so it will automatically run on commit:

```bash
pre-commit install
```

This will check all files modified by your commit and will prevent the commit if a hook fails. To check all files, you can run

```bash
pre-commit run --all-files
```

This will also be run by CI if you push to the repository.

## Translation

1. Update the `.po`-files with

    ```bash
    python manage.py makemessages -a
    ```

2. Edit the `.po`-files, e.g. `guidedtours/locale/de/LC_MESSAGES/django.po`. [Poedit](https://poedit.net) is an excellent GUI for this!

Note that `pre-commit` will automatically compuile the translations for you.
