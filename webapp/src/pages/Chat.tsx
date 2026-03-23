import { useState, useEffect, useRef } from 'react';
import { Send, Plus, Search, Image, FileText, Copy, Sparkles, Check, Download } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../lib/supabase';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  strategy?: any;
  copy_final?: string;
  created_at: string;
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showTools, setShowTools] = useState(false);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [plataforma, setPlataforma] = useState('Instagram');
  const [objetivo, setObjetivo] = useState('Engajamento');
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      loadOrCreateChat();
    }
  }, [user]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadOrCreateChat = async () => {
    console.log('🔄 Iniciando loadOrCreateChat para o usuário:', user?.id);
    try {
      const { data: existingChats, error: selectError } = await supabase
        .from('chats')
        .select('id')
        .eq('user_id', user!.id)
        .order('created_at', { ascending: false })
        .limit(1)
        .maybeSingle();

      if (selectError) console.error('❌ Erro ao buscar chat existente:', selectError);

      if (existingChats) {
        console.log('✅ Chat encontrado:', existingChats.id);
        setCurrentChatId(existingChats.id);
        await loadMessages(existingChats.id);
      } else {
        console.log('➕ Criando novo chat...');
        const { data: newChat, error: insertError } = await supabase
          .from('chats')
          .insert({ user_id: user!.id, title: 'Nova Conversa' })
          .select()
          .single();

        if (insertError) console.error('❌ Erro ao criar novo chat:', insertError);
        if (newChat) {
          console.log('✅ Novo chat criado:', newChat.id);
          setCurrentChatId(newChat.id);
        }
      }
    } catch (err) {
      console.error('🔥 Erro crítico no loadOrCreateChat:', err);
    }
  };

  const loadMessages = async (chatId: string) => {
    const { data } = await supabase
      .from('messages')
      .select('*')
      .eq('chat_id', chatId)
      .order('created_at', { ascending: true });

    if (data) setMessages(data);
  };

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    if (!currentChatId) {
      await loadOrCreateChat();
      if (!currentChatId) return;
    }

    const userMessage = input.trim();
    setInput('');
    setLoading(true);

    // Add user message optimistically
    const tempUserMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: userMessage,
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, tempUserMsg]);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          user_id: user!.id,
          chat_id: currentChatId,
          plataforma,
          objetivo
        })
      });

      if (!response.ok) throw new Error('Falha na comunicação');
      
      const data = await response.json();
      
      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        strategy: data.strategy,
        copy_final: data.copy_final,
        created_at: new Date().toISOString()
      };

      setMessages((prev) => [...prev, aiMsg]);
      
      // Save to Supabase (User message then AI message)
      await supabase.from('messages').insert([
        { chat_id: currentChatId, user_id: user!.id, role: 'user', content: userMessage },
        { 
          chat_id: currentChatId, 
          user_id: user!.id, 
          role: 'assistant', 
          content: data.response,
          // metadata: JSON.stringify({ strategy: data.strategy, copy_final: data.copy_final })
        }
      ]);

    } catch (error) {
       console.error(error);
       setMessages((prev) => [...prev, {
         id: 'error-' + Date.now(),
         role: 'assistant',
         content: "⚠️ Mestre, conexão instável. Verifique o backend.",
         created_at: new Date().toISOString()
       }]);
    }
    setLoading(false);
  };

  return (
    <div className="flex-1 flex flex-col h-screen bg-[#030303]">
      {/* Header */}
      <div className="backdrop-blur-2xl bg-black/40 border-b border-white/5 px-8 py-5 flex items-center justify-between sticky top-0 z-10">
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></div>
            <div className="absolute inset-0 w-3 h-3 rounded-full bg-emerald-500 blur-sm animate-pulse"></div>
          </div>
          <div>
            <h1 className="text-white font-semibold tracking-tight premium-gradient-text">Arquiteto Vivo v10</h1>
            <p className="text-[10px] text-gray-500 uppercase tracking-widest font-medium">Neural Engine Online</p>
          </div>
        </div>
        
        <div className="flex gap-3">
          <select 
            value={plataforma} 
            onChange={(e) => setPlataforma(e.target.value)}
            className="glass-button text-white text-xs rounded-xl px-4 py-2 outline-none cursor-pointer"
          >
            <option value="Instagram">📸 Instagram</option>
            <option value="LinkedIn">💼 LinkedIn</option>
            <option value="TikTok">🎥 TikTok</option>
          </select>
          <select 
            value={objetivo} 
            onChange={(e) => setObjetivo(e.target.value)}
            className="glass-button text-white text-xs rounded-xl px-4 py-2 outline-none cursor-pointer"
          >
            <option value="Engajamento">🚀 Engajamento</option>
            <option value="Venda">💰 Venda</option>
            <option value="Autoridade">🏛️ Autoridade</option>
          </select>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-8 py-10 space-y-10 scrollbar-hide">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full opacity-30 select-none">
            <Sparkles size={64} className="text-white mb-6 animate-pulse" />
            <h2 className="text-2xl font-light tracking-tighter text-white">AGENCIAIA V10</h2>
            <p className="text-sm text-gray-400 mt-2">Pronto para forjar sua próxima campanha mestre.</p>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-in fade-in slide-in-from-bottom-4 duration-500`}
          >
            <div className={`max-w-[85%] group relative ${
              message.role === 'user' 
                ? 'glass-card bg-white/[0.05] gold-glow px-6 py-4' 
                : 'w-full'
            }`}>
              {message.role === 'assistant' ? (
                <div className="space-y-6">
                  {/* Strategy Block */}
                  <div className="glass-card bg-emerald-500/[0.02] border-emerald-500/10 p-6">
                    <div className="flex items-center gap-2 mb-4 text-emerald-400 opacity-60">
                      <Sparkles size={14} />
                      <span className="text-[10px] uppercase tracking-[0.2em] font-bold">Visão Estratégica</span>
                    </div>
                    <div className="text-gray-100 font-serif text-lg leading-relaxed whitespace-pre-wrap">
                      {(() => {
                        const parts = message.content.split(/(!\[Arte\]\(.*?\))/g);
                        return parts.map((part, i) => {
                          const imgMatch = part.match(/!\[Arte\]\((.*?)\)/);
                          if (imgMatch) {
                            const url = imgMatch[1];
                            return (
                              <div key={i} className="my-6 rounded-2xl overflow-hidden border border-white/10 shadow-2xl bg-black/20 group/img relative">
                                <img 
                                  src={url} 
                                  alt="Neural Design" 
                                  className="w-full h-auto"
                                  loading="lazy"
                                />
                                <div className="absolute inset-0 bg-black/40 opacity-0 group-hover/img:opacity-100 transition-opacity flex items-center justify-center gap-4">
                                  <a 
                                    href={url} 
                                    target="_blank" 
                                    rel="noreferrer"
                                    className="p-4 glass-button rounded-2xl bg-emerald-500/20 hover:bg-emerald-500/40 text-emerald-400"
                                  >
                                    <Download size={24} />
                                  </a>
                                </div>
                              </div>
                            );
                          }
                          return part;
                        });
                      })()}
                    </div>
                  </div>

                  {/* Copy Block if exists */}
                  {message.copy_final && (
                    <div className="glass-card bg-white/[0.02] p-6 relative group/copy">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-2 text-gray-400 opacity-60">
                          <FileText size={14} />
                          <span className="text-[10px] uppercase tracking-[0.2em] font-bold">Copy Final Masterizada</span>
                        </div>
                        <button 
                          onClick={() => handleCopy(message.copy_final!, message.id)}
                          className="p-2 glass-button rounded-lg hover:bg-emerald-500/20 text-gray-400 hover:text-emerald-400 transition-all"
                        >
                          {copiedId === message.id ? <Check size={16} /> : <Copy size={16} />}
                        </button>
                      </div>
                      <div className="bg-black/40 rounded-2xl p-6 border border-white/5">
                        <p className="text-emerald-50/90 font-mono text-sm leading-relaxed whitespace-pre-wrap">
                          {message.copy_final}
                        </p>
                      </div>
                      
                      {/* Action Buttons */}
                      <div className="flex gap-3 mt-6">
                        <button 
                          onClick={() => { setInput("/design " + message.copy_final?.substring(0, 100)); }}
                          className="flex-1 glass-button py-3 rounded-2xl flex items-center justify-center gap-2 text-xs font-bold text-white hover:bg-white/10"
                        >
                          <Image size={16} />
                          GERAR DESIGN OURO
                        </button>
                        <button className="px-5 glass-button py-3 rounded-2xl text-gray-500 hover:text-white">
                          <Download size={16} />
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-white/90 leading-relaxed font-medium">
                  {message.content}
                </p>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start animate-in fade-in duration-300">
             <div className="glass-card px-6 py-4">
                <div className="flex gap-2">
                  <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce [animation-delay:0.1s]"></div>
                  <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce [animation-delay:0.2s]"></div>
                </div>
             </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="px-8 pb-8 pt-4">
        <form onSubmit={handleSubmit} className="relative max-w-5xl mx-auto">
          <div className="glass-card bg-white/[0.04] p-2 flex items-center gap-2 shadow-2xl">
            <button
              type="button"
              onClick={() => setShowTools(!showTools)}
              className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
                showTools ? 'bg-emerald-500 text-white' : 'glass-button text-gray-400'
              }`}
            >
              <Plus size={20} className={showTools ? 'rotate-45 transition-transform' : 'transition-transform'} />
            </button>

            {showTools && (
              <div className="absolute bottom-[calc(100%+12px)] left-0 flex gap-2 animate-in slide-in-from-bottom-2 duration-300">
                <button 
                  type="button"
                  onClick={() => { setInput("/pesquisa "); setShowTools(false); }}
                  className="glass-button px-6 py-3 rounded-2xl text-white text-xs font-bold flex items-center gap-2 bg-black/80"
                >
                  <Search size={14} className="text-emerald-400" />
                  PESQUISA
                </button>
                <button 
                  type="button"
                  onClick={() => { setInput("/copy "); setShowTools(false); }}
                  className="glass-button px-6 py-3 rounded-2xl text-white text-xs font-bold flex items-center gap-2 bg-black/80"
                >
                  <FileText size={14} className="text-blue-400" />
                  COPY
                </button>
                <button 
                  type="button"
                  onClick={() => { setInput("/design "); setShowTools(false); }}
                  className="glass-button px-6 py-3 rounded-2xl text-white text-xs font-bold flex items-center gap-2 bg-black/80"
                >
                  <Image size={14} className="text-purple-400" />
                  DESIGN
                </button>
              </div>
            )}

            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Cite seu tema ou use um comando (/...)"
              className="flex-1 bg-transparent text-white placeholder-gray-600 outline-none px-4 text-sm font-medium"
            />

            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="w-12 h-12 rounded-2xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-20 disabled:grayscale flex items-center justify-center transition-all shadow-lg shadow-emerald-900/20 group"
            >
              <Send size={18} className="text-white group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
