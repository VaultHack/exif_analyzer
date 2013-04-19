#!/usr/bin/env python

import sys
import os
import string
import csv
import cairo
import time

from PIL import Image
from PIL.ExifTags import TAGS

import cairoplot
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
day_dict = {"Monday" : 0, "Tuesday" : 0, "Wednesday" : 0, "Thursday" : 0, "Friday" : 0, "Saturday" : 0, "Sunday" : 0}
month_dict = {}
year_dict = {}
weekday_mapping = {0 : "Monday", 1 : "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
month_mapping = {1 : "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 
              10: "October", 11: "November", 12: "December"}

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

                if str(aperture) in aperture_dict:
                    aperture_dict[str(aperture)] = aperture_dict[str(aperture)] + 1
                else: 
                    aperture_dict[str(aperture)] = 1
                    
                if str(exposure) in exposure_dict:
                    exposure_dict[str(exposure)] = exposure_dict[str(exposure)] + 1
                else: 
                    exposure_dict[str(exposure)] = 1

                if str(focallength) in focallength_dict:
                    focallength_dict[str(focallength)] = focallength_dict[str(focallength)] + 1
                else: 
                    focallength_dict[str(focallength)] = 1

                if str(iso) in iso_dict:
                    iso_dict[str(iso)] = iso_dict[str(iso)] + 1
                else: 
                    iso_dict[str(iso)] = 1

              
                
                if datetime != "Unknown":
                    datetime_struct = time.strptime(datetime, "%Y:%m:%d %H:%M:%S")
                    print("%s"%datetime_struct)
                    day = weekday_mapping[datetime_struct.tm_wday]
                    month = month_mapping[datetime_struct.tm_mon]
                    year = datetime_struct.tm_year
                    monthyear = str(month) + " " + str(year)

                    if str(day) in day_dict:
                        day_dict[str(day)] = day_dict[str(day)] + 1
                    else: 
                        day_dict[str(day)] = 1

                    if str(month) in month_dict:
                        month_dict[str(month)] = month_dict[str(month)] + 1
                    else: 
                        month_dict[str(month)] = 1
                        
                    if str(year) in year_dict:
                        year_dict[str(year)] = year_dict[str(year)] + 1
                    else: 
                        year_dict[str(year)] = 1

            except AttributeError:
                #print("Found no EXIF header... Skipping picture %s"%full_file)
                print(".")

print("Cameras: %s\n"%camera_dict)
print("Apertures: %s\n"%aperture_dict)
print("Exposures: %s\n"%exposure_dict)
print("Focallength: %s\n"%focallength_dict)
print("ISOs: %s\n"%iso_dict)
print("Years: %s\n"%year_dict)
print("Month: %s\n"%month_dict)
print("Day: %s\n"%day_dict)


write_csv_from_dict(camera_dict, "cameras.csv")
write_csv_from_dict(iso_dict, "iso.csv")

 #Define a new backgrond
background = cairo.LinearGradient(300, 0, 300, 400)
background.add_color_stop_rgb(0.0,0.0,0.0,0.0)
background.add_color_stop_rgb(0.7,0.7,0.7,0.7)

cairoplot.pie_plot("cameras", camera_dict, 700, 700, background = background, gradient = True, shadow = True)
cairoplot.pie_plot("apertures", aperture_dict, 500, 500, background = background, gradient = True, shadow = True)
cairoplot.pie_plot("exposures", exposure_dict, 500, 500, background = background, gradient = True, shadow = True)
cairoplot.pie_plot("focallength", focallength_dict, 500, 500, background = background, gradient = True, shadow = True)
cairoplot.pie_plot("iso", iso_dict, 500, 500, background = background, gradient = True, shadow = True)
cairoplot.pie_plot("day", day_dict, 500, 500, background = background, gradient = True, shadow = True)
cairoplot.pie_plot("year", year_dict, 500, 500, background = background, gradient = True, shadow = True)
cairoplot.pie_plot("month", month_dict, 500, 500, background = background, gradient = True, shadow = True)
