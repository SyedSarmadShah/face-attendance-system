import React, { useEffect, useState } from 'react';
import { api } from '../api';
import TopBar from './TopBar';
import StatsCards from './StatsCards';
import AttendanceTable from './AttendanceTable';

export default function Dashboard({ user, onLogout, onToast }) {
  const [records, setRecords] = useState([]);
  const [stats, setStats] = useState(null);
  const [busyCamera, setBusyCamera] = useState(false);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const [attendanceRes, statsRes] = await Promise.all([api.attendance(), api.stats()]);
      setRecords(attendanceRes.records || []);
      setStats(statsRes);
    } catch (err) {
      onToast(err.message, 'danger');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const startCamera = async () => {
    setBusyCamera(true);
    try {
      const res = await api.startCamera();
      onToast(res.message || 'Camera started');
    } catch (err) {
      onToast(err.message, 'danger');
    } finally {
      setBusyCamera(false);
    }
  };

  return (
    <div style={{ paddingTop: 32, display: 'flex', flexDirection: 'column', gap: 16 }}>
      <TopBar user={user} onLogout={onLogout} />
      <StatsCards stats={stats} />

      <div className="card" style={{ padding: 16, display: 'flex', gap: 12, alignItems: 'center', marginTop: 12 }}>
        <div style={{ flex: 1 }}>
          <div style={{ color: '#e9ecf5', fontWeight: 700, marginBottom: 4 }}>Camera</div>
          <div style={{ color: '#9aa3c1', fontSize: 14 }}>Launch the face attendance camera. A desktop window will open; press q to quit.</div>
        </div>
        <button
          onClick={startCamera}
          disabled={busyCamera}
          style={{
            background: '#4adede',
            color: '#0b1021',
            border: 'none',
            padding: '10px 14px',
            borderRadius: 10,
            fontWeight: 700,
            cursor: 'pointer',
            minWidth: 140,
            opacity: busyCamera ? 0.7 : 1,
          }}
        >
          {busyCamera ? 'Starting...' : 'Open Camera'}
        </button>
      </div>

      <div>
        <div style={{ margin: '18px 0 8px', fontWeight: 700 }}>Attendance Records</div>
        {loading ? (
          <div style={{ color: '#9aa3c1' }}>Loading...</div>
        ) : (
          <AttendanceTable records={records} />
        )}
      </div>
    </div>
  );
}
