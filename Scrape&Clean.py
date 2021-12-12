# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 17:01:45 2020
Modified on Fri Jul 9 15:10:00 2021

@author: Sven Veismann
Modified by : Mudassir Waheed
"""

import re
import urllib.request
import bs4
import io
import csv
import os
import time
import html2text
from shutil import move

# Function to get company information and header
def parse(file1):
    hand = open(file1)
    identity = ""
    for line in hand:
        line = line.strip()
        if re.findall('^COMPANY CONFORMED NAME:', line):
            k = line.find(':')
            comnam = line[k + 1:]
            comnam = comnam.strip()
            identity = '<HEADER>\nCOMPANY NAME: ' + str(comnam) + '\n'
            break

    hand = open(file1)
    for line in hand:
        line = line.strip()
        if re.findall('^CENTRAL INDEX KEY:', line):
            k = line.find(':')
            cik = line[k + 1:]
            cik = cik.strip()
            identity = identity + 'CIK: ' + str(cik) + '\n'
            break

    hand = open(file1)
    for line in hand:
        line = line.strip()
        if re.findall('^STANDARD INDUSTRIAL CLASSIFICATION:', line):
            k = line.find(':')
            sic = line[k + 1:]
            sic = sic.strip()
            siccode = []
            for s in sic:
                if s.isdigit():
                    siccode.append(s)
                    # print siccode
            identity = identity + 'SIC: ' + ''.join(siccode) + '\n'
            break

    hand = open(file1)
    for line in hand:
        line = line.strip()
        if re.findall('^CONFORMED SUBMISSION TYPE:', line):
            k = line.find(':')
            subtype = line[k + 1:]
            subtype = subtype.strip()
            # print subtype
            identity = identity + 'FORM TYPE: ' + str(subtype) + '\n'
            break

    hand = open(file1)
    for line in hand:
        line = line.strip()
        if re.findall('^CONFORMED PERIOD OF REPORT:', line):
            k = line.find(':')
            cper = line[k + 1:]
            cper = cper.strip()
            # print cper
            identity = identity + 'REPORT PERIOD END DATE: ' + str(cper) + '\n'
            break

    hand = open(file1)
    for line in hand:
        line = line.strip()
        if re.findall('^FILED AS OF DATE:', line):
            k = line.find(':')
            fdate = line[k + 1:]
            fdate = fdate.strip()
            # print fdate
            identity = identity + 'FILE DATE: ' + str(fdate) + '\n' + '</HEADER>\n'
            break
    return identity

# SETUP
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# SETUP
# Please set the folder where you would like to have the files saved.
filepath = "C:\Users\Mudassir\Desktop\url scrapper"

# What is the name of the download list?
# Format of the csv file needs to be:
# CIK,Company Name,Form Type,Date Filed,Filename,fyr,yearoffiling,fyear,gvkey,datadate
download = "urls.txt"

# Debbuging mode
deb_mode = False

file_counter = 0

os.chdir(filepath)
temp = "temp.txt"
h=html2text.HTML2Text()
# HERE STARTS THE ACTUAL PROGRAM
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

with open(download, 'r') as txtfile:
    reader = csv.reader(txtfile, delimiter=',')


    for line in reader:
            
        # Get information on current report to be downloaded
        print("Current report is: {}".format(line))
        CIKNUM = line[0].strip()
        gvkey = line[8].strip()
        fyear = line[7].strip()
        FileDate = line[3].strip()
        FileName = FileDate + "_" + str(line[0].strip()) + ".txt"
        url = 'https://www.sec.gov/Archives/' + line[4].strip()

        # Download the file
        while True:
            try:
                print("Trying")
                urllib.request.urlretrieve(url.strip(), temp)
                break
            except:
                print("Waiting")
                time.sleep(10)

        # Create the header
        new_header = parse(temp)

        move('temp.txt', 'temp.html')
        with open('temp.html') as f:
            x=f.read()
            soup = bs4.BeautifulSoup(x,'lxml')
            h.ignore_images=True
            h.ignore_links=True
            h.bypass_tables=True
            h.ignore_tables=True
            text=h.handle(soup.get_text())
            text = re.sub("(?<=[<])([\S\s]*)(?=[>])", '', text)
            text = re.sub("(?<=begin 644)([\S\s]*)(?=end)", '', text)
            text = re.sub("(?<=begin 644)([\S\s]*)(?=[\S\s]*)", '', text)
        # FINALIZATION
        #   -----------------------------------------------------------------------------------------------------------
        #   -----------------------------------------------------------------------------------------------------------
        #   -----------------------------------------------------------------------------------------------------------

        # Create final filename
        out_file = str(gvkey) + "_" + FileDate + "_" + fyear + "_" + str(CIKNUM) + "_" + "full.txt"
        out_file_formated = str(gvkey) + "_" + FileDate + "_" + fyear + "_" + str(CIKNUM) + "_" + "full_formated.txt"

        # Save file
        with io.open(out_file, 'w', encoding="utf-8") as out:
            out.write(new_header)
            out.write(text) 