import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { LayoutDashboard, Receipt, BarChart3, Tags, UserRound, Plus, LogOut } from "lucide-react";
import useAuth from "../context/useAuth";
import logo from "../assets/logo.png";
import "./AppLayout.css";

const navigation=[{name:"Dashboard",path:"/dashboard",icon:LayoutDashboard},{name:"Expenses",path:"/expenses",icon:Receipt},{name:"Analytics",path:"/analytics",icon:BarChart3},{name:"Categories",path:"/categories",icon:Tags},{name:"Profile",path:"/profile",icon:UserRound}];
function NavigationItem({item}){const Icon=item.icon;return <NavLink to={item.path} className={({isActive})=>`navigation-item ${isActive?"active":""}`}><Icon size={19}/><span>{item.name}</span></NavLink>}
export default function AppLayout(){const {user,logout}=useAuth();const navigate=useNavigate();const initials=(user?.full_name||"U").split(" ").map(x=>x[0]).slice(0,2).join("").toUpperCase();function handleLogout(){logout();navigate("/login",{replace:true})}return <div className="app-shell">
<header className="topbar"><div className="brand"><img src={logo} className="brand-logo" alt="Expense Tracker"/><div><strong>Expense Tracker</strong><small>Smart money management</small></div></div><div className="topbar-user"><div className="user-copy"><strong>{user?.full_name||"User"}</strong><span>{user?.email||""}</span></div><NavLink to="/profile" className="user-avatar" aria-label="Profile">{initials}</NavLink></div></header>
<aside className="sidebar"><div><p className="sidebar-label">WORKSPACE</p><nav>{navigation.map(item=><NavigationItem key={item.path} item={item}/>)}</nav></div><div className="sidebar-bottom"><NavLink to="/expenses/add" className="sidebar-add"><Plus size={18}/><span>Add Expense</span></NavLink><button className="sidebar-logout" onClick={handleLogout}><LogOut size={17}/><span>Sign out</span></button></div></aside>
<main className="main-content"><Outlet/></main>
<NavLink to="/expenses/add" className="floating-add" aria-label="Add Expense"><Plus size={24}/></NavLink>
<nav className="mobile-navigation">{navigation.map(item=><NavigationItem key={item.path} item={item}/>)}</nav>
</div>}
