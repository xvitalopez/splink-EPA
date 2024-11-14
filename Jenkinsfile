pipeline {
    agent any
    
    environment {
        GIT_CREDENTIALS = credentials('github-pat-token') // Replace with your credential ID
        TF_VAR_region = 'eu-north-1'
    }
    
    stages {
            stage('Checkout') {
            steps {
                 // Use the credentials in the git command
                git branch: 'main', credentialsId: 'github-pat-token', url: 'https://github.com/xvitalopez/splink-EPA.git'
                // Use the correct Git credentials ID in the `git` step
            }
        }
         stage('Initialize AWS Credentials') {
        steps {
            withCredentials([[
                $class: 'AmazonWebServicesCredentialsBinding',
                credentialsId: 'aws-credentials' // Update with your actual AWS credentials ID
            ]]) {
                // You can now access AWS using your credentials
                sh 'terraform init'
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
            echo 'This always runs after pipeline completion'
        }
    }
}
}
