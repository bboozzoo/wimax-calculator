#!/usr/bin/env python

from wimax import *
o = OFDM(OFDM.BW_7_MHz, OFDM.CP_1_16)

print o.get_n()
print o.get_Fs()
print o.get_subcarrier_spacing()
