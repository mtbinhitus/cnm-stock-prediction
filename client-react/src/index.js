import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, Navigate, RouterProvider } from "react-router-dom";
import Homepage from "./pages/Homepage.js";
import Prediction from "./pages/Prediction.js";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/search/BINANCE:BTCUSDT" />
  },
  {
    path: "/search/:symbol",
    element: <Homepage />
  },
  {
    path: "/prediction",
    element: <Prediction />
  }
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);