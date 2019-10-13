################################################################################
# May012019 Initailization.
# May122019 for Chariot thruput test.
# May182019 Adapt from Test_GUI_02.tcl
# Oct122019 Adapt from Test_Chariot_GUI_02.tcl
################################################################################
package require Tcl 8.4
#package require Tk 8.5
#package require tile
#package require Tktable

set currpath [file dirname [file normalize [info script]]];#[file dirname [info script]]
set lib_path [regsub -all "test" $currpath "lib"];#[file join  ".." "lib"]
set log_path  [regsub -all "test" $currpath "logs"]
lappend auto_path $lib_path
source "$lib_path/API_Misc.tcl"
source "$lib_path/API_GUI.tcl"
package require cmdline

################################################################################
# CML parsing Procedure
################################################################################
set parameters {
    {config_ini.arg ""   "Assing configuration INI file."}
    {direction.arg ""   "LAN<-->WAN or LAN-->WAN or LAN<--WAN and all."}
    {moduration.arg ""   "11n or 11ac and 11ax an ."}
    {debug           "Turn on debugging, default=off"}
}

set usage "- A Tcl script to  excute Chairot by cmdline"
array set options [cmdline::getoptions ::argv $parameters $usage]
parray options

set Func_INI::currPath $currpath
set Func_INI::log_Path $log_path
set Func_INI::lib_Path $lib_path
set inifile [file join $Func_INI::lib_Path "chariot_config_ini" $options(config_ini)]
#puts $inifile
################################################################################
# Get INI file paramter
################################################################################
set Func_INI::verbose on;#on off
set Func_INI::logfile [file join $log_path inifile.log]

Func_INI::_GetChariot_Param $inifile
#Func_INI::_GetDUT $inifile
#Func_INI::_GetTopologyIP $inifile
#Func_INI::_GetWLAN_ClientModelName $inifile
#Func_INI::_GetCriteria $inifile


# source Chariot related API
set path_chariot [dict get $Func_INI::dict_Chariot_Param "chariot_path"];#get chariot directory
puts $path_chariot

lappend auto_path $path_chariot
source "$lib_path/API_Chariot.tcl"

set Func_Chariot::verbose on;#on off
set Func_Chariot::logfile [file join $log_path chariot.log]


################################################################################
# https://www.doulos.com/knowhow/tcltk/examples/buttons/
################################################################################

################################################################################
# Start Here
################################################################################
set COPYRIGHT {
    Copyright (c) 2019, 2020 QA,
    This program is free to modify, extend at will.  The author(s)
    provides no warrantees, guarantees or any responsibility for usage.
}
set VERSION "    If you have question, please contact QA Dept."

array set pref [list \
        debug		0 \
        usesession	1 \
        sessionfile	[file join [file normalize $env(HOME)] .tksqlite]\
        appname		"Chariot Thruput Test"  \
        enable_encoding	[lsort -dictionary [encoding names]] \
        recent_file [list] \
        openTypeSqlite	[list {"SQLite Files" {.db .db2 .db3 .sqlite}} {"All Files" *}] \
        openTypeSql		[list {"SQL Files" {.sql}} {"All Files" *}] \
        openTypeText	[list {"Text Files" {.txt .csv .tab .tsv .dat}} {"All Files" *}] \
        ]


################################################################################
# Run Here
# as below
#  £f tclsh85 Test_Chariot_CML.tcl -config_ini ac8260_ch01_wpa2aes_setup.ini -direction lan2wan -moduration 11ac
################################################################################
################################################################################
# add_button "LAN--->WLAN"   [list Func_Chariot::RunRoutine_11ac_lan2wlan]
# add_button "LAN<---WLAN"   [list Func_Chariot::RunRoutine_11ac_wlan2lan]
# add_button "LAN<--->WLAN"  [list Func_Chariot::RunRoutine_11ac_lan2wlan2lan]
# add_button  "11ac All Test" {Func_Chariot::RunRoutine_11ac_lan2wlan; \
#            Func_Chariot::RunRoutine_11ac_wlan2lan; \
#            Func_Chariot::RunRoutine_11ac_lan2wlan2lan}
# 
# add_button "LAN--->WLAN"   [list Func_Chariot::RunRoutine_11n_lan2wlan]
# add_button "LAN<---WLAN"   [list Func_Chariot::RunRoutine_11n_wlan2lan]
# add_button "LAN<--->WLAN"  [list Func_Chariot::RunRoutine_11n_lan2wlan2lan]
# add_button "11n All Test" {Func_Chariot::RunRoutine_11n_lan2wlan; \
#            Func_Chariot::RunRoutine_11n_wlan2lan; \
#            Func_Chariot::RunRoutine_11n_lan2wlan2lan}
################################################################################
if {[string tolower $options(config_ini)] == "11n" } {
    switch -regexp [string tolower $options(direction)] {
        {^lantowlan$} {
            [list Func_Chariot::RunRoutine_11n_lan2wlan]
        }
        {^wlantolan$} {
            [list Func_Chariot::RunRoutine_11n_wlan2lan]
        }
        {^lantowlantolan$} {
            [list Func_Chariot::RunRoutine_11n_lan2wlan2lan]
        }
        {^all$} {
            {Func_Chariot::RunRoutine_11n_lan2wlan; \
             Func_Chariot::RunRoutine_11n_wlan2lan; \
             Func_Chariot::RunRoutine_11n_lan2wlan2lan}
        }
    };#switch
    
} elseif {[string tolower $options(config_ini)] == "11ac" } {
    switch -regexp [string tolower $options(direction)] {
        {^lantowlan$} {
            #[list Func_Chariot::RunRoutine_11ac_lan2wlan]
            Func_Chariot::RunRoutine_11ac_lan2wlan
        }
        {^wlantolan$} {
            #[list Func_Chariot::RunRoutine_11ac_wlan2lan]
            Func_Chariot::RunRoutine_11ac_wlan2lan
        }
        {^lantowlantolan$} {
            #[list Func_Chariot::RunRoutine_11ac_lan2wlan2lan]
            Func_Chariot::RunRoutine_11ac_lan2wlan2lan
        }
        {^all$} {
            {Func_Chariot::RunRoutine_11ad_lan2wlan; \
             Func_Chariot::RunRoutine_11ac_wlan2lan; \
             Func_Chariot::RunRoutine_11ac_lan2wlan2lan}
        }
    };#switch
    
} else {
    
}

