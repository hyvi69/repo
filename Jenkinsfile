pipeline {
    agent any
    environment {
        IMAGE_NAME = 'repo-web'
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
            bat 'C:\Python\Python311\python.exe -m venv venv'
            // Upgrade pip
            bat 'venv\\Scripts\\python.exe -m pip install --upgrade pip'
            // Install requirements
            bat 'venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            // Install compatible Werkzeug
            bat 'venv\\Scripts\\python.exe -m pip install Werkzeug==2.2.3'
        }
    }
}


        stage('Run Tests') {
            when {
                expression {
                    fileExists('test_app.py') || fileExists('tests') || fileExists('test')
                }
            }
            steps {
                script {
                    // Run pytest tests if tests exist
                    bat 'venv\\Scripts\\pytest -v'
                }
            }
        }

        stage('Static Code Analysis (Bandit)') {
            steps {
                script {
                    // Run Bandit for static code analysis (save report)
                    bat 'venv\\Scripts\\bandit -r . -f txt -o bandit-report.txt || exit 0'
                }
            }
        }

        stage('Check Dependency Vulnerabilities (Safety)') {
            steps {
                script {
                    // Run Safety to check Python dependencies (save report)
                    bat 'venv\\Scripts\\safety check --full-report -r requirements.txt > safety-report.txt || exit 0'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image with explicit tag
                    bat "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Container Vulnerability Scan (Trivy)') {
            steps {
                script {
                    // Scan Docker image with Trivy (save report)
                    bat "trivy image --no-progress ${IMAGE_NAME}:latest > trivy-report.txt || exit 0"
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    // Deploy Docker containers
                    bat 'docker compose up -d'
                }
            }
        }
    }

    post {
        always {
            // Clean workspace after build
            cleanWs()
            // Archive security scan reports (if present)
            archiveArtifacts artifacts: 'bandit-report.txt, safety-report.txt, trivy-report.txt', allowEmptyArchive: true
        }
    }
}
