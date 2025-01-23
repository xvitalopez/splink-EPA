pipeline {
    agent any
    stages {
        stage('Check Python') {
            steps {
                bat '"C:Users\\xvita\\AppData\\Local\\Programs\\Python\\Python312 --version"'
                bat '"C:Users\\\\xvita\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python312\\\\Scripts\\\\pip --version"'
            }
        }
        stage('Install dependencies') {
            steps {
                script {
                    bat 'pip install -r requirements.txt' 
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    bat 'pytest --rootdir --maxfail=5 --disable-warnings --junitxml=reports/test-results.xml'
                }
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
