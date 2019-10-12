# ChangeLog
# By Philip Shen 
# ---------------------------------------------------------------------
# Apr272019 Initialize 
################################################################################
namespace eval Func_INI {
    package require inifile
    
    variable verbose off
    variable logfile {};#"../logs/inifile.log"
    variable currPath    {}
    variable log_Path    {}
    variable lib_Path    {}
    variable list_sections {}
    variable list_keys {}
    variable list_values {}
    variable list_TopologyIP    {}
    variable dict_TopologyIP    {}
    variable list_WLAN_ClientModelName    {}
    variable dict_WLAN_ClientModelName    {}
    variable list_Chariot_Param    {}
    variable dict_Chariot_Param    {}   
    variable list_Criteria    {}
    variable dict_Criteria    {}
    variable list_DUT    {}
    variable dict_DUT    {}
    variable list_TopologyIP_QoS    {}
    variable dict_TopologyIP_QoS    {}
    variable list_ep01_ipaddr    {}
    variable list_ep02_ipaddr    {}
    variable list_ep01_ipaddr_v6    {}
    variable list_ep02_ipaddr_v6    {}
    
    variable testChrfile_11ac_lan2wlan    {}
    variable testChrfile_11ac_wlan2lan    {}
    variable testChrfile_11ac_wan2lan    {}
    variable testChrfile_11ac_wan2wlan    {}
    
    variable testChrfile_11ac_wan2lan2wan    {}
    variable testChrfile_11ac_wan2wlan2wan    {}
    
    variable testChrfile_11ac_wlan2wan        {}
    variable testChrfile_11ac_wan2wlan        {}
    variable testChrfile_11ac_wlan2wan2wlan     {}
    
    variable testChrfile_11ac_wan2wlan2wan    {}
    
    variable testChrfile_11n_lan2wlan    {}
    variable testChrfile_11n_wlan2lan    {}
    variable testChrfile_11n_wan2lan    {}
    variable testChrfile_11n_wan2wlan    {}
    
    variable testChrfile_11n_lan2wlan2lan    {}
}
proc Func_INI::GetSections {inifname} {
    variable list_sections
    
    set hinifile [ini::open $inifname r]
    set list_sections [ini::sections $hinifile]
    ini::close $hinifile
    #list length == 0
    if ![llength $list_sections] {
        return false
    }
    return true
}
proc Func_INI::GetKeys {inifname section} {
    variable list_keys
    
    set hinifile [ini::open $inifname r]
    set list_keys [ini::keys $hinifile $section]
    ini::close $hinifile
    if ![llength $list_keys] {
        return false
    }
    return true
}
proc Func_INI::GetValue {inifname section key} {
    variable list_values
    
    set hinifile [ini::open $inifname r]
    set keyvalue [ini::value $hinifile $section $key]
    ini::close $hinifile
    
    if ![string length $keyvalue] {
        return false
    }
    
    set list_values [split $keyvalue ',']
    return true
}
proc Func_INI::Log {level filename list_msg} {
    foreach temp $list_msg {
        set msg "$temp"
        Log::tofile $level $filename $msg
    }
}

proc Func_INI::_GetTopologyIP {inifname} {
    variable list_sections
    variable list_keys
    variable list_values
    variable list_TopologyIP
    variable dict_TopologyIP
    variable verbose
    variable logfile
    
    set retval [GetSections $inifname]
    if {$retval == false} {
        return false
    }
    
    foreach temp $list_sections {
        switch -regexp $temp {
            {^Topology$} {
                set sec_topology $temp
            }
        };#switch
    }
    
    set retval [GetKeys $inifname $sec_topology]
    if {$retval == false} {
        return false
    }
    
    foreach temp $list_keys {
        set retval [GetValue $inifname $sec_topology $temp]
        lappend list_TopologyIP $list_values
        
        # store to dict from ini file
        dict set dict_TopologyIP [string tolower $temp] [lindex $list_values 0]
    }
    
    if {$verbose == on} {
        # Log "info" $logfile [list "[lindex $list_keys 0] = [lindex $list_TopologyIP 0]" \
                # "[lindex $list_keys 1] = [lindex $list_TopologyIP 1]" \
                # "[lindex $list_keys 2] = [lindex $list_TopologyIP 2]" \
                # "[lindex $list_keys 3] = [lindex $list_TopologyIP 3]" \
                # "[lindex $list_keys 4] = [lindex $list_TopologyIP 4]"]
        foreach item [dict keys $dict_TopologyIP] {
            set value [dict get $dict_TopologyIP $item]
            Log "info" $logfile [list "$item = $value"]
        }
    };#if {$verbose == on}
    
    return true
}
proc Func_INI::_GetTopologyIP_QoS {inifname} {
    variable list_sections
    variable list_keys
    variable list_values
    variable list_TopologyIP_QoS
    variable dict_TopologyIP_QoS
    variable verbose
    variable logfile
    
    set retval [GetSections $inifname]
    if {$retval == false} {
        return false
    }
    
    foreach temp $list_sections {
        switch -regexp $temp {
            {^Topology_QoS$} {
                set sec_topology_qos $temp
            }
        };#switch
    }
    
    set retval [GetKeys $inifname $sec_topology_qos]
    if {$retval == false} {
        return false
    }
    
    foreach temp $list_keys {
        set retval [GetValue $inifname $sec_topology_qos $temp]
        lappend list_TopologyIP_QoS $list_values
        
        # store to dict from ini file
        dict set dict_TopologyIP_QoS [string tolower $temp] [lindex $list_values 0]
    }
    
    if {$verbose == on} {
        
        foreach item [dict keys $dict_TopologyIP_QoS] {
            set value [dict get $dict_TopologyIP_QoS $item]
            Log "info" $logfile [list "$item = $value"]
        }
    };#if {$verbose == on}
    
    return true
}

