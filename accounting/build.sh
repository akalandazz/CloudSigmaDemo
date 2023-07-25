VERSION_SHA=`git log --format=format:%H -n 1`
VERSION_NAME=`git describe --tags`
docker-compose build --build-arg VERSION_NAME=${VERSION_NAME} --build-arg VERSION_SHA=${VERSION_SHA}

# tag the resulting image with the version
docker tag users_server:latest users_server:${VERSION_NAME}
