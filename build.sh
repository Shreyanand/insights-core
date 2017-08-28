#!/bin/bash

set -ev

py.test

if [ "`python -V 2>&1`" != "Python 2.6.9" ]; then 
    flake8;
    sphinx-build -W -b html -qa -E docs docs/_build/html;
    if [ "${TRAVIS_PULL_REQUEST}" == "false" ]; then
        git rev-list HEAD | head -1 > insights/COMMIT
        docker login -u $DOCKER_USER -p $DOCKER_PASS
        export REPO=jhjaggars/insights-core
        docker build -f Dockerfile -t $REPO:$COMMIT .
        docker tag $REPO:$COMMIT $REPO:$TRAVIS_BRANCH
        if [ "$TRAVIS_BRANCH" == "master" ]; then
            docker tag $REPO:$COMMIT $REPO:latest
        fi
        docker push $REPO
    fi
fi

