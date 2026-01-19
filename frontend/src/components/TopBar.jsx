import React from 'react';

export default function TopBar({ user, onLogout }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 }}>
      <div>
        <div style={{ color: '#9aa3c1', fontSize: 13 }}>Logged in as</div>
        <div style={{ fontSize: 20, fontWeight: 700 }}>{user.username}</div>
      </div>
      <button
        onClick={onLogout}
        style={{
          background: '#ff6b6b',
          color: '#0b1021',
          border: 'none',
          padding: '10px 14px',
          borderRadius: 10,
          fontWeight: 700,
          cursor: 'pointer',
        }}
      >
        Logout
      </button>
    </div>
  );
}
