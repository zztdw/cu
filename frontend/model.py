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
    
#####################
#这段代码定义了一个名为Cafeteria的类，
# 用于创建自助餐厅对象。在__init__函数中，
# 首先根据传入的字典参数info初始化对象的各个属性，
# 包括自助餐厅的id、name、address、开放时间和关闭时间、状态、等待时间、经度和纬度、类型等。
# 其中，开放时间和关闭时间是根据从json文件中获取的hours_open和hours_closed字符串属性创建了一个datetime对象，
# 并将其格式化为"%H:%M:%S"格式的字符串，以便于后续的比较和显示。同时，该类的状态属性有一个默认值，
# 即根据当前时间与开放和关闭时间的比较确定状态，但如果json中传递了该属性，则以传递的属性值为准。
#getAttr函数是该类的一个方法，
# 用于返回一个字典，其中包含该类的所有属性及其对应的值。
# 这个字典包含了该自助餐厅的所有属性信息，可以用于前端页面的显示和操作。
#####################