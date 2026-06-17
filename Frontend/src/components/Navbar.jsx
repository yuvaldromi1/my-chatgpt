import { NavLink } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="navbar">
      <span className="navbar-brand">🤖 My ChatGPT</span>
      <div className="navbar-links">
        <NavLink to="/" end>
          בית
        </NavLink>
        <NavLink to="/about">אודות</NavLink>
      </div>
    </nav>
  )
}
