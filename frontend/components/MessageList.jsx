import React from 'react';
import Message from './Message';

const MessageList = ({ messages }) => (
  <div className="message-list">
    {messages.map((msg, idx) => (
      <Message key={idx} text={msg.text} sender={msg.sender} />
    ))}
  </div>
);

export default MessageList;
