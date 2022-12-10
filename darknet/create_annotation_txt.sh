
template="0 0.039663 0.039663 0.074519 0.074519"

ls *.jpg | while read line
do
	filename=`echo ${line} | sed -e 's/.jpg/.txt/'`
	echo ${template} > ${filename}
done
