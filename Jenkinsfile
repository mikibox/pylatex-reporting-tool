pipeline {
    agent {
        docker {
            image 'miquelrfairman/reportingapp:latest'
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'python -m compileall .'
            }
        }
        stage('Test') {
            steps {
                sh 'python -m unittest tests.py'
            }
        }
        stage('Deliver') {
            steps {
                sh 'pyinstaller -y --add-data database:database gui.py'
                sh '''
                    cd dist/
                    ls -alt
                    zip -r gui gui

                '''
            }
            post {
                success {
                    archiveArtifacts 'dist/gui.zip'
                    copyArtifacts(projectName: 'reportingapppipeline',target: '/home')
                }
                failure {
                    sh 'rm -r dist build'
                }
            }
        }
    }
}