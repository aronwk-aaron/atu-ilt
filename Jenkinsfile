
node('worker'){
    step('Checkout Code')[{
        bbs_checkout(
            branches: [[name: params.BRANCH]],
            credentialsId: 'jira',
            id: '4cb99901-7fe3-46f3-a934-e4bde92eb5d6',
            projectName: 'ILT',
            repositoryName: 'atu-ilt',
            serverId: 'c7ae57bb-3c1a-4ec6-b598-a2660b26e64f',
            sshCredentialsId: 'aronwk'
        )
    }
    def tag = ''
    step("Build Container"){

        if (params.BRANCH.contains('master')){
            tag = 'latest'
        } else {
            tag = params.BRANCH.repace('\\', '-')
        }
        sh 'sudo docker build -t aronwk/ilt:${tag} .'
    }
    stage("Push Container"){
        withCredentials([usernamePassword(credentialsId: 'docker-hub-token', passwordVariable: 'password', usernameVariable: 'username')]) {
            sh 'docker login -u ${username} -p ${password}'
            sh 'docker push aronwk/ilt:${tag}'
            sh 'docker logout'
        }
    }
}
