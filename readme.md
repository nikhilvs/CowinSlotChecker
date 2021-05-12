
# Problem 

https://www.cowin.gov.in/home provide lot of info, from which checking available slots is difficult.
So this script just check available slots across districts and beep a sound if available.

# Setup Guide

## 1. pip3 install -r requirements.txt

## 2. Change districtIds info, it's hard coded for Bangalore regions

## 3. Run python3 cowin_checker.py

## 4. Put this in linux watch command like
    `watch -n 60 -b python3 cowin_checker.py`
