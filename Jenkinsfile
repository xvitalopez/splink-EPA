pipeline {
    agent any
    
    environment {
        // GitHub Personal Access Token stored as a secret text in Jenkins
        GIT_CREDENTIALS = credentials('github-pat-token') // 
        
        // Terraform region
        TF_VAR_region = 'eu-north-1'
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout the code using Git credentials
                git branch: 'main', 
                    credentialsId: 'github-pat-token', //
                    url: 'https://github.com/xvitalopez/splink-EPA.git'
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                // Execute tests 
                sh 'pytest test/'
            }
            post {
                always {
                    // Publish test results
                    junit 'tests/*.xml'
                }
            }
        }
        
        stage('Terraform Init') {
            steps {
                // Initialize Terraform with AWS credentials
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials', // 
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    dir('terraform') {
                        sh 'terraform init'
                    }
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
            // Actions that always run after all stages, regardless of success or failure
            echo 'This always runs after pipeline completion'
        }
    }
}
