
template="0 0.015278 0.006875 0.028704 0.012917"
ddir=$1

if [ $# -ne 1 ]; then
	echo "ERROR: set data directory"
	exit 1
fi


ls ${ddir}/*.jpg | while read line
do
	filename=`echo ${line} | sed -e 's/.jpg/.txt/'`
	echo ${template} > ${filename}
done
