pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        DOCKER_IMAGE = "hyvi69/repo:${env.BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-creds'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python') {
            steps {
                sh '''
                    set -euxo pipefail
                    python3 -V || true
                    pip3 -V || true
                    if command -v python3 >/dev/null 2>&1; then PY=python3; else PY=python; fi
                    $PY -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Unit tests') {
            steps {
                sh '''
                    set -euxo pipefail
                    . .venv/bin/activate
                    pytest --junitxml=pytest-report.xml -q
                '''
            }
            post {
                always {
                    junit 'pytest-report.xml'
                }
            }
        }

        stage('Docker build') {
            when {
                expression { return fileExists('Dockerfile') }
            }
            steps {
                sh '''
                    set -euxo pipefail
                    docker version
                    docker build -t "$DOCKER_IMAGE" .
                '''
            }
        }

        stage('Docker push (optional)') {
            when {
                allOf {
                    expression { return env.DOCKERHUB_CREDENTIALS_ID }
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS_ID, usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                    sh '''
                        set -euxo pipefail
                        echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
                        docker push "$DOCKER_IMAGE"
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}