proc Func_INI::_GetChariot_Param {inifname} {
    variable list_sections
    variable list_keys
    variable list_values
    variable list_Chariot_Param
    variable dict_Chariot_Param
    variable verbose
    variable logfile
    
    set retval [GetSections $inifname]
    if {$retval == false} {
        return false
    }
    
    foreach temp $list_sections {
        switch -regexp $temp {
            {^Chariot_Param} {
                set sec_chariot_param $temp
            }
        };#switch
    }
    
    set retval [GetKeys $inifname $sec_chariot_param]
    if {$retval == false} {
        return false
    }
    
    foreach temp $list_keys {
        set retval [GetValue $inifname $sec_chariot_param $temp]
        lappend list_Chariot_Param $list_values
        # store to dict from ini file
        dict set dict_Chariot_Param [string tolower $temp] [lindex $list_values 0]
    }
    
    if {$verbose == on} {
        # Log "info" $logfile [list "[lindex $list_keys 0] = [lindex $list_Chariot_Param 0]" \
                # "[lindex $list_keys 1] = [lindex $list_Chariot_Param 1]" \
                # "[lindex $list_keys 2] = [lindex $list_Chariot_Param 2]" \
                # "[lindex $list_keys 3] = [lindex $list_Chariot_Param 3]" ]
        foreach item [dict keys $dict_Chariot_Param] {
            set value [dict get $dict_Chariot_Param $item]
            Log "info" $logfile [list "$item = $value"]
        }
    }
    
    return true
}

proc Func_INI::_GetCriteria {inifname} {
    variable list_sections
    variable list_keys
    variable list_values
    variable list_Criteria
    variable dict_Criteria
    variable verbose
    variable logfile
    
    
    set retval [GetSections $inifname]
    if {$retval == false} {
        return false
    }
    
    foreach temp $list_sections {
        switch -regexp $temp {
            {^Criteria} {
                set sec_criteria $temp
            }
        };#switch
    }
    
    set retval [GetKeys $inifname $sec_criteria]
    if {$retval == false} {
        return false
    }
    
    foreach temp $list_keys {
        set retval [GetValue $inifname $sec_criteria $temp]
        lappend list_Criteria $list_values
        
        # store to dict from ini file
        dict set dict_Criteria [string tolower $temp] [lindex $list_values 0]        
    }
    
    if {$verbose == on} {
        # Log "info" $logfile [list "[lindex $list_keys 0] = [lindex $list_Criteria 0]" \
                # "[lindex $list_keys 1] = [lindex $list_Criteria 1]" ]
        foreach item [dict keys $dict_Criteria] {
            set value [dict get $dict_Criteria $item]
            # puts "$item = $value"
            Log "info" $logfile [list "$item = $value"]
        }
    }
    
    return true
}

