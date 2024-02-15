pipeline {
	agent any
		stages {
			stage('Initial'){
				steps{
					withEnv([“HOME=${env.WORKSPACE}”]) {
					sh “curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python” 
					sh “$HOME/.poetry/bin/poetry install”
				}
			}
		}
}
