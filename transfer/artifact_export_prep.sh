if [ "X${REPOSITORY_TYPE}" = "X" ] ; then
echo "REPOSITORY_TYPE not defined"
sleep 1
exit 1
fi

if [ "X${ART_EXPORT_ROOTDIR}" = "X" ] ; then
    echo "ROOTDIR not defined"
    ART_EXPORT_ROOTDIR="/export/jenkins_matrix_build/repo"
    #exit 1
    if [ "X${REPOSITORY_TYPE}" = "Xpublic" ] ; then
        ART_EXPORT_ROOTDIR="/export/jenkins_matrix_build/public_repo"
    fi
    if [ "X${REPOSITORY_TYPE}" = "Xprivate" ] ; then
        ART_EXPORT_ROOTDIR="/export/jenkins_matrix_build/private_repo"
    fi
fi
export ART_EXPORT_ROOTDIR
