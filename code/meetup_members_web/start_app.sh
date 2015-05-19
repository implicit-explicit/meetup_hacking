#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

pushd `dirname $0` > /dev/null
cd $DIR
gunicorn -c gunicorn_config.py app:app
popd > /dev/null