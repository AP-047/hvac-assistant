import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userMessage = { type: "user", content: query };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await axios.post("http://host.docker.internal:8000/api/chat", { query });
      const botMessage = { 
        type: "bot", 
        content: response.data.answer,
        sources: response.data.sources
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { 
        type: "error", 
        content: "Sorry, I encountered an error. Please try again." 
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setQuery("");
    setIsLoading(false);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🏢 HVAC Design Assistant</h1>
        <p>Get expert guidance on HVAC system design and calculations</p>
      </header>

      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h3>Welcome! How can I help you with HVAC design today?</h3>
              <div className="sample-questions">
                <button onClick={() => setQuery("How do I calculate cooling load for a 100m² office?")}>
                  Sample: Calculate cooling load
                </button>
                <button onClick={() => setQuery("What are the ventilation requirements for commercial spaces?")}>
                  Sample: Ventilation requirements
                </button>
              </div>
            </div>
          )}
          
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.type}-message`}>
              <div className="message-content">
                {message.content}

                {message.sources && (
                  <div className="sources">
                    <strong>Sources:</strong>
                    {message.sources.map((s, i) => (
                      <div key={i} className="source-item">
                        <a href={s.url} target="_blank" rel="noopener noreferrer">
                          {s.title}
                        </a>
                        <span className="chunk-id"> (chunk {s.chunk_id})</span>
                        <p className="snippet">{s.snippet}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message bot-message">
              <div className="message-content loading">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                Analyzing HVAC documents...
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask your HVAC question here..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading || !query.trim()}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
