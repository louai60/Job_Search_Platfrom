import React from "react";

const TestComponent: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <h1 className="text-4xl font-bold text-blue-600">Tailwind CSS is working!</h1>
      <p className="mt-4 text-lg text-gray-700">This is a test component.</p>
      <button className="mt-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
        Click Me
      </button>
    </div>
  );
};

export default TestComponent;
