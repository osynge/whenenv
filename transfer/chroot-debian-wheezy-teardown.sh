function ycheckrc () {
echo $@
$@
rc=$?
if [ $[${rc}] != 0 ] ; then
    exit ${rc}
fi
}
find chroot | grep artifacts.tgz
ycheckrc mv chroot/artifacts.tgz .

python /root/chrootbuilder \
  --dest  chroot \
  --clean
