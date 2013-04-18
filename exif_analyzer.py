#!/usr/bin/env python

import sys
import os
import string
import csv

from PIL import Image
from PIL.ExifTags import TAGS

dirname = sys.argv[1]

print("Searching folder: %s\n"%(dirname))

def write_csv_from_dict(dict, outfile):
    keysList = []
    valueList = []
    
    for key in dict: 
        keysList.append(key)
        valueList.append(dict[key])

    with open(outfile, 'wb') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(keysList)
        file_writer.writerow(valueList)

def get_exif_data(fn):
  date = "Unknown"
  aperture = "Unknown"
  focallength = "Unknown"
  camera = "Unknown"
  camera_brand = "Unknown"
  exposure = "Unknown"
  iso = "Unknown"

  ret = {}
  i = Image.open(fn)
  info = i._getexif()
  for tag, value in info.items():
    decoded = TAGS.get(tag, tag)
    ret[decoded] = value
    #print("%s: %s"%(decoded, value))
    if (decoded == "DateTimeOriginal"):
      date = value
    if (decoded == "ApertureValue"):
        aperture = value
    if (decoded == "FocalLength"):
        focallength = value
    if (decoded == "Model"):
        camera = value
    if (decoded == "ExposureTime"):
        exposure = value
    if (decoded == "ISOSpeedRatings"):
        iso = value
    if (decoded == "Make"):
        camera_brand = value

  return date, aperture, focallength, camera_brand, camera, exposure, iso

camera_dict = {}
aperture_dict = {}
exposure_dict = {}
focallength_dict = {}
iso_dict = {}


for filename in os.listdir(dirname):
    full_file = dirname + filename

    if os.path.isdir(full_file):
        #print("DIR: %s"%(filename))
        pass

    if os.path.isfile(full_file):
        #print("FILE: %s"%(filename))
        if ".jpg" in filename:
            #print("FOUND PICTURE!!!")
            try:
                datetime, aperture, focallength, camera_brand, camera_model, exposure, iso = get_exif_data(full_file)
                print("Picture %s was taken at: %s with camera: %s - %s |\n aperture: %s\n focallength: %s\n exposure: %s\n iso: %s\n"%
                      (full_file, datetime, camera_brand, camera_model , aperture, focallength, exposure, iso))

                full_camera = camera_brand + " " + camera_model

                # Start ANALYZING data
                if full_camera in camera_dict:
                    camera_dict[full_camera] = camera_dict[full_camera] + 1
                else: 
                    camera_dict[full_camera] = 1

                if aperture in aperture_dict:
                    aperture_dict[aperture] = aperture_dict[aperture] + 1
                else: 
                    aperture_dict[aperture] = 1
                    
                if exposure in exposure_dict:
                    exposure_dict[exposure] = exposure_dict[exposure] + 1
                else: 
                    exposure_dict[exposure] = 1

                if focallength in focallength_dict:
                    focallength_dict[focallength] = focallength_dict[focallength] + 1
                else: 
                    focallength_dict[focallength] = 1

                if iso in iso_dict:
                    iso_dict[iso] = iso_dict[iso] + 1
                else: 
                    iso_dict[iso] = 1

            except AttributeError:
                #print("Found no EXIF header... Skipping picture %s"%full_file)
                print(".")

print("Cameras: %s\n"%camera_dict)
print("Apertures: %s\n"%aperture_dict)
print("Exposures: %s\n"%exposure_dict)
print("Focallength: %s\n"%focallength_dict)
print("ISOs: %s\n"%iso_dict)

write_csv_from_dict(camera_dict, "cameras.csv")

