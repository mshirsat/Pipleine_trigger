pipeline {
    agent any
    parameters {
        url = "cbjenkins-fm.devtools.intel.com/teams-dcai-dpea-paiv"
        string(name: 'job_name', defaultValue: '', description: '')
        string(name: 'token', defaultValue: '', description: '')
        string(name: 'parameters', defaultValue: '', description: '')
        string(name: 'parameter_values', defaultValue: '', description: '')
    }
    stages {
        stage('run script') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'mycreds', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh 'python3 api_trigger.py -u $USERNAME -p $PASSWORD --url ${params.url} --job_name ${params.job_name} --token ${params.token}'
                }
            }
        }
    }
}
