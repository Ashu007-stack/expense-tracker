import {useEffect,useMemo,useState} from "react";
import {ArrowRight,CalendarDays,Receipt,TrendingDown,Wallet,Tag,Lightbulb} from "lucide-react";
import {Link} from "react-router-dom";
import useAuth from "../context/useAuth";
import {getDashboardSummary,getExpenses} from "../services/api";
import {CATEGORIES,money,shortDate} from "../utils/format";
import "./FinancePages.css";

export default function Dashboard(){const {user}=useAuth();const [summary,setSummary]=useState(null);const [expenses,setExpenses]=useState([]);const [error,setError]=useState("");useEffect(()=>{Promise.all([getDashboardSummary(),getExpenses({limit:100})]).then(([s,e])=>{setSummary(s);setExpenses(e||[])}).catch(e=>setError(e.message));},[]);
const categoryData=useMemo(()=>CATEGORIES.map(category=>({category,total:expenses.filter(e=>e.category===category).reduce((a,e)=>a+Number(e.amount),0)})).filter(x=>x.total>0).sort((a,b)=>b.total-a.total).slice(0,5),[expenses]);
const max=categoryData[0]?.total||1; const recent=expenses.slice(0,5);
return <div className="finance-page"><div className="page-heading"><div><p className="eyebrow">OVERVIEW</p><h1>Hello, {user?.full_name?.split(" ")[0]||"there"}</h1><p>Here is your financial overview for today.</p></div><Link className="primary-btn compact" to="/expenses/add"> <Receipt size={16}/> Add Expense</Link></div>
{error&&<div className="error-banner">{error}</div>}
<div className="insight-card"><div className="insight-icon"><Lightbulb size={21}/></div><div><span>Spending Insight</span><p>{categoryData[0]?`Your highest spending category is ${categoryData[0].category} at ${money(categoryData[0].total)}.`:"Add your first expense to start seeing spending insights."}</p></div><ArrowRight size={19}/></div>
<div className="metric-grid"><Metric icon={Wallet} label="Total Spent" value={money(summary?.total_amount)}/><Metric icon={CalendarDays} label="This Month" value={money(summary?.this_month_total)}/><Metric icon={TrendingDown} label="Average Expense" value={money(summary?.average_expense)}/><Metric icon={Tag} label="Transactions" value={summary?.total_expenses??0}/></div>
<div className="two-column"><section className="panel"><div className="section-title"><div><p className="eyebrow">BREAKDOWN</p><h2>Top Categories</h2></div><Link to="/categories">View all <ArrowRight size={15}/></Link></div>{categoryData.length?categoryData.map(x=><div className="category-row" key={x.category}><div><span>{x.category}</span><b>{money(x.total)}</b></div><div className="progress"><i style={{width:`${(x.total/max)*100}%`}}/></div></div>):<Empty text="No category data yet."/>}</section>
<section className="panel"><div className="section-title"><div><p className="eyebrow">ACTIVITY</p><h2>Recent Expenses</h2></div><Link to="/expenses">View all <ArrowRight size={15}/></Link></div>{recent.length?recent.map(e=><ExpenseRow key={e.id} expense={e}/>):<Empty text="No expenses yet."/>}</section></div></div>}
function Metric({icon:Icon,label,value}){return <div className="metric-card"><div className="metric-icon"><Icon size={18}/></div><span>{label}</span><strong>{value}</strong></div>}
function ExpenseRow({expense}){return <div className="expense-row"><div className="expense-avatar">{expense.category?.slice(0,1)||"E"}</div><div><strong>{expense.title}</strong><span>{expense.category} • {shortDate(expense.expense_date)}</span></div><b>{money(expense.amount)}</b></div>}
function Empty({text}){return <div className="empty">{text}</div>}
