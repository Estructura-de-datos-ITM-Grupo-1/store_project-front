import { BrowserRouter as Router } from 'react-router-dom';

import './App.css';
import { Suspense } from 'react';
import { AppRouter } from './Router';
import { Toaster } from 'sonner';

function App() {
  return (
    <>
      <Toaster richColors position="top-center" />
      <Router>
        <Suspense fallback={<div>Loading...</div>}>
          <AppRouter />
        </Suspense>
      </Router>
    </>
  );
}

export default App;
