pipeline {
    agent {
        docker {
            image 'python:3.12'
        }
    }
    stages {
        stage('Check Python') {
            steps {
                bat 'python --version'
                bat 'pip --version'
            }
        }

        stage('List Installed Libraries') {
            steps {
                bat 'pip list'
            }
        }

        stage('Install dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
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
