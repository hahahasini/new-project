import { useState, useEffect } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';

const NAV_LINKS = [
  { to: '/nail', label: 'Nail Analysis', id: 'nav-nail' },
  { to: '/tongue', label: 'Tongue Analysis', id: 'nav-tongue' },
  { to: '/skin', label: 'Skin Analysis', id: 'nav-skin' },
];

function SunIcon() {
  return (
    <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="5" />
      <line x1="12" y1="1" x2="12" y2="3" />
      <line x1="12" y1="21" x2="12" y2="23" />
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
      <line x1="1" y1="12" x2="3" y2="12" />
      <line x1="21" y1="12" x2="23" y2="12" />
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
    </svg>
  );
}

function MoonIcon() {
  return (
    <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </svg>
  );
}

function Navbar() {
  const { theme, toggleTheme } = useTheme();
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const handleLinkClick = () => setMenuOpen(false);

  return (
    <header className={`navbar ${scrolled ? 'navbar--scrolled' : ''}`} id="app-navbar">
      <div className="navbar-inner">

        {/* Logo */}
        <Link to="/" className="navbar-logo" id="nav-home" onClick={handleLinkClick}>

          <span className="navbar-logo-text">VitaDetect</span>

        </Link>

        {/* Desktop Links */}
        <nav className="navbar-links" aria-label="Main navigation">
          {NAV_LINKS.map(({ to, label, id }) => (
            <NavLink
              key={to}
              to={to}
              id={id}
              className={({ isActive }) => `nav-link ${isActive ? 'nav-link--active' : ''}`}
            >
              <span className="nav-link-label">{label}</span>
            </NavLink>
          ))}
        </nav>

        {/* Right controls */}
        <div className="navbar-controls">
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label={theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'}
            id="theme-toggle-btn"
            title={theme === 'dark' ? 'Light mode' : 'Dark mode'}
          >
            {theme === 'dark' ? <SunIcon /> : <MoonIcon />}
          </button>

          <button
            className={`hamburger ${menuOpen ? 'hamburger--open' : ''}`}
            onClick={() => setMenuOpen(v => !v)}
            aria-label="Toggle navigation"
            aria-expanded={menuOpen}
            id="hamburger-btn"
          >
            <span /><span /><span />
          </button>
        </div>
      </div>

      {/* Mobile Dropdown */}
      <div className={`mobile-menu ${menuOpen ? 'mobile-menu--open' : ''}`} aria-hidden={!menuOpen}>
        {NAV_LINKS.map(({ to, label, id }) => (
          <NavLink
            key={to}
            to={to}
            id={`mobile-${id}`}
            className={({ isActive }) => `mobile-nav-link ${isActive ? 'nav-link--active' : ''}`}
            onClick={handleLinkClick}
          >
            {label}
          </NavLink>
        ))}
      </div>
    </header>
  );
}

export default Navbar;
