set interface [lindex $argv 0]
set seconds [lindex $argv 1]
set seconds_sum [expr $seconds *1000]
ios_config "interface $interface" "shutdown"
after $seconds_sum
ios_config "interface $interface" "no shutdown"