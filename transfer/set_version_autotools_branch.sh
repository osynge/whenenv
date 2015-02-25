ORIGINALDIR=`pwd`
export SRC_VERSION
cd $BUILD_SRC


sed -i  "/^AC_INIT/ s/)/_rc${BUILD_NUMBER})/"  configure.ac 
