set -x
rm -rf vm_overlays
rm -f ./*.cpio.bz2
dirStart=`pwd`
git clone git://git.fritz.box/vm_overlays.git vm_overlays
cd vm_overlays

branches="debian-7-yokel-prod sl-6-yokel-testing-prod sl-6-yokel-testing-trunk"

for this in $branches ; do
rm -f ${this}.cpio.bz2
done

for this in $branches ; do
cd ${dirStart}/vm_overlays
git branch $this origin/$this
git checkout $this
cd content
find . -print |cpio -o -Hnewc |bzip2 -9 -z -q -f > ${dirStart}/${this}.cpio.bz2
done
cd ${dirStart}
ls *.cpio.bz2

su exporter -c"vmcaster \
   --database sqlite:////var/lib/vmcaster/local.db \
   --upload-image debian-7-yokel-prod.cpio.bz2 \
   --select-image 333fe448-28c9-44da-a9cb-402818d433bb \
   --verbose    --verbose"

su exporter -c"vmcaster \
   --database sqlite:////var/lib/vmcaster/local.db \
   --upload-image sl-6-yokel-testing-prod.cpio.bz2 \
   --select-image 6b9384e5-5923-4d47-aaab-0fde0c52f8b8 \
   --verbose    --verbose"

su exporter -c"vmcaster \
   --database sqlite:////var/lib/vmcaster/local.db \
   --upload-image sl-6-yokel-testing-trunk.cpio.bz2 \
   --select-image bba0d5e8-3c70-49e0-8479-a42278aea120 \
   --verbose    --verbose"

rm -f ./*.cpio.bz2

