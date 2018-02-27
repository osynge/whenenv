if [ "X${DIR_EXPORT_ROOT}" = "X" ] ; then
    echo "DIR_EXPORT_ROOT not defined"
    DIR_EXPORT_ROOT="/export/jenkins_matrix_build/repo"
    #exit 1
    if [ "X${REPOSITORY_TYPE}" = "Xpublic" ] ; then
        DIR_EXPORT_ROOT="/export/jenkins_matrix_build/public_repo"
    fi
    if [ "X${REPOSITORY_TYPE}" = "Xprivate" ] ; then
        DIR_EXPORT_ROOT="/export/jenkins_matrix_build/private_repo"
    fi
fi
export DIR_EXPORT_ROOT
sleep 5
