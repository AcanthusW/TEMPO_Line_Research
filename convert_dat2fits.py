
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt

def load_data(file_name):
    """Loads data from a specified .dat file.
    
    Parameters:
    file_name (str): Path to the .dat file to be loaded.
    
    Returns:
    freq (list): List of frequencies from the file.
    temp (list): List of temperature values from the file.
    """
    freq = []
    temp = []
    
    try:
        with open(file_name, 'r') as infile:
            lines = infile.readlines()
            for line in lines[1:]:
                words = line.split()
                freq.append(float(words[0]))
                temp.append(float(words[1]))
        return freq, temp
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return [], []

def create_fits(freq, temp, output_fits='output.fits'):
    """Creates a FITS file from frequency and temperature data.
    
    Parameters:
    freq (list): List of frequencies.
    temp (list): List of temperature values.
    output_fits (str): Path to save the generated FITS file.
    
    Returns:
    None
    """
    if not freq or not temp:
        print("Empty data. FITS file creation aborted.")
        return

    hdu = fits.PrimaryHDU()
    hdu.data = np.array([[temp]]).T
    hd = hdu.header
    
    # Setting header details
    hd['NAXIS'] = 3
    hd['NAXIS1'] = 1
    hd['NAXIS2'] = 1
    hd['NAXIS3'] = len(freq)
    hd['BUNIT'] = 'T'
    hd['CTYPE1'] = 'RA---CAR'
    hd['CDELT1'] = (1.0e-4, 'degrees')
    hd['CTYPE2'] = 'DEC--CAR'
    hd['CDELT2'] = (1.0e-4, 'degrees')
    hd['CTYPE3'] = 'FREQ'
    hd['CRVAL3'] = freq[len(freq)//2]
    hd['CDELT3'] = freq[1] - freq[0]
    hd['CRPIX3'] = len(freq)//2
    hd['CUNIT3'] = 'Hz'
    hd['RESTFREQ'] = freq[len(freq)//2]

    fits.writeto(output_fits, hdu.data, hd, overwrite=True)
    print(f"FITS file {output_fits} created successfully.")

def main():
    # Change the default path to your own directory
    input_file = 'data/G013.6562-00.5997_SPW_0_p_spec.dat'
    output_file = 'data/G013.6562-00.5997_SPW_0_p_spec.fits'

    print(f"Loading data from: {input_file}")
    freq, temp = load_data(input_file)

    create_fits(freq, temp, output_fits=output_file)

if __name__ == "__main__":
    main()
