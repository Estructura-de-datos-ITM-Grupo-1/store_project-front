import { Outlet } from 'react-router-dom';
import Sidebar from '../../components/SideBar/SideBar';
import Topbar from '../../components/TopBar/TopBar';

const Dashboard = () => {
  return (
    <>
      <Sidebar />
      <Topbar />
      <main className="pt-20 pl-0 sm:pl-64 md:pl-24 pr-8 w-full h-screen overflow-x-auto">
        <Outlet />
      </main>
    </>
  );
};

export default Dashboard;
