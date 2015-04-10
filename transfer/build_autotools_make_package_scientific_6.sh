ORIGINALDIR=`pwd`
cd $BUILD_SRC
make rpm
cp RPMS/x86_64/* dist
cp SRPMS/* dist
