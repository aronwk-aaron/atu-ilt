properties([
  parameters([
    gitParameter(
        branch: '',
        branchFilter: 'origin/(.*)',
        defaultValue: 'master',
        description: '',
        name: 'BRANCH',
        quickFilterEnabled: false,
        selectedValue: 'NONE',
        sortMode: 'NONE',
        tagFilter: '*',
        useRepository: 'git@github.com:aronwk-aaron/atu-ilt.git',
        type: 'PT_BRANCH'
    )
  ])
])

node('worker'){
    stage('Clone Code'){
        checkout([
            $class: 'GitSCM',
            branches: [[name: params.BRANCH]],
            extensions: [],
            userRemoteConfigs: [
                [
                    credentialsId: 'aronwk',
                    url: 'git@github.com:aronwk-aaron/atu-ilt.git'
                ]
            ]
        ])
    }
    def tag = ''
    stage("Build Container"){

        if (params.BRANCH.contains('master')){
            tag = 'latest'
        } else {
            tag = params.BRANCH.replace('\\', '-')
        }
        sh "docker build -t aronwk/ilt:${tag} ."
    }
    stage("Push Container"){
        withCredentials([usernamePassword(credentialsId: 'docker-hub-token', passwordVariable: 'password', usernameVariable: 'username')]) {
            sh "docker login -u ${username} -p ${password}"
            sh "docker push aronwk/ilt:${tag}"
            sh 'docker logout'
        }
    }
}
