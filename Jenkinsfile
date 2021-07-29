pipeline {
    agent any
    parameters {
        string(name: 'instance_ip', description: 'ip of the Application Server')
    }

    stages {
        stage('update') {
            steps {
                git branch: 'main', url: 'https://github.com/Arvind-Jagirala/ITGlue_Repo.git'
                sh "ansible-playbook application-deploy.yml -i hosts --limit ${params.instance_ip}"

            }

        }
    }
}
