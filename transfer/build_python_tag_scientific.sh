pwd
if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
ORIGINALDIR=`pwd`
cd $BUILD_SRC
python setup.py bdist_rpm \
    --requires  "python-sqlalchemy m2crypto python-magic smimeX509validation "
cd $ORIGINALDIR
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/dist
