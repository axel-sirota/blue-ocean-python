#!/usr/bin/env groovy

def testPypi = 'https://test.pypi.org/legacy/'
def String imageName = "axelsirota/pluralsight-audition/jenkins-sample"
def String dockerArguments
def appImage

pipeline {
    agent any
    stages {
        stage('Setup Environment') {
            steps {
                sh '''#!/bin/bash
                    python3 -m pip install virtualenv
                    mkdir -p ${env.WORKSPACE}/report
                ''' 
            }
        }
        stage ('Build Image') {
            steps {
                script {
                    appImage = docker.build("${imageName}:0.${env.BUILD_ID}", "-f ${env.WORKSPACE}/docker/Dockerfile .")
                    dockerArguments = "-it -v ${env.WORKSPACE}/report:/report -p 5000:5000"
                }
            }
        }
        stage('Compile') {
            steps {
                script {
                    appImage.inside(dockerArguments){
                        sh "entrypoint.sh python -m  compileall -f app"
                    }
                }
            }
        }
        stage('Build and install'){
            steps {
                script {
                    appImage.inside(dockerArguments){
                        sh "entrypoint.sh python setup.py bdist_wheel"
                        sh "entrypoint.sh python setup.py install"
                    }
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    appImage.inside(dockerArguments){ 
                        sh "entrypoint.sh python setup.py pytest"
                    }
                }
                step([$class: 'JUnitResultArchiver', testResults: "${env.WORKSPACE}/report/tests.xml"])
                step([$class: 'CoberturaPublisher', autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: "${env.WORKSPACE}/report/coverage.xml", failUnhealthy: true, failUnstable: true, maxNumberOfBuilds: 0, onlyStable: true, sourceEncoding: 'ASCII', zoomCoverageChart: true])
            }
        }
        stage('Code Checking') {
            steps {
                script {
                    appImage.inside(dockerArguments){
                        sh "entrypoint.sh python -m pylint app --exit-zero >> report/pylint.log"
                    }
                }
                step([
                    $class                     : 'WarningsPublisher',
                    parserConfigurations       : [[parserName: 'PYLint', pattern   : "${env.WORKSPACE}/report/pylint.log"]],
                    unstableTotalAll           : '20',
                    usePreviousBuildAsReference: true
                ])
                step([
                    $class                     : 'WarningsPublisher',
                    parserConfigurations       : [[parserName: 'Flake8', pattern   : "${env.WORKSPACE}/report/flake8.log"]],
                    unstableTotalAll           : '20',
                    usePreviousBuildAsReference: true
                ])
            }
        }
        stage('Archive reports') {
            steps {
                archive "${env.WORKSPACE}/report/*"
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
