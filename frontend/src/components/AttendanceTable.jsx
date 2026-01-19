import React from 'react';

export default function AttendanceTable({ records }) {
  if (!records || records.length === 0) {
    return (
      <div className="card" style={{ padding: 20, marginTop: 16 }}>
        <div style={{ color: '#9aa3c1' }}>No attendance records yet.</div>
      </div>
    );
  }

  return (
    <div className="card" style={{ padding: 0, marginTop: 16, overflowX: 'auto' }}>
      <table className="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Date</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {records.map((r, idx) => (
            <tr key={`${r.Name}-${r.Date}-${r.Time}-${idx}`}>
              <td>{r.Name}</td>
              <td>{r.Date}</td>
              <td>{r.Time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
