
template="0 0.07875 0.07875 0.1125 0.1125"

ls *.jpg | while read line
do
	filename=`echo ${line} | sed -e 's/.jpg/.txt/'`
	echo ${template} > ${filename}
done
