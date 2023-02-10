# Summary

This repo contains the Rover's new GUI for competition. 

The code is composed of flask, for the backend and isolated to the api folder, and React, for the frontend.

# Dependencies

## Python: Dependencies and venv ##
For the sake of simplicity, I've run the code so as to require a virtual environment in the api folder
To create the virtual environment:
```
cd api
python -m venv venv
```

To activate the virtual environment run:

(Windows)
```
venv\Scripts\activate
```
(Ubuntu)
```
source ./venv/bin/activate
```

Then we need to install a few libraries:
```
pip install opencv-python Flask python-dotenv
```

## React: How to install ##
To use React, we have to install Node.js

[here's](https://nodejs.org/en/download/) a link to the installer.

To ensure you've downloaded node, run:
```
npx -v
``` 
which should show something like `9.2.0`

and 
```
npm -v
```
which should show something like `9.2.0`. 

Then run 
```
cd react-flask-app
npm install
```
to install all required dependencies.

# Running the Web App #
First we need to start the API (the backend):
```
cd api 
# activate venv
flask run
```
(`python api.py` also works)

Now open another terminal. Then we can start React (the frontend):
```
npm start
```
Lastly, open another terminal and type
```
python video_sender.py
```

Then you should see something (kinda) like this:
![cool guy](coolguy.png)
