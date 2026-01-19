import React from 'react';

export default function TopBar({ user, onLogout }) {
  const getRoleBadge = (role) => {
    const styles = {
      admin: { bg: '#ff6b9d', text: '👑 Admin' },
      teacher: { bg: '#4adede', text: '👨‍🏫 Teacher' },
      student: { bg: '#feca57', text: '🎓 Student' }
    };
    const style = styles[role] || styles.student;
    return (
      <span style={{ 
        padding: '4px 12px', 
        marginLeft: 8,
        borderRadius: 12, 
        background: style.bg, 
        color: '#0b1021', 
        fontSize: 12, 
        fontWeight: 700 
      }}>
        {style.text}
      </span>
    );
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 }}>
      <div>
        <div style={{ color: '#9aa3c1', fontSize: 13 }}>Logged in as</div>
        <div style={{ fontSize: 20, fontWeight: 700, display: 'flex', alignItems: 'center' }}>
          {user.username}
          {getRoleBadge(user.role)}
        </div>
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
