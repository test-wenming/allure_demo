pipeline{
    agent any
    stages {
        stage("run_pytest"){
             steps{
                bat 'pytest --alluredir allure-results --clean-alluredir'
             }
        }
    }
    post {
        always {
            // 无论构建成功或失败都执行的操作
            script {
                // 生成Allure报告
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
     }
}