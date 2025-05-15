import React from 'react';

export const Login = React.lazy(() => import('./login/Login'));
export const Dashboard = React.lazy(() => import('./dashboard/Dashboard'));
export const Dispatches = React.lazy(() => import('./Dispatches/Dispatches'));
export const ProductOrder = React.lazy(
  () => import('./ProductOrder/ProductOrder')
);
export const InternalMovement = React.lazy(
  () => import('./InternalMovement/InternalMovement')
);
export const LatestScannedProducts = React.lazy(
  () => import('./LatestScannedProducts/LatestScannedProducts')
);
export const Reading = React.lazy(() => import('./Reading/Reading'));
export const Drivers = React.lazy(() => import('./drivers/Drivers'));
export const Scanner = React.lazy(() => import('./scanner/Scanner'));

