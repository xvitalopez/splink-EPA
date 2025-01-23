pipeline {
    agent {
        docker {
            image 'python:3.10' // Updated to Python 3.10
        }
    }
    stages {
        stage('Check Python') {
            steps {
                bat 'python --version'
                bat 'pip --version'
            }
        }

        stage('Install dependencies') { // This stage installs required libraries
            steps {
                bat 'pip install -r requirements.txt' // Install dependencies
            }
        }

        stage('Debug Installed Libraries') { // Optional debugging stage
            steps {
                bat 'pip list' // Verifies installed libraries
            }
        }

        stage('Run Tests') {
            steps {
                bat 'pytest --rootdir --maxfail=5 --disable-warnings --junitxml=reports/test-results.xml'
            }
        }

        stage('Publish Test Results') {
            steps {
                junit '**/reports/test-results.xml'
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed. Archiving artifacts and cleaning up.'
            archiveArtifacts artifacts: '**/reports/test-results.xml', fingerprint: true
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
