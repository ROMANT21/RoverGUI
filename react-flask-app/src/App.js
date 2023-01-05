import React, { useState, useEffect } from 'react';
import logo from './SoRo Logo_Circle_Crimson.png';
import './App.css';
import StreamControl from './components/StreamControl';

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <img src="/video_feed"></img>
        <button onClick={handleStop}>Stop Stream</button>
        <button onClick={handleStart}>Start Stream</button>
      </header>
    </div>
  );
}

function handleStop() {
  StreamControl.SendCommand("stop");
}

function handleStart(){
  StreamControl.SendCommand("start");
}

export default App;
