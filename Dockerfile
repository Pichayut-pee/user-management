# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.11

<<<<<<< HEAD
=======
RUN apt-get update
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

#download and install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install


>>>>>>> 5ffb2f7062f9a0dc1437c9ade04409ed449d1e67
# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
<<<<<<< HEAD
COPY . user_mangement
WORKDIR /user_mangement

# runs the production server
EXPOSE 8001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001", "--noreload"]
=======
COPY . scraping
WORKDIR /scraping

# runs the production server
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
>>>>>>> 5ffb2f7062f9a0dc1437c9ade04409ed449d1e67
