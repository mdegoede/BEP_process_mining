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

jre8\bin\java -classpath "%X%" -Djava.library.path=.//lib -Xmx1G org.processmining.contexts.uitopia.packagemanager.PMFrame

set X=



