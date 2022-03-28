::cisco::eem::event_register_cli occurs 1 pattern "^bounce\s.+\s\d" sync no skip yes enter
#
# Import Namespaces
#
namespace import ::cisco::eem::*
namespace import ::cisco::lib::*

array set arr_einfo [event_reqinfo]
set command $arr_einfo(msg)
set fspace [ string first " " $command ]
set args [ string range $command [ expr $fspace+1 ] end ]
set sspace [ string first " " $args ]
set seconds [ string range $args [ expr $sspace+1 ] end  ]
set interface [ string range $args 0 [ expr $sspace-1 ] ]

set seconds_sum [expr $seconds *1000]
puts "Interface $interface will be bounced with a $seconds delay. Are you sure? (y/n)"
set answer [gets stdin]
if {$answer == "y"} {
    ios_config "interface $interface" "shutdown"
    after $seconds_sum
    ios_config "interface $interface" "no shutdown"
}
