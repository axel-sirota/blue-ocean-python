#!/usr/bin/env groovy

pythonExecutable = '$WORKSPACE/temp/bin/python3'
def testPypi = 'https://test.pypi.org/legacy/'


def runTests(int threshold, String unitTime, String typeOfTest) {
    println "Llegue"
    println "${pythonExecutable} setup.py nosetests --verbose --with-xunit --xunit-file=output/xunit.xml --with-xcoverage --xcoverage-file=output/coverage.xml --cover-package=funniest --tests tests/${typeOfTest}"
    timestamps {
        timeout(time: threshold, unit: unitTime) {
            try {
                sh "${pythonExecutable} setup.py nosetests --verbose --with-xunit --xunit-file=output/xunit.xml --with-xcoverage --xcoverage-file=output/coverage.xml --cover-package=funniest --tests tests/${typeOfTest}"
            } finally {
                step([$class: 'JUnitResultArchiver', testResults: 'output/xunit.xml'])
                step([$class: 'CoberturaPublisher', autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'output/coverage.xml', failUnhealthy: true, failUnstable: true, maxNumberOfBuilds: 0, onlyStable: true, sourceEncoding: 'ASCII', zoomCoverageChart: true])
            }
        }
    }
}

def cleanup() {
    def exec = """
        rm -rf *
        pip3 install --quiet virtualenv
        virtualenv --no-site-packages -p \$(which python3) temp
        . ${env.WORKSPACE}/temp/bin/activate
        mkdir output
    """
    sh exec
}

node {

        stage('Clean') {
            cleanup()
        }

        stage('Checkout SCM') {
            checkout scm
        }

        stage('Compile') {
            timeout(time: 30, unit: 'SECONDS') {
                sh "${pythonExecutable} -m compileall -f -q funniest_ieee"
            }
        }

        stage('Build .whl & .tar.gz') {
            sh "${pythonExecutable} setup.py bdist_wheel"
        }

        stage('Install dependencies') {
            sh "${pythonExecutable} -m pip install -U --quiet ."
        }

        stage('Unit Tests') {
            runTests(30, 'MINUTES', 'units')
        }

        stage('Code checking') {

            sh "${pythonExecutable} -m pylint --output-format=parseable --reports=y funniest_ieee > output/pylint.log || exit 0"
            sh "${pythonExecutable} -m flake8 --exit-zero --output-file=output/flake8.log funniest_ieee"
                        step([
                $class                     : 'WarningsPublisher',
                parserConfigurations       : [[parserName: 'PYLint', pattern   : 'output/pylint.log']],
                unstableTotalAll           : '20',
                usePreviousBuildAsReference: true
            ])
            step([
                $class                     : 'WarningsPublisher',
                parserConfigurations       : [[parserName: 'Flake8', pattern   : 'output/flake8.log']],
                unstableTotalAll           : '20',
                usePreviousBuildAsReference: true
            ])
        }


        stage('Archive build artifact: .whl , .tar.gz and reports') {
            archive 'dist/*'
            archive 'output/*'
        }
}

input('Deploy to Pypi?')

node {
        stage('Deploy to Pypi') {
            sh "${pythonExecutable} -m twine upload --config-file .pypirc -r test dist/funniest_ieee-0.5-py2.py3-none-any.whl"
        }

        stage('Clean all'){
            sh 'rm -rf temp'
        }

}
