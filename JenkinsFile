pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        AWS_ACCOUNT_ID = '276096488420'
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

        IMAGE_MAIN = "${ECR_REGISTRY}/fifa/main-page"
        IMAGE_GROUPS = "${ECR_REGISTRY}/fifa/group-stage"
        IMAGE_H2H = "${ECR_REGISTRY}/fifa/h2h"
        IMAGE_TOURNAMENT = "${ECR_REGISTRY}/fifa/tournament"
        IMAGE_RESULTS = "${ECR_REGISTRY}/fifa/tournament-results"

        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Basic Tests') {
            steps {
                sh '''
                    echo "Running basic project validation..."

                    test -f requirements.txt
                    test -f app.py
                    test -f groupstages.py
                    test -f tournament.py
                    test -f results.py
                    test -f predictor.py

                    test -f Dockerfiles/Dockerfile.main
                    test -f Dockerfiles/Dockerfile.groups
                    test -f Dockerfiles/Dockerfile.h2h
                    test -f Dockerfiles/Dockerfile.tournament
                    test -f Dockerfiles/Dockerfile.results

                    echo "Basic validation passed."
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    echo "Building Docker images..."

                    docker build -f Dockerfiles/Dockerfile.main \
                        -t ${IMAGE_MAIN}:${IMAGE_TAG} .

                    docker build -f Dockerfiles/Dockerfile.groups \
                        -t ${IMAGE_GROUPS}:${IMAGE_TAG} .

                    docker build -f Dockerfiles/Dockerfile.h2h \
                        -t ${IMAGE_H2H}:${IMAGE_TAG} .

                    docker build -f Dockerfiles/Dockerfile.tournament \
                        -t ${IMAGE_TOURNAMENT}:${IMAGE_TAG} .

                    docker build -f Dockerfiles/Dockerfile.results \
                        -t ${IMAGE_RESULTS}:${IMAGE_TAG} .

                    echo "All Docker images built successfully."
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                    echo "Logging into Amazon ECR..."

                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login \
                        --username AWS \
                        --password-stdin ${ECR_REGISTRY}

                    echo "ECR login successful."
                '''
            }
        }

        stage('Push Images to ECR') {
            steps {
                sh '''
                    echo "Pushing images to ECR..."

                    docker push ${IMAGE_MAIN}:${IMAGE_TAG}
                    docker push ${IMAGE_GROUPS}:${IMAGE_TAG}
                    docker push ${IMAGE_H2H}:${IMAGE_TAG}
                    docker push ${IMAGE_TOURNAMENT}:${IMAGE_TAG}
                    docker push ${IMAGE_RESULTS}:${IMAGE_TAG}

                    echo "All images pushed successfully."
                '''
            }
        }
    }

    post {
        success {
            echo "CI pipeline completed successfully!"
            echo "Images pushed with tag: ${IMAGE_TAG}"
        }

        failure {
            echo "Pipeline failed. Check the stage logs above."
        }
    }
}