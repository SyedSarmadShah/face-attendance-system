import React, { useEffect, useState } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { api } from '../api';

export default function Analytics({ onToast }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(30);

  useEffect(() => {
    loadAnalytics();
  }, [days]);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const result = await api.analytics(days);
      setData(result);
    } catch (err) {
      onToast('Failed to load analytics', 'danger');
    } finally {
      setLoading(false);
    }
  };

  const exportCSV = () => {
    if (!data || !data.daily_trend) return;
    
    const csv = [
      ['Date', 'Attendance Count'],
      ...data.daily_trend.map(d => [d.date, d.count])
    ].map(row => row.join(',')).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `attendance_analytics_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    onToast('CSV exported successfully', 'success');
  };

  if (loading) {
    return <div style={{ padding: 40, textAlign: 'center', color: '#9aa3c1' }}>Loading analytics...</div>;
  }

  if (!data) {
    return <div style={{ padding: 40, textAlign: 'center', color: '#9aa3c1' }}>No data available</div>;
  }

  const COLORS = ['#4adede', '#ff6b9d', '#feca57', '#48dbfb', '#ff9ff3'];

  return (
    <div style={{ padding: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2 style={{ fontSize: 24, margin: 0 }}>📊 Analytics Dashboard</h2>
        <div style={{ display: 'flex', gap: 12 }}>
          <select 
            value={days} 
            onChange={(e) => setDays(Number(e.target.value))}
            style={{ padding: '8px 12px', borderRadius: 8, background: '#11162c', color: '#e9ecf5', border: '1px solid #1f2640' }}
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
          <button
            onClick={exportCSV}
            style={{ padding: '8px 16px', borderRadius: 8, background: '#4adede', color: '#0b1021', fontWeight: 600, cursor: 'pointer' }}
          >
            📥 Export CSV
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 24 }}>
        <div className="card" style={{ padding: 20 }}>
          <div style={{ color: '#9aa3c1', fontSize: 12, marginBottom: 4 }}>Attendance Rate</div>
          <div style={{ fontSize: 28, fontWeight: 700, color: '#4adede' }}>{data.attendance_rate}%</div>
        </div>
        <div className="card" style={{ padding: 20 }}>
          <div style={{ color: '#9aa3c1', fontSize: 12, marginBottom: 4 }}>Avg Daily Attendance</div>
          <div style={{ fontSize: 28, fontWeight: 700, color: '#ff6b9d' }}>{data.avg_daily_attendance}</div>
        </div>
        <div className="card" style={{ padding: 20 }}>
          <div style={{ color: '#9aa3c1', fontSize: 12, marginBottom: 4 }}>Total Registered</div>
          <div style={{ fontSize: 28, fontWeight: 700, color: '#feca57' }}>{data.total_registered}</div>
        </div>
      </div>

      {/* Daily Trend Chart */}
      <div className="card" style={{ padding: 20, marginBottom: 24 }}>
        <h3 style={{ fontSize: 16, marginBottom: 16 }}>📈 Daily Attendance Trend</h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={data.daily_trend}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2640" />
            <XAxis dataKey="date" stroke="#9aa3c1" />
            <YAxis stroke="#9aa3c1" />
            <Tooltip contentStyle={{ background: '#11162c', border: '1px solid #1f2640', borderRadius: 8 }} />
            <Legend />
            <Line type="monotone" dataKey="count" stroke="#4adede" strokeWidth={2} name="Attendance" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 16 }}>
        {/* Weekly Summary */}
        <div className="card" style={{ padding: 20 }}>
          <h3 style={{ fontSize: 16, marginBottom: 16 }}>📅 Weekly Summary</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={data.weekly_summary}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2640" />
              <XAxis dataKey="week" stroke="#9aa3c1" />
              <YAxis stroke="#9aa3c1" />
              <Tooltip contentStyle={{ background: '#11162c', border: '1px solid #1f2640', borderRadius: 8 }} />
              <Bar dataKey="count" fill="#4adede" name="Attendance" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Attendance by Person */}
        <div className="card" style={{ padding: 20 }}>
          <h3 style={{ fontSize: 16, marginBottom: 16 }}>👤 Attendance by Person</h3>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                data={data.attendance_by_person}
                dataKey="count"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label={(entry) => `${entry.name}: ${entry.count}`}
              >
                {data.attendance_by_person.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: '#11162c', border: '1px solid #1f2640', borderRadius: 8 }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Peak Times */}
        {data.peak_times && data.peak_times.length > 0 && (
          <div className="card" style={{ padding: 20 }}>
            <h3 style={{ fontSize: 16, marginBottom: 16 }}>⏰ Peak Attendance Times</h3>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={data.peak_times}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2640" />
                <XAxis dataKey="hour" stroke="#9aa3c1" label={{ value: 'Hour', position: 'insideBottom', offset: -5 }} />
                <YAxis stroke="#9aa3c1" />
                <Tooltip contentStyle={{ background: '#11162c', border: '1px solid #1f2640', borderRadius: 8 }} />
                <Bar dataKey="count" fill="#ff6b9d" name="Check-ins" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
}
