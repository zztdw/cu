let map = null; //映射对象
var center = {lat:37.48136592227171,  lng:121.44883175667697} //初始化时地图的中心
var zoom = 16 //地图的缩放（比例）
//代码审查：关于 flask route api 的评论
let locationUrl = "/locations" //这是 flask 应用的 api 路由，详细信息见 app.py
let highlightUrl = "/highlight" //这是 flask 应用的 api 路由，详细信息见 app.py
let highlighted = -1
let markers = [] // list of markers
let cafeterias = [] // list of cafeteria object

//代码审查：关于输入和输出的注释
//从获取的数据创建对象
//输入：从json文件解析出来的数据结构
//返回：一个包含属性的自助餐厅对象
function createObject(data) {
    let id = data.id;
    let name = data.name;
    let location = { lat: parseFloat(data.coords_lat), lng: parseFloat(data.coords_lon)};
    let open_time = data.hours_open;
    let close_time = data.hours_closed;
    let status = data.status;
    let wait_times = data.wait_times
    let type = "Fast Food"
    if (data.type){
        type = data.type
    }
    let icon = "burger"
    if( type == "Dining"){
        icon = "utensils"
    }
    if (type == "Cafe"){
        icon = "coffee"
    }
    let crowd = "high"
    if (wait_times == "< 5 min") {
        crowd = 'low'
    }
    if (wait_times == "5 - 15 min"){
        crowd = 'medium'
    }
    if (status == "Closed") {
        crowd = 'closed'
    }
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
            <div class="wait">等待时间: ${cafeteria.wait_times}</div>
            <div class="wait">营业时间: ${cafeteria.open}</div>
            <div class="wait">闭店时间: ${cafeteria.close}</div>
            <div class="wait">状态: ${cafeteria.status}</div>
        </div>
        `;
    return content;
}

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