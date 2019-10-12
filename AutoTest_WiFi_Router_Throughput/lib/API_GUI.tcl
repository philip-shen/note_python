################################################################################
# Ttk MessageBox
# wrapper of ttk::dialog for using it like tk_messageBox
################################################################################
namespace eval Message {} {;#<<<
    variable retval {}
}

proc Message::msgset {btn} {
    variable retval $btn
}

# return selected button name
proc Message::show {args} {
    variable retval
    if [winfo exists .ttkmessage] {
        destroy .ttkmessage
    }
    eval ttk::dialog .ttkmessage $args -command {Message::msgset}
    wm withdraw .ttkmessage
    lower .ttkmessage .
    update
    if {[tk windowingsystem] eq "x11"} {
        ::Util::moveCenter .ttkmessage
    } else {
        ::Util::moveCenter .ttkmessage \
                [list [winfo reqwidth .ttkmessage] [winfo reqheight .ttkmessage]]
    }
    
    Util::ngrab set .ttkmessage
    wm transient .ttkmessage .
    wm deiconify .ttkmessage
    focus -force .ttkmessage
    tkwait window .ttkmessage
    Util::ngrab release
    return $retval
}
################################################################################
# -icon
# Specifies an icon to display. Must be one of the following: error, info, question or warning.
#
# -type
# Specifies a set of buttons to be displayed. The following values are possible:
# abortretryignore
# Displays three buttons whose symbolic names are abort, retry and ignore.
# ok
#     Displays one button whose symbolic name is ok.
# okcancel
#             Displays two buttons whose symbolic names are ok and cancel.
# retrycancel
#              Displays two buttons whose symbolic names are retry and cancel.
# yesno
#      Displays two buttons whose symbolic names are yes and no.
# yesnocancel
#             Displays three buttons whose symbolic names are yes, no and cancel.
# user
#     Displays buttons of -buttons option.
################################################################################
proc Message::popup {list_args} {
    set icon_opt    [lindex $list_args 0]
    set appname    [lindex $list_args 1]
    set version    [lindex $list_args 2]
    set strmsg    [lindex $list_args 3]
    set strdetail    [lindex $list_args 4]
    
    show -buttons ok -icon $icon_opt -title "$appname  Version:$version\n" \
            -message $strmsg -detail $strdetail -type okcancel
}
proc Message::popup_buttopt {list_args } {
    set icon_opt    [lindex $list_args 0]
    set appname    [lindex $list_args 1]
    set version    [lindex $list_args 2]
    set strmsg    [lindex $list_args 3]
    set strdetail    [lindex $list_args 4]
    set str_buttopt   [lindex $list_args 5]
    #abortretryignore; ok; okcancel;retrycancel;yesno;yesnocancel;
    set retval [show -buttons $str_buttopt -icon $icon_opt -title "$appname  Version:$version\n" \
            -message $strmsg -detail $strdetail -type yesnocancel -default yes]
    
    return $retval
}
namespace eval Util {
    variable grabStack [list]
}
proc Util::moveCenter {widget {size {}}} {
    set sw [winfo vrootwidth $widget]
    set sh [winfo vrootheight $widget]
    if {[llength $size] == 0} {
        update idletask
        set w [winfo width $widget]
        set h [winfo height $widget]
    } else {
        set w [lindex $size 0]
        set h [lindex $size 1]
    }
    wm geometry $widget +[expr {($sw-$w)/2}]+[expr {($sh-$h)/2}]
}
# Nested grab command
# ngrab set .w   : stack window and grab it.
# ngrab release  : release a top of stack window.
proc Util::ngrab {command {w {}}} {
    variable grabStack
    switch -exact -- $command {
        set {
            if {$w eq {}} { error "wrong args : ngrab command window" }
            grab set $w
            focus -force $w
            lappend grabStack $w
        }
        release {
            set cur [lindex $grabStack end]
            set grabStack [lrange $grabStack 0 "end-1"]
            if {[llength $grabStack] == 0} {
                grab release $cur
                return
            }
            grab set [lindex $grabStack end]
        }
    }
}
namespace eval Statusbar {;#<<<
    variable var
    array set var {
        encoding {}
        version {}
        time {}
        row {}
    }
}
proc Statusbar::Statusbar {} {
    ttk::frame .statusbar
    ttk::label .statusbar.enc -textvariable [namespace current]::var(encoding)
    ttk::label .statusbar.ver -textvariable [namespace current]::var(version)
    ttk::label .statusbar.time -textvariable [namespace current]::var(time)
    ttk::label .statusbar.row -textvariable [namespace current]::var(row)
    ttk::label .statusbar.dummy
    foreach w [winfo children .statusbar] {
        $w configure -takefocus 0 -relief flat -anchor w -padding 0
    }
    foreach n {0 1 2 3} {
        ttk::separator .statusbar.sep$n -orient vertical
    }
    pack .statusbar.ver .statusbar.sep0 .statusbar.enc .statusbar.sep1 \
            -fill y -side left -pady 2 -padx 1
    
    pack .statusbar.time .statusbar.sep2 .statusbar.row .statusbar.sep3 \
            -fill y -side right -pady 2 -padx 1
    
    return .statusbar
}

