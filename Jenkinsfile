pipeline {
    agent {
        docker {
            image 'ubuntu:latest' // Changed to Ubuntu
        }
    }
    stages {
        stage('Set Up Environment') {
            steps {
                sh '''
                    apt-get update
                    apt-get install -y python3 python3-pip curl unzip
                    curl -fsSL https://releases.hashicorp.com/terraform/1.5.3/terraform_1.5.3_linux_amd64.zip -o terraform.zip
                    unzip terraform.zip
                    mv terraform /usr/local/bin/
                    terraform --version
                    python3 --version
                '''
            }
        }

        stage('Terraform Apply') {
            steps {
                sh '''
                    terraform init
                    terraform plan
                    terraform apply -auto-approve
                '''
            }
        }

        // Unit test stages temporarily removed for now.
    }

    post {
        always {
            echo 'Pipeline completed. Archiving artifacts and cleaning up.'
            archiveArtifacts artifacts: '**/terraform.tfstate', fingerprint: true
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
