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
                sh 'pip install -r requirement.txt'
            }
        }

        stage('Test') {
            steps {
                echo "Running tests for version ${APP_VERSION}"
                sh 'pytest tests/'
            }
        }
    }
}
