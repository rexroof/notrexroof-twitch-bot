# just a helper script to build and run this container. 

docker build -t notrexroof .

  # -v /path/to/config_folder:/root/.config/opsdroid \
docker run --env-file=.env --rm -it \
  -v $PWD/configuration.yaml:/root/.config/opsdroid/configuration.yaml \
  notrexroof
