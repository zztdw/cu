//定义一个映射对象并初始化为空
let map = null;
//定义一个包含地图中心经纬度信息的对象
var center = {lat:37.48136592227171, lng:121.44883175667697}
//定义地图的缩放比例
var zoom = 16
//定义 flask 应用的 api 路由
let locationUrl = "/locations"
let highlightUrl = "/highlight"
//初始化一些变量
let highlighted = -1 //用于记录当前高亮的自助餐厅的下标，初始值为-1
let markers = [] //标记点的列表
let cafeterias = [] //自助餐厅对象的列表

//定义一个函数用于创建自助餐厅对象
function createObject(data) {
let id = data.id; //自助餐厅id
let name = data.name; //自助餐厅名称
let location = { lat: parseFloat(data.coords_lat), lng: parseFloat(data.coords_lon)}; //自助餐厅位置经纬度
let open_time = data.hours_open; //自助餐厅营业开始时间
let close_time = data.hours_closed; //自助餐厅营业结束时间
let status = data.status; //自助餐厅营业状态
let wait_times = data.wait_times //自助餐厅等待时间
let type = "Fast Food" //自助餐厅类型，默认为快餐
if (data.type){
type = data.type //如果有自助餐厅类型，使用该类型
}
let icon = "burger" //自助餐厅标记点的图标，初始为汉堡图标
if( type == "Dining"){
icon = "utensils" //如果是正餐餐厅，使用餐具图标
}
if (type == "Cafe"){
icon = "coffee" //如果是咖啡厅，使用咖啡图标
}
let crowd = "high" //自助餐厅拥挤程度，默认为高
if (wait_times == "< 5 min") { crowd = 'low' } //如果等待时间小于5分钟，拥挤程度为低
if (wait_times == "5 - 15 min"){ crowd = 'medium' } //如果等待时间在5-15分钟之间，拥挤程度为中
if (status == "Closed") { crowd = 'closed' } //如果自助餐厅已关闭，拥挤程度为关闭
//返回包含自助餐厅信息的对象
return {
id: id,
name: name,
status: status,
wait_times: wait_times,
type: type,
icon: icon,
open: open_time,
close: close_time,
crowd: crowd,
location: location
}
}

//向地图添加标记的函数
function addMarker(cafeterias) {
    for (const cafeteria of cafeterias) {
        const advancedMarkerView = new google.maps.marker.AdvancedMarkerView({
            map: null, //当map为null时，标记不会显示在地图上，我们将在其他函数中显示标记
            content: buildContent(cafeteria),
            position: cafeteria.location,
        });
        const element = advancedMarkerView.element;

        //为每个标记添加事件监听器

        //添加事件侦听器：当指针进入标记时，标记将突出显示
        ["focus", "pointerenter"].forEach((event) => {
            element.addEventListener(event, () => {
                highlight(advancedMarkerView);
            });
        });
        //添加事件侦听器：当指针离开标记时，标记将取消突出显示
        ["blur", "pointerleave"].forEach((event) => {
            element.addEventListener(event, () => {
                unhighlight(advancedMarkerView);
            });
        });
        //添加事件监听器：当点击标记时，标记将取消高亮
        advancedMarkerView.addListener("click", (event) => {
            unhighlight(advancedMarkerView);
        });
        markers.push(advancedMarkerView)
    }
}

//使标记响应显示细节
function highlight(markerView) {
    markerView.content.classList.add("highlight");
    markerView.element.style.zIndex = 1;
}

function unhighlight(markerView) {
    markerView.content.classList.remove("highlight");
    markerView.element.style.zIndex = "";
}

//为标记创建相对 DOM 以使响应函数工作
function buildContent(cafeteria) {
    const content = document.createElement("div");

    content.classList.add("property");
    content.innerHTML = `
        <div class="icon">
            <i aria-hidden="true" class="fa fa-solid fa-${cafeteria.icon} ${cafeteria.crowd}" title="${cafeteria.icon}"></i>
            <span class="fa-sr-only">${cafeteria.icon}</span>
        </div>
        <div class="details">
            <div class="name">${cafeteria.name}</div>
            <div class="wait">Estimate: ${cafeteria.wait_times}</div>
            <div class="wait">Open: ${cafeteria.open}</div>
            <div class="wait">Close: ${cafeteria.close}</div>
            <div class="wait">Status: ${cafeteria.status}</div>
        </div>
        `;
    return content;
}
//addMarker(cafeterias): 这个函数的作用是将餐厅的信息cafeterias添加到地图上，每个餐厅都会有一个标记。
//在for循环中，对于cafeterias中的每一个元素
//都会调用new google.maps.marker.AdvancedMarkerView创建一个新的标记对象，并将它存储在markers数组中但此时还没有将其添加到地图上。
//highlight(markerView)和unhighlight(markerView): 这两个函数用于在标记上应用高亮效果和取消高亮效果。
//当指针进入标记时，highlight函数会使标记突出显示；当指针离开标记时，unhighlight函数会使标记取消突出显示。
//buildContent(cafeteria): 这个函数用于创建每个标记的内容，返回一个相对 DOM 元素
//该函数使用 cafeterias 的数据来创建包含有关餐厅的详细信息的元素，如名称、等待时间、开放时间、关闭时间和状态
//然后，使用这些信息创建一个包含 HTML 代码的字符串，并将其分配给新创建的 div 元素的innerHTML属性。最后，将这个 div 元素返回给调用者，用于添加到标记中。
//在地图中显示给定的制造商
function setMarkerOn(marker) {
    marker.map = map;
}

