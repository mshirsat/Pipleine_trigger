pipeline {
    agent any
    stages {
        stage('install jenkins') {
            steps {
                sh 'pip3 install jenkins'
            }
        }
        stage('run script') {
            steps {
                sh 'python3 api_trigger.py'
            }
        }
    }
}
