import React, { useContext } from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';
import { ChatContext } from '../context/ChatContext';

const ChatWindow = () => {
  const { messages } = useContext(ChatContext);

  return (
    <div className="chat-window">
      <MessageList messages={messages} />
      <UserInput />
    </div>
  );
};

export default ChatWindow;
