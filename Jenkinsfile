pipeline {
    agent any
    
    environment {
        TF_VAR_region = 'eu-north-1'
        TF_VAR_access_key = credentials('AKIAXEFUNJKKKJFZLLF7') // Manage credentials in Jenkins
        TF_VAR_secret_key = credentials('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')
    }
    
    stages {
        stage('Checkout') {
            steps {
                node {
                    git branch: 'main', url: 'https://github.com/xvitalopez/splink-EPA.git'
                }
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                node {
                    // Execute tests (this example uses PyTest)
                    sh 'pytest test/'
                }
            }
            post {
                always {
                    junit 'tests/*.xml' // Publish test results
                }
            }
        }
        
        stage('Terraform Init') {
            steps {
                node {
                    dir('terraform') {
                        sh 'terraform init'
                    }
                }
            }
        }
        
        stage('Terraform Plan') {
            steps {
                node {
                    dir('terraform') {
                        sh 'terraform plan -out=plan.out'
                    }
                }
            }
        }
        
        stage('Terraform Apply') {
            steps {
                node {
                    dir('terraform') {
                        sh 'terraform apply -auto-approve plan.out'
                    }
                }
            }
        }
    }
    
    post {
        always {
            node {
                cleanWs() // Clean up workspace
            }
        }
    }
}
