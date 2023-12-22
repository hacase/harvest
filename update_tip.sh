git pull --quiet
echo sending data
git add .
git commit --quiet -m 'update plot'
git push --quiet
echo sent data