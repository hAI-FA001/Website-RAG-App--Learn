import React, { useState, useEffect } from 'react';
import UrlInput from './components/UrlInput';
import ChatInterface from './components/ChatInterface';

function App() {
  const [showChat, setShowChat] = useState(false);

  const handleUrlSubmitted = () => {
    setShowChat(true);
  }

  useEffect(() => {
    return () => {
      fetch("http://localhost:5000/delete-index", {
        method: "POST"
      }).then((res) => {
        if (!res.ok) {
          console.error("Error deleting index: ", res.statusText);
        }
      }).catch((error) => {
        console.error("Error: ", error);
      })
    }
  }, []);

  return (
    <div className='App'>
      {
        !showChat ? (
          <UrlInput onSubmit={handleUrlSubmitted} />
        ) : (
            <ChatInterface />
        )
      }
    </div>
  )
}

export default App;