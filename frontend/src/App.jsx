import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { LoginForm } from './components/auth/LoginForm';
import { RegisterForm } from './components/auth/RegisterForm';
import Layout from './app/layout'; 
import { Toaster } from '@/components/ui/sonner';

function App() {
  return (
    <Router>
      <Toaster position="top-right" />
      <Routes>
        {/* Login Route (outside the Layout) */}
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />

        {/* Layout Wrapping Routes */}
        <Route
          element={<Layout />}
        >

          {/* Home Route inside Layout */}
          <Route
            path="/"
            element={
              <div>
                <h1>Welcome to the App</h1>
                <p>This is the main content area.</p>
                <Link to="/login">Go to Login</Link>
              </div>
            }
          />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;

