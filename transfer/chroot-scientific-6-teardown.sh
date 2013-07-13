if [ "X" == "X${CHROOT}" ] then 
    echo "No CHROOT set"
    exit 1
fi
    
chrootbuilder \
  --dest  ${CHROOT} \
  --clean
