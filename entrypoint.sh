#!/bin/bash
set -e

TMP=$(mktemp)

curl -Ss http://ngrok:4040/api/tunnels > $TMP

proto=$(jq -r .tunnels[0].proto  $TMP )
NGROK_URL=$(jq -r .tunnels[0].public_url  $TMP)

if [ $proto = "https" ] ; then
  echo "found ngrok:  $proto $NGROK_URL"
else
  proto=$(jq -r .tunnels[1].proto $TMP)
  NGROK_URL=$(jq -r .tunnels[1].public_url $TMP)
  echo "found ngrok:  $proto $NGROK_URL"
fi

rm -rf $TMP

export NGROK_URL
exec "$@"
