################################################################################
# May012019 Initailization.
# May122019 for Chariot thruput test.
# May182019 from Test_GUI_02.tcl
################################################################################
package require Tcl 8.4
package require Tk 8.4
package require tile
package require Tktable

set currpath [file dirname [file normalize [info script]]];#[file dirname [info script]]
set lib_path [regsub -all "test" $currpath "lib"];#[file join  ".." "lib"]
set log_path  [regsub -all "test" $currpath "logs"]
lappend auto_path $lib_path
source "$lib_path/API_Misc.tcl"
source "$lib_path/API_GUI.tcl"

set Func_INI::currPath $currpath
set Func_INI::log_Path $log_path
set Func_INI::lib_Path $lib_path
#set inifile [file join $Func_INI::currPath setup.ini]
set inifile [file join $Func_INI::lib_Path "chariot_config_ini" "setup.ini"]
################################################################################
# Get INI file paramter
################################################################################
set Func_INI::verbose on;#on off
set Func_INI::logfile [file join $log_path inifile.log]

Func_INI::_GetChariot_Param $inifile
Func_INI::_GetDUT $inifile
Func_INI::_GetTopologyIP $inifile
Func_INI::_GetWLAN_ClientModelName $inifile
#Func_INI::_GetCriteria $inifile

# source Chariot related API
set path_chariot [dict get $Func_INI::dict_Chariot_Param "chariot_path"];#get chariot directory
lappend auto_path $path_chariot
#package require ChariotExt;#10/13/2019
source "$lib_path/API_Chariot.tcl"

set Func_Chariot::verbose on;#on off
set Func_Chariot::logfile [file join $log_path chariot.log]
#set Func_Chariot::reTest [dict get $Func_INI::dict_Chariot_Param "retest"]
set Func_Chariot::inifile $inifile;#Otc132019 bug

# Set chariot related parameters for testing
#set TestGUI::maxretry $Func_Chariot::reTest

set TestGUI::verbose on
set TestGUI::log_path $Func_INI::log_Path
# set timeout interval unit:second
#set TestGUI::timeout_interval    1

set TestGUI::logfile $Func_INI::logfile
################################################################################
# GUI Procedure
################################################################################
set config(elide,time) 0
set config(elide,level) 0
foreach level [logger::levels] {
    set config(elide,$level) 0
}
#
# Create a simple logger with the servicename 'global'
#
#
proc createLogger {} {
    global mylogger
    set mylogger [logger::init global]
    
    # loggers logproc takes just one arg, so curry
    # our proc with the loglevel and use an alias
    foreach level [logger::levels] {
        interp alias {} insertLogLine_$level {} insertLogLine $level
        ${mylogger}::logproc $level insertLogLine_$level
    }
}

# Put the logmessage to the logger system
proc sendMessageToLog {level} {
    ${::mylogger}::$level $::logmessage
}

################################################################################
# https://www.doulos.com/knowhow/tcltk/examples/buttons/
################################################################################
destroy  .buttons
toplevel .buttons
wm title .buttons "Function Buttons"
set count 0

proc add_frame {title} {
    
    global frame count
    set frame .buttons.frame$count
    frame $frame -border 2 -relief groove
    label $frame.label -text $title
    
    pack  $frame       -side top -padx 1 -pady 1 -anchor n -fill both
    pack  $frame.label -side top  -padx 2 -pady 2
    
    incr count
}

proc add_button {title command} {
    global frame count
    ttk::style configure TButton -width 18 -height 18 -font "serif 18"
    ttk::button $frame.$count -text $title -command $command
    
    pack   $frame.$count -side left -pady 1 -padx 1 -fill x
    
    incr count
}

proc createGUI {str_title } {
    global mylogger
    global logwidget
    
    wm title . $str_title
    
    # The output window
    labelframe .log -text "Output Message"
    text .log.text -yscrollcommand [list .log.yscroll set] -wrap none
    set logwidget .log.text
    scrollbar .log.yscroll -orient vertical -command [list $logwidget yview]
    frame .log.buttons
    frame .log.buttons.elide
    
    grid .log.text .log.yscroll -sticky nsew
    grid configure .log.yscroll -sticky nws
    grid .log.buttons.elide -sticky ew
    grid .log.buttons -columnspan 200 -sticky ew
    grid .log -sticky ew;#news
    grid columnconfigure . 0 -weight 1
    grid rowconfigure . 0 -weight 0
    grid rowconfigure . 1 -weight 1
    grid columnconfigure .log 0 -weight 1
    grid columnconfigure .log 1 -weight 0
    grid rowconfigure .log 0 -weight 1
    
    ################################################################################
    # Add Function button widget     
    ################################################################################
    add_frame  "Exit"
    add_button "Exit"   {exit}
    
    add_frame  "11ac Test"
    add_button "LAN--->WLAN"   [list Func_Chariot::RunRoutine_11ac_lan2wlan]
    add_button "LAN<---WLAN"   [list Func_Chariot::RunRoutine_11ac_wlan2lan]
    add_button "LAN<--->WLAN"  [list Func_Chariot::RunRoutine_11ac_lan2wlan2lan]
    add_button  "11ac All Test" {Func_Chariot::RunRoutine_11ac_lan2wlan; \
                                 Func_Chariot::RunRoutine_11ac_wlan2lan; \
                                 Func_Chariot::RunRoutine_11ac_lan2wlan2lan}
                                
    add_frame  "11n Test"
    add_button "LAN--->WLAN"   [list Func_Chariot::RunRoutine_11n_lan2wlan]
    add_button "LAN<---WLAN"   [list Func_Chariot::RunRoutine_11n_wlan2lan]
    add_button "LAN<--->WLAN"  [list Func_Chariot::RunRoutine_11n_lan2wlan2lan]
    add_button "11n All Test" {Func_Chariot::RunRoutine_11n_lan2wlan; \
                                Func_Chariot::RunRoutine_11n_wlan2lan; \
                                Func_Chariot::RunRoutine_11n_lan2wlan2lan}
            
    # Now we create some fonts
    # a fixed font for the first two columns, so they stay nicely lined up
    # a proportional font for the message as it is probably better to read
    #
    font create logger::timefont -family {Courier} -size 10;#8
    font create logger::levelfont -family {Courier} -size 10;#8
    font create logger::msgfont -family {Arial} -size 12;#10
    $logwidget tag configure logger::time -font logger::timefont
    $logwidget tag configure logger::level -font logger::levelfont
    $logwidget tag configure logger::message -font logger::msgfont
    
    # Now we create some colors for the levels, so our messages appear in different colors
    # color<->levels {debug,info,notice,warn,error,critical }
    foreach level [logger::levels] color {darkgrey lightgrey lightgreen lightblue red orange} {
        $logwidget tag configure logger::$level -background $color
    }
    
    # Disable the widget, so it is read only
    $logwidget configure -state disabled
    
}
proc insertLogLine {level txt} {
    global logwidget
    
    $logwidget configure -state normal
    $logwidget insert end "<[clock format [clock seconds] -format "%H:%M:%S"]> " \
            [list logger::time logger::$level] \
            $txt\n [list logger::message logger::$level]
    
    $logwidget yview moveto 1;update
    $logwidget configure -state disabled
}

proc GUIRun {str_title} {
    createLogger
    createGUI $str_title
}

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
################################################################################
append  str_title $pref(appname) " " Version ":" $VERSION
        
GUIRun $str_title