pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                script {
                    sh 'pip install -r requirements.txt' 
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'pytest --rootdir --maxfail=5 --disable-warnings --junitxml=reports/test-results.xml'
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
