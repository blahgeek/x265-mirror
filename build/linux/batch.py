#!/usr/bin/env python
import os
import sys
import subprocess

tsfolder = os.getenv('HEVC_TESTSEQ_FOLDER', '/testsequences')
limit = os.getenv('HEVC_TESTSEQ_COUNT', '16')
saverecon = os.getenv('HEVC_SAVE_RECON', '0')

seq = ['BQMall_832x480_60.y4m',
'BQSquare_416x240_60.y4m',
'BQTerrace_1920x1080_60.y4m',
'BasketballDrillText_832x480_50.y4m',
'BasketballDrill_832x480_50.y4m',
'BasketballDrive_1920x1080_50.y4m',
'BasketballPass_416x240_50.y4m',
'BlowingBubbles_416x240_50.y4m',
'Cactus_1920x1080_50.y4m',
'ChinaSpeed_1024x768_30.y4m',
'Flowervase_416x240_30.y4m',
'Flowervase_832x480_30.y4m',
'FourPeople_1280x720_60.y4m',
'Johnny_1280x720_60.y4m',
'Keiba_416x240_30.y4m',
'Keiba_832x480_30.y4m',
'Kimono1_1920x1080_24.y4m',
'KristenAndSara_1280x720_60.y4m',
'Mobisode2_416x240_30.y4m',
'Mobisode2_832x480_30.y4m',
'ParkScene_1920x1080_24.y4m',
'PartyScene_832x480_50.y4m',
'PeopleOnStreet_2560x1600_30_crop.y4m',
'RaceHorses_416x240_30.y4m',
'RaceHorses_832x480_30.y4m',
'SlideEditing_1280x720_30.y4m',
'SlideShow_1280x720_20.y4m',
'Tennis_1920x1080_24.y4m',
'Traffic_2560x1600_30_crop.y4m',
'vidyo1_720p_60.y4m',
'vidyo3_720p_60.y4m',
'vidyo4_720p_60.y4m']

seq = seq[:int(limit)]

fullpath = [os.path.join(tsfolder, f) for f in seq]
for f in fullpath:
    if not os.path.exists(f):
        print f, 'missing'
        break
else:
    print 'All test sequences found'

print 'Running...'
procs = []
for i, path in enumerate(fullpath):
    base, ext = os.path.splitext(seq[i])
    cmdline = ['./x265-cli', '-c', '../../cfg/encoder_I_15P.cfg',
               '-i', path, '-b', base + '.hevc']
    if saverecon in ('1', 'Y'):
        cmdline.append('-o')
        cmdline.append(base + '_recon.y4m')
    else:
        cmdline.append('-o')
        cmdline.append('')
    cmdline += sys.argv[1:]
    procs.append(subprocess.Popen(cmdline, shell=False,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE))

fp = open('batchrun-log.txt', 'w')
fp.write('# generated by ' + ' '.join(sys.argv) + '\n\n')
for proc in procs:
    out, err = proc.communicate()
    fp.write('# stdout\n')
    fp.write(out)
    fp.write('# stderr\n')
    fp.write(err)
fp.close();
print 'Run completed, see batchrun-log.txt'
