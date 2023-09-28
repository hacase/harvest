git pull &> /dev/null
git add .
echo sending data
git commit -m  'update tip data' &> /dev/null
sleep 7
git push &> /dev/null

echo sent data.