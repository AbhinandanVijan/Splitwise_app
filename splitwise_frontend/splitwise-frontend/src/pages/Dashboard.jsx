import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const { token, logout } = useAuth();
  const [groups, setGroups] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const res = await axios.get("http://localhost:8000/api/v1/groups/my-groups", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setGroups(res.data);
      } catch (err) {
        console.error("Error fetching groups:", err);
        alert("Failed to load groups");
      }
    };

    fetchGroups();
  }, [token]);

  return (
    <div className="p-6 min-h-screen bg-gray-50">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Your Groups</h1>
        <button
          className="text-red-500 underline text-sm"
          onClick={() => {
            logout();
            navigate("/");
          }}
        >
          Logout
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {groups.length === 0 ? (
          <p className="text-gray-500">You are not part of any groups yet.</p>
        ) : (
          groups.map((group) => (
            <div
              key={group.id}
              className="bg-white shadow-md rounded-lg p-4 hover:shadow-lg cursor-pointer transition-all"
              onClick={() => navigate(`/group/${group.id}`)}
            >
              <h2 className="text-xl font-semibold">{group.name}</h2>
              <p className="text-sm text-gray-500">
                Created: {new Date(group.created_at).toLocaleDateString()}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
