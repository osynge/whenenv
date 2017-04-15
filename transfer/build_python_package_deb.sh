ORIGINALDIR=`pwd`
if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi

if [ "X${DIR_ART_DPKG}" = "X" ] ; then
    echo "DIR_ART_DPKG not defined"
    exit 1
fi

cd $BUILD_SRC
python setup.py --command-packages=stdeb.command sdist_dsc
cd deb_dist/
cd `find -type d | find -type d | head -n 2 | tail -n 1`
pwd
debuild -uc -us
# Now move packages to Artifact directory
cd ..
rsync -ltgoDv * ${DIR_ART_DPKG}/


#python setup.py bdist_rpm \
#    --release rc${CHECKOUT_DATE} \
#    --requires  "${RPM_DEPENDS}"

#if [ "X${DIR_ART_SRPMS}" != "X" ] ; then
#mv dist/*.src.rpm \
#    ${DIR_ART_SRPMS}
#fi

#if [ "X${DIR_ART_RPMS}" != "X" ] ; then
#mv dist/*.rpm \
#    ${DIR_ART_RPMS}
#fi
