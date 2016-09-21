@echo off
set SCP=c:\bin\PuTTY\pscp.exe

set par=%1
set SRC=mallet%par%.bib
set USER=fmallet
set SERVER=srv-aoste.inria.fr
set REMOTE=/net/servers/www-sop/members/Frederic.Mallet/publis


set TGT=%USER%@%SERVER%:%REMOTE%/20%par%/

echo %SCP% %SRC% %TGT%
%SCP% %SRC% %TGT%
