import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import AppLayout from "./layouts/AppLayout";
import Dashboard from "./pages/Dashboard";
import Expenses from "./pages/Expenses";
import AddExpense from "./pages/AddExpense";
import Analytics from "./pages/Analytics";
import Categories from "./pages/Categories";
import Profile from "./pages/Profile";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import VerifyOTP from "./pages/VerifyOTP";
import AuthProvider from "./context/AuthProvider";
import useAuth from "./context/useAuth";
import "./App.css";

function Protected({children}){const {user,loading}=useAuth();if(loading)return <div className="route-loading">Loading...</div>;return user?children:<Navigate to="/login" replace/>}
function Public({children}){const {user,loading}=useAuth();if(loading)return <div className="route-loading">Loading...</div>;return user?<Navigate to="/dashboard" replace/>:children}
export default function App(){return <AuthProvider><BrowserRouter><Routes>
<Route path="/login" element={<Public><Login/></Public>}/><Route path="/signup" element={<Public><Signup/></Public>}/><Route path="/verify-otp" element={<Public><VerifyOTP/></Public>}/>
<Route element={<Protected><AppLayout/></Protected>}><Route path="/" element={<Navigate to="/dashboard" replace/>}/><Route path="/dashboard" element={<Dashboard/>}/><Route path="/expenses" element={<Expenses/>}/><Route path="/expenses/add" element={<AddExpense/>}/><Route path="/analytics" element={<Analytics/>}/><Route path="/categories" element={<Categories/>}/><Route path="/profile" element={<Profile/>}/></Route>
<Route path="*" element={<Navigate to="/dashboard" replace/>}/></Routes></BrowserRouter></AuthProvider>}
