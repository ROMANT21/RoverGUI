import React, { useState, useEffect } from 'react';
import logo from './SoRo Logo_Circle_Crimson.png';
import './App.css';

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <img src="/video_feed"></img>
      </header>
    </div>
  );
}

export default App;
