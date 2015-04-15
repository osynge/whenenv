if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/dist
rm -rf $BUILD_SRC
ls *.xml
