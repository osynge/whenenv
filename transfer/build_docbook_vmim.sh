ORIGINALDIR=`pwd`
cd $BUILD_SRC/docs/book
make html
make pdf
make epub
make man
cd $ORIGINALDIR
rm -rf build
mv $BUILD_SRC/docs/book build
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/*.pdf build/Book build/Book.epub 
