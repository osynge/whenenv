set -x
rm -rf vm_overlays
dirStart=`pwd`
git clone git://git.fritz.box/vm_overlays.git vm_overlays
cd vm_overlays

branches=`git branch  -a | grep remote | sed -e 's/.*remotes\/origin\///'`
for this in $branches ; do
cd ${dirStart}/vm_overlays
git checkout origin/$this
cd content
find . -print |cpio -o -Hnewc |bzip2 -9 -z -q -f > ${dirStart}/${this}.cpio.bz2
done


su exporter -c"vmcaster \
   --database sqlite:////var/lib/vmcaster/local.db \
   --upload-image debian-7-yokel-prod.cpio.bz2 \
   --select-image 333fe448-28c9-44da-a9cb-402818d433bb \
   --verbose    --verbose"
rm -rf sl6.cpio.bz2
