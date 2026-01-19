import React from 'react';

export default function StatsCards({ stats }) {
  const items = [
    { label: 'Total Records', value: stats?.total_records ?? stats?.total_attendance_records ?? 0, icon: 'REC' },
    { label: 'Today', value: stats?.today_attendance ?? 0, icon: 'DAY' },
    { label: 'Unique People', value: stats?.unique_people ?? 0, icon: 'PEP' },
    { label: 'Faces in Dataset', value: stats?.total_faces_in_dataset ?? (stats?.dataset_faces ? Object.keys(stats.dataset_faces).length : 0), icon: 'IMG' },
  ];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 14 }}>
      {items.map((item) => (
        <div key={item.label} className="card" style={{ padding: 16 }}>
          <div style={{ fontSize: 14, color: '#9aa3c1' }}>{item.label}</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginTop: 8 }}>
            <div style={{ fontSize: 13, letterSpacing: 1, color: '#9aa3c1', border: '1px solid #1f2640', padding: '6px 10px', borderRadius: 10 }}>{item.icon}</div>
            <div style={{ fontSize: 28, fontWeight: 800 }}>{item.value}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
