import React from "react";
import { Link } from "react-router-dom";

const SideBar: React.FC = () => {
  return (
    <div className="fixed top-0 left-0 h-full w-64 bg-gray-800 text-white shadow-lg">
      <div className="p-4">
        <h2 className="text-2xl font-bold">Sidebar</h2>
      </div>
      <nav className="mt-4">
        <ul>
          <li className="p-2 hover:bg-gray-700">
            <Link to="/dashboard">Dashboard</Link>
          </li>
          <li className="p-2 hover:bg-gray-700">
            <Link to="/profile">Profile</Link>
          </li>
          <li className="p-2 hover:bg-gray-700">
            <Link to="/settings">Settings</Link>
          </li>
          <li className="p-2 hover:bg-gray-700">
            <Link to="/logout">Logout</Link>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default SideBar;