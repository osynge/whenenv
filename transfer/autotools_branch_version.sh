ORIGINALDIR=`pwd`
export SRC_VERSION
cd $BUILD_SRC


if [  "X${CHECKOUT_DATE}" = "X" ] ; then
    echo "CHECKOUT_DATE not defined"
    exit 1
fi

# Modify version number with build number

sed -i  "/^AC_INIT/ s/)/_rc${CHECKOUT_DATE})/"  configure.ac
