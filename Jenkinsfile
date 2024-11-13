pipeline {
    agent any
    
    environment {
        GIT_CREDENTIALS = credentials('github-credentials') // Add your credentials ID here
        TF_VAR_region = 'eu-north-1'
        // For AWS credentials, use Jenkins' AWS credentials plugin if needed or store securely
        TF_VAR_access_key = credentials('aws-access-key-id') // Store the AWS access key securely
        TF_VAR_secret_key = credentials('aws-secret-access-key') // Store the AWS secret key securely
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                git branch: 'main', url: 'https://github.com/xvitalopez/splink-EPA.git'
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                // Execute tests (this example uses PyTest)
                sh 'pytest test/'
            }
            post {
                always {
                    junit 'tests/*.xml' // Publish test results
                }
            }
        }

        stage('Terraform Init') {
            steps {
                // Run Terraform Init in the terraform directory
                dir('terraform') {
    
