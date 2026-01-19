import React, { useEffect, useState } from 'react';
import LoginForm from './components/LoginForm';
import Dashboard from './components/Dashboard';
import { api } from './api';

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const checkSession = async () => {
      try {
        const data = await api.session();
        if (data.authenticated) {
          setUser({ username: data.username });
        }
      } catch {
        // not logged in
      } finally {
        setLoading(false);
      }
    };
    checkSession();
  }, []);

  const showToast = (msg, type = 'info') => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3200);
  };

  const handleLogin = async (username, password) => {
    const res = await api.login(username, password);
    if (res.success) {
      setUser({ username });
      showToast('Logged in');
    }
  };

  const handleRegister = async (username, password) => {
    const res = await api.register(username, password);
    if (res.success) {
      showToast('Registered! You can login now', 'success');
    }
  };

  const handleLogout = async () => {
    await api.logout();
    setUser(null);
    showToast('Logged out');
  };

  if (loading) {
    return (
      <div className="container" style={{ paddingTop: '120px', textAlign: 'center', color: '#9aa3c1' }}>
        Loading...
      </div>
    );
  }

  return (
    <div className="container">
      {user ? (
        <Dashboard user={user} onLogout={handleLogout} onToast={showToast} />
      ) : (
        <LoginForm onLogin={handleLogin} onRegister={handleRegister} onToast={showToast} />
      )}

      {toast && (
        <div className="toast">
          <span>{toast.msg}</span>
        </div>
      )}
    </div>
  );
}
