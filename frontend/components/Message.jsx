import React from 'react';

const Message = ({ text, sender }) => (
  <div className={`message ${sender}`}>
    <span>{text}</span>
  </div>
);

export default Message;
