import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent="sector_locator",timeout=10)


df = pd.DataFrame(columns=["sector", "latitude",'longitude'])

for sector in range(1, 116):
    location = geolocator.geocode("Sector {}, Gurgaon".format(sector))
    if location:
        df.loc[len(df)] = [f"sector {sector}",location.latitude,location.longitude]
    else:
        df.loc[len(df)] = [f"sector {sector}",np.nan,np.nan]
    time.sleep(1)


location = geolocator.geocode("Sohna, Haryana")
df.loc[len(df)]=["sohna",location.latitude,location.longitude]

print(df)
df.to_csv("gurgaon_sectors_coordinates.csv", index=False)