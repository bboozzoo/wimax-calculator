#!/usr/bin/env python

import wicalc
o = wicalc.OFDM(wicalc.OFDM.BW_7_MHz, wicalc.OFDM.CP_1_16)

print o.get_n()
print o.get_Fs()
print o.get_subcarrier_spacing()
