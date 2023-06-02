pipeline{
    agent any
    stages {
        stage("add_allure"){
             steps{
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
             }
        }
     }
}