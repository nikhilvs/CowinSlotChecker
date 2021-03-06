#!/usr/bin/env python3

import simpleaudio as sa
import json
import argparse
import requests
from datetime import datetime
from datetime import timedelta

districtIds = [
    276,  # Bangalore Rural
    265,  # Bangalore Urban
    294  # BBMP

]

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}"

payload = {}
headers = {
    'authority': 'cdn-api.co-vin.in',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'accept': 'application/json, text/plain, */*',
    'dnt': '1',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'origin': 'https://www.cowin.gov.in',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.cowin.gov.in/',
    'accept-language': 'en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,ml-IN;q=0.6,ml;q=0.5,en-GB;q=0.4,en-US;q=0.3'
}


def check_slots_by_district(district_ids, options) -> object:
    available_slots = []
    for districtId in district_ids:
        today = datetime.now().strftime("%d-%m-%Y")
        next_week = (datetime.now() + timedelta(days=7)).strftime("%d-%m-%Y")
        fort_night = (datetime.now() + timedelta(days=11)).strftime("%d-%m-%Y")
        for date_str in [today, next_week, fort_night]:
            request_url = url.format(districtId, date_str)
            response = requests.request("GET", request_url, headers=headers, data=payload)
            if not response.ok:
                print("Issue: {}".format(response.text))
                return available_slots
            json_data = response.json()
            if options.debug:
                print(f'centers count: {len(json_data["centers"])}')
            for center in json_data["centers"]:
                for session in center["sessions"]:
                    if session["available_capacity"] > 0:
                        data = {
                            "center_id": center["center_id"],
                            "name": center["name"],
                            "address": center["address"],
                            "state_name": center["state_name"],
                            "district_name": center["district_name"],
                            "block_name": center["block_name"],
                            "pincode": center["pincode"],
                            "lat": center["lat"],
                            "long": center["long"],
                            "from": center["from"],
                            "to": center["to"],
                            "fee_type": center["fee_type"],
                            "session": session
                        }
                        # print(json.dumps(data, indent=4, sort_keys=True))
                        if options.debug or filter_user_args(options, session):
                            available_slots.append(data)

    return available_slots


def filter_user_args(options, session):
    return ((options.age18 and session["min_age_limit"] == 18) or
            (options.age45 and session["min_age_limit"] == 45)) and \
           (
                   (options.covishield and session["vaccine"] == "COVISHIELD") or
                   (options.covaxin and session["vaccine"] == "COVAXIN") or
                   (options.sputnik and session["vaccine"] == "SPUTNIK")
           ) and \
           options.dose1 and session["available_capacity_dose1"] > 0 or \
           options.dose2 and session["available_capacity_dose2"] > 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cowin Vaccine Slot Availability Checker')
    parser.add_argument('-d', '--debug', help='Debug filter options', action="store_true")
    parser.add_argument('-f', '--age45', help='Filter by 45+ age', action="store_true")
    parser.add_argument('-e', '--age18', help='Filter by 18+ age', action="store_true")
    parser.add_argument('-c', '--covaxin', help='Filter by cvaxin', action="store_true")
    parser.add_argument('-s', '--sputnik', help='Filter by sputnik', action="store_true")
    parser.add_argument('-b', '--covishield', help='Filter by covishield', action="store_true")
    parser.add_argument('-d1', '--dose1', help='Filter by dose1', action="store_true")
    parser.add_argument('-d2', '--dose2', help='Filter by dose2', action="store_true")
    user_options = parser.parse_args()
    print(user_options)
    availableSlots = check_slots_by_district(districtIds, user_options)
    if len(availableSlots) > 0:
        wave_obj = sa.WaveObject.from_wave_file('speech.wav')
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until sound has finished playing
        print(json.dumps(availableSlots, indent=4, sort_keys=True))
