pipeline {
    agent any
    stages {
        stage('install jenkins') {
            steps {
                sh 'pip3 install python-jenkins --proxy http://proxy-dmz.intel.com:911'
            }
        }
        stage('run script') {
            steps {
                sh 'python3 api_trigger.py'
            }
        }
    }
}
