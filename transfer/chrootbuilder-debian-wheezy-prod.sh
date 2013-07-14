GITLOCATION="git://git.fritz.box/chrootbuilder.git"
rm -rf build
git clone ${GITLOCATION} build
cd build
#latest_tag=\$(git tag | org_desy_grid_virt_sort_release.py | tail -n 1)
#git checkout \${latest_tag}
python setup.py bdist_rpm \
    --requires  "python"
