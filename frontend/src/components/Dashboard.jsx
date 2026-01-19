import React, { useEffect, useState } from 'react';
import { api } from '../api';
import TopBar from './TopBar';
import StatsCards from './StatsCards';
import AttendanceTable from './AttendanceTable';
import Analytics from './Analytics';

export default function Dashboard({ user, onLogout, onToast }) {
  const [records, setRecords] = useState([]);
  const [stats, setStats] = useState(null);
  const [busyCamera, setBusyCamera] = useState(false);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('attendance');

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

      {/* Tab Navigation */}
      <div className="card" style={{ padding: 0, display: 'flex', gap: 0 }}>
        <button
          onClick={() => setActiveTab('attendance')}
          style={{
            flex: 1,
            padding: '12px 24px',
            background: activeTab === 'attendance' ? '#4adede' : 'transparent',
            color: activeTab === 'attendance' ? '#0b1021' : '#9aa3c1',
            border: 'none',
            borderRadius: '12px 0 0 12px',
            cursor: 'pointer',
            fontWeight: 600
          }}
        >
          📋 Attendance Records
        </button>
        <button
          onClick={() => setActiveTab('analytics')}
          style={{
            flex: 1,
            padding: '12px 24px',
            background: activeTab === 'analytics' ? '#4adede' : 'transparent',
            color: activeTab === 'analytics' ? '#0b1021' : '#9aa3c1',
            border: 'none',
            borderRadius: '0 12px 12px 0',
            cursor: 'pointer',
            fontWeight: 600
          }}
        >
          📊 Analytics
        </button>
      </div>

      {activeTab === 'attendance' && (
        <>
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
        </>
      )}

      {activeTab === 'analytics' && <Analytics onToast={onToast} />}
    </div>
  );
}
