#!/usr/bin/env python3

import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import json
import folium
import webbrowser
import os
import time
import socket
import sys

def print_banner():
    print("="*50)
    print("   IP & PHONE NUMBER İNFO TOOL")
    print("        BY CYBERTANK0")
    print("="*50)
    print("")
    print("[1] Lookup IP Address")
    print("[2] Lookup Phone Number")
    print("[3] Lookup My Own IP")
    print("[4] Exit")
    print("="*50)

def get_own_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        return None

def ip_info(ip_address):
    print(f"[*] Looking up IP address: {ip_address}")
    
    apis = [
        f'http://ip-api.com/json/{ip_address}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query',
        f'https://ipinfo.io/{ip_address}/json'
    ]
    
    all_data = {}
    
    for api in apis:
        try:
            response = requests.get(api, timeout=10)
            if response.status_code == 200:
                data = response.json()
                all_data.update(data)
                break
        except:
            continue
    
    if not all_data:
        print("[!] Failed to get IP information!")
        return None
    
    return all_data

def display_ip_info(data, ip):
    print("\n" + "="*50)
    print("IP ADDRESS DETAILS")
    print("="*50)
    
    fields = {
        'query': 'IP Address',
        'ip': 'IP Address',
        'country': 'Country',
        'countryCode': 'Country Code',
        'region': 'Region',
        'regionName': 'Region Name',
        'city': 'City',
        'zip': 'Postal Code',
        'lat': 'Latitude',
        'lon': 'Longitude',
        'timezone': 'Timezone',
        'isp': 'ISP',
        'org': 'Organization',
        'as': 'AS Number'
    }
    
    lat, lon = None, None
    
    for key, label in fields.items():
        if key in data and data[key]:
            value = data[key]
            if key == 'lat':
                lat = value
            elif key == 'lon':
                lon = value
            print(f"{label}: {value}")
    
    print("="*50)
    
    if lat and lon:
        create_map(lat, lon, ip)
    
    return lat, lon

def create_map(latitude, longitude, ip):
    try:
        map_obj = folium.Map(location=[float(latitude), float(longitude)], zoom_start=12)
        folium.Marker(
            [float(latitude), float(longitude)],
            popup=f'IP: {ip}',
            tooltip=ip
        ).add_to(map_obj)
        
        map_file = f'ip_location_{ip}.html'
        map_obj.save(map_file)
        print(f"\nMap created: {map_file}")
        print("Opening map in browser...")
        webbrowser.open(f'file://{os.path.abspath(map_file)}')
    except Exception as e:
        print(f"Map creation failed: {e}")

def phone_info(phone_number):
    print(f"[*] Looking up phone number: {phone_number}")
    
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        
        if not phonenumbers.is_valid_number(parsed_number):
            print("[!] Invalid phone number!")
            return None
        
        print("\n" + "="*50)
        print("PHONE NUMBER DETAILS")
        print("="*50)
        
        country = geocoder.description_for_number(parsed_number, "en")
        print(f"Country: {country}")
        
        service_provider = carrier.name_for_number(parsed_number, "en")
        if service_provider:
            print(f"Carrier: {service_provider}")
        else:
            print("Carrier: Not available")
        
        time_zones = timezone.time_zones_for_number(parsed_number)
        if time_zones:
            print(f"Time Zone: {', '.join(time_zones)}")
        
        print(f"Country Code: {parsed_number.country_code}")
        print(f"National Number: {parsed_number.national_number}")
        
        if phonenumbers.is_possible_number(parsed_number):
            print("Validity: Valid number format")
        
        print("="*50)
        
        return parsed_number
        
    except phonenumbers.NumberParseException as e:
        print(f"[!] Error parsing number: {e}")
        return None

def main():
    while True:
        print_banner()
        
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                ip = input("Enter IP address: ").strip()
                if ip:
                    data = ip_info(ip)
                    if data:
                        display_ip_info(data, ip)
                else:
                    print("[!] No IP address entered!")
                    
            elif choice == '2':
                phone = input("Enter phone number (with country code, e.g., +1234567890): ").strip()
                if phone:
                    phone_info(phone)
                else:
                    print("[!] No phone number entered!")
                    
            elif choice == '3':
                my_ip = get_own_ip()
                if my_ip:
                    print(f"[*] Your IP address: {my_ip}")
                    data = ip_info(my_ip)
                    if data:
                        display_ip_info(data, my_ip)
                else:
                    print("[!] Could not get your IP address!")
                    
            elif choice == '4':
                print("Exiting...")
                sys.exit(0)
                
            else:
                print("[!] Invalid choice! Please enter 1-4")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        except Exception as e:
            print(f"[!] Error: {e}")
        
        input("\nPress Enter to continue...")
        os.system('clear' if os.name == 'posix' else 'cls')

if __name__ == "__main__":
    main()
