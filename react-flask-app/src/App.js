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
        <img src="/video_feed/0"></img>
        <img src="/video_feed/1"></img>
        <img src="/video_feed/2"></img>
        <Streams/>
        <button onClick={handleStop}>Stop Stream</button>
        <button onClick={handleStart}>Start Stream</button>
      </header>
    </div>
  );
}

function Streams() {
}

function handleStop() {
  StreamControl.SendCommand("stop");
}

function handleStart(){
  StreamControl.SendCommand("start");
}

export default App;
