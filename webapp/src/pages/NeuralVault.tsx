import { useState, useEffect } from 'react';
import { Download, Copy, Archive } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../lib/supabase';

interface VaultItem {
  id: string;
  topic: string;
  image_url: string;
  copy_content: string;
  created_at: string;
  ctr: number;
  likes: number;
  saves: number;
}

export default function NeuralVault() {
  const [items, setItems] = useState<VaultItem[]>([]);
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      loadItems();
    }
  }, [user]);

  const loadItems = async () => {
    const { data, error } = await supabase
      .from('performance_logs')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) {
      console.error("Erro ao carregar Neural Vault:", error);
      return;
    }

    if (data) {
      setItems(data);
    }
  };

  const handleCopy = async (text: string) => {
    await navigator.clipboard.writeText(text);
  };

  return (
    <div className="flex-1 h-screen overflow-y-auto bg-[#030303]">
      <div className="max-w-7xl mx-auto px-10 py-12">
        {/* Header Section */}
        <div className="flex items-end justify-between mb-16 border-b border-white/5 pb-10">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)] animate-pulse"></div>
              <span className="text-[10px] uppercase tracking-[0.3em] font-bold text-emerald-500/80">Inteligência Armazenada</span>
            </div>
            <h1 className="text-white text-5xl font-light tracking-tight mb-2">Neural Vault</h1>
            <p className="text-gray-500 font-serif italic">Seu repositório mestre de ativos de alta performance.</p>
          </div>

          <div className="flex gap-4">
            <div className="glass-card px-6 py-3 flex flex-col items-end">
              <span className="text-[8px] uppercase tracking-widest text-gray-500 mb-1">Total de Ativos</span>
              <span className="text-2xl font-light text-white">{items.length}</span>
            </div>
          </div>
        </div>

        {/* Content Grid */}
        {items.length === 0 ? (
          <div className="text-center py-32 glass-card rounded-3xl border-dashed border-white/5 bg-transparent">
            <Archive size={48} className="text-gray-700 mx-auto mb-6" />
            <p className="text-gray-400 text-xl font-light mb-2">Cofre de Inteligência Vazio</p>
            <p className="text-gray-600 text-sm max-w-xs mx-auto">Suas idéias e insights validados aparecerão aqui.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {items.map((item) => (
              <div
                key={item.id}
                className="group relative"
              >
                <div className="glass-card rounded-[2.5rem] overflow-hidden transition-all duration-700 group-hover:border-emerald-500/40 group-hover:bg-emerald-500/[0.02] group-hover:-translate-y-3 shadow-2xl shadow-transparent group-hover:shadow-emerald-500/10 border border-white/5">
                  <div className="p-10">
                    <div className="flex items-center justify-between mb-8">
                      <div className="flex items-center gap-3">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></div>
                        <span className="text-[10px] text-emerald-500/80 uppercase tracking-[0.2em] font-black">Insight Validado</span>
                      </div>
                      <span className="text-[10px] text-gray-700 font-serif italic">{new Date(item.created_at).toLocaleDateString()}</span>
                    </div>

                    <h3 className="text-white text-2xl font-light mb-8 leading-tight tracking-tight group-hover:text-emerald-400 transition-colors duration-500">
                      {item.topic}
                    </h3>

                    <div className="relative group/content mb-8">
                        <div className="p-6 rounded-2xl bg-white/[0.02] border border-white/5 text-gray-400 text-sm font-serif italic line-clamp-4 group-hover:text-gray-300 transition-colors">
                            "{item.copy_content || 'Nenhum conteúdo de copy gerado para este insight'}"
                        </div>
                    </div>
                    
                    <div className="flex items-center justify-between pt-8 border-t border-white/5">
                        <div className="flex gap-8">
                            <div className="flex flex-col">
                                <span className="text-[9px] text-gray-600 uppercase tracking-widest mb-1.5">Eficiência</span>
                                <span className="text-emerald-400 text-sm font-light tracking-widest">{item.ctr}% <span className="text-[10px] text-gray-600">CTR</span></span>
                            </div>
                            <div className="flex flex-col">
                                <span className="text-[9px] text-gray-600 uppercase tracking-widest mb-1.5">Interação</span>
                                <div className="flex items-center gap-3">
                                    <span className="text-white text-xs font-bold">{item.likes} <span className="text-[8px] text-gray-700 uppercase">Luvs</span></span>
                                </div>
                            </div>
                        </div>
                        
                        <div className="flex gap-3">
                             <button
                                onClick={() => handleCopy(item.copy_content)}
                                className="p-3 rounded-xl bg-white/5 border border-white/5 text-gray-500 hover:text-emerald-400 hover:border-emerald-500/30 transition-all"
                             >
                                <Copy size={16} />
                             </button>
                             <button className="p-3 rounded-xl bg-white/5 border border-white/5 text-gray-500 hover:text-emerald-400 hover:border-emerald-500/30 transition-all">
                                <Download size={16} />
                             </button>
                        </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
