import { useState } from 'react';
import { useAuth } from './contexts/AuthContext';
import Login from './pages/Login';
import Chat from './pages/Chat';
import NeuralVault from './pages/NeuralVault';
import Integrations from './pages/Integrations';
import Settings from './pages/Settings';
import Sidebar from './components/Sidebar';

function App() {
  const { user, loading } = useAuth();
  const [currentPage, setCurrentPage] = useState('chat');

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-white text-lg">Carregando...</div>
      </div>
    );
  }

  // Comentado para facilitar os testes conforme solicitado
  // if (!user) {
  //   return <Login />;
  // }

  const renderPage = () => {
    switch (currentPage) {
      case 'chat':
        return <Chat />;
      case 'vault':
        return <NeuralVault />;
      case 'integrations':
        return <Integrations />;
      case 'settings':
        return <Settings />;
      default:
        return <Chat />;
    }
  };

  return (
    <div className="min-h-screen bg-black flex">
      <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />
      {renderPage()}
    </div>
  );
}

export default App;
