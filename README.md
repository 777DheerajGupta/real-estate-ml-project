# Real Estate ML Project

A machine learning project for real estate price prediction and analysis, deployed on AWS with containerized infrastructure.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Docker](#docker)
- [AWS Deployment](#aws-deployment)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project leverages machine learning to predict real estate property prices. The application is containerized using Docker and deployed on AWS infrastructure, utilizing S3 for data storage and EC2 for computation.

## ✨ Features

- **Price Prediction**: ML models for accurate real estate price forecasting
- **Data Processing**: Efficient data pipeline with data validation and preprocessing
- **Cloud Storage**: AWS S3 integration for data management
- **Scalable Deployment**: AWS EC2 instances for production workloads
- **Containerized**: Docker support for consistent environments
- **API Endpoints**: RESTful API for model inference

## 🏗️ Architecture

```
┌─────────────────┐
│   Docker Image  │
│   Application   │
└────────┬────────┘
         │
    ┌────┴─────────┬──────────────┐
    │              │              │
┌───▼────┐  ┌─────▼─────┐  ┌────▼────┐
│ AWS S3 │  │  AWS EC2  │  │  Models │
│ (Data) │  │ (Compute) │  │ Storage │
└────────┘  └───────────┘  └─────────┘
```

## 📦 Prerequisites

- Python 3.8 or higher
- Docker & Docker Compose
- AWS Account with:
  - S3 bucket access
  - EC2 instance access
  - IAM credentials configured
- Git
- pip (Python package manager)

## 🚀 Setup & Installation

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/777DheerajGupta/real-estate-ml-project.git
   cd real-estate-ml-project
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your AWS credentials and configuration
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# S3 Configuration
S3_BUCKET_NAME=your-bucket-name
S3_DATA_PATH=data/
S3_MODELS_PATH=models/

# Application Configuration
MODEL_TYPE=random_forest  # or gradient_boosting, neural_network
DEBUG=False
LOG_LEVEL=INFO
PORT=5000
```

### AWS Setup

1. **Create an S3 bucket**:
   ```bash
   aws s3api create-bucket --bucket your-bucket-name --region us-east-1
   ```

2. **Create IAM user** with S3 and EC2 permissions

3. **Configure AWS CLI**:
   ```bash
   aws configure
   ```

## 💻 Usage

### Training the Model

```bash
python train.py \
  --data-path data/train.csv \
  --model-type random_forest \
  --test-size 0.2 \
  --save-model
```

### Making Predictions

```bash
python predict.py \
  --model-path models/model.pkl \
  --data-path data/test.csv \
  --output results/predictions.csv
```

### Starting the API Server

```bash
python app.py
# API available at http://localhost:5000
```

### API Endpoints

- `GET /` - Health check
  ```bash
  curl http://localhost:5000/
  ```

- `POST /predict` - Make price predictions
  ```bash
  curl -X POST http://localhost:5000/predict \
    -H "Content-Type: application/json" \
    -d '{
      "bedrooms": 3,
      "bathrooms": 2,
      "square_feet": 1500,
      "location": "downtown",
      "age_years": 10
    }'
  ```

- `GET /model-info` - Get model information
  ```bash
  curl http://localhost:5000/model-info
  ```

## 🐳 Docker

### Building the Docker Image

```bash
docker build -t real-estate-ml:latest .
```

### Running with Docker

```bash
docker run -p 5000:5000 \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e AWS_REGION=us-east-1 \
  -e S3_BUCKET_NAME=your-bucket \
  real-estate-ml:latest
```

### Docker Compose

Start the application using Docker Compose:

```bash
docker-compose up -d
```

Stop the application:

```bash
docker-compose down
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: real-estate-ml
    ports:
      - "5000:5000"
    environment:
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_REGION=${AWS_REGION}
      - S3_BUCKET_NAME=${S3_BUCKET_NAME}
      - MODEL_TYPE=${MODEL_TYPE}
      - DEBUG=${DEBUG}
    volumes:
      - ./models:/app/models
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

## ☁️ AWS Deployment

### Deploying to AWS EC2

1. **Launch an EC2 instance**:
   - AMI: Ubuntu 20.04 LTS (ami-0c55b159cbfafe1f0)
   - Instance type: t2.medium or larger
   - Storage: 20GB minimum
   - Security group: 
     - Allow SSH (port 22) from your IP
     - Allow HTTP (port 80) for API
     - Allow HTTPS (port 443)

2. **Connect to your instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install dependencies on EC2**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker.io docker-compose python3-pip git
   sudo usermod -aG docker ubuntu
   newgrp docker
   ```

4. **Clone and deploy**:
   ```bash
   git clone https://github.com/777DheerajGupta/real-estate-ml-project.git
   cd real-estate-ml-project
   
   # Create .env file with your AWS credentials
   cp .env.example .env
   nano .env  # Edit with your credentials
   
   # Start the application
   docker-compose up -d
   ```

5. **Verify deployment**:
   ```bash
   curl http://localhost:5000/
   docker logs -f real-estate-ml
   ```

### AWS S3 Integration

**Download training data from S3**:
```bash
python scripts/download_from_s3.py \
  --bucket your-bucket-name \
  --key data/train.csv \
  --output data/train.csv
```

**Upload trained models to S3**:
```bash
python scripts/upload_to_s3.py \
  --bucket your-bucket-name \
  --local-path models/model.pkl \
  --s3-key models/trained_models/model.pkl
```

**Sync entire data directory**:
```bash
aws s3 sync s3://your-bucket-name/data/ ./data/
aws s3 sync ./models/ s3://your-bucket-name/models/
```

### Monitoring & Logs

Monitor your EC2 instance:

```bash
# View application logs
docker logs -f real-estate-ml

# Check system resources
docker stats real-estate-ml

# Monitor disk usage
df -h

# View AWS CloudWatch metrics (via AWS Console)
# Goto: CloudWatch > Metrics > EC2 > Select your instance
```

## 📁 Project Structure

```
real-estate-ml-project/
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── app.py                          # Flask/FastAPI application
├── train.py                        # Model training script
├── predict.py                      # Batch prediction script
├── config.py                       # Configuration management
├── data/
│   ├── raw/                        # Raw data
│   ├── processed/                  # Processed data
│   └── test/
├── models/                         # Trained ML models
├── scripts/
│   ├── download_from_s3.py
│   ├── upload_to_s3.py
│   ├── preprocess.py
│   └── evaluate.py
├── src/
│   ├── __init__.py
│   ├── models/                     # Model implementations
│   ├── features/                   # Feature engineering
│   └── utils/                      # Utility functions
├── tests/
│   ├── test_model.py
│   ├── test_api.py
│   └── test_preprocessing.py
└── logs/                           # Application logs
```

## 🧪 Testing

Run all tests:

```bash
pytest tests/ -v
```

Run specific test file:

```bash
pytest tests/test_model.py -v
```

Run with coverage:

```bash
pytest tests/ --cov=src/ --cov-report=html
```

## 📊 Model Evaluation

Evaluate model performance:

```bash
python scripts/evaluate.py \
  --model-path models/model.pkl \
  --data-path data/test.csv
```

## 🔐 Security Best Practices

- **Never commit credentials**: Add `.env` to `.gitignore`
- **Use IAM roles**: Prefer IAM roles over access keys on EC2
- **Encrypt data**: Enable S3 bucket encryption
- **Restrict security groups**: Only open necessary ports
- **Enable versioning**: Turn on S3 bucket versioning
- **Rotate credentials**: Regularly rotate AWS credentials
- **Use secrets manager**: Consider AWS Secrets Manager for sensitive data

## 🚨 Troubleshooting

### Docker Issues

**Container won't start**:
```bash
docker logs real-estate-ml
docker ps -a
docker inspect real-estate-ml
```

**Port already in use**:
```bash
docker-compose down
# Or change port in docker-compose.yml
```

### AWS Connection Issues

**S3 access denied**:
- Check IAM permissions
- Verify AWS credentials in `.env`
- Confirm bucket name spelling

**EC2 connection timeout**:
- Verify security group allows your IP
- Check instance status in AWS Console
- Test: `ping your-instance-ip`

## 📈 Performance Tips

- Use appropriate instance types for your workload
- Enable S3 transfer acceleration for faster uploads
- Implement caching for frequently predicted values
- Monitor CloudWatch metrics for bottlenecks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For questions or support, please open an issue on GitHub or contact the maintainer.

## 🔗 Useful Resources

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Docker Documentation](https://docs.docker.com/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Last Updated**: June 7, 2026
**Maintained by**: 777DheerajGupta
