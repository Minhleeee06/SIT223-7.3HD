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
                sh '''
            export SONAR_HOST_URL=http://localhost:9000
            export SONAR_TOKEN=your-token-here
            sonar-scanner \
                -Dsonar.projectKey=cybersec-api-python \
                -Dsonar.sources=. \
                -Dsonar.inclusions=App.py \
                -Dsonar.host.url=http://localhost:9000 \
                -Dsonar.login=$SONAR_TOKEN
        '''
            }
        }
        
    }
}
