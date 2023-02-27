all:
	buildozer android debug deploy
run:
	buildozer android run logcat

connect:
	adb connect 192.168.50.134:6666
