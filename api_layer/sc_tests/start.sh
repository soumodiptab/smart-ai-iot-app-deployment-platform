kill -9 $(ps aux|grep '[p]ython3 s1.py' | awk ' { print $2 } ')
python3 s1.py &
sleep 1
kill -9 $(ps aux|grep '[p]ython3 s2.py' | awk ' { print $2 } ')
python3 s2.py &
sleep 1
kill -9 $(ps aux|grep '[p]ython3 s3.py' | awk ' { print $2 } ')
python3 s3.py &
sleep 1
kill -9 $(ps aux|grep '[p]ython3 c1.py' | awk ' { print $2 } ')
python3 c1.py &
sleep 1
kill -9 $(ps aux|grep '[p]ython3 c2.py' | awk ' { print $2 } ')
python3 c2.py &
sleep 1