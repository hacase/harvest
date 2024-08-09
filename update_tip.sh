git pull --quiet
echo sending data
git add .
git commit --quiet -m 'update data'
git push --quiet
echo sent data