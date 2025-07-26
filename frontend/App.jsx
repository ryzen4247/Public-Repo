import React from 'react';
import ChatWindow from './components/ChatWindow';
import { ChatProvider } from './context/ChatContext';
import './styles.css';

const App = () => (
  <ChatProvider>
    <div className="app">
      <ChatWindow />
    </div>
  </ChatProvider>
);

export default App;
