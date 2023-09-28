git pull --quiet
git add .
echo sending data
git commit --quiet -m  'update tip data'
sleep 7
git push --quiet

echo sent data.
