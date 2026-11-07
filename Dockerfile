# * Use an official lightweight Python 3.12 image
FROM python:3.12-slim

# // Set the working directory inside the container
WORKDIR /app

# ? Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# * Install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# // Copy the rest of the application code
COPY . .

# ! Expose the port the app runs on
EXPOSE 8000

# * Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]