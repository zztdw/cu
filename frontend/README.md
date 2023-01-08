# Google Map Frontend
This is google map frontend for team hungry horde.
## How to run
        cd ..
        pip3 install -r requirement.txt
        cd frontend
        python3 app.py
## Description
This is application for frontend (client server). I use flask as frontend server to solve the problem of CORS. This app will render the page containing customized google map.

The core of google map, also the core of this frontend is [script.js](./static/script.js) which contains how create google map, how to customize it and how event listener added to UI component.

The skeleton of frontend is [index.html](./templates/index.html) file, which contains the DOM of webpage.

The style for google map DOM is defined ub [style.css](./static/style.css) and style for filter wrapper container is in [wrapper.css](./static/wrapper.css).

Note: this part miss the backend server, so you can't see effect from backend if you really run this frontend server, but fake data will be displayed.

## Code Submission
[jiaxi_frontend](./jiaxi_frontend/) is not my part, but I integrated it in my application because of project requirement, also I submitted it in code submission in case you really want to run it.