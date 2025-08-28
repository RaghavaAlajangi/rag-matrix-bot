# Use a lightweight official Python image as the base
FROM python:alpine

WORKDIR /matrixbot

COPY requirements.txt /matrixbot/requirements.txt

# --no-cache-dir prevents pip from storing cache, reducing image size
RUN pip install --no-cache-dir -r /matrixbot/requirements.txt

# This line fix no module named 'pkg_resources' error
RUN pip install setuptools

# Copy the application code
COPY . /matrixbot/.

# Command to run the bot when the container starts
ENTRYPOINT ["python3"]
CMD ["-m", "bot"]
