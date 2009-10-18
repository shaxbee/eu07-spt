To run a very draft edition of Scenery Editor you need to install:

* Python 2.5
* wxPython 2.8.9
* PyYAML 3.08

To run the editor:

cd src
python Application.py


Unit tests:
------------
You need all previous dependencies plus:

* Nose 0.11.1

Tu run test file:
1) export env. variable PYTHONPATH with <SVN_ROOT>/applications/sptEditor/src
2) go to test/ directory and run python t_xxx.py

This will be changed in near future - unit tests will be run from SConscript.

