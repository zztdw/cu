from datetime import datetime
#这是来自后端 json 文件的自助餐厅类，
#创建对象对象可以更容易地在前端执行操作
class Cafeteria:
    def __init__(self, info:dict) -> None:
        curr = datetime.now()
        self.id = info.get("id", -1)
        self.name = info.get("name", "Unknown")
        self.address = info.get("address", "No available address.")
        open = info.get("hours_open", "09:00:00").split(":")
        close = info.get("hours_closed", "18:00:00").split(":")
        #这将为打开和关闭时间创建一个日期时间对象，这些将用于
#如果未从 json 传递状态，则确定当前状态
        open_time = curr.replace(hour=int(open[0]), minute=int(open[1]), second=int(open[2]))
        close_time = curr.replace(hour=int(close[0]), minute=int(close[1]), second=int(close[2]))
        self.hours_open = open_time.strftime("%H:%M:%S")
        self.hours_closed = close_time.strftime("%H:%M:%S")
        #默认状态由打开、关闭和当前时间决定
        self.status = "Open" if curr > open_time and curr < close_time else "Closed"
        #来自 json 的真实状态
        if(info.get("status")=='Open' or info.get("status") == "Closed"):
            self.status = info.get("status")
        self.wait_times = info.get("wait_times","< 5 min")
        self.coords_lat = info.get("coords_lat","0")
        self.coords_lon = info.get("coords_lon","0")
        self.type =  info.get("type", "Fast Food")
        
    #该函数将返回一个字典，其中包含该类的所有属性
    def getAttr(self):
        return self.__dict__

