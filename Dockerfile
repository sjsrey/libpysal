FROM jupyter/scipy-notebook

LABEL maintainer="Serge Rey <sjsrey@gmail.com>"


# Install any needed packages specified in requirements
COPY requirements.txt /home/$NB_USER
RUN pip install --trusted-host pypi.python.org -r /home/$NB_USER/requirements.txt
COPY requirements_dev.txt /home/$NB_USER
RUN pip install --trusted-host pypi.python.org -r /home/$NB_USER/requirements_dev.txt
COPY requirements_plus_pip.txt /home/$NB_USER
RUN pip install --trusted-host pypi.python.org -r /home/$NB_USER/requirements_plus_pip.txt
COPY requirements_tests.txt /home/$NB_USER
RUN pip install --trusted-host pypi.python.org -r /home/$NB_USER/requirements_tests.txt


