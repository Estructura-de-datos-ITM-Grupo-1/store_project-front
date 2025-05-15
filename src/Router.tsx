import { useRoutes } from 'react-router-dom';
import {
  Dashboard,
  Dispatches,
  Drivers,
  InternalMovement,
  LatestScannedProducts,
  Login,
  ProductOrder,
  Reading,
  Scanner,
} from './pages';

export const AppRouter = () => {
  const routes = useRoutes([
    {
      path: '/',
      element: <Login />,
    },
    {
      path: 'conductores',
      element: <Drivers />,
    },
    {
      path: 'dashboard',
      element: <Dashboard />,
      children: [
        {
          path: 'productos-escaneados',
          element: <LatestScannedProducts />,
        },
        {
          path: 'orden-producto',
          element: <ProductOrder />,
        },
        {
          path: 'movimiento-interno',
          element: <InternalMovement />,
        },
        {
          path: 'despachos',
          element: <Dispatches />,
        },
        {
          path: 'lectura',
          element: <Reading />,
        },
        {
          path: 'scanner',
          element: <Scanner />,
        },
      ],
    },
  ]);
  return routes;
};
