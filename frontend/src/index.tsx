/**
 * Main Entry Point for Web3 Job Seeker Frontend
 * 
 * This file serves as the entry point for the React application.
 * It renders the root App component and sets up global styles.
 * 
 * @author Web3 Job Seeker Team
 * @version 1.0.0
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Import global styles
import './index.css';

// Get the root element
const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

// Render the app
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
