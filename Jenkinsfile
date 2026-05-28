pipeline {
    agent any
 
    environment {
        IMAGE_NAME  = "cybersec-api"
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
                sh "python3 -m pytest"
            }
        }
        // STAGE 3
        stage('Code Quality') {
            steps {
                echo "Running code quality analysis with pylint"
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
                        ${IMAGE_NAME}:${APP_VERSION} | tee trivy-report.txt
                """
             }
          }

          //STAGE 5
          stage('Deploy') {
          steps {
                echo "Deploying to staging..."
                sh "docker compose -f Docker_compose.YML down || true"
                sh "APP_VERSION=${APP_VERSION} docker compose -f Docker_compose.YML up -d"
                sh 'sleep 10'
                sh "curl -s http://localhost:3000/health"
            }
        }

          //STAGE 6
          stage('Release') {
          steps {
              sh "docker tag ${IMAGE_NAME}:${APP_VERSION} ${IMAGE_NAME}:release-${APP_VERSION}"
              echo "Released version ${APP_VERSION}"
            }
        }

        //STAGE 7
        stage('Monitoring') {
            steps {
                echo "Running post-deploy monitoring check"
                sh '''
                    echo "____Health check_____"
                    curl -sf http://localhost:3000/health
 
                    echo "____Password endpoint____"
                    curl -sf -X POST http://localhost:3000/api/password/check \
                        -H "Content-Type: application/json" \
                        -d "{"password":"Monitor#Check99"}"
 
                    echo "____Breach endpoint____"
                    curl -sf -X POST http://localhost:3000/api/breach/check \
                        -H "Content-Type: application/json" \
                        -d "{"email":"monitor@check.com"}"
 
                    echo "All monitors checks passed"
                '''
            }
        }
    }
}
