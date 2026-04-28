import { Routes, Route, Outlet } from 'react-router-dom';
import './App.css';
import Navbar  from './components/Navbar';
import Footer  from './components/Footer';
import HomePage   from './pages/HomePage';
import NailPage   from './pages/NailPage';
import TonguePage from './pages/TonguePage';
import SkinPage   from './pages/SkinPage';

/* ── Layout: Navbar + page content + Footer ── */
function Layout() {
  return (
    <div className="app">
      <Navbar />
      <div className="page-outlet">
        <Outlet />
      </div>
      <Footer />
    </div>
  );
}

/* ── Root Router ── */
function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/"       element={<HomePage />}   />
        <Route path="/nail"   element={<NailPage />}   />
        <Route path="/tongue" element={<TonguePage />} />
        <Route path="/skin"   element={<SkinPage />}   />
      </Route>
    </Routes>
  );
}

export default App;
