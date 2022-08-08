png=` ping -c 5 185.18.214.189 | tail -n 1 | awk '{print $4}' | cut -d "/" -f 2 | cut -d "." -f 1`
echo "ping: $png"
if [ $png -gt 150 ]
then
    echo "DoS"
else
    echo "ok"
fi