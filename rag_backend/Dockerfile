# Use a lightweight official Python image as the base
FROM python:alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt

# --no-cache-dir prevents pip from storing cache, reducing image size
RUN pip install --no-cache-dir -r /app/requirements.txt

# This line fix no module named 'pkg_resources' error
RUN pip install setuptools

# Copy the application code
COPY . /app/.

# Command to run the bot when the container starts
ENTRYPOINT ["python3"]
CMD ["-m", "rag_backend"]
