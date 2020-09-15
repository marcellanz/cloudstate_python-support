#!/usr/bin/env bash

RUN_SUFFIX=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)

PROXY_NAME=cloudstate-proxy-$RUN_SUFFIX
USER_FUNCTION_NAME=cloudstate-function-$RUN_SUFFIX
FUNCTION_CLIENT_NAME=cloudstate-function-client-$RUN_SUFFIX
TCK_NAME=cloudstate-tck-$RUN_SUFFIX
NETWORK_NAME=tck-network-$RUN_SUFFIX

#  fresh docker build
docker build -t dev-cloudstate-tck:local ./

docker network create $NETWORK_NAME

#  primary tck tests for shopping cart
docker run -d --network $NETWORK_NAME --name $PROXY_NAME -p 9000:9000 \
    -e USER_FUNCTION_HOST=$TCK_NAME \
    -e USER_FUNCTION_PORT=8090 \
    cloudstateio/cloudstate-proxy-dev-mode
sleep 10
docker run -d --network $NETWORK_NAME --name $USER_FUNCTION_NAME -p 8080:8080 dev-cloudstate-tck:local \
    server \
    shoppingcart
sleep 10
docker run --rm --network $NETWORK_NAME --name $TCK_NAME -p 8090:8090 \
    -e TCK_HOST=0.0.0.0 \
    -e TCK_PROXY_HOST=$PROXY_NAME \
    -e TCK_FRONTEND_HOST=$USER_FUNCTION_NAME \
    cloudstateio/cloudstate-tck

status=$?
echo "Removing docker containers"
docker rm -f $PROXY_NAME
docker rm -f $USER_FUNCTION_NAME

#  secondary integration tests for stateless function:
docker run -d --network $NETWORK_NAME --name $USER_FUNCTION_NAME -p 8080:8080 dev-cloudstate-tck:local \
    server \
    functiondemo \
    shoppingcart
sleep 10
docker run -d --network $NETWORK_NAME --name $PROXY_NAME -p 9000:9000 \
    -e USER_FUNCTION_HOST=$USER_FUNCTION_NAME \
    -e USER_FUNCTION_PORT=8080 \
    cloudstateio/cloudstate-proxy-dev-mode
sleep 10
docker run --network $NETWORK_NAME --name $FUNCTION_CLIENT_NAME dev-cloudstate-tck:local \
    client \
    server_host $PROXY_NAME \
    functiondemo \
    shoppingcart

status1=$?

docker rm -f $PROXY_NAME
docker rm -f $USER_FUNCTION_NAME

docker network rm $NETWORK_NAME

RETURNSTATUS=1
if [ "${status1}" == 0 ] && [ "${status}" == 0 ]; then
  RETURNSTATUS=0
fi

exit $RETURNSTATUS
