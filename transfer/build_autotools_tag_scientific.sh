# Now we make the artifacts
rm -f artifacts.tgz
tar -zcvf artifacts.tgz ${BUILD_SRC}/dist
rm -rf ${BUILD_SRC}
