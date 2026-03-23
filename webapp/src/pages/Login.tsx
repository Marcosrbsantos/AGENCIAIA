import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { signIn, signUp } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isSignUp) {
        await signUp(email, password);
      } else {
        await signIn(email, password);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao autenticar');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="backdrop-blur-xl bg-white/5 rounded-3xl p-8 border border-white/10 shadow-2xl">
          <div className="text-center mb-8">
            <h1 className="text-white text-3xl font-light tracking-wider mb-2"
                style={{ textShadow: '0 0 20px rgba(148, 0, 0, 0.5)' }}>
              AGENCIAIA
            </h1>
            <p className="text-gray-400 text-sm">A Porta de Entrada do Mestre</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="E-mail"
                required
                className="w-full bg-transparent text-white px-0 py-3 border-0 border-b border-gray-600
                         focus:border-[#940000] focus:outline-none transition-colors placeholder-gray-500"
              />
            </div>

            <div>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Senha"
                required
                className="w-full bg-transparent text-white px-0 py-3 border-0 border-b border-gray-600
                         focus:border-[#940000] focus:outline-none transition-colors placeholder-gray-500"
              />
            </div>

            {error && (
              <p className="text-red-400 text-sm text-center">{error}</p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#940000] text-white py-4 rounded-2xl font-medium
                       hover:bg-[#b30000] transition-colors disabled:opacity-50
                       disabled:cursor-not-allowed shadow-lg shadow-[#940000]/30"
            >
              {loading ? 'Processando...' : isSignUp ? 'Criar Conta' : 'Entrar'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <button
              onClick={() => setIsSignUp(!isSignUp)}
              className="text-gray-400 text-sm hover:text-white transition-colors"
            >
              {isSignUp ? 'Já tem conta? Entre' : 'Novo aqui? Crie sua conta'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
