import React, { useState } from 'react';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);

    const handleSubmit = (e) => {
        e.preventDefault();
        const messageText = e.target.messageText.value.trim();
        if (!messageText) return;

        const newMessages = [...messages, { text: messageText, sender: 'user' }];
        setMessages(newMessages);
        e.target.messageText.value = '';

        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ messageText }),
        })
        .then(response => response.json())
        .then(data => {
            const botMessage = { text: data.answer, sender: 'bot' };
            setMessages([...newMessages, botMessage]);

            const chatPanel = document.getElementById("chatPanel");
            chatPanel.scrollTop = chatPanel.scrollHeight;

            speakResponse(botMessage.text);
        })
        .catch(error => console.error('Error:', error));
    };

    const speakResponse = (text) => {
        const synth = window.speechSynthesis;
        const msg = new SpeechSynthesisUtterance();
        const voices = synth.getVoices();
        msg.voice = voices[0];
        msg.rate = 1;
        msg.pitch = 1;
        msg.text = text;
        synth.speak(msg);
    };

    const handleClear = () => {
        setMessages([]);
    };

    const handleVoice = () => {
        // Add voice recognition logic here
    };

    return (
        <div className="container">
            <div className="row">
                <h3 className="text-center">
                    <small><strong>Artificial</strong></small>
                    <span style={{ color: 'white' }}> Intelligence!!! </span>
                    <small><strong>Here</strong></small>
                    <span style={{ color: 'white' }}> I am..</span>
                </h3>
                <div className="col-md-4 col-md-offset-4">
                    <div id="chatPanel" className="panel panel-info">
                        <div className="panel-heading">
                            <strong><span className="glyphicon glyphicon-globe"></span> Talk with Me !!! (You: Green / Bot: White) </strong>
                        </div>
                        <div className="panel-body fixed-panel">
                            <ul className="media-list">
                                {messages.map((message, index) => (
                                    <li key={index} className={`media ${message.sender}`}>
                                        <div className="media-body">
                                            <div className="media">
                                                <div style={{ textAlign: message.sender === 'user' ? 'right' : 'left', color: message.sender === 'user' ? '#2EFE2E' : 'white' }} className="media-body">
                                                    {message.text}
                                                    <hr />
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div className="panel-footer">
                            <form onSubmit={handleSubmit}>
                                <div className="input-group">
                                    <input type="text" className="form-control" placeholder="Enter Message" name="messageText" autoFocus />
                                    <span className="input-group-btn">
                                        <button className="btn btn-info" type="submit">Send</button>
                                        <button className="btn btn-info" type="button" onClick={handleClear}>Clear</button>
                                        <button className="btn btn-info" type="button" onClick={handleVoice}>Voice</button>
                                    </span>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Chatbot;
