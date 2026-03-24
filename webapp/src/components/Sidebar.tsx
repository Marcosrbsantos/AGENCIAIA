import { MessageSquare, Lightbulb, Settings, Database, LogOut } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

interface SidebarProps {
  currentPage: string;
  onNavigate: (page: string) => void;
}

export default function Sidebar({ currentPage, onNavigate }: SidebarProps) {
  const { signOut } = useAuth();

  const navItems = [
    { id: 'chat', icon: MessageSquare, label: 'Chat' },
    { id: 'vault', icon: Lightbulb, label: 'Insights' },
    { id: 'integrations', icon: Database, label: 'Backup' },
    { id: 'settings', icon: Settings, label: 'Config' },
  ];

  return (
    <div className="w-24 h-screen backdrop-blur-3xl bg-black/40 border-r border-white/5 flex flex-col items-center py-10 relative z-20">
      {/* Brand Logo */}
      <div className="mb-14 relative group">
        <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center transition-all group-hover:border-emerald-500/40 group-hover:bg-emerald-500/20">
          <span className="text-emerald-500 font-black text-xs tracking-tighter">V11</span>
        </div>
        <div className="absolute inset-x-0 -bottom-4 opacity-0 group-hover:opacity-100 transition-opacity flex justify-center">
          <div className="h-1 w-4 bg-emerald-500/50 rounded-full blur-[1px]"></div>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="flex-1 flex flex-col gap-8">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentPage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-all relative group
                ${isActive
                  ? 'glass-button bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                  : 'text-gray-500 hover:text-gray-300'}`}
              title={item.label}
            >
              <Icon size={22} className={isActive ? 'drop-shadow-[0_0_8px_rgba(16,185,129,0.5)]' : ''} />
              
              {!isActive && (
                <div className="absolute left-full ml-4 px-3 py-1.5 glass-card text-[10px] text-white opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none uppercase tracking-widest font-bold z-50">
                  {item.label}
                </div>
              )}
              
              {isActive && (
                <div className="absolute -left-[1px] w-1 h-6 bg-emerald-500 rounded-r-full shadow-[0_0_10px_rgba(16,185,129,0.8)]"></div>
              )}
            </button>
          );
        })}
      </nav>

      {/* Bottom Actions */}
      <div className="flex flex-col gap-6">
        <button
          onClick={() => signOut()}
          className="w-14 h-14 rounded-2xl text-gray-600 hover:text-rose-400 hover:bg-rose-500/5 transition-all flex items-center justify-center group"
          title="Sair da Arca"
        >
          <LogOut size={22} />
        </button>
      </div>
    </div>
  );
}