proc Func_INI::_GetWLAN_ClientModelName {inifname} {
    variable list_sections
    variable list_keys
    variable list_values
    variable list_WLAN_ClientModelName
    variable dict_WLAN_ClientModelName
    variable verbose
    variable logfile
    
    set retval [GetSections $inifname]
    if {$retval == false} {
        return false
    }
    
    foreach temp $list_sections {
        switch -regexp $temp {
            {^WLAN_Client} {
                set sec_wlan_clientmodelname $temp
            }
        };#switch
    }
    
    set retval [GetKeys $inifname $sec_wlan_clientmodelname]
    if {$retval == false} {
        return false
    }
    
    foreach temp $list_keys {
        set retval [GetValue $inifname $sec_wlan_clientmodelname $temp]
        lappend list_WLAN_ClientModelName $list_values
        
        # store to dict from ini file
        dict set dict_WLAN_ClientModelName [string tolower $temp] [lindex $list_values 0]
    }
    
    if {$verbose == on} {
        # Log "info" $logfile [list "[lindex $list_keys 0] = [lindex $list_WLAN_ClientModelName 0]"]
        
        foreach item [dict keys $dict_WLAN_ClientModelName] {
            set value [dict get $dict_WLAN_ClientModelName $item]
            Log "info" $logfile [list "$item = $value"]
        }
    }
    
    return true
}

