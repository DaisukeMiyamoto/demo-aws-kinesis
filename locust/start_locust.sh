#!/bin/bash

TARGET=http://.elasticbeanstalk.com

locust --slave &
locust --slave &
locust --slave &
locust --slave &
locust --no-web --expect-slaves 4 --master -H ${TARGET} -c 20 -r 100
