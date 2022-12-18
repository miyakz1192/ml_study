
ls *.jpg | while read line
do
	filename=`echo ${line} | sed -e 's/.jpg/.xml/'`
	cp /tmp/master.xml ${filename}
done
