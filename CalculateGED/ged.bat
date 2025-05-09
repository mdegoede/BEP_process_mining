@GOTO start

:add
 @set X=%X%;%1
 @GOTO :eof

:start
@set X=.\dist\ProM-Framework.jar
@set X=%X%;.\dist\ProM-Contexts.jar
@set X=%X%;.\dist\ProM-Models.jar
@set X=%X%;.\dist\ProM-Plugins.jar

@for /R .\lib %%I IN ("*.jar") DO @call :add .\lib\%%~nI.jar

@set IMPORTMODELA=%1.pnml
@set IMPORTMODELB=%2.pnml
@set OUTPUT=%1-%2.ged.log

jre8\bin\java -da -Xmx8G -classpath "%X%" -Djava.library.path=.//lib -Djava.util.Arrays.useLegacyMergeSort=true org.processmining.contexts.cli.CLI -f ged.txt 1> %OUTPUT% 2>&1

set X=
