if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
if [ "X${RPM_DEPENDS}" = "X" ] ; then
    echo "RPM_DEPENDS not defined"
    exit 1
fi
ORIGINALDIR=`pwd`
cd $BUILD_SRC
python setup.py sdist
echo "made src"