proc Func_INI::_GetDUT {inifname} {
    variable list_sections
    variable list_keys
    variable list_values
    variable list_DUT
    variable dict_DUT
    variable verbose
    variable logfile
    
    set retval [GetSections $inifname]
    if {$retval == false} {
        return false
    }
    
    foreach temp $list_sections {
        switch -regexp $temp {
            {^DUT} {
                set sec_dut $temp
            }
        };#switch
    }
    
    set retval [GetKeys $inifname $sec_dut]
    if {$retval == false} {
        return false
    }
    
    foreach temp $list_keys {
        set retval [GetValue $inifname $sec_dut $temp]
        lappend list_DUT $list_values
        # store to dict from ini file
        dict set dict_DUT [string tolower $temp] [lindex $list_values 0]
    }
    
    if {$verbose == on} {
        
        # Log "info" $logfile [list "[lindex $list_keys 0] = [lindex $list_DUT 0]" \
                # "[lindex $list_keys 1] = [lindex $list_DUT 1]"  \
                # "[lindex $list_keys 2] = [lindex $list_DUT 2]"]
        
        foreach item [dict keys $dict_DUT] {
            set value [dict get $dict_DUT $item]
            Log "info" $logfile [list "$item = $value"]
        }
        
    }
    
    return true
}
################################################################################
# Procedure : PingTest
# Purpose   : Before connecting, check host if exists.
################################################################################
proc Func_INI::PingTest {host} {
    catch {exec ping.exe $host -n 1} pingmsg
    set result [string first "Reply" $pingmsg]
    
    if { $result == -1} {
        # puts "Ping $host no Reply"; update
        return false
    } else {
        # puts "Ping $host OK"; update
        return true
    }
}
########################################
# tcl script for ping not working
# https://stackoverflow.com/questions/12524919/tcl-script-for-ping-not-working
##########################################
proc Func_INI::Ping_igp {host} {
    variable verbose
    variable logfile
    
    if {[catch {exec ping $host -n 1} result]} { set result 0 }
    
    if { [regexp "0% "  $result]} {;#"0% loss"
        set logstr "$host alive"
        # show info on widget
        insertLogLine notice $logstr
        #puts $logstr
        
        if {$verbose == on} {
            Log "info" $logfile [list $logstr]
        }
        return true
    } else {
        set logstr "$host failed"
        # show info on widget
        insertLogLine critical $logstr
        #puts $logstr
        
        if {$verbose == on} {
            Log "info" $logfile [list $logstr]
        }
        
        return false
    }
}
proc Func_INI::ChkDUTalive {strIPAddr} {
    
    #set retval [PingTest $strIPAddr]
    set retval [Ping_igp $strIPAddr]
    return $retval
}
proc Func_INI::ChkTopologyalive {} {
    set strmsg "Check WLAN_EP_IPAddr Status"
    insertLogLine critical $strmsg
    set retval_wlan_ep [Func_INI::ChkDUTalive [dict get $Func_INI::dict_TopologyIP "wlan_ep_ipaddr"]]
    
    set strmsg "Check LAN_EP_IPAddr Status"
    insertLogLine critical $strmsg
    set retval_lan_ep [Func_INI::ChkDUTalive [dict get $Func_INI::dict_TopologyIP "lan_ep_ipaddr"]]
    
    set strmsg "Check DUT_LAN_IPAddr Status"
    insertLogLine critical $strmsg
    set retval_dut_lan [Func_INI::ChkDUTalive [dict get $Func_INI::dict_TopologyIP "dut_lan_ipaddr"]]
    
    #check topology status
    if {($retval_wlan_ep == "true") && ($retval_lan_ep == "true") \
                && ($retval_dut_lan == "true")} {
        set strmsg "Check Topology Status Alive!"
        insertLogLine critical $strmsg
        return true
    } else  {
        set strmsg "Check Topology Status not Available!"
        insertLogLine critical $strmsg
        return false
    }
}
proc Func_INI::ChkTopologyalive_ListIPAdd {list_ipaddr} {
    # dafault value setting
    set retval true
    
    #each ip add in list_ipaddr
    foreach ipaddr $list_ipaddr {
        set retval_ipaddr [Func_INI::ChkDUTalive $ipaddr]
        
        # return value if "false" then set retval
        if {$retval_ipaddr == "false"} {
            set retval false
        };#if {$retval_ipaddr == "false"}
        
    };#foreach
    
    return $retval
}
proc Func_INI::ChkTopologyalive_QoS {} {
    variable verbose
    variable logfile
    variable list_ep01_ipaddr
    variable list_ep02_ipaddr
    
    # Check EP01_IPAddr EP02_IPAddr paris number if match
    set list_ep01_ipaddr [split \
                        [dict get $Func_INI::dict_TopologyIP_QoS "ep01_ipaddr"] ";"]
    set num_ep01_ipaddr [llength $list_ep01_ipaddr]
    set strmsg "EP01_IPAddr Numbers: $num_ep01_ipaddr"
    insertLogLine critical $strmsg
    
    if {$verbose == on} {
        Log "info" $logfile [list "list_ep01_ipaddr" $list_ep01_ipaddr]
        Log "info" $logfile [list $strmsg]
    };#if {$verbose == on}
    
    set list_ep02_ipaddr [split \
            [dict get $Func_INI::dict_TopologyIP_QoS "ep02_ipaddr"] ";"]
    set num_ep02_ipaddr [llength $list_ep02_ipaddr]
    set strmsg "EP02_IPAddr Numbers: $num_ep02_ipaddr"
    insertLogLine critical $strmsg
    
    if {$verbose == on} {
        Log "info" $logfile [list "list_ep02_ipaddr" $list_ep02_ipaddr]
        Log "info" $logfile [list $strmsg]
    };#if {$verbose == on}
    
    if {($num_ep01_ipaddr > 0) && ($num_ep02_ipaddr > 0) \
                && ($num_ep01_ipaddr == $num_ep02_ipaddr)} {
        
        set strmsg "Check EP01 and EP02 pair matches!"
        insertLogLine critical $strmsg
        
        if {$verbose == on} {
            Log "info" $logfile [list $strmsg]
        };#if {$verbose == on}
        #return true
    
    } else  {
        set strmsg "Check EP01 and EP02 pair didn't matches!"
        insertLogLine critical $strmsg
        
        if {$verbose == on} {
            Log "info" $logfile [list $strmsg]
        };#if {$verbose == on}
        return false
    }
    
    set strmsg "Check EP01_IPAddr Status"
    insertLogLine critical $strmsg
    # sort uniqu value in list
    set list_unique_ep01_ipaddr [lsort -unique $list_ep01_ipaddr]
    #check list ip address
    set retval_ep01 [Func_INI::ChkTopologyalive_ListIPAdd $list_unique_ep01_ipaddr]
    
    set strmsg "Check EP02_IPAddr Status"
    insertLogLine critical $strmsg
    set list_unique_ep02_ipaddr [lsort -unique $list_ep02_ipaddr]
    set retval_ep02 [Func_INI::ChkTopologyalive_ListIPAdd $list_unique_ep02_ipaddr]
    
    #check topology status
    if {($retval_ep01 == "true") && ($retval_ep02 == "true")} {
        set strmsg "Check QoS Topology Status Alive!"
        insertLogLine critical $strmsg
        
        if {$verbose == on} {
            Log "info" $logfile [list $strmsg]
        };#if {$verbose == on}        
        return true
    } else  {
        set strmsg "Check QoS Topology Status not Available!"
        insertLogLine critical $strmsg
        
        if {$verbose == on} {
            Log "info" $logfile [list $strmsg]
        };#if {$verbose == on}
        return false
    };#if 
    
}
proc Func_INI::ChkTopologyalive_QoS_v6 {} {
    variable verbose
    variable logfile
    variable list_ep01_ipaddr_v6
    variable list_ep02_ipaddr_v6
    
    # Check EP01_IPAddr_v6 EP02_IPAddr_v6 paris number if match
    set list_ep01_ipaddr_v6 [split \
            [dict get $Func_INI::dict_TopologyIP_QoS "ep01_ipaddr_v6"] ";"]
    set num_ep01_ipaddr_v6 [llength $list_ep01_ipaddr_v6]
    set strmsg "EP01_IPAddr_v6 Numbers: $num_ep01_ipaddr_v6"
    insertLogLine critical $strmsg
    
    if {$verbose == on} {
        Log "info" $logfile [list "list_ep01_ipaddr_v6" $list_ep01_ipaddr_v6]
        Log "info" $logfile [list $strmsg]
    };#if {$verbose == on}
    
    set list_ep02_ipaddrset_v6 [split \
            [dict get $Func_INI::dict_TopologyIP_QoS "ep02_ipaddr_v6"] ";"]
    set num_ep02_ipaddr_v6 [llength $list_ep02_ipaddr_v6]
    set strmsg "EP02_IPAddr_v6 Numbers: $num_ep02_ipaddr_v6"
    insertLogLine critical $strmsg
    
    if {$verbose == on} {
        Log "info" $logfile [list "list_ep02_ipaddr_v6" $list_ep02_ipaddr_v6]
        Log "info" $logfile [list $strmsg]
    };#if {$verbose == on} 
    
    if {($num_ep01_ipaddr_v6 > 0) && ($num_ep02_ipaddr_v6 > 0) \
                && ($num_ep01_ipaddr_v6 == $num_ep02_ipaddr_v6)} {
        
        set strmsg "Check EP01_v6 and EP02_v6 pair matches!"
        insertLogLine critical $strmsg
        
        if {$verbose == on} {
            Log "info" $logfile [list $strmsg]
        };#if {$verbose == on}
        #return true
        
    } else  {
        set strmsg "Check EP01_v6 and EP02_v6 pair didn't matches!"
        insertLogLine critical $strmsg
        
        if {$verbose == on} {
            Log "info" $logfile [list $strmsg]
        };#if {$verbose == on}
        return false
    }
    
    set strmsg "Check EP01_IPAddr_v6 Status"
    insertLogLine critical $strmsg
    # sort uniqu value in list
    set list_unique_ep01_ipaddr_v6 [lsort -unique $list_ep01_ipaddr_v6]
    #check list ip address
    set retval_ep01_v6 [Func_INI::ChkTopologyalive_ListIPAdd $list_unique_ep01_ipaddr_v6]
    
    set strmsg "Check EP02_IPAddr_v6 Status"
    insertLogLine critical $strmsg
    set list_unique_ep02_ipaddr_v6 [lsort -unique $list_ep02_ipaddr_v6]
    set retval_ep02_v6 [Func_INI::ChkTopologyalive_ListIPAdd $list_unique_ep02_ipaddr_v6]
    
    #check topology status
    if {($retval_ep01_v6 == "true") && ($retval_ep02_v6 == "true")} {
        set strmsg "Check QoS_v6 Topology Status Alive!"
        insertLogLine critical $strmsg
        
        if {$verbose == on} {
            Log "info" $logfile [list $strmsg]
        };#if {$verbose == on}        
        return true
    } else  {
        set strmsg "Check QoS_v6 Topology Status not Available!"
        insertLogLine critical $strmsg
        
        if {$verbose == on} {
            Log "info" $logfile [list $strmsg]
        };#if {$verbose == on}        
        return false
    };#if
    
}
proc Func_INI::GenChariotTestFile_11ac_lan2wlan {} {
    variable verbose
    variable logfile
    variable testChrfile_11ac_lan2wlan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11ac_lan2wlan] {unset Func_INI::testChrfile_11ac_lan2wlan}
    
    append testChrfile_11ac_lan2wlan [dict get $Func_INI::dict_DUT "dut_modelname"] "_" \
            [dict get $Func_INI::dict_DUT "dut_fwver"] "_" \
            [dict get $Func_INI::dict_DUT "dut_hwver"] "_" \
            [dict get $Func_INI::dict_WLAN_ClientModelName "wlan_modelname"] "_" \
            "11ac" "_" "LAN2WLAN" "_" \
            "$Func_Chariot::pairCount" "Pair(s)" "_" \
            [clock format [clock seconds] -format "%H%M%S_%m%d%Y"] ".tst"
    
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11ac_lan2wlan]
    }
}

