import React, { useState } from 'react';

export default function LoginForm({ onLogin, onRegister, onToast }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [mode, setMode] = useState('login');
  const [busy, setBusy] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      onToast('Username and password required', 'warn');
      return;
    }
    setBusy(true);
    try {
      if (mode === 'login') {
        await onLogin(username.trim(), password);
      } else {
        await onRegister(username.trim(), password);
      }
    } catch (err) {
      onToast(err.message, 'danger');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="card" style={{ padding: 32, maxWidth: 520, margin: '120px auto' }}>
      <div style={{ marginBottom: 12, color: '#9aa3c1', textTransform: 'uppercase', letterSpacing: 2, fontSize: 12 }}>
        Face Attendance
      </div>
      <h1 style={{ fontSize: 28, marginBottom: 12 }}>Welcome</h1>
      <p style={{ color: '#9aa3c1', marginBottom: 24 }}>Secure login for teachers</p>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
        <label style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <span style={{ color: '#c9d0e7', fontSize: 14 }}>Username</span>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="your_username"
            style={{ padding: 12, borderRadius: 10, background: '#0b1021', color: '#e9ecf5', border: '1px solid #1f2640' }}
          />
        </label>
        <label style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <span style={{ color: '#c9d0e7', fontSize: 14 }}>Password</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            style={{ padding: 12, borderRadius: 10, background: '#0b1021', color: '#e9ecf5', border: '1px solid #1f2640' }}
          />
        </label>

        <div style={{ display: 'flex', gap: 10, marginTop: 6 }}>
          <button
            type="submit"
            disabled={busy}
            style={{
              flex: 1,
              padding: 12,
              borderRadius: 10,
              background: '#4adede',
              color: '#0b1021',
              fontWeight: 700,
              cursor: 'pointer',
              opacity: busy ? 0.7 : 1,
            }}
          >
            {busy ? 'Please wait...' : mode === 'login' ? 'Login' : 'Create account'}
          </button>
          <button
            type="button"
            onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
            style={{
              padding: 12,
              borderRadius: 10,
              background: '#11162c',
              color: '#e9ecf5',
              border: '1px solid #1f2640',
              width: 160,
              cursor: 'pointer',
            }}
          >
            {mode === 'login' ? 'Register' : 'Back to login'}
          </button>
        </div>
      </form>
    </div>
  );
}
