pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                script {
                    // Install dependencies, e.g., using npm or pip
                    sh 'pip install -r requirements.txt' // For Python
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run the tests and generate test report
                    sh 'pytest --rootdir --maxfail=5 --disable-warnings --junitxml=reports/test-results.xml' // For Python (pytest)
                }
            }
        }

        stage('Publish Test Results') {
            steps {
                junit '**/reports/test-results.xml' // Path to your test report
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed. Archiving artifacts and cleaning up.'
            archiveArtifacts artifacts: '**/reports/test-results.xml', fingerprint: true
        }
        success {
            echo 'Pipeline succeeded! Notifying you.'
            mail to: 'xvitalopez@gmail.com',
                 subject: "Build Successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The Jenkins build ${env.JOB_NAME} #${env.BUILD_NUMBER} succeeded.\n\nCheck it here: ${env.BUILD_URL}"
        }
        failure {
            echo 'Pipeline failed! Sending notifications.'
            mail to: 'xvitalopez@gmail.com',
                 subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The Jenkins build ${env.JOB_NAME} #${env.BUILD_NUMBER} failed.\n\nCheck it here: ${env.BUILD_URL}"
        }
    }
}
