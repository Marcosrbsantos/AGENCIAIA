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
  const [hoveredItem, setHoveredItem] = useState<string | null>(null);
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
            <p className="text-gray-400 text-xl font-light mb-2">Cofre Vazio</p>
            <p className="text-gray-600 text-sm max-w-xs mx-auto">As estratégias geradas no chat aparecerão aqui automaticamente após a validação neural.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {items.map((item) => (
              <div
                key={item.id}
                className="group relative"
                onMouseEnter={() => setHoveredItem(item.id)}
                onMouseLeave={() => setHoveredItem(null)}
              >
                <div className="glass-card rounded-3xl overflow-hidden transition-all duration-500 group-hover:border-emerald-500/30 group-hover:bg-white/[0.03] group-hover:-translate-y-2">
                  <div className="aspect-[4/3] bg-black relative overflow-hidden">
                    <img
                      src={item.image_url || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop'}
                      alt={item.topic}
                      className="w-full h-full object-cover opacity-60 group-hover:scale-110 transition-transform duration-700"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent"></div>
                    
                    <div className="absolute top-4 right-4 flex gap-2">
                       <div className="px-3 py-1.5 rounded-full backdrop-blur-md bg-black/40 border border-white/10 flex items-center gap-1.5">
                          <span className="w-1 h-1 rounded-full bg-emerald-500"></span>
                          <span className="text-[9px] text-white font-bold tracking-widest uppercase">{item.ctr}% CTR</span>
                       </div>
                    </div>

                    {hoveredItem === item.id && (
                      <div className="absolute inset-0 bg-emerald-950/20 backdrop-blur-[2px] flex items-center justify-center gap-4 transition-all animate-in fade-in zoom-in duration-300">
                        <button
                          onClick={() => handleCopy(item.copy_content)}
                          className="w-14 h-14 rounded-2xl glass-button bg-white/10 hover:bg-emerald-500/20 hover:border-emerald-500/40 flex items-center justify-center transition-all group/btn"
                          title="Copiar Inteligência"
                        >
                          <Copy size={20} className="text-white group-hover/btn:text-emerald-400 group-hover/btn:scale-110 transition-all" />
                        </button>
                      </div>
                    )}
                  </div>

                  <div className="p-8">
                    <div className="flex items-center gap-3 mb-4">
                       <span className="text-[9px] text-gray-500 uppercase tracking-widest font-black border-l border-emerald-500 pl-2">Creative Asset</span>
                       <span className="text-[9px] text-gray-700">{new Date(item.created_at).toLocaleDateString()}</span>
                    </div>
                    <h3 className="text-white text-xl font-light mb-6 line-clamp-2 leading-snug group-hover:text-emerald-400 transition-colors">{item.topic}</h3>
                    
                    <div className="flex items-center justify-between pt-6 border-t border-white/5">
                        <div className="flex gap-6">
                            <div className="flex flex-col">
                                <span className="text-[8px] text-gray-500 uppercase tracking-tighter mb-1">Likes</span>
                                <span className="text-white text-xs font-bold">{item.likes}</span>
                            </div>
                            <div className="flex flex-col">
                                <span className="text-[8px] text-gray-500 uppercase tracking-tighter mb-1">Saves</span>
                                <span className="text-white text-xs font-bold">{item.saves}</span>
                            </div>
                        </div>
                        <Download size={16} className="text-gray-500 cursor-pointer hover:text-emerald-400 transition-colors" />
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
