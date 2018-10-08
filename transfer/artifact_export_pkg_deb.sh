if [ "X${DIR_EXPORT_DPKG}" = "X" ] ; then
    echo "DIR_EXPORT_DPKG not defined"
    sleep 1
    exit 1
fi

if [ "X${DIR_ART_DPKG}" = "X" ] ; then
    echo "DIR_ART_DPKG not defined"
    sleep 1
    exit 1
fi

mkdir -p ${DIR_EXPORT_DPKG}

set +e
files_art_bin=$(ls ${DIR_ART_DPKG}/*.deb)
set -e
changed=0
RSYNC_LOG_FILE=rsync_log_file.log
if [ "X${files_art_bin}" != "X" ] ; then
    for art_bin in $files_art_bin
    do
        rm -f ${RSYNC_LOG_FILE}
        touch ${RSYNC_LOG_FILE}
        /usr/bin/rsync  --log-file=${RSYNC_LOG_FILE}   -v --ignore-existing ${art_bin} ${DIR_EXPORT_DPKG}
        LOGLEN=`wc -l ${RSYNC_LOG_FILE} | cut -d' ' -f1`
        echo LOGLEN=${c}
        if [ "X${LOGLEN}" != "X3" ] ; then
            changed=1
        fi
    done
    if [ "X${changed}" != "X0" ] ; then
        # Publish packages
        pushd ${DIR_EXPORT_DPKG}
        dpkg-scanpackages . | gzip > Packages.gz
        popd
    fi
fi
