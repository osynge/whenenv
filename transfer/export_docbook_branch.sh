pwd
if [ "X${DIR_EXPORT_ROOT}" = "X" ] ; then
    echo "DIR_EXPORT_ROOT not defined"
    DIR_EXPORT_ROOT="/export/docbook_matrix/public_repo"
    #exit 1
    if [ "X${REPOSITORY_TYPE}" = "Xpublic" ] ; then
        DIR_EXPORT_ROOT="/export/docbook_matrix/public_repo"
    fi
    if [ "X${REPOSITORY_TYPE}" = "Xprivate" ] ; then
        DIR_EXPORT_ROOT="/export/docbook_matrix/private_repo"
    fi
fi
tar -zxvf artifacts.tgz
rm -f artifacts.tgz
RELEASE_TYPE="development"
PLATFORM="x86_64"
FLAVOR="scientific/6"
mkdir -p ${DIR_EXPORT_ROOT}
dir_pdf_a4="${DIR_EXPORT_ROOT}/${RELEASE_TYPE}/pdf/a4"
dir_pdf_letter="${DIR_EXPORT_ROOT}/${RELEASE_TYPE}/pdf/letter"
dir_epub="${DIR_EXPORT_ROOT}/${RELEASE_TYPE}/epub"
dir_html_single="${DIR_EXPORT_ROOT}/${RELEASE_TYPE}/html/single"
dir_html_multi="${DIR_EXPORT_ROOT}/${RELEASE_TYPE}/html/multi"

mkdir -p ${dir_pdf_a4}
mkdir -p ${dir_pdf_letter}
mkdir -p ${dir_html_single}
mkdir -p ${dir_html_multi}
mkdir -p ${dir_epub}

/usr/bin/rsync -va --ignore-existing build/Book-a4.pdf \
    ${dir_pdf_a4}/${PRODUCT}-a4-${SRC_VERSION}.pdf
/usr/bin/rsync -va --ignore-existing build/Book-letter.pdf \
    ${dir_pdf_letter}/${PRODUCT}-letter-${SRC_VERSION}.pdf
/usr/bin/rsync -va --ignore-existing build/Book.epub \
    ${dir_epub}/${PRODUCT}-${SRC_VERSION}.epub
/usr/bin/rsync -va --ignore-existing build/Book.html \
    ${dir_html_single}/${PRODUCT}-${SRC_VERSION}.html
/usr/bin/rsync -va --ignore-existing build/Book/* \
    ${dir_html_multi}/${PRODUCT}-${SRC_VERSION}
