import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../lib/supabase';

interface UserSettings {
  design_mode: 'anatomia' | 'solar';
  art_intensity: number;
  voice_instructions: string;
}

export default function Settings() {
  const [settings, setSettings] = useState<UserSettings>({
    design_mode: 'anatomia',
    art_intensity: 50,
    voice_instructions: '',
  });
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      loadSettings();
    }
  }, [user]);

  const loadSettings = async () => {
    const { data } = await supabase
      .from('user_settings')
      .select('*')
      .eq('user_id', user!.id)
      .maybeSingle();

    if (data) {
      setSettings({
        design_mode: data.design_mode,
        art_intensity: data.art_intensity,
        voice_instructions: data.voice_instructions,
      });
    } else {
      await supabase
        .from('user_settings')
        .insert({ user_id: user!.id });
    }
  };

  const handleSave = async (field: keyof UserSettings, value: string | number) => {
    const updated = { ...settings, [field]: value };
    setSettings(updated);

    await supabase
      .from('user_settings')
      .update({ [field]: value })
      .eq('user_id', user!.id);
  };

  const designModes = [
    {
      id: 'anatomia' as const,
      name: 'Anatomia do Marketing',
      description: 'Estética vintage com traços escuros',
      preview: 'bg-gradient-to-br from-gray-900 via-gray-800 to-black',
    },
    {
      id: 'solar' as const,
      name: 'Solar Clean - JC Antunes',
      description: 'Tons claros, laranja e cinza gelo',
      preview: 'bg-gradient-to-br from-orange-100 via-gray-100 to-gray-300',
    },
  ];

  return (
    <div className="flex-1 h-screen overflow-y-auto bg-[#030303]">
      <div className="max-w-4xl mx-auto px-10 py-12">
        <div className="mb-12 border-b border-white/5 pb-8">
           <div className="flex items-center gap-2 mb-4">
              <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></div>
              <span className="text-[10px] uppercase tracking-[0.3em] font-bold text-emerald-500/80">Laboratório Neuroestético</span>
            </div>
          <h1 className="text-white text-4xl font-light tracking-tight mb-2">Configurações de Estilo</h1>
          <p className="text-gray-500 font-serif italic text-sm">Ajuste o tom e a intensidade da sua inteligência criativa.</p>
        </div>

        <div className="space-y-8">
          <div className="glass-card rounded-3xl overflow-hidden">
            <div className="px-8 py-5 border-b border-white/5 bg-white/[0.02]">
              <h2 className="text-white text-sm font-bold uppercase tracking-widest">Modo de Design Ativo</h2>
            </div>

            <div className="p-8 grid md:grid-cols-2 gap-6">
              {designModes.map((mode) => (
                <button
                  key={mode.id}
                  onClick={() => handleSave('design_mode', mode.id)}
                  className={`group relative overflow-hidden rounded-2xl transition-all duration-500 ${
                    settings.design_mode === mode.id
                      ? 'ring-2 ring-emerald-500 shadow-xl shadow-emerald-500/20'
                      : 'ring-1 ring-white/5 hover:ring-white/10'
                  }`}
                >
                  <div className={`h-44 ${mode.preview} group-hover:scale-110 transition-transform duration-700`}></div>
                  <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent flex flex-col justify-end p-6">
                    <h3 className="text-white font-bold text-lg mb-1">{mode.name}</h3>
                    <p className="text-gray-400 text-xs font-serif italic">{mode.description}</p>
                  </div>
                  {settings.design_mode === mode.id && (
                    <div className="absolute top-4 right-4 w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center shadow-lg shadow-emerald-500/40">
                      <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  )}
                </button>
              ))}
            </div>
          </div>

          <div className="glass-card rounded-3xl overflow-hidden">
            <div className="px-8 py-5 border-b border-white/5 bg-white/[0.02]">
              <h2 className="text-white text-sm font-bold uppercase tracking-widest">Intensidade da Direção de Arte</h2>
            </div>

            <div className="p-8">
              <div className="flex items-center gap-8">
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={settings.art_intensity}
                  onChange={(e) => handleSave('art_intensity', parseInt(e.target.value))}
                  className="flex-1 h-1 bg-white/5 rounded-lg appearance-none cursor-pointer
                           [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-6 [&::-webkit-slider-thumb]:h-6
                           [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-emerald-500
                           [&::-webkit-slider-thumb]:shadow-xl [&::-webkit-slider-thumb]:shadow-emerald-500/40
                           [&::-moz-range-thumb]:w-6 [&::-moz-range-thumb]:h-6
                           [&::-moz-range-thumb]:rounded-full [&::-moz-range-thumb]:bg-emerald-500
                           [&::-moz-range-thumb]:border-0 [&::-moz-range-thumb]:shadow-xl"
                  style={{
                    background: `linear-gradient(to right, #10b981 0%, #10b981 ${settings.art_intensity}%, rgba(255,255,255,0.05) ${settings.art_intensity}%, rgba(255,255,255,0.05) 100%)`
                  }}
                />
                <div className="w-16 text-center">
                  <span className="text-emerald-500 text-2xl font-light">{settings.art_intensity}</span>
                </div>
              </div>

              <div className="flex justify-between mt-4">
                <span className="text-gray-600 text-[10px] uppercase tracking-widest font-bold">Subjetivo</span>
                <span className="text-gray-600 text-[10px] uppercase tracking-widest font-bold">Dogmático</span>
              </div>
            </div>
          </div>

          <div className="glass-card rounded-3xl overflow-hidden">
            <div className="px-8 py-5 border-b border-white/5 bg-white/[0.02]">
              <h2 className="text-white text-sm font-bold uppercase tracking-widest">Diretriz de Tom de Voz</h2>
            </div>

            <div className="p-8">
              <textarea
                value={settings.voice_instructions}
                onChange={(e) => handleSave('voice_instructions', e.target.value)}
                placeholder="Insira o arquétipo e o tom de voz mestre..."
                rows={6}
                className="w-full bg-black/40 border border-white/5 text-white px-6 py-4 rounded-2xl
                         focus:border-emerald-500/50 focus:outline-none transition-all resize-none
                         placeholder:text-gray-800 font-serif italic"
              />
              <div className="mt-4 flex items-center gap-3">
                 <div className="w-1 h-1 rounded-full bg-emerald-500 animate-pulse"></div>
                 <p className="text-gray-600 text-[10px] uppercase tracking-widest font-bold">
                    Estas instruções modulam a personalidade de toda a rede neural.
                 </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