proc Statusbar::clear {} {
    variable var
    set var(encoding) "Encoding : unknown"
    set var(version) "Version : unknown"
    set var(time) "Time : 0 msec"
    set var(row) "Rows : 0 lines"
}

proc Statusbar::update {} {
    variable var
    set var(encoding) "Encoding : A"
    set var(version) "Version : B"
    set var(time) "Time : C"
    set var(row) "Rows : D"
}

namespace eval TestGUI {} {
    variable verbose off
    variable log_path
    variable logfile
    variable timeout_interval
    variable maxretry
}
proc TestGUI::showinfo {} {
    variable log_path
    variable maxretry
    
    # Read variables from INI file
    set inifile [file join $Func_INI::currPath setup.ini]
    Func_INI::_GetChariot_Param $inifile
    Func_INI::_GetDUT $inifile
    Func_INI::_GetTopologyIP $inifile
    Func_INI::_GetWLAN_ClientModelName $inifile
    Func_INI::_GetCriteria $inifile
    
    # Set chariot related parameters
    set Func_Chariot::pairCount [dict get $Func_INI::dict_Chariot_Param "paircount"]
    set Func_Chariot::reTest [dict get $Func_INI::dict_Chariot_Param "retest"]
    
    # Set chariot related parameters for testing
    set TestGUI::maxretry $Func_Chariot::reTest
    
    set TestGUI::verbose on
    set TestGUI::log_path $Func_INI::log_Path
    # set timeout interval unit:second
    set TestGUI::timeout_interval    1
    
    set TestGUI::logfile $Func_INI::logfile
    # Check Topology Status
    set retval [Func_INI::ChkTopologyalive]
    if {$retval == "false"} {
        set strmsg "********** Please Double Check Topology Status! **********"
        
        insertLogLine critical $strmsg
        return 
    } else  {
        update
    };#if {$retval == "false"}
    
    for {set retry 0} {$retry < $maxretry} {incr retry} {
        # LAN-->WLAN
        ################################################################################
        # Prevent duplicate string
        if [info exist Func_INI::testChrfile_11ac_lan2wlan] {unset Func_INI::testChrfile_11ac_lan2wlan}
        # Setup Chariot test file name
        Func_INI::GenChariotTestFile_11ac_lan2wlan
        
        # Set absoluate path
        if [info exist testChrfile_11ac_lan2wlan] {unset testChrfile_11ac_lan2wlan}
        append testChrfile_11ac_lan2wlan $log_path / $Func_INI::testChrfile_11ac_lan2wlan
        
        set Func_Chariot::testFile $testChrfile_11ac_lan2wlan
        
        # show log header on widget
        insertLogLine info $Func_Chariot::testFile
        
        # Break timer
        TestGUI::Timer
        
        # WLAN-->LAN
        ################################################################################
        
        # Prevent duplicate string
        if [info exist Func_INI::testChrfile_11ac_lan2wan] {unset Func_INI::testChrfile_11ac_lan2wan}
        # Setup Chariot test file name
        Func_INI::GenChariotTestFile_11ac_wlan2lan
        
        # Set absoluate path
        if [info exist testChrfile_11ac_wlan2lan] {unset testChrfile_11ac_wlan2lan}
        append testChrfile_11ac_wlan2lan $log_path / $Func_INI::testChrfile_11ac_wlan2lan
                
        set Func_Chariot::testFile $testChrfile_11ac_wlan2lan
        
        # show log header on widget
        insertLogLine notice $Func_Chariot::testFile
    }
}
proc TestGUI::Timer {} {
    variable verbose
    variable logfile
    variable timeout_interval
    variable maxretry
    
    # set retrytimes 0
    # set strmsg "maxretry=$maxretry; timeout_interval=$timeout_interval; $strinfo"
    # Log::LogList_level "info" $logfile [list $strmsg]
    set retrytimes 1   
    
    # while {1} {
        # incr retrytimes
        ##Check retry times to break
        # if {$retrytimes > $maxretry} { break }
        
        set timeout_duration [expr $timeout_interval * $retrytimes]
        # set strmsg "Waiting $timeout_duration seconds. $strinfo. MaxRetry=$maxretry; \
                # Retrytimes=$retrytimes."
        
        set strmsg "Waiting $timeout_duration seconds."
        
        insertLogLine critical $strmsg
        
        if {$verbose == on} {
            Log::LogList_level "info" $logfile [list $strmsg]
        };#if {$verbose == on}
        
        # Log::LogList_level "info" "$csv_logfname.csv" [list $strmsg]
        
        after [expr $timeout_interval * 1000]; update
        
    # };#while {1}
    
    return true
}