proc Func_INI::GenChariotTestFile_11ac_wlan2lan {} {
    variable verbose
    variable logfile
    variable testChrfile_11ac_lan2wlan
    variable testChrfile_11ac_wlan2lan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11ac_lan2wlan] {unset Func_INI::testChrfile_11ac_lan2wlan}
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11ac_lan2wlan
    # Regsub string
    set testChrfile_11ac_wlan2lan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11ac_lan2wlan "WLAN2LAN"]
    
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11ac_wlan2lan]
    }
}
proc Func_INI::GenChariotTestFile_11ac_lan2wlan2lan {} {
    variable verbose
    variable logfile
    variable testChrfile_11ac_lan2wlan
    variable testChrfile_11ac_lan2wlan2lan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11ac_lan2wlan] {unset Func_INI::testChrfile_11ac_lan2wlan}
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11ac_lan2wlan
    
    # Regsub string
    set testChrfile_11ac_lan2wlan2lan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11ac_lan2wlan "LAN2WLAN2LAN"]
            
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11ac_lan2wlan2lan]
    }
        
}
proc Func_INI::GenChariotTestFile_11ac_wan2wlan2wan {} {
    variable verbose
    variable logfile
    variable testChrfile_11ac_lan2wlan
    variable testChrfile_11ac_wan2wlan2wan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11ac_lan2wlan] {unset Func_INI::testChrfile_11ac_lan2wlan}
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11ac_lan2wlan
    # Regsub string
    set testChrfile_11ac_wan2wlan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11ac_lan2wlan "WAN2WLAN2WAN"]
    
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11ac_wan2wlan2wan]
    }
}

