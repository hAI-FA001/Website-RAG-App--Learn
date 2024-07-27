import { useEffect, useRef, useState } from "react";
import ChatMessage from './ChatMessage';

function ChatInterface() {
    const [messages, setMessages] = useState([]);
    const [inputTxt, setInputTxt] = useState('');

    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrolIntoView({
            behavior: "smooth"
        })
    };

    useEffect(scrollToBottom, [messages]);

    const handleSendMessage = async (e) => {
        e.preventDefault();

        // check if empty
        if (!inputTxt.trim()) return;
        const userMessage = {
            text: inputTxt,
            isBot: false
        };
        const body = {
            chatHistory: [...messages, userMessage],
            question: inputTxt
        }

        // concat old messages + this new message
        setMessages([...messages, userMessage]);
        setInputTxt('');

        const res = await fetch("http://localhost:5000/handle-query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        const data = await res.json();
        const botMessage = {
            text: data.answer,
            isBot: true
        };
        
        setMessages(current => [...current, botMessage]);
    };

    return (
        <div className="chat-container">
            <header className="chat-header">
                URL Q/A
            </header>
            {
                messages.length === 0
                &&
                <div className="chat-message bot-message">
                        <p className="initial-message">
                            Hi there! I'm trained to answer questions about websites.
                            Try asking a question below.
                    </p>
                </div>
            }
            <div className="chat-message">
                {
                    messages.map((m, idx) => (
                        <ChatMessage key={idx} message={m} />
                    ))
                }
                <div ref={messagesEndRef} />
            </div>
            <form className="chat-input" onSubmit={handleSendMessage}>
                <input
                    type="text"
                    placeholder="Type a question and press enter"
                    value={inputTxt}
                    onChange={(e) => setInputTxt(e.target.value)}
                />
            </form>
        </div>
    );
}

export default ChatInterface;