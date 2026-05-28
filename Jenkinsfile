pipeline {
    agent any
 
    environment {
        IMAGE_NAME  = 'cybersec-api'
        APP_VERSION = "1.0.${BUILD_NUMBER}"
    }
      stages {
         // STAGE !
        stage('Build') {
            steps {
                echo "Building version ${APP_VERSION}"
                sh "pip install -r requirement.txt"
                sh "docker build -t ${IMAGE_NAME}:${APP_VERSION} -t ${IMAGE_NAME}:latest ."
                echo "Image ${IMAGE_NAME}:${APP_VERSION} built successfully"
            }
        }
        // STAGE 2
        stage('Test') {
            steps {
                echo "Running tests for version ${APP_VERSION}"
                sh 'python3 -m pytest'
            }
        }
        // STAGE 3
        stage('Code Quality') {
            steps {
                echo 'Running code quality analysis with pylint...'
        sh 'pip install pylint'
        sh 'pylint App.py --exit-zero --output-format=text | tee pylint-report.txt'
        sh 'cat pylint-report.txt'
            }
        }

        // STAGE 4
          stage('Security') {
            steps {
                echo 'Scanning image with Trivy...'
                sh """
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v trivy-cache:/root/.cache/ \
                        aquasec/trivy:latest image \
                        --exit-code 0 \
                        --severity HIGH,CRITICAL \
                        --format table \
                        --output trivy-report.txt \
                        ${IMAGE_NAME}:${APP_VERSION}
                """
                sh 'cat trivy-report.txt'
            }
          }
    }
}
