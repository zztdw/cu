from datetime import datetime

# Author: Bingxu Hu
# This is cafeteria class from json file from backend,
# creating object object make it easier to perform operation on frontend
class Cafeteria:
    def __init__(self, info:dict) -> None:
        curr = datetime.now()
        self.id = info.get("id", -1)
        self.name = info.get("name", "Unknown")
        self.address = info.get("address", "No available address.")
        open = info.get("hours_open", "09:00:00").split(":")
        close = info.get("hours_closed", "18:00:00").split(":")
        # This will create a datetime object for open and close time, these will be used for 
        # determining current status if status is not passed from json
        open_time = curr.replace(hour=int(open[0]), minute=int(open[1]), second=int(open[2]))
        close_time = curr.replace(hour=int(close[0]), minute=int(close[1]), second=int(close[2]))
        self.hours_open = open_time.strftime("%H:%M:%S")
        self.hours_closed = close_time.strftime("%H:%M:%S")
        # default status decided by open, close and current time
        self.status = "Open" if curr > open_time and curr < close_time else "Closed"
        # real status from json
        if(info.get("status")=='Open' or info.get("status") == "Closed"):
            self.status = info.get("status")
        self.wait_times = info.get("wait_times","< 5 min")
        self.coords_lat = info.get("coords_lat","0")
        self.coords_lon = info.get("coords_lon","0")
        self.type =  info.get("type", "Fast Food")
        
    # This function will return a dict which contains all the attributes of this class
    def getAttr(self):
        return self.__dict__

# fake data 1
sett = Cafeteria({
    "id" : 1,
    "name" : "Sett Pub",
    "address" : "1308 W Dayton St room 105, Madison, WI 53715",
    "hours_open" : "11:00:00",
    "hours_closed" : "23:30:00",
    "wait_times" : "> 20 min",
    "status" : "Open",
    "type" : "Fast Food",
    "coords_lat" : "43.071328653947916",
    "coords_lon" : "-89.4077521876059",
})
# fake data 2
gordon = Cafeteria({
    "id" : 2,
    "name" : "Gordon Dining and Event Center",
    "address" : "770 W Dayton St, Madison, WI 53706",
    "hours_open" : "09:00:00",
    "hours_closed" : "23:30:00",
    "status" : "Open",
    "wait_times" : "5 - 15 min",
    "type" : "Dining",
    "coords_lat" : "43.07125867881556",
    "coords_lon" : "-89.39863335870125",
})
# fake data 3
capital = Cafeteria({
    "id" : 3,
    "name" : "Capital Cafe",
    "address" : "975 University Ave, Madison, WI 53715",
    "hours_open" : "08:00:00",
    "hours_closed" : "23:30:00",
    "status" : "Open",
    "wait_times" : "< 5 min",
    "type" : "Cafe",
    "coords_lat" : "43.072379022579604",
    "coords_lon" : "-89.40102623896776",
})
        
