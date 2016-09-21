@echo off
set SCP=c:\bin\PuTTY\pscp.exe

set par=%1
set SRC=mallet20%par%.shtml
set USER=fmallet
set SERVER=srv-aoste.inria.fr
set REMOTE=/net/servers/www-sop/members/Frederic.Mallet/publis


set mydate=%date:~-4%%date:~3,2%%date:~0,2%
set name=%mydate%.shtml
set TGT=%USER%@%SERVER%:%REMOTE%/20%par%/%name%

echo %SCP% %SRC% %TGT%
%SCP% %SRC% %TGT%
