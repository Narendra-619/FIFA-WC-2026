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

        stage('Skip Check') {
            steps {
                script {
                    def lastCommit = sh(script: "git log -1 --pretty=%B", returnStdout: true).trim()
                    if (lastCommit.contains('[skip ci]')) {
                        echo "Last commit was a CI manifest update — skipping build to avoid a loop."
                        currentBuild.result = 'NOT_BUILT'
                        error("Skipping: manifest-only commit")
                    }
                }
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

                stage('Update K8s Manifests') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-creds', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                    sh '''
                        git config user.email "jenkins-ci@fifa-predictor.local"
                        git config user.name "Jenkins CI"

                        sed -i "s|image: .*fifa/main-page:.*|image: ${IMAGE_MAIN}:${IMAGE_TAG}|" kubernetes/deployments/main-page.yaml
                        sed -i "s|image: .*fifa/group-stage:.*|image: ${IMAGE_GROUPS}:${IMAGE_TAG}|" kubernetes/deployments/groups-deployment.yaml
                        sed -i "s|image: .*fifa/h2h:.*|image: ${IMAGE_H2H}:${IMAGE_TAG}|" kubernetes/deployments/h2h-deployment.yaml
                        sed -i "s|image: .*fifa/tournament:.*|image: ${IMAGE_TOURNAMENT}:${IMAGE_TAG}|" kubernetes/deployments/tournament-deployment.yaml
                        sed -i "s|image: .*fifa/tournament-results:.*|image: ${IMAGE_RESULTS}:${IMAGE_TAG}|" kubernetes/deployments/results-deployment.yaml

                        git add kubernetes/deployments/*.yaml
                        git commit -m "ci: update image tags to build ${IMAGE_TAG} [skip ci]"
                        git push https://${GIT_USER}:${GIT_PASS}@github.com/Narendra-619/FIFA-WC-2026.git HEAD:master
                    '''
                }
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