//在地图中显示给定的制造器
function setMarkerOff(marker) {
    marker.map = null;
}
//根据复选框值在地图上显示标记
function filterCrowd() {
    let low = $("#low-check").prop("checked")
    let medium = $("#medium-check").prop("checked")
    let high = $("#high-check").prop("checked")
    let close = $("#close-check").prop("checked")
    for (let i = 0; i < markers.length; i++) {
        if(cafeterias[i].crowd === "high"){
            if (high) {
                setMarkerOn(markers[i])
            }
            else{
                setMarkerOff(markers[i])
            }
        }
        else if(cafeterias[i].crowd === "low"){
            if (low) {
                setMarkerOn(markers[i])
            }
            else{
                setMarkerOff(markers[i])
            }
        }
        else if(cafeterias[i].crowd === "medium"){
            if (medium) {
                setMarkerOn(markers[i])
            }
            else{
                setMarkerOff(markers[i])
            }
        }
        else if(cafeterias[i].crowd === "closed"){
            if (close) {
                setMarkerOn(markers[i])
            }
            else{
                setMarkerOff(markers[i])
            }
        }
    }
}

//为过滤 UI 组件添加事件监听器
$("#high-check").change(filterCrowd)
$("#medium-check").change(filterCrowd)
$("#low-check").change(filterCrowd)
$("#close-check").change(filterCrowd)


//根据type值在地图上显示makers
function filterType() {
    let fast = $("#fast-check").prop("checked")
    let dining = $("#dining-check").prop("checked")
    let cafe = $("#cafe-check").prop("checked")
    for (let i = 0; i < markers.length; i++) {
        if(cafeterias[i].type === "Fast Food"){
            if (fast) {
                setMarkerOn(markers[i])
            }
            else{
                setMarkerOff(markers[i])
            }
        }
        else if(cafeterias[i].type === "Dining"){
            if (dining) {
                setMarkerOn(markers[i])
            }
            else{
                setMarkerOff(markers[i])
            }
        }
        else if(cafeterias[i].type === "Cafe"){
            if (cafe) {
                setMarkerOn(markers[i])
            }
            else{
                setMarkerOff(markers[i])
            }
        }
    }
}

$("#fast-check").change(filterType)
$("#dining-check").change(filterType)
$("#cafe-check").change(filterType)


//从后端 API 获取数据的函数

const fetchLocation = async () => {
    const response = await fetch(locationUrl);
    const data = await response.json(); //从http响应中提取JSON
    for(let i = 0; i < data.length; i++){
        cafeterias.push(createObject(data[i]))
    }
}
const fetchHighlight = async () => {
    const response = await fetch(highlightUrl);
    const data = await response.json(); //从http响应中提取JSON
    highlighted = data[0]
}

//代码审查：关于等待获取数据的评论
//代码审查：获取更接近其调用者的数据。
//初始化地图
async function initMap() {
    //使用 JQuery 使地图布局响应切换
    var myWrapper = $("#wrapper");
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
        myWrapper.one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(e) {
            //转换结束后执行的代码
            google.maps.event.trigger(map, 'resize');
        });
    });
   //等待数据获取完成进行下一步，否则数据不会显示
    await fetchLocation()
    await fetchHighlight()
    addMarker(cafeterias)
    if(highlighted != -1){
        for (let i = 0; i < cafeterias.length; i++) {
            const current = cafeterias[i];
            if(current.id === highlighted){
                center = current.location
                zoom = 19
                highlight(markers[i])
            }
        }
    }
    //创建地图
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: zoom,
        center: center,
        mapId: "4504f8b37365c3d0"
    });
    //基于餐厅创建标记并推送到标记
    
    // 添加所有标记到地图
    for (let i = 0; i < markers.length; i++) {
        setMarkerOn(markers[i]) 
    }
}


//每次自动加载窗口时初始化地图。
window.initMap = initMap;