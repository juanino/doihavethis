# doihavethis
Compare multi-level directory structure of pictures to some pile of pictures or videos you just found on a disk.

# How it works
1. git clone the repo
2. edit master_dir with the top of your photo tree directory
3. edit questionable_dir with the location of some files in questions to check
4. run ./doihavethis.py
5. the output of the script will note "You should preserve" for files in the questionable directory
   that it can't find matching md5sum's for in the master. (They must not exist or are differnent/corrupt).

# Some issues
1. I'm lazy. the md5sum code doesn't buffer, so it will use a ridiculous amount of memory if you have a big file
2. the md5sum of the master and questionable directories are not stored anywhere. it's slow since it calculates them every time. fine by me.
3. the python dict is in memory for both md5sum (master and questionable) so it can take up a lot of memory
4. it likely only works in python 2, i'm too lazy to fix the print statements

# Why did i do this
Mostly because I seem to rewrite variations of this all the time and i can't find my code.
This way I'm documenting it for myself, my friends and any other shmuck who has to combine a bunch of old disks, drives, sd cards, whatever.
Just copy all your files into a working dir and point the questionable dir at it and your master at the location of all your other photos.
As drives got bigger, it makes no sense to have bunches of disks laying around.

Also, it is handy if you are not sure which files you pulled off an SD card, or if you happen to (like in my case) blow away or corrupt an SD card
and use the wonderful photorec and testdisk to recover the files off the chip, but have no idea which files you already downloaded since recovery
pulls every non-clobbered file off that chip, even if you meant to delete it previously.

# links
https://www.cgsecurity.org/wiki/PhotoRec_Step_By_Step
