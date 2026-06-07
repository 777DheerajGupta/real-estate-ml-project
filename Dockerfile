FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only code files — NO datasets folder
COPY Home.py .
COPY model_loader.py .
COPY pages/ ./pages/

EXPOSE 8501

CMD ["streamlit", "run", "Home.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]