import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/AuthContext";

export default function GroupDetail() {
  const { id } = useParams(); // group ID from URL
  const { token } = useAuth();
  const [groupName, setGroupName] = useState("");
//   const [groupUsers, setGroupUsers] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [balances, setBalances] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    amount: "",
    description: "",
    split_type: "equal",
    split_details: {}, // { user_id: amount }
    });

  const [settleForm, setSettleForm] = useState({
        payer: "",
        payee: "",
        amount: "",
        payer_id: "",
        payee_id: "",
          
      });

    const [groupUsers, setGroupUsers] = useState([
        {
            username: "",
            email: "",
            id: "",
            created_at: ""
          }
    ]);
      


  useEffect(() => {
    if (!token) return;

    const fetchGroupData = async () => {
      try {
        // 1. Get expenses
        const expRes = await axios.get(`http://localhost:8000/api/v1/expenses/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setExpenses(expRes.data);
        if (expRes.data.length > 0) {
          setGroupName(`Group #${expRes.data[0].group_id}`);
        }

        // 2. Get balances
        const balRes = await axios.get(`http://localhost:8000/api/v1/groups/${id}/balances`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setBalances(balRes.data);
      } catch (err) {
        console.error(err);
        alert("Failed to fetch group data");
      }
      // 3. Getting group members
      const userRes = await axios.get(`http://localhost:8000/api/v1/groups/${id}/users`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      console.log(userRes.data)
      setGroupUsers(userRes.data);
      
    };

    fetchGroupData();
  }, [id, token]);

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">{groupName}</h1>

      <h2 className="text-xl font-semibold mb-2">Expenses</h2>
      {expenses.length === 0 ? (
        <p className="text-gray-500 mb-4">No expenses yet.</p>
      ) : (
        <ul className="space-y-2 mb-6">
          {expenses.map((exp) => (
            <li key={exp.id} className="bg-white shadow rounded p-3">
              <div className="flex justify-between">
                <span className="font-semibold">{exp.description}</span>
                <span className="text-gray-600">₹{exp.amount}</span>
              </div>
              <div className="text-xs text-gray-400">
                Paid by User ID: {exp.payer_id}
              </div>
            </li>
          ))}
        </ul>
      )}

      <h2 className="text-xl font-semibold mb-2">Balances</h2>
      <div className="mt-6 bg-white p-4 rounded shadow-md">
  <h3 className="text-lg font-semibold mb-2">Settle Up</h3>

  <select
  className="w-full p-2 mb-2 border rounded"
  value={settleForm.payer_id}
  onChange={(e) =>
    setSettleForm({ ...settleForm, payer_id: parseInt(e.target.value) })
  }
>
  <option value="">Select Payer</option>
  {groupUsers.map((user) => (
    <option key={user.id} value={user.id}>
      {user.username}
    </option>
  ))}
</select>




<select
  className="w-full p-2 mb-2 border rounded"
  value={settleForm.payee_id}
  onChange={(e) =>
    setSettleForm({ ...settleForm, payee_id: parseInt(e.target.value) })
  }
>
  <option value="">Select Payee</option>
  {groupUsers
    .filter((user) => user.id !== settleForm.payer_id)
    .map((user) => (
      <option key={user.id} value={user.id}>
        {user.username}
      </option>
    ))}
</select>


  <input
    type="number"
    placeholder="Amount"
    className="w-full p-2 border mb-2 rounded"
    value={settleForm.amount}
    onChange={(e) => setSettleForm({ ...settleForm, amount: e.target.value })}
  />

  <button
    className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
    onClick={async () => {
      try {

        // console.log("Settlement request: \n");
        // console.log("settleForm.payer_id: "+ settleForm.payer_id);
        // console.log("settleForm.payee_id: "+ settleForm.payee_id,);
        await axios.post("http://localhost:8000/api/v1/settlement/settle_up", {
          group_id: parseInt(id),
        //   payer_username: settleForm.payer,
        //   payee_username: settleForm.payee,
          payer_id: settleForm.payer_id,
          payee_id: settleForm.payee_id,
          amount: parseFloat(settleForm.amount),
        }, {
          headers: { Authorization: `Bearer ${token}` },
        });
        
        console.log("Settle payload:", {
            group_id: parseInt(id),
            payer_id: settleForm.payer_id,
            payee_id: settleForm.payee_id,
            amount: parseFloat(settleForm.amount)
          });
          

        alert("Settlement recorded!");
        window.location.reload();
      } catch (err) {
        console.error(err);
        alert("Failed to record settlement");
      }
    }}
  >
    Submit
  </button>
</div>

      {balances.length === 0 ? (
        <p className="text-gray-500">All settled!</p>
      ) : (
        <ul className="space-y-1">
          {balances.map((bal, idx) => (
            <li
              key={idx}
              className={`text-sm ${
                bal.balance < 0 ? "text-red-500" : "text-green-600"
              }`}
            >
              {bal.user} {bal.balance < 0 ? "owes" : "is owed"} ₹
              {Math.abs(bal.balance).toFixed(2)}
            </li>
          ))}
        </ul>
      )}

        <button 
        className="mt-6 mb-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        onClick={() => setShowForm(!showForm)}
        >
        {showForm ? "Cancel" : "Add Expense"}
        </button>

        {showForm && (
    <div className="bg-white p-4 rounded shadow-md mb-6">
        <h3 className="text-lg font-semibold mb-2">Add New Expense</h3>

        <input
        type="number"
        placeholder="Amount"
        className="w-full p-2 border mb-2 rounded"
        value={formData.amount}
        onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
        />

        <input
        type="text"
        placeholder="Description"
        className="w-full p-2 border mb-2 rounded"
        value={formData.description}
        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
        />

        <select
        className="w-full p-2 border mb-2 rounded"
        value={formData.split_type}
        onChange={(e) => setFormData({ ...formData, split_type: e.target.value })}
        >
        <option value="equal">Equal</option>
        <option value="unequal">Unequal</option>
        <option value="percentage">Percentage</option>
        </select>

        {formData.split_type !== "equal" && (
        <div className="mb-2">
            <p className="text-sm text-gray-600 mb-1">Split Details:</p>
            {balances.map((bal) => (
            <div key={bal.user} className="flex items-center mb-1">
                <span className="w-1/2">{bal.user}</span>
                <input
                type="number"
                className="w-1/2 p-1 border rounded"
                placeholder="Amount / %"
                onChange={(e) => {
                    const updated = { ...formData.split_details };
                    updated[bal.user] = parseFloat(e.target.value);
                    setFormData({ ...formData, split_details: updated });
                }}
                />
            </div>
            ))}
        </div>
        )}

        <button
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        onClick={async () => {
            try {
            await axios.post("http://localhost:8000/api/v1/expenses/", {
                amount: parseFloat(formData.amount),
                description: formData.description,
                group_id: parseInt(id),
                split_type: formData.split_type,
                split_details: formData.split_type === "equal" ? null : formData.split_details,
            }, {
                headers: { Authorization: `Bearer ${token}` },
            });

            alert("Expense added!");
            window.location.reload();
            } catch (err) {
            console.error(err);
            alert("Failed to add expense");
            }
        }}
        >
        Submit
        </button>
    </div>
    )}



    </div>
  );
}
