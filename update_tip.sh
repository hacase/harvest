git pull --quiet
echo sending data
git add .
git commit --quiet -m 'rewrite offline holidays'
git push --quiet
echo sent data