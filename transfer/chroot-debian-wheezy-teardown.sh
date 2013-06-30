function ycheckrc () {
echo $@
$@
rc=$?
if [ $[${rc}] != 0 ] ; then
    exit ${rc}
fi
}
ycheckrc mv ${CHROOT}/artifacts.tgz .

ycheckrc python /root/chrootbuilder \
  --dest  ${CHROOT}  \
  --clean
