ORIGINALDIR=`pwd`
if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
cd $BUILD_SRC
python setup.py bdist_rpm \
    --requires  "${RPM_DEPENDS}"
