all:
	scons -Q --jobs=4

clean:
	scons -Q -c

doxy:
	scons -Q -c doc
	scons -Q doc

check:
	scons -Q check
