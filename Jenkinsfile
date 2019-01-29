pipeline {
  agent {
    kubernetes {
      label 'python-gcloud'
      defaultContainer 'jnlp'
      serviceAccount 'helm'
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: gcloud
    image: gcr.io/cidc-dfci/gcloud-helm:latest
    command:
    - cat
    tty: true
  - name: python
    image: python:3.6.5
    command:
    - cat
    tty: true
"""
    }
  }
  environment {
      GOOGLE_APPLICATION_CREDENTIALS = credentials('google-service-account')
      CODECOV_TOKEN = credentials('cidc-cli-codecov-token')
  }
  stages {
    stage('Checkout SCM') {
      steps {
        container('python') {
          checkout scm
        }
      }
    }
    stage('Run unit tests') {
      steps {
        container('python') {
          sh 'pip3 install -r requirements.txt'
          sh 'pytest --html=command_line_tests.html'
          sh 'pytest --cov-report xml:coverage.xml --cov ./'
          sh 'curl -s https://codecov.io/bash | bash -s - -t ${CODECOV_TOKEN}'
        }
      }
    }
    stage('Upload report (dev)') {
      when {
        not {
          anyOf {
            branch "master";
            branch "staging"
          }
        }
      }
      steps {
        container('gcloud') {
          sh 'gsutil cp command_line_tests.html gs://cidc-test-reports/cidc-cli/dev'
        }
      }
    }
    stage('Upload report (staging)') {
      steps {
        when {
          branch 'staging'
        }
        container('gcloud') {
          sh 'gsutil cp command_line_tests.html gs://cidc-test-reports/cidc-cli/staging'
        }
      }
    }
    stage('Upload report (master)') {
      when {
        branch 'master'
      }
      steps {
        container('gcloud') {
          sh 'gsutil cp command_line_tests.html gs://cidc-test-reports/cidc-cli/master'
        }
      }
    }
  }
}