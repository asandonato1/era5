import cdsapi
import numpy as np

# ------------------------- USAGE ---------------------------
# from downloader import *
# years = [year for year in range(startingYear, endYear + 1)]
#
# downloadSets(years)
# ------------------------- USAGE ---------------------------


def randomDays():
    # this function just picks 3 random days in a month
    
    n1, n2, n3 = np.random.randint(1, 29), np.random.randint(1, 29), np.random.randint(1, 29) 
    
    while(n1 == n2 or n1 == n3 or n2 == n3):
        if(n1 == n2): 
            while(n1 == n2):
                n1 = np.random.randint(1,29)
        elif(n1 == n3): 
            while(n1 == n3):
                n3 = np.random.randint(1,29)
        elif(n2 == n3):
            while(n2 == n3):
                n2 = np.random.randint(1,29)
    return [n1,n2,n3]

def downloadSets(years, random = False): 
    # takes as input a list of years. in our case, [i for i in range(1990, 2026)]. 
    # also takes "random" as input, which dictates if the days used for the downloads are random or not. by default, the days are the ones after the else statement in the for loop 
    for idx, year in enumerate(years): # looping over years list
        if(random == True):
            days = randomDays()
        else: days = ["7", "11", "21"] # default days i was using
        print(f"Request {idx + 1}: Year {year}") # just to keep track of which requests are being made
        print("-----------------------------------------------------")
        dataset = "derived-era5-single-levels-daily-statistics" # dataset used
        request = {
            "product_type": "reanalysis", 
            "variable": [ # which variables are being request
            "10m_u_component_of_wind", # wind component
            "10m_v_component_of_wind", # wind component
            "2m_temperature", # air temperature right above sea level
            "mean_sea_level_pressure", # sea level pressure
            "mean_wave_period",
            "sea_surface_temperature", # temperature of the sea surface
            "surface_pressure", # pressure at the surface
            "total_precipitation", # total precipitation
            "surface_net_solar_radiation", # shortwave
            "surface_net_thermal_radiation", # longwave
            "evaporation"
            ],
            "year": year, # the current year we are downloading data from
            "month": [ # here, all of the months are selected
                "01", "02", "03",
                "04", "05", "06",
                "07", "08", "09",
                "10", "11", "12"
            ],
            "day": days, # since cds imposes a data limit, only three days can be selected using the 6h resolution/frequency
            "daily_statistic": "daily_mean", # using the daily mean of each statistic
            "time_zone": "utc+00:00",
            "frequency": "6_hourly"
    }
    
        client = cdsapi.Client()
        client.retrieve(dataset, request).download() # this downloads the data.

    # so, the current "problem", in my opinion, is the amount of days that are being selected
    # limiting the amount of days to only 3 can be potentially harmful in capturing some finer details
    # to limit that problem, i tried to choose days in each separate week of the month. this, however
    # causes a problem: it slows down the speed of the download. for some reason, the downloads of 
    # statistics from non-consecutive days are way slower that consecutive days. who knows why...
    # be that as it may, the requests also, usually, take a while to be approved. so the download of 
    # over 30 years should take a while.
    
    return 0