proc Func_INI::GenChariotTestFile_11ac_wan2lan2wan {} {
    variable verbose
    variable logfile
    variable testChrfile_11ac_lan2wlan
    variable testChrfile_11ac_wan2lan2wan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11ac_lan2wlan] {unset Func_INI::testChrfile_11ac_lan2wlan}
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11ac_lan2wlan
    # Regsub string
    set testChrfile_11ac_wan2lan2wan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11ac_lan2wlan "WAN2LAN2WAN"]
            
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11ac_wan2lan2wan]
    }
}
proc Func_INI::GenChariotTestFile_11ac_lan2wan {} {
    variable verbose
    variable logfile
    variable testChrfile_11ac_lan2wlan
    variable testChrfile_11ac_lan2wan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11ac_lan2wlan] {unset Func_INI::testChrfile_11ac_lan2wlan}
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11ac_lan2wlan
    # Regsub string
    set testChrfile_11ac_lan2wan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11ac_lan2wlan "LAN2WAN"]
    
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11ac_lan2wan]
    }
}
proc Func_INI::GenChariotTestFile_11ac_wan2lan {} {
    variable verbose
    variable logfile
    variable testChrfile_11ac_lan2wlan
    variable testChrfile_11ac_wan2lan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11ac_lan2wlan] {unset Func_INI::testChrfile_11ac_lan2wlan}
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11ac_lan2wlan
    # Regsub string
    set testChrfile_11ac_wan2lan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11ac_lan2wlan "WAN2LAN"]
    
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11ac_wan2lan]
    }
}

