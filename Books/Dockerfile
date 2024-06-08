# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:alpine3.17

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /bookapp

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy the application files to the container
COPY . .

# Expose port 5001 for the application
EXPOSE 5001

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /bookapp
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
CMD ["python3", "app.py"]
