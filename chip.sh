#!/bin/bash
if [ ! -f ./core-modules.yaml ]; then
    echo "No core module configuration found, creating one from defaults..."
    cp ./core-modules.yaml.default ./core-modules.yaml
fi

for dir in ./modules/*; do
    str+=" -f ${dir}/compose.yml"
done

docker compose -f docker-compose-base.yml ${str} config > /tmp/chiptemp
modules=($(docker run --rm -v "/tmp":/workdir mikefarah/yq  '.services.* | key + ":" + .expose[0]' chiptemp))
rm /tmp/chiptemp

core_modules=($(docker run --rm -v "${PWD}":/workdir mikefarah/yq '.* | key + ":" + .' core-modules.yaml))

> setup.env
for module in ${modules[@]}; do
    name=${module%%:*}
    name=${name//-/_}
    name=${name^^}
    echo ${name}=${module} >> setup.env
    for core_module in ${core_modules[@]}; do
        core=${core_module%%:*}
        core=${core^^}
        core_name=${core_module##*:}
        core_name=${core_name//-/_}
        core_name=${core_name^^}
        if [[ "$core_name" == "$name" ]]; then
            echo $core=$name >> setup.env
        fi
    done
done
echo "Created module-address and core-module mappings in setup.env..."

modules_up=""
for core_module in ${core_modules[@]}; do
        modules_up+=${core_module##*:}" "
done

case $1 in
  start)
    if [[ -z "$2" ]] ; then
        echo "Booting system with core modules:"
        echo $modules_up
        docker compose -f docker-compose-base.yml ${str} build ${modules_up}
        docker compose -f docker-compose-base.yml ${str} up ${modules_up}
    else
        echo "Starting specific modules: "+"${@:2}"
        docker compose -f docker-compose-base.yml ${str} build "${@:2}"
        docker compose -f docker-compose-base.yml ${str} up "${@:2}"
    fi
    ;;

  stop)
    echo "Taking down full system and removing volume data..."
    docker compose -f docker-compose-base.yml ${str} down -v
    ;;

  restart)
    echo "Restarting system with clean volume data..."
    docker compose -f docker-compose-base.yml ${str} down -v
    docker compose -f docker-compose-base.yml ${str} build ${modules_up}
    docker compose -f docker-compose-base.yml ${str} up ${modules_up}
    ;;

  *)
    echo "Please use either 'start' or 'stop' or 'restart'"
    ;;
esac