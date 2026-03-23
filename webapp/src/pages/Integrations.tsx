import { useState, useEffect } from 'react';
import { CheckCircle, XCircle, Github } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../lib/supabase';

interface Integration {
  groq_api_key: string;
  pollinations_token: string;
  github_connected: boolean;
  github_repo: string;
}

export default function Integrations() {
  const [integration, setIntegration] = useState<Integration>({
    groq_api_key: '',
    pollinations_token: '',
    github_connected: false,
    github_repo: '',
  });
  const [testing, setTesting] = useState<string | null>(null);
  const [testResults, setTestResults] = useState<Record<string, boolean>>({});
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      loadIntegration();
    }
  }, [user]);

  const loadIntegration = async () => {
    const { data } = await supabase
      .from('integrations')
      .select('*')
      .eq('user_id', user!.id)
      .maybeSingle();

    if (data) {
      setIntegration(data);
    } else {
      await supabase
        .from('integrations')
        .insert({ user_id: user!.id });
    }
  };

  const handleSave = async (field: keyof Integration, value: string | boolean) => {
    const updated = { ...integration, [field]: value };
    setIntegration(updated);

    await supabase
      .from('integrations')
      .update({ [field]: value })
      .eq('user_id', user!.id);
  };

  const handleTest = async (service: string) => {
    setTesting(service);
    await new Promise(resolve => setTimeout(resolve, 1500));
    setTestResults({ ...testResults, [service]: true });
    setTesting(null);
  };

  return (
    <div className="flex-1 h-screen overflow-y-auto bg-[#030303]">
      <div className="max-w-4xl mx-auto px-10 py-12">
        <div className="mb-12 border-b border-white/5 pb-8">
           <div className="flex items-center gap-2 mb-4">
              <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></div>
              <span className="text-[10px] uppercase tracking-[0.3em] font-bold text-emerald-500/80">Central de Conexões</span>
            </div>
          <h1 className="text-white text-4xl font-light tracking-tight mb-2">Integration Hub</h1>
          <p className="text-gray-500 font-serif italic text-sm">Conectores neurais e APIs externas.</p>
        </div>

        <div className="space-y-8">
          <div className="glass-card rounded-3xl overflow-hidden">
            <div className="px-8 py-5 border-b border-white/5 bg-white/[0.02]">
              <h2 className="text-white text-sm font-bold uppercase tracking-widest">Motores de IA</h2>
            </div>

            <div className="p-8 space-y-8">
              <div>
                <label className="block text-gray-500 text-[10px] uppercase tracking-widest font-bold mb-3">Groq API Key</label>
                <div className="flex gap-4">
                  <input
                    type="password"
                    value={integration.groq_api_key}
                    onChange={(e) => handleSave('groq_api_key', e.target.value)}
                    placeholder="gsk_..."
                    className="flex-1 bg-black/40 border border-white/5 text-white px-6 py-4 rounded-2xl focus:border-emerald-500/50 focus:outline-none transition-all placeholder:text-gray-800"
                  />
                  <button
                    onClick={() => handleTest('groq')}
                    disabled={!integration.groq_api_key || testing === 'groq'}
                    className="px-8 py-4 glass-button bg-emerald-500/10 text-emerald-500 border-emerald-500/20 hover:bg-emerald-500/20 disabled:opacity-30 disabled:cursor-not-allowed rounded-2xl transition-all flex items-center gap-3 font-bold text-xs uppercase tracking-widest"
                  >
                    {testing === 'groq' ? (
                      'Sincronizando...'
                    ) : testResults.groq ? (
                      <>
                        <CheckCircle size={18} />
                        Ok
                      </>
                    ) : (
                      'Validar'
                    )}
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-gray-500 text-[10px] uppercase tracking-widest font-bold mb-3">Pollinations Token</label>
                <div className="flex gap-4">
                  <input
                    type="password"
                    value={integration.pollinations_token}
                    onChange={(e) => handleSave('pollinations_token', e.target.value)}
                    placeholder="token..."
                    className="flex-1 bg-black/40 border border-white/5 text-white px-6 py-4 rounded-2xl focus:border-emerald-500/50 focus:outline-none transition-all placeholder:text-gray-800"
                  />
                  <button
                    onClick={() => handleTest('pollinations')}
                    disabled={!integration.pollinations_token || testing === 'pollinations'}
                    className="px-8 py-4 glass-button bg-emerald-500/10 text-emerald-500 border-emerald-500/20 hover:bg-emerald-500/20 disabled:opacity-30 disabled:cursor-not-allowed rounded-2xl transition-all flex items-center gap-3 font-bold text-xs uppercase tracking-widest"
                  >
                    {testing === 'pollinations' ? (
                      'Sincronizando...'
                    ) : testResults.pollinations ? (
                      <>
                        <CheckCircle size={18} />
                        Ok
                      </>
                    ) : (
                      'Validar'
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="glass-card rounded-3xl overflow-hidden">
            <div className="px-8 py-5 border-b border-white/5 bg-white/[0.02]">
              <h2 className="text-white text-sm font-bold uppercase tracking-widest">Backup & Repositório</h2>
            </div>

            <div className="p-8">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center">
                    <Github size={24} className="text-white" />
                  </div>
                  <div>
                    <p className="text-white font-medium text-lg tracking-tight">GitHub Context</p>
                    <p className="text-gray-500 text-sm font-serif italic">
                      {integration.github_connected ? `Repositório: ${integration.github_repo}` : 'Conexão inativa'}
                    </p>
                  </div>
                </div>

                <button
                  className={`px-8 py-4 rounded-2xl transition-all font-bold text-xs uppercase tracking-widest ${
                    integration.github_connected
                      ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      : 'glass-button bg-white/5 text-gray-400 border border-white/10 hover:text-white'
                  }`}
                >
                  {integration.github_connected ? 'Ativo' : 'Conectar'}
                </button>
              </div>
            </div>
          </div>

          <div className="glass-card rounded-3xl overflow-hidden opacity-40 grayscale group hover:grayscale-0 transition-all duration-700">
            <div className="px-8 py-5 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
              <h2 className="text-white text-sm font-bold uppercase tracking-widest">Growth Engine</h2>
              <span className="px-3 py-1 bg-yellow-500/10 text-yellow-500 text-[8px] font-black uppercase tracking-widest rounded-full border border-yellow-500/20">
                Neural Phase 4
              </span>
            </div>

            <div className="p-8">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-600 to-emerald-900 flex items-center justify-center shadow-lg shadow-emerald-900/20">
                  <span className="text-white font-black text-xl tracking-tighter italic">M</span>
                </div>
                <div>
                  <p className="text-white font-medium text-lg tracking-tight">Meta Ads Sync</p>
                  <p className="text-gray-500 text-sm font-serif italic">Injeção direta de criativos em campanhas ativas.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
