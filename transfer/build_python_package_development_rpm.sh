ORIGINALDIR=`pwd`
if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
cd $BUILD_SRC
python setup.py bdist_rpm \
    --release rc${CHECKOUT_DATE} \
    --requires  "${RPM_DEPENDS}"

if [ "X${DIR_ART_SRPMS}" != "X" ] ; then
mv dist/*.src.rpm \
    ${DIR_ART_SRPMS}
fi

if [ "X${DIR_ART_RPMS}" != "X" ] ; then
mv dist/*.rpm \
    ${DIR_ART_RPMS}
fi
