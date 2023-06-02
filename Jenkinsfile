pipeline{
    agent any
    stages {
        stage("run_pytest"){
             steps{
                bat 'pytest --alluredir allure-results --clean-alluredir'
             }
        }
        stage("add_allure"){
             steps{
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
             }
        }
     }
}