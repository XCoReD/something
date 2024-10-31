import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import Layout from './components/Layout';
import LoginPage from './pages/LoginPage';
import StorageListPage from './pages/StorageListPage';
import StorageEditPage from './pages/StorageEditPage';
import { UserRole } from './types';

function App() {
  const { isAuthenticated, user } = useAuth();

  if (!isAuthenticated) {
    return <LoginPage />;
  }

  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/storages" replace />} />
          <Route path="/storages" element={<StorageListPage />} />
          <Route 
            path="/storage/:id" 
            element={
              user.role === UserRole.VIEWER ? 
                <Navigate to="/storages" replace /> : 
                <StorageEditPage />
            } 
          />
          <Route path="*" element={<Navigate to="/storages" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;