proc Func_INI::GenChariotTestFile_11ac_wlan2wan {} {
    variable verbose
    variable logfile
    variable testChrfile_11ac_lan2wlan
    variable testChrfile_11ac_wlan2wan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11ac_lan2wlan] {unset Func_INI::testChrfile_11ac_lan2wlan}
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11ac_lan2wlan
    
    # Regsub string
    set testChrfile_11ac_wlan2wan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11ac_lan2wlan "WLAN2WAN"]
            
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11ac_wlan2wan]
    }
            
}
proc Func_INI::GenChariotTestFile_11ac_wlan2wan2wlan {} {
    variable verbose
    variable logfile
    variable testChrfile_11ac_lan2wlan
    variable testChrfile_11ac_wlan2wan2wlan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11ac_lan2wlan] {unset Func_INI::testChrfile_11ac_lan2wlan}
    
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11ac_lan2wlan
    
    # Regsub string
    set testChrfile_11ac_wlan2wan2wlan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11ac_lan2wlan "WLAN2WAN2WLAN"]
    
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11ac_wlan2wan2wlan]
    }
}
proc Func_INI::GenChariotTestFile_11ac_wan2wlan {} {
    variable verbose
    variable logfile
    variable testChrfile_11ac_lan2wlan
    variable testChrfile_11ac_wan2wlan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11ac_lan2wlan] {unset Func_INI::testChrfile_11ac_lan2wlan}
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11ac_lan2wlan
    
    # Regsub string
    set testChrfile_11ac_wan2wlan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11ac_lan2wlan "WAN2WLAN"]
    
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11ac_wan2wlan]
    }
}
proc Func_INI::GenChariotTestFile_qos_lan_wlan2wan {} {
    variable verbose
    variable logfile
    variable testChrfile_11ac_lan2wlan
    variable testChrfile_qos_lan_wlan2wan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11ac_lan2wlan] {unset Func_INI::testChrfile_11ac_lan2wlan}
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11ac_lan2wlan
    
    # Regsub string
    set testChrfile_qos_lan_wlan2wan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11ac_lan2wlan "LAN-WLANtoWAN"]
    set testChrfile_qos_lan_wlan2wan \
            [regsub -all "11ac" $Func_INI::testChrfile_qos_lan_wlan2wan "QoS"]
    
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_qos_lan_wlan2wan]
    }
}
proc Func_INI::GenChariotTestFile_11n_lan2wlan {} {
    variable verbose
    variable logfile
    variable testChrfile_11n_lan2wlan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11n_lan2wlan] {unset Func_INI::testChrfile_11n_lan2wlan}
    
    append testChrfile_11n_lan2wlan [dict get $Func_INI::dict_DUT "dut_modelname"] "_" \
            [dict get $Func_INI::dict_DUT "dut_fwver"] "_" \
            [dict get $Func_INI::dict_DUT "dut_hwver"] "_" \
            [dict get $Func_INI::dict_WLAN_ClientModelName "wlan_modelname"] "_" \
            "11n" "_" "LAN2WLAN" "_" \
            "$Func_Chariot::pairCount" "Pair(s)" "_" \
            [clock format [clock seconds] -format "%H%M%S_%m%d%Y"] ".tst"
            
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11n_lan2wlan]
    }
    
}
proc Func_INI::GenChariotTestFile_11n_wlan2lan {} {
    variable verbose
    variable logfile
    variable testChrfile_11n_lan2wlan
    variable testChrfile_11n_wlan2lan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11n_lan2wlan] {unset Func_INI::testChrfile_11n_lan2wlan}
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11n_lan2wlan
    # Regsub string
    set testChrfile_11n_wlan2lan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11n_lan2wlan "WLAN2LAN"]
    
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11n_wlan2lan]
    }
    
}
proc Func_INI::GenChariotTestFile_11n_lan2wlan2lan {} {
    variable verbose
    variable logfile
    variable testChrfile_11n_lan2wlan
    variable testChrfile_11n_lan2wlan2lan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11n_lan2wlan] {unset Func_INI::testChrfile_11n_lan2wlan}
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11n_lan2wlan
    
    # Regsub string
    set testChrfile_11n_lan2wlan2lan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11n_lan2wlan "LAN2WLAN2LAN"]
    
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11n_lan2wlan2lan]
    }
}
proc Func_INI::GenChariotTestFile_11n_wan2lan {} {
    variable verbose
    variable logfile
    variable testChrfile_11n_lan2wlan
    variable testChrfile_11n_wan2lan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11n_lan2wlan] {unset Func_INI::testChrfile_11n_lan2wlan}
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11n_lan2wlan
    # Regsub string    
    set testChrfile_11n_wan2lan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11n_lan2wlan "WAN2LAN"]
    
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11n_wan2lan]
    }
}
proc Func_INI::GenChariotTestFile_11n_wan2wlan {} {
    variable verbose
    variable logfile
    variable testChrfile_11n_lan2wlan
    variable testChrfile_11n_wan2wlan
    
    # Prevent duplicate string
    if [info exist Func_INI::testChrfile_11n_lan2wlan] {unset Func_INI::testChrfile_11n_lan2wlan}
    # Creat a new test filename
    Func_INI::GenChariotTestFile_11n_lan2wlan
    # Regsub string
    set testChrfile_11n_wan2wlan \
            [regsub -all "LAN2WLAN" $Func_INI::testChrfile_11n_lan2wlan "WAN2WLAN"]
    
    if {$verbose == on} {
        Log "info" $logfile [list $testChrfile_11n_wan2wlan]
    }
}
########################################
# Define a simple custom logproc
##########################################
namespace eval Log {
    package require logger
}

