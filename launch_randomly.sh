WORKDIR=/home/andrei/land_parsing
time_span=480 #launching period in minutes
minutes=$((RANDOM*time_span/32768)) # dividing by the maximal value of RANDOM plus one
at -f $WORKDIR/launch.sh now + $minutes minutes
