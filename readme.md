
# Problem 

https://www.cowin.gov.in/home provide lot of info, from which checking available slots is difficult.
So this script just check available slots across districts and beep a sound if available.

# Setup Guide

* `pip3 install -r requirements.txt`

* Change districtIds info, it's hard coded for Bangalore regions

* Run `python3 cowin_checker.py`

* You can run the script using linux watch utility like :
  
```
watch -n 60 -b python3 cowin_checker.py
```

Above command will run every minute and alert you if available, 
also it prints details of available vaccination centre's 

## How to get District ID

1. Use `GET` https://cdn-api.co-vin.in/api/v2/admin/location/states to get state id

2. The use `GET` https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id} 
   to get district info 