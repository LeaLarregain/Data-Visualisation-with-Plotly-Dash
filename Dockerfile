# Use the official Python base image
FROM python:3.11

# Set the working directory of the container
WORKDIR /app

# Copy the requirements file containing your dependencies list into the container
COPY requirements.txt .

# Install necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code of the app (there is only one file), can copy all current dir using `.`
COPY . .

# Expose port 8050, the default port used by plotly dash
EXPOSE 8050

# Start the Dash app
CMD ["python", "app.py"]