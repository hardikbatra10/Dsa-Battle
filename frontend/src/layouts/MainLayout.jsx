import { Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar/Navbar';
import Footer from '../components/Footer/Footer';

// Standard page chrome: navbar + centered content column + footer.
// Used for every route except the full-height contest page.
export default function MainLayout() {
  return (
    <>
      <Navbar />
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8 sm:px-6">
        <Outlet />
      </main>
      <Footer />
    </>
  );
}
