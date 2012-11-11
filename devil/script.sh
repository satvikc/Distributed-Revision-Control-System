#//script.sh, uses script and scriptreplay to record and playback virtual terminal.
#//Copyright (C) 2007  Hean Kuan Ong ( mysurface[at]gmail.com )
#//
#//This program is free software; you can redistribute it and/or
#//modify it under the terms of the GNU General Public License
#//as published by the Free Software Foundation; either version 2
#//of the License, or (at your option) any later version.
#//
#//This program is distributed in the hope that it will be useful,
#//but WITHOUT ANY WARRANTY; without even the implied warranty of
#//MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#//GNU General Public License for more details.
#//
#//You should have received a copy of the GNU General Public License
#//along with this program; if not, write to the Free Software
#//Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#!/bin/bash

SCRIPT=`which script`
SCRIPTREPLAY=`which scriptreplay`

if [ ! -n $SCRIPT ]
then
    echo "script is not installed, please install script.";
    exit
fi

if [ ! -n $SCRIPTREPLAY ]
then
    echo "scriptreplay is not installed, please install scriptreplay.";
    exit
fi

if [ "$1" == "-r" ]
then
    if [ ! -n $2 ]
    then
        read -p "what is your session name? " NAME
    else
        NAME=$2
    fi
    echo "script recording will start soon, type exit to end the recording"
    script -t 2>$NAME.timing -a $NAME.session;
    tar czf $NAME $NAME.timing $NAME.session
    rm $NAME.timing $NAME.session
    echo "run $0 -p and specified $NAME to play"
elif [ "$1" == "-p" ]
then
    if [ ! -n "$2" ]
    then
        read -p "What file you wanna play? " NAME
    else
        NAME=$2
    fi
    if [ -e $NAME ]
    then
        tar -zxf $NAME
        scriptreplay $NAME.timing $NAME.session
        rm $NAME.timing $NAME.session
        echo "that is the end of the script play."
    else
        echo "the file $NAME doesn't exist."
    fi
else
    echo `basename $0` " record and playback terminal session."
    echo "usage: "
    echo `basename $0` " -r to record"
    echo `basename $0` " -p to play"
fi
