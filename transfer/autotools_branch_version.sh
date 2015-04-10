ORIGINALDIR=`pwd`
export SRC_VERSION
cd $BUILD_SRC

# Modify version number with build number

sed -i  "/^AC_INIT/ s/)/_rc${BUILD_NUMBER})/"  configure.ac 
