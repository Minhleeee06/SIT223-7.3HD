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
                echo 'Running SonarQube analysis'
                withSonarQubeEnv('SonarQube') {
                    sh 'sonar-scanner -Dproject.settings=SONAR.PROPERTIES'
                }
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
    }
}
