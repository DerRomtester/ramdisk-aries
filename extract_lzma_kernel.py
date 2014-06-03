#!/usr/bin/env python

# Copyright (C) 2014 Pawit Pornkitprasan
#
# Script to extract cpio ramdisk from LZMA compressed kernels
# Tested on galaxysmtd boot.img from CM11

# Config
fileIn = "boot.img"
fileOut = "whole_disk.cpio"

# Code
from subprocess import Popen, PIPE, STDOUT
import struct

def align(x, length):
  return ((x + length - 1) / length) * length

print "Reading zImage..."

zImage = open(fileIn, "rb").read()

lzmaStart = zImage.find('\x5D\0\0\0')

p = Popen(['unlzma'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
piggy = p.communicate(zImage[lzmaStart:])[0]

# Retroactively find end from size
lzmaEnd = zImage.find(struct.pack('<I', len(piggy)))

cpioStart = piggy.find("0707")
cpioEnd = piggy.rfind("00TRAILER!!!\0") + len("00TRAILER!!!\0")

# Align
cpioEnd = align(cpioEnd, 4)

out = open(fileOut, 'w')
out.write(piggy[cpioStart:cpioEnd])
out.close()
