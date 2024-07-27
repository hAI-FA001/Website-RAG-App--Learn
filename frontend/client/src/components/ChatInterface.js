import { useEffect, useRef, useState } from "react";
import ChatMessage from './ChatMessage';

function ChatInterface() {
    const [messages, setMessages] = useState([]);
    const [inputTxt, setInputTxt] = useState('');

    const messagesEndRef = useRef(null);

    var accumulatedAnswer = "";

    function updateLastMessage(current) {
        // this will be the new history
        const updatedHistory = [...current];
        // last chat = bot message
        const lastChatIdx = updatedHistory.length - 1;
                
        updatedHistory[lastChatIdx] = {
            // keep all keys/properties
            ...updatedHistory[lastChatIdx],
            // except "text"
            text: accumulatedAnswer
        };

        return updatedHistory;
    };

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
        const botMessage = {
            text: "",
            isBot: true
        };

        // concat old messages + this new message
        setMessages([...messages, userMessage, botMessage]);
        setInputTxt('');

        const res = await fetch("http://localhost:5000/handle-query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });
        
        if (!res.body) return;

        // for streaming
        let decoder = new TextDecoderStream();
        const reader = res.body.pipeThrough(decoder).getReader();
        accumulatedAnswer = "";

        while (true) {
            var { value, done } = await reader.read();

            if (done) break;

            accumulatedAnswer += value;

            // set last bot message
            setMessages(updateLastMessage);
        }
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