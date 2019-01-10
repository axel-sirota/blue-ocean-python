#!/usr/bin/env groovy

def testPypi = 'https://test.pypi.org/legacy/'
def String imageName = "axelsirota/jenkins-sample/jenkins-sample"
def String dockerArguments
def appImage

pipeline {
    agent any
    stages {
        stage ('Build Image') {
            steps {
                script {
                    appImage = docker.build("${imageName}:0.${env.BUILD_ID}", "-f ${env.WORKSPACE}/docker/Dockerfile .")
                }
            }
        }
        stage('Compile') {
            steps {
                script {
                    appImage.inside(){
                        sh "entrypoint.sh python -m  compileall -f app"
                    }
                }
            }
        }
        stage('Build and install'){
            steps {
                script {
                    appImage.inside(){
                        sh "entrypoint.sh python setup.py bdist_wheel"
                        sh "entrypoint.sh python setup.py install"
                    }
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    appImage.inside(){
                        sh "entrypoint.sh python setup.py pytest"
                        sh "ls -lah ."
                        sh "ls -lah report"
                        sh "ls -lah ${env.WORKSPACE}"
                        junit allowEmptyResults: true, testResults: "report/tests.xml"
                        cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: "report/coverage.xml", conditionalCoverageTargets: '70, 0, 0', lineCoverageTargets: '80, 0, 0', maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false
                        step([
                                    $class                     : 'WarningsPublisher',
                                    parserConfigurations       : [[parserName: 'Flake8', pattern   : "report/flake8.log"]],
                                    unstableTotalAll           : '20',
                                    usePreviousBuildAsReference: true
                                ])
                    }
                }
            }
        }
        stage('Code Checking') {
            steps {
                script {
                    appImage.inside(){
                        sh "entrypoint.sh python -m pylint app --exit-zero >> report/pylint.log"
                    }
                }
                step([
                        $class                     : 'WarningsPublisher',
                        parserConfigurations       : [[parserName: 'PYLint', pattern   : "report/pylint.log"]],
                        unstableTotalAll           : '20',
                        usePreviousBuildAsReference: true
                    ])
            }
        }
        stage('Archive reports') {
            steps {
                archive "report/*"
            }
        }
        stage('Decide to deploy to Docker Hub') {
            agent none
            steps {
                script {
                env.TAG_ON_DOCKER_HUB = input message: 'User input required',
                    parameters: [choice(name: 'Deploy to Docker Hub', choices: 'no\nyes', description: 'Choose "yes" if you want to deploy this build')]
                }
            }
        }
        stage('Deploy to Docker Hub') {
            agent any
            when {
                environment name: 'TAG_ON_DOCKER_HUB', value: 'yes'
            }
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-key') {
                        appImage.push()
                    }
                }
            }
        }
    }
}
