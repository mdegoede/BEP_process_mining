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

jre8\bin\java -Xmx6G -XX:MaxPermSize=256m -Djava.system.class.loader=org.processmining.framework.util.ProMClassLoader -classpath "%X%" -XX:+UseCompressedOops -Djava.library.path=.//lib -Djava.util.Arrays.useLegacyMergeSort=true org.processmining.contexts.uitopia.UI

set X=
