"use client"
import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';

const ENDPOINT = "http://localhost:8080";
const socket = io(ENDPOINT);

function Home() {
  const [messages, setMessages] = useState([]);
  const [spotifyLink, setSpotifyLink] = useState('');
  const lastBoxRef = useRef(null);

  const handleTransferClick = async () => {
    setMessages(["Starting Transfer..."]);
    const response = await fetch('http://localhost:8080/api/transfer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ spotifyLink }),
    });

    const data = await response.json();
    setMessages(prevMessages => [...prevMessages, data.message]);
  };

  useEffect(() => {
    socket.on("update", data => {
      setMessages(prevMessages => [...prevMessages, data.message]);
      if (lastBoxRef.current) {
        lastBoxRef.current.scrollTop = lastBoxRef.current.scrollHeight;
      }
    });

    return () => {
      socket.off("update");
    };
  }, []);

  const handleInputChange = (event) => {
    setSpotifyLink(event.target.value);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-b from-purple-800 to-blue-800">
      <div className="flex flex-col items-center justify-center">
        <h1 className="text-6xl font-extrabold text-white text-center mb-4">Welcome !</h1>
        <p className="text-lg text-gray-300 text-center mb-8">Easily transfer your Spotify playlists to YouTube Music</p>
        <input
          type="text"
          name="spotifyLink"
          placeholder="Enter Spotify Link" 
          className="w-80 h-12 rounded-lg px-4 focus:outline-none focus:ring focus:border-blue-300 bg-gray-800 text-white placeholder-gray-400"
          value={spotifyLink}
          onChange={handleInputChange}
          required
        />
        <br />
        <button 
          type="button" 
          onClick={handleTransferClick} 
          className="bg-blue-600 text-white px-6 py-2 rounded-lg mt-4 hover:bg-blue-600 focus:outline-none focus:ring focus:border-blue-300"
        >
            Transfer
        </button>
      </div>
      <div className="bg-gray-900 w-2/3 h-72 mt-8 p-4 rounded-lg border border-gray-300 overflow-auto" ref={lastBoxRef}>
        <div className="text-green-500 font-mono text-lg p-4">
          {messages.map((message, index) => (
            <div key={index}>
              {message}
              {index !== messages.length - 1 && <br />} 
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Home;