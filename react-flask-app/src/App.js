import React, { useState, useEffect } from 'react';
import logo from './SoRo Logo_Circle_Crimson.png';
import './App.css';
import StreamControl from './components/StreamControl';
import { CameraStream } from './components/CameraStream';

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        {/* <img src="/video_feed/0"></img>
        <img src="/video_feed/1"></img>
        <img src="/video_feed/2"></img> */}
        <CameraStream id='0'/>
        <CameraStream id='1'/>
        <CameraStream id='2'/>
        <div>
          <button onClick={handleStop}>Stop Stream</button>
          <button onClick={handleStart}>Start Stream</button>
        </div>
        <div>
          Quality Slider: <input onChange={sendQuality} type='range' min='0' max='100' class='slider' id='quality_slider'></input>
        </div>
      </header>
    </div>
  );
}

function sendQuality() {
  StreamControl.SendValue("quality", document.getElementById("quality_slider").value);
}

function handleStop() {
  StreamControl.SendCommand("stop");
}

function handleStart(){
  StreamControl.SendCommand("start");
}

export default App;
