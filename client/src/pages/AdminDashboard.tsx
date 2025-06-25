import { useEffect, useState } from 'react';
import axios from 'axios';

export default function AdminDashboard() {
  const [users, setUsers] = useState([]);

  const fetchUsers = async () => {
    const token = localStorage.getItem('authToken');
    const res = await axios.get('http://localhost:5000/api/admin/users', {
      headers: { Authorization: `Bearer ${token}` },
    });
    setUsers(res.data);
  };

  const toggleSubscription = async (id: number, currentStatus: boolean) => {
    const token = localStorage.getItem('authToken');
    await axios.put(
      `http://localhost:5000/api/admin/users/${id}/subscription`,
      { subscription_active: !currentStatus },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    fetchUsers(); // refresh list
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Admin: Manage Users</h1>
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2">Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Toggle</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u: any) => (
            <tr key={u.id} className="border-t">
              <td className="p-2">{u.name}</td>
              <td>{u.email}</td>
              <td>{u.role}</td>
              <td>{u.subscription_active ? 'Active' : 'Expired'}</td>
              <td>
                <button
                  className="px-3 py-1 bg-blue-500 text-white rounded"
                  onClick={() => toggleSubscription(u.id, u.subscription_active)}
                >
                  {u.subscription_active ? 'Deactivate' : 'Activate'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
