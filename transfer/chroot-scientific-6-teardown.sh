function ycheckrc () {
echo $@
$@
rc=$?
if [ $[${rc}] != 0 ] ; then
    exit ${rc}
fi
}
ycheckrc mv ${CHROOT}/artifacts.tgz .



export CROOT_DIR="/root/sl6"
chrootbuilder \
  --dest  ${CROOT_DIR} \
  --clean
