pipeline {
    
    agent any

    options {
        disableConcurrentBuilds()
    }

    triggers {
        pollSCM('H */4 * * 1-5')
    }

    stages {
        
        stage("Build and start test image") {
            steps {
                sh "docker-compose up --build -d"
            }
        }

        // TO-DO: 
        // stage ('Run Test') {}

    }

    post {
        always {
            deleteDir()
        }

        success {
            mail to:"000@gmail.com", subject:"SUCCESS: ${currentBuild.fullDisplayName}", body: "Pipeline Succeeded."
        }
    
        failure {
            mail to:"000@gmail.com", subject:"FAILURE: ${currentBuild.fullDisplayName}", body: "Pipeline Failed."
        }

    }

}