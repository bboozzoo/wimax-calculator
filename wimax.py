#!/usr/bin/end python

import math

def s_to_ms(value_in_s):
    return value_in_s * 1000.0

def s_to_us(value_in_s):
    return value_in_s * 1000000.0

class OFDMError(Exception):
    def __init__(self, what):
        self.__what = what
    def __str__(self):
        return self.__what

class OFDM:
    Nfft = 256
    Nused = 200
    
    BW_1_75_MHz = 1750000
    BW_3_MHz =    3000000
    BW_3_5_MHz =  3500000
    BW_5_5_MHz =  5500000
    BW_7_MHz =    7000000
    BW_10_MHz =  10000000

    CP_1_4 = 1/4.0
    CP_1_8 = 1/8.0
    CP_1_16 = 1/16.0
    CP_1_32 = 1/32.0

    __valid_cp = [CP_1_4, CP_1_8, CP_1_16, CP_1_32]
    __valid_bw = [BW_3_MHz, BW_3_5_MHz, BW_7_MHz]

    def __init__(self, bw, cp):
        self.__bw = bw 
        self.__cp = cp
        self.__validate_bw()
        self.__validate_cp()

        self.__Fs = 0
        self.__subcarrier_spacing = 0
        self.__n = 0

        self.__calc_n()
        self.__calc_Fs()
        self.__calc_subcarrier_spacing()
        self.__calc_symbol_times()

    def __validate_bw(self):
        if not self.__bw in self.__valid_bw:
            raise OFDMError("Invalid BW: %d" % (self.__bw))

    def __validate_cp(self):
        if not self.__cp in self.__valid_cp:
            raise OFDMError("Invalid CP: %d" % (self.__cp))

    def __calc_n(self):
        factors = [(1.75, 8.0/7), \
                   (1.5,  86.0/75), \
                   (1.25, 144.0/125), \
                   (2.75, 316.0/275), \
                   (2.0,  57.0/50)]
        fallback_factor = 8.0/7
        n = fallback_factor

        for f in factors:
            (integer, fraction) = divmod(self.__bw, f[0])
            if (fraction == 0.0):
                n = f[1]
                break
        self.__n = n

    def __calc_Fs(self):
        Fs = math.floor(self.__n * self.__bw / 8000) * 8000
        self.__Fs = Fs
    
    def __calc_subcarrier_spacing(self):
        self.__subcarrier_spacing = self.__Fs / self.Nfft

    def __calc_symbol_times(self):
        self.__symbol_useful_time = 1.0 / self.__subcarrier_spacing
        self.__symbol_cp_time = self.__cp * self.__symbol_useful_time
        self.__symbol_total_time = self.__symbol_useful_time + self.__symbol_cp_time

    def get_Fs(self):
        return self.__Fs

    def get_n(self):
        return self.__n

    def get_subcarrier_spacing(self):
        return self.__subcarrier_spacing

    def get_symbol_time(self):
        return self.__symbol_total_time

    def get_symbol_cp_time(self):
        return self.__symbol_cp_time

    def get_symbol_useful_time(self):
        return self.__symbol_useful_time

    def get_cs(self):
        return 1.0 / self.__Fs

    def get_ps(self):
        return 4.0 / self.__Fs

    def get_symbol_time_in_cs(self):
        return self.__symbol_total_time / self.get_cs()

    def get_symbol_time_in_ps(self):
        return self.__symbol_total_time / self.get_ps()

if __name__ == '__main__':
    pass

