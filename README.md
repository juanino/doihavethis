# doihavethis
Compare multi-level directory structure of pictures to some pile of pictures or videos you just found on a disk.

# How it works
* get python3 for your platform (tested with python 3.4.3)
* git clone the repo
* copy sampleconfig.py to doihavethisconfig.py
* edit master_dir in your config with the top of your photo tree directory
* edit questionable_dir in your config with the location of some files in questions to check
* run ./doihavethis.py
* the output of the script will note "You should preserve" for files in the questionable directory
   that it can't find matching md5sum's for in the master. (They must not exist or are different/corrupt).
* all useful output goes to the log file configured in the tunables section as log_file
* stdout prints -D- when it finds a directory or "F" when it's working on a hash for a file and the resulting comparison data (which is also in the info log)

# Some issues
* I'm lazy. the md5sum code doesn't buffer, so it will use a ridiculous amount of memory if you have a big file
* the md5sum of the master and questionable directories are not stored anywhere. it's slow since it calculates them every time. fine by me.
* the python dict is in memory for both md5sum (master and questionable) so it can take up a lot of memory
* it only works against one master dir. if you have 2 libraries you need to run it twice for now

# Why did i do this
Mostly because I seem to rewrite variations of this all the time and i can't find my code.
This way I'm documenting it for myself, my friends and any other shmuck who has to combine a bunch of old disks, drives, sd cards, whatever.
Just copy all your files into a working dir and point the questionable dir at it and your master at the location of all your other photos.
As drives got bigger, it makes no sense to have bunches of disks laying around.

Also, it is handy if you are not sure which files you pulled off an SD card, or if you happen to (like in my case) blow away or corrupt an SD card
and use the wonderful photorec and testdisk to recover the files off the chip, but have no idea which files you already downloaded since recovery
pulls every non-clobbered file off that chip, even if you meant to delete it previously.

# links
* [Tool for recovering photos](https://www.cgsecurity.org/wiki/PhotoRec_Step_By_Step)
* [Using config files in python](https://martin-thoma.com/configuration-files-in-python)
