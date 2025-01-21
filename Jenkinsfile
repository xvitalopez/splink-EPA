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
                    sh 'pytest --maxfail=5 --disable-warnings --junitxml=reports/test-results.xml' // For Python (pytest)
                    // Or for Java with Maven
                    // sh 'mvn test'
                }
            }
        }

        stage('Publish Test Results') {
            steps {
                junit '**/reports/test-results.xml' // Path to your test report
            }
        }
    }
}
