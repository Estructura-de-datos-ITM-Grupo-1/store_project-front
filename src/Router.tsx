import { useRoutes } from 'react-router-dom';

import ClientsPage from './pages/Clients/ClientsPage';
import CashBalancingPage from './pages/CashBalancing/CashBalancingPage';
import ConfigModulePage from './pages/ConfigModule/ConfigModulePage';
import InventoryPage from './pages/Inventory/InventoryPage';
import ReportsPage from './pages/Resports/ReportsPage';
import ServicesPage from './pages/ServiceModule/ServicesPage';
import TaxPage from './pages/Tax/TaxPage';
import Login from './pages/login/Login';
import Dashboard from './pages/dashboard/Dashboard';

export const AppRouter = () => {
  const routes = useRoutes([
    {
      path: '/',
      element: <Login />,
    },
    
    {
      path: 'dashboard',
      element: <Dashboard />,
      children: [
        {
          path: 'clients',
          element: <ClientsPage />,
        },
        {
          path: 'cash-balancing',
          element: <CashBalancingPage />, // Debes crear o importar este componente
        },
        {
          path: 'config-module',
          element: <ConfigModulePage />, // Debes crear o importar este componente
        },
        {
          path: 'inventory',
          element: <InventoryPage />, // Debes crear o importar este componente
        },
        {
          path: 'reports',
          element: <ReportsPage />, // Debes crear o importar este componente
        },
        {
          path: 'services',
          element: <ServicesPage />, // Debes crear o importar este componente
        },
        {
          path: 'tax', // Este va fuera de dashboard
          element: <TaxPage />, // Debes crear o importar este componente
        },
      ],
    },
  ]);
  return routes;
};
