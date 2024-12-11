import React from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    // ... (logout logic from previous steps)
  };

  return (
    <div className="bg-blue-100 min-h-screen">
      {/* Header Section */}
      <header className="bg-blue-500 p-4 text-white flex justify-between items-center">
        <div className="flex items-center">
          {/* Inline SVG Ship Logo (Example) */}
          <svg
            className="w-12 h-12 mr-2"
            viewBox="0 0 100 100"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M10 50 C 20 20, 80 20, 90 50"
              stroke="white"
              strokeWidth="5"
            />
            <path d="M5 80 L 95 80" stroke="white" strokeWidth="3" />
            {/* Add more SVG paths for ship details */}
          </svg>
          <h1 className="text-xl font-bold">ShipKeep Co</h1>
        </div>
        <button
          onClick={handleLogout}
          className="bg-yellow-300 text-blue-800 px-4 py-2 rounded-md hover:bg-yellow-400"
        >
          Logout
        </button>
      </header>

      {/* Hero Banner */}
      <section className="p-8 text-center bg-blue-200">
        <h2 className="text-3xl font-bold text-blue-800 mb-4">
          Discover Your Dream Cruise
        </h2>
        <p className="text-lg text-blue-900 mb-6">
          Explore exotic destinations and book your perfect getaway.
        </p>
        <button className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">
          Explore Cruises
        </button>
      </section>

      {/* Featured Destinations */}
      <section className="p-8">
        <h3 className="text-2xl font-bold text-blue-800 mb-6">
          Featured Destinations
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Destination Card (Example) */}
          <div className="bg-white rounded-lg shadow-md p-4">
            <img
              src="https://via.placeholder.com/400x250"
              alt="Caribbean"
              className="w-full h-48 object-cover rounded-t-lg"
            />
            <div className="p-4">
              <h4 className="text-xl font-semibold text-blue-800">
                The Caribbean
              </h4>
              <p className="text-gray-700">From $799</p>
              <button className="mt-4 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-md">
                Book Now
              </button>
            </div>
          </div>
          {/* Repeat for other destinations */}
        </div>
      </section>

      {/* Why Choose Us? */}
      <section className="p-8 bg-blue-200">
        <h3 className="text-2xl font-bold text-blue-800 mb-6">
          Why Choose ShipKeep Co?
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 text-center">
          {/* Benefit Card (Example) */}
          <div className="p-4">
            <svg
              className="w-16 h-16 mx-auto mb-2 text-blue-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M9 5l7 7-7 7"
              />
            </svg>
            <h4 className="text-xl font-semibold text-blue-800">
              Best Price Guarantee
            </h4>
            <p className="text-gray-700">
              Find the lowest prices for your dream cruise.
            </p>
          </div>
          {/* Repeat for other benefits */}
        </div>
      </section>
    </div>
  );
}

export default Home;
