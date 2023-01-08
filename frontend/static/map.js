let map = null; // map object
var center = {lat:43.0722, lng:-89.4008} // the center of the map when initialized
var zoom = 15 // zoom (scale) of the map
// code review: comment about flask route api
let locationUrl = "/locations" // This is api route for flask application, detailed info see app.py
let highlightUrl = "/highlight" // This is api route for flask application, detailed info see app.py
let highlighted = -1
let markers = [] // list of markers
let cafeterias = [] // list of cafeteria object

// code review: comment about input and output
// create object from fetched data
// input: data structure parsed from json file
// return: a cafeteria object containing attributes
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


// code review: comment why map is null
// code review: detailed explination comment about event, each part of adding event listener.
// function adding markers to the map
function addMarker(cafeterias) {
    for (const cafeteria of cafeterias) {
        const advancedMarkerView = new google.maps.marker.AdvancedMarkerView({
            map: null, // when map is null, the marker will not be displayed on map, we will show marker in other function
            content: buildContent(cafeteria),
            position: cafeteria.location,
        });
        const element = advancedMarkerView.element;

        // add event listener to each marker

        // add event listener: when pointer enter the marker, the marker will be highlighted
        ["focus", "pointerenter"].forEach((event) => {
            element.addEventListener(event, () => {
                highlight(advancedMarkerView);
            });
        });
        // add event listener: when pointer leave the marker, the marker will be unhighlighted
        ["blur", "pointerleave"].forEach((event) => {
            element.addEventListener(event, () => {
                unhighlight(advancedMarkerView);
            });
        });
        // add event listener: when clicking the marker, the marker will be unhighlighted
        advancedMarkerView.addListener("click", (event) => {
            unhighlight(advancedMarkerView);
        });
        markers.push(advancedMarkerView)
    }
}

// making marker responsive to show details
function highlight(markerView) {
    markerView.content.classList.add("highlight");
    markerView.element.style.zIndex = 1;
}

function unhighlight(markerView) {
    markerView.content.classList.remove("highlight");
    markerView.element.style.zIndex = "";
}

// create relative DOM for the marker to make responsive functions working
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

// show given makers in the map
function setMarkerOn(marker) {
    marker.map = map;
}

// show given makers in the map
function setMarkerOff(marker) {
    marker.map = null;
}

// show markers on map according to the checkbox value
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

// add event listener to filtering UI components
$("#high-check").change(filterCrowd)
$("#medium-check").change(filterCrowd)
$("#low-check").change(filterCrowd)
$("#close-check").change(filterCrowd)


// show makers on map according to the type value
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

// code review: more explination about pipeline of flask and backend
// function that fetch data from backend API
// pipeline: backend API -> flask frontend app -> this javascript call flask API to get the data
const fetchLocation = async () => {
    const response = await fetch(locationUrl);
    const data = await response.json(); //extract JSON from the http response
    for(let i = 0; i < data.length; i++){
        cafeterias.push(createObject(data[i]))
    }
}
const fetchHighlight = async () => {
    const response = await fetch(highlightUrl);
    const data = await response.json(); //extract JSON from the http response
    highlighted = data[0]
}

// code review: comment about await fetch data
// code review: fetch data closer to its caller.
// initialize the map
async function initMap() {
    // using JQuery to make layout of map response to toggle
    var myWrapper = $("#wrapper");
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
        myWrapper.one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(e) {
            // code to execute after transition ends
            google.maps.event.trigger(map, 'resize');
        });
    });
    // wait for data fetching finish to do next step, or data will not be displayed
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
    // create map
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: zoom,
        center: center,
        mapId: "4504f8b37365c3d0"
    });
    // create marker basing on the cafeterias and push to marker
    
    // add all markers to map
    for (let i = 0; i < markers.length; i++) {
        setMarkerOn(markers[i]) 
    }
}


// initialize map every time load the window automatically.
window.initMap = initMap;