FROM python:alpine3.17

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /loanApp

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy the application files to the container
COPY . .

# Expose port 5002 for the application
EXPOSE 5002

# Creates a non-root user with an explicit UID and adds permission to access the /loanApp folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /loanApp
USER appuser

CMD ["python3", "loansApp.py"]
