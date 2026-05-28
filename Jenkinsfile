pipeline {
    agent any
 
    environment {
        IMAGE_NAME  = 'cybersec-api'
        APP_VERSION = "1.0.${BUILD_NUMBER}"
    }

      stages {
 
        stage('Build') {
            steps {
                echo "Building version ${APP_VERSION}"
                sh "pip install -r requirement.txt"
                sh "docker build -t ${IMAGE_NAME}:${APP_VERSION} -t ${IMAGE_NAME}:latest ."
                echo "Image ${IMAGE_NAME}:${APP_VERSION} built successfully"
            }
        }

        stage('Test') {
            steps {
                echo "Running tests for version ${APP_VERSION}"
                sh 'python3 -m pytest'
            }
        }

        
    }
}
