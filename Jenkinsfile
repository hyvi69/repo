pipeline {
    agent any
    environment {
        IMAGE_NAME = 'python-devsecops-jenkins_app'
    }
    stages {
        stage('Checkout') {
            steps {
                // Pull the code from GitHub
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Create virtual environment
                    bat 'python -m venv venv'
                    // Upgrade pip
                    bat 'venv\\Scripts\\pip install --upgrade pip'
                    // Install requirements
                    bat 'venv\\Scripts\\pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run pytest tests
                    bat 'venv\\Scripts\\pytest -v'
                }
            }
        }

        stage('Static Code Analysis (Bandit)') {
            steps {
                script {
                    // Run Bandit for static code analysis
                    bat 'venv\\Scripts\\bandit -r .'
                }
            }
        }

        stage('Check Dependency Vulnerabilities (Safety)') {
            steps {
                script {
                    // Run Safety to check Python dependencies
                    bat 'venv\\Scripts\\safety check -r requirements.txt'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image using Docker Compose
                    bat 'docker-compose build'
                }
            }
        }

        stage('Container Vulnerability Scan (Trivy)') {
            steps {
                script {
                    // Scan Docker image with Trivy
                    bat "trivy image ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    // Deploy Docker containers
                    bat 'docker-compose up -d'
                }
            }
        }
    }

    post {
        always {
            // Clean workspace after build
            cleanWs()
        }
    }
}
