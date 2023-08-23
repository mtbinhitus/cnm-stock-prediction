import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, Navigate, RouterProvider } from "react-router-dom";
import App from "./App.js";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/search/BINANCE:BTCUSDT" />
  },
  {
    path: "/search/:symbol",
    element: <App />
  },
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);