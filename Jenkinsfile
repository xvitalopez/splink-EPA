pipeline {
    agent any
    
    environment {
        GIT_CREDENTIALS = credentials('github-credentials') // Add your credentials ID here
        TF_VAR_region = 'eu-north-1'
        TF_VAR_access_key = credentials('AKIAXEFUNJKKE25KXRXG') // Manage credentials in Jenkins
        TF_VAR_secret_key = credentials('AKIAXEFUNJKKE25KXRXG')
    }
    
    stages {
        stage('Checkout') {
            steps {
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
                    dir('terraform') {
                        sh 'terraform init'
                    }
                }
            }
        
        
        stage('Terraform Plan') {
            steps {
                    dir('terraform') {
                        sh 'terraform plan -out=plan.out'
                    }
                }
            }
        
        stage('Terraform Apply') {
            steps {
                    dir('terraform') {
                        sh 'terraform apply -auto-approve plan.out'
                    }
                }
            }
        }
    
    post {
        always {
                cleanWs() // Clean up workspace
            }
        }
    }