# Define a simple custom logproc
proc Log::log_to_file {lvl logfiletxt} {
    # set logfile "mylog.log"
    set msg "\[[clock format [clock seconds] -format "%H:%M:%S %m%d%Y"]\] \
            [lindex $logfiletxt 1]"
    set f [open [lindex $logfiletxt 0] {WRONLY CREAT APPEND}] ;# instead of "a"
    fconfigure $f -encoding utf-8
    puts $f $msg
    close $f
}
################################################################################
#${log}::logproc level
# ${log}::logproc level command
# ${log}::logproc level argname body
# This command comes in three forms - the third, older one is deprecated
# and may be removed from future versions of the logger package.
# The current set version takes one argument, a command to be executed
# when the level is called. The callback command takes on argument,
# the text to be logged. If called only with a valid level logproc returns
# the name of the command currently registered as callback command.
# logproc specifies which command will perform the actual logging for a given level.
# The logger package ships with default commands for all log levels,
# but with logproc it is possible to replace them with custom code.
# This would let you send your logs over the network, to a database, or anything else.
################################################################################
proc Log::tofile {level strfilename strtext} {
    # Initialize the logger
    set log [logger::init global]
    
    # Install the logproc for all levels
    foreach lvl [logger::levels] {
        interp alias {} log_to_file_$lvl {} Log::log_to_file $lvl
        ${log}::logproc $lvl log_to_file_$lvl
    }
    
    ${log}::$level [list $strfilename $strtext]
    
    return true
}

proc Log::parray {a {pattern *}} {
    upvar 1 $a array
    if ![array exists array] {
        error "\"$a\" isn't an array"
    }
    set maxl 0
    foreach name [lsort [array names array $pattern]] {
        if {[string length $name] > $maxl} {
            set maxl [string length $name]
        }
    }
    set maxl [expr {$maxl + [string length $a] + 2}]
    foreach name [lsort [array names array $pattern]] {
        set nameString [format %s(%s) $a $name]
        puts stdout [format "%-*s = %s" $maxl $nameString $array($name)]
    }
}
proc Log::LogList_level {level filename list_msg} {
    set path_logfile [file join ".." "log" $filename]
    
    foreach temp $list_msg {
        set strmsg "$temp"
        Log::tofile $level $path_logfile $strmsg
    }
}

proc Log::LogOut {str_out path_logfile} {
    
    #set path_logfile [file join ".." "log" $logfname]
    # set clk [clock format [clock seconds] -format "%b%d%H%M%S%Y"]
    # append str_out;# "  ";append Str_Out $clk
    
    set rnewinfd [open $path_logfile a]
    puts $rnewinfd $str_out
    flush $rnewinfd;close $rnewinfd
}

namespace eval Func_CSV {
    package require csv
    package require struct
    
    variable verbose off
    variable logfile "../log/csvfile.log"
    
    variable list_noisepathfname_ChNum {}
    variable str_noisepathfname_CO ""
    variable str_noisepathfname_CPE ""
    
    variable LoopLen
    variable BTLen
    variable TestProfile ""
    variable sepChar ","
    variable str_testplan_table ""
    variable LoopType ""
}

proc Func_CSV::Read {list_csvfname} {
    
    variable sepChar
    variable verbose
    variable logfile
    
    if {[llength $list_csvfname] == 0} {
        set list_csvfname -
    }
    
    set stdin 1
    set first 1
    if [info exists m] {m destroy }
    
    # struct::matrix m
    set list_csv {}
    
    foreach f $list_csvfname {
        if {![string compare $f -]} {
            if {!$stdin} {
                puts stderr "Cannot use - (stdin) more than once"
                exit -1
            }
            set in stdin; set stdin 0
        } else {
            set in [open $f r]
        };#if {![string compare $f -]}
        
        if {$first} {
            if {$verbose == on} {
                Log "info" $logfile [list "CSV File= $f"]
            }
            
            while {[eof $in] != 1} {
                if {[gets $in line] > 0} {
                    switch -regexp $line  {
                        {^(#|;)} {
                            continue
                        }
                        {([0-9]|[0-9][0-9]|[0-9][0-9][0-9]),} {
                            set list_data [::csv::split $line $sepChar]
                        }
                        {([0-9][0-9][0-9][0-9]),} {
                            set list_data [::csv::split $line $sepChar]
                        }
                        default {
                            set list_data [::csv::split $line $sepChar]
                        }
                    };#switch -regexp $linr
                    # m add columns [llength $list_data]
                    # m add row $list_data
                    lappend list_csv $list_data
                };#if {[gets $in line] > 0}
                
            };#while {[eof $in] != 1}
        };#if {$first}
        
        # csv::read2matrix $in m $sepChar
        
        if {[string compare $f -]} {
            close $in
        }
    };#foreach f $list_csvfname
    
    return $list_csv
}

proc Func_CSV::Log {level filename list_msg} {
    foreach temp $list_msg {
        set msg "$temp"
        Log::tofile $level $filename $msg
    }
}