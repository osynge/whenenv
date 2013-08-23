

ORIGINALDIR=`pwd`
cd $BUILD_SRC
make html
make pdf
cd $ORIGINALDIR

rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/*.pdf build/Book
