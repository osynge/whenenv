pwd
if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
if [ "X${RPM_DEPENDS}" = "X" ] ; then
    echo "RPM_DEPENDS not defined"
    exit 1
fi

if [ "X${PYTHON_VENV}" = "X" ] ; then
    PYTHON_VENV=`pwd`/venv
fi
rm -rf $PYTHON_VENV
rm -rf nosetests.xml
virtualenv -q --system-site-packages $PYTHON_VENV
. ${PYTHON_VENV}/bin/activate
ORIGINALDIR=`pwd`
cd $BUILD_SRC
python setup.py install
python setup.py nosetests
deactivate
cp nosetests.xml ${ORIGINALDIR}/nosetests.xml
rm -rf ${PYTHON_VENV}
cd $ORIGINALDIR
