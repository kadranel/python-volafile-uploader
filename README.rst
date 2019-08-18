=====================
Python Volafile Uploader
=====================

Lightweight commandline interface for uploading to volafile.org rooms via volapi_. (Currently the uploader is working on volapi 5.17.0)

.. _volapi: https://github.com/volafiled/python-volapi


Installation
------------

0) What do you need?
  a) Python 3.7
  b) pip
1) How to install
  a) Download the newest release of the downloader at https://github.com/kadranel/python-volafile-uploader/archive/1.0.2.zip or git clone this repository.
  b) Unzip and enter the folder with you favourite shell, then type:
::

    pip3 install -r requirements.txt

2) Edit the config.py to enter a username/password combination that should be used everytime unless specified in the command.


Start the uploader
------------
::

    python3 uploader.py -r ROOMID -p PASSWORD[OPTIONAL] -u VOLAFILE_USER[OPTIONAL] -up VOLAFILE_USER_PASSWORD[OPTIONAL] -f FILES

a) ROOMID: https://volafile.org/r/ROOMID
b) PASSWORD: The room password if it exists
c) VOLAFILE_USER: Overwrite for VOLAFILE_USER in config.py
d) VOLAFILE_USER_PASSWORD: Overwrite for VOLAFILE_USER_PASSWORD in config.py
e) FILES: Files/Folders to upload. Multiple files/folders can be added here at once, by simply appending them with a " " inbetween. 

Example: You want to upload /home/user/some_file.jpg to https://volafile.org/r/n7yc3pgw
In this case the userdata from config.py will be used, unless none is specified. The uploader will upload as "volapi" in that case.
::

    python3 uploader.py -r n7yc3pgw -f /home/user/some_file.jpg

Example: You want to upload several files/folders of files to https://volafile.org/r/gentoomen
In this case the userdata in config.py will be overwritten.
::

    python3 uploader.py -r gentoomen -u avoss -up 'ArTiCle13!' -f /home/user/some_file.jpg relativepath.mp4 '/folder/path with spaces/'


Other
------------
If you have any issues/questions just post a new issue. Otherwise feel free to share, improve, use and make it your own.
For more examples of how to use the python-volapi and what you can do with it you can look at my python-volafile-downloader_.

.. _python-volafile-downloader: https://github.com/kadranel/python-volafile-downloader
