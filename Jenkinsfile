pipeline {
    agent any
    
    environment {
        GIT_CREDENTIALS = credentials('github-credentials') // Add your credentials ID here
        TF_VAR_region = 'eu-north-1'
        TF_VAR_access_key = credentials('AKIAXEFUNJKKKJFZLLF7') // Manage credentials in Jenkins
        TF_VAR_secret_key = credentials('t8llF9PAqH/SlRX5D5XVz16oRK/JYHjh2Pohqz0Y')
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Use the correct Git credentials ID in the `git` step
                git branch: 'main', 
                    url: 'https://github.com/xvitalopez/splink-EPA.git', 
                    credentialsId: 'github-credentials'
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
}
