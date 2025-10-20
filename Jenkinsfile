pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        IMAGE_NAME = 'repo-web'
        CONTAINER_NAME = 'repo-web'
        APP_PORT = '5001'
    }

    stages {
        stage('Checkout') {
            steps {
                // Use the Jenkins job's configured SCM
                checkout scm
            }
        }

        stage('Build Docker Image') {
            when {
                expression { return fileExists('Dockerfile') }
            }
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            set -euxo pipefail
                            docker build -t "$IMAGE_NAME" .
                        '''
                    } else {
                        bat '''
                            @echo on
                            docker build -t "%IMAGE_NAME%" .
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                expression { return fileExists('docker-compose.yml') || fileExists('docker-compose.yaml') }
            }
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            set -euxo pipefail
                            docker compose down || true
                            docker rm -f "$CONTAINER_NAME" || true
                            APP_PORT="$APP_PORT" docker compose up -d
                        '''
                    } else {
                        bat '''
                            @echo on
                            docker compose down || exit /b 0
                            docker rm -f "%CONTAINER_NAME%" || exit /b 0
                            set APP_PORT=%APP_PORT%
                            docker compose up -d
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                if (isUnix()) {
                    sh '''
                        set -euxo pipefail
                        docker compose down || true
                    '''
                } else {
                    bat '''
                        @echo on
                        docker compose down || exit /b 0
                    '''
                }
            }
        }
    }
}
