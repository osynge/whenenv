if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
ORIGINALDIR=`pwd`
cd $BUILD_SRC
sizes="16 22 24 32 48 72 128"
basedirect="icons"
set +x
for item in `ls icons/*.svg`
do
   for size in $sizes
   do
       name=$(echo $item | sed -e 's/.*\///' | sed -e 's/\.svg.*$//')
       cmd="convert  -background transparent  -resize ${size}x${size} $item  ${basedirect}/${name}_${size}x${size}.png"
       $cmd
   done
done
set -x
cd $ORIGINALDIR
