import React, { useEffect, useState } from 'react';
import { api } from '../api';

export default function AdminPanel({ onToast }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editUser, setEditUser] = useState(null);
  const [formData, setFormData] = useState({ username: '', password: '', role: 'student' });

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const result = await api.admin.getUsers();
      setUsers(result.users);
    } catch (err) {
      onToast(err.message || 'Failed to load users', 'danger');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.admin.createUser(formData.username, formData.password, formData.role);
      onToast('User created successfully', 'success');
      setShowCreateModal(false);
      setFormData({ username: '', password: '', role: 'student' });
      loadUsers();
    } catch (err) {
      onToast(err.message, 'danger');
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await api.admin.updateUser(editUser.id, { 
        role: formData.role, 
        password: formData.password || undefined 
      });
      onToast('User updated successfully', 'success');
      setEditUser(null);
      setFormData({ username: '', password: '', role: 'student' });
      loadUsers();
    } catch (err) {
      onToast(err.message, 'danger');
    }
  };

  const handleDelete = async (userId, username) => {
    if (!confirm(`Delete user "${username}"?`)) return;
    try {
      await api.admin.deleteUser(userId);
      onToast('User deleted', 'success');
      loadUsers();
    } catch (err) {
      onToast(err.message, 'danger');
    }
  };

  const getRoleBadge = (role) => {
    const colors = { admin: '#ff6b9d', teacher: '#4adede', student: '#feca57' };
    return (
      <span style={{ 
        padding: '4px 12px', 
        borderRadius: 12, 
        background: colors[role] || '#9aa3c1', 
        color: '#0b1021', 
        fontSize: 12, 
        fontWeight: 600 
      }}>
        {role}
      </span>
    );
  };

  if (loading) {
    return <div style={{ padding: 40, textAlign: 'center', color: '#9aa3c1' }}>Loading users...</div>;
  }

  return (
    <div style={{ padding: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2 style={{ fontSize: 24, margin: 0 }}>👥 User Management</h2>
        <button
          onClick={() => setShowCreateModal(true)}
          style={{ 
            padding: '10px 20px', 
            borderRadius: 8, 
            background: '#4adede', 
            color: '#0b1021', 
            fontWeight: 600, 
            cursor: 'pointer' 
          }}
        >
          ➕ Create User
        </button>
      </div>

      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#11162c', borderBottom: '1px solid #1f2640' }}>
              <th style={{ padding: 16, textAlign: 'left', color: '#9aa3c1', fontWeight: 600 }}>Username</th>
              <th style={{ padding: 16, textAlign: 'left', color: '#9aa3c1', fontWeight: 600 }}>Role</th>
              <th style={{ padding: 16, textAlign: 'left', color: '#9aa3c1', fontWeight: 600 }}>Created</th>
              <th style={{ padding: 16, textAlign: 'right', color: '#9aa3c1', fontWeight: 600 }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id} style={{ borderBottom: '1px solid #1f2640' }}>
                <td style={{ padding: 16 }}>{user.username}</td>
                <td style={{ padding: 16 }}>{getRoleBadge(user.role)}</td>
                <td style={{ padding: 16, color: '#9aa3c1' }}>{new Date(user.created_at).toLocaleDateString()}</td>
                <td style={{ padding: 16, textAlign: 'right' }}>
                  <button
                    onClick={() => {
                      setEditUser(user);
                      setFormData({ username: user.username, password: '', role: user.role });
                    }}
                    style={{ 
                      padding: '6px 12px', 
                      marginRight: 8, 
                      borderRadius: 6, 
                      background: '#11162c', 
                      color: '#4adede', 
                      border: '1px solid #1f2640', 
                      cursor: 'pointer' 
                    }}
                  >
                    ✏️ Edit
                  </button>
                  <button
                    onClick={() => handleDelete(user.id, user.username)}
                    style={{ 
                      padding: '6px 12px', 
                      borderRadius: 6, 
                      background: '#11162c', 
                      color: '#ff6b9d', 
                      border: '1px solid #1f2640', 
                      cursor: 'pointer' 
                    }}
                  >
                    🗑️ Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Create User Modal */}
      {showCreateModal && (
        <div style={{ 
          position: 'fixed', 
          top: 0, 
          left: 0, 
          right: 0, 
          bottom: 0, 
          background: 'rgba(0,0,0,0.7)', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center', 
          zIndex: 1000 
        }}>
          <div className="card" style={{ padding: 32, width: 400, maxWidth: '90%' }}>
            <h3 style={{ marginBottom: 20 }}>Create New User</h3>
            <form onSubmit={handleCreate} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <input
                placeholder="Username"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                required
                style={{ padding: 12, borderRadius: 8, background: '#0b1021', color: '#e9ecf5', border: '1px solid #1f2640' }}
              />
              <input
                type="password"
                placeholder="Password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required
                style={{ padding: 12, borderRadius: 8, background: '#0b1021', color: '#e9ecf5', border: '1px solid #1f2640' }}
              />
              <select
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                style={{ padding: 12, borderRadius: 8, background: '#0b1021', color: '#e9ecf5', border: '1px solid #1f2640' }}
              >
                <option value="student">Student</option>
                <option value="teacher">Teacher</option>
                <option value="admin">Admin</option>
              </select>
              <div style={{ display: 'flex', gap: 10, marginTop: 10 }}>
                <button
                  type="submit"
                  style={{ flex: 1, padding: 12, borderRadius: 8, background: '#4adede', color: '#0b1021', fontWeight: 600, cursor: 'pointer' }}
                >
                  Create
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  style={{ flex: 1, padding: 12, borderRadius: 8, background: '#11162c', color: '#e9ecf5', border: '1px solid #1f2640', cursor: 'pointer' }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit User Modal */}
      {editUser && (
        <div style={{ 
          position: 'fixed', 
          top: 0, 
          left: 0, 
          right: 0, 
          bottom: 0, 
          background: 'rgba(0,0,0,0.7)', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center', 
          zIndex: 1000 
        }}>
          <div className="card" style={{ padding: 32, width: 400, maxWidth: '90%' }}>
            <h3 style={{ marginBottom: 20 }}>Edit User: {editUser.username}</h3>
            <form onSubmit={handleUpdate} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <input
                type="password"
                placeholder="New Password (leave empty to keep current)"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                style={{ padding: 12, borderRadius: 8, background: '#0b1021', color: '#e9ecf5', border: '1px solid #1f2640' }}
              />
              <select
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                style={{ padding: 12, borderRadius: 8, background: '#0b1021', color: '#e9ecf5', border: '1px solid #1f2640' }}
              >
                <option value="student">Student</option>
                <option value="teacher">Teacher</option>
                <option value="admin">Admin</option>
              </select>
              <div style={{ display: 'flex', gap: 10, marginTop: 10 }}>
                <button
                  type="submit"
                  style={{ flex: 1, padding: 12, borderRadius: 8, background: '#4adede', color: '#0b1021', fontWeight: 600, cursor: 'pointer' }}
                >
                  Update
                </button>
                <button
                  type="button"
                  onClick={() => setEditUser(null)}
                  style={{ flex: 1, padding: 12, borderRadius: 8, background: '#11162c', color: '#e9ecf5', border: '1px solid #1f2640', cursor: 'pointer' }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
