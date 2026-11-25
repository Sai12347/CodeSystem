import React, { useState } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { UserProvider } from './context/UserContext';
import { VisualizerProvider } from './context/VisualizerContext';
import { Navbar, ActiveTab } from './components/common/Navbar';
import { Footer } from './components/common/Footer';
import { LiveAnnouncer } from './components/common/LiveAnnouncer';
import { DashboardView } from './components/dashboard/DashboardView';
import { AlgorithmVisualizer } from './components/visualizer/AlgorithmVisualizer';
import { LearnCatalogView } from './components/learn/LearnCatalogView';
import { PracticeArenaView } from './components/practice/PracticeArenaView';
import { CompanyPrepView } from './components/companies/CompanyPrepView';
import { AiTutorChatView } from './components/ai-tutor/AiTutorChatView';
import { ProgressProfileView } from './components/profile/ProgressProfileView';

export const AppContent: React.FC = () => {
  const [activeTab, setActiveTab] = useState<ActiveTab>('dashboard');

  return (
    <div className="min-h-screen flex flex-col bg-apple-bg dark:bg-apple-darkBg text-zinc-900 dark:text-zinc-100 transition-colors">
      <LiveAnnouncer />
      <Navbar activeTab={activeTab} onTabChange={setActiveTab} />

      <main className="flex-1 w-full" id="main-content">
        {activeTab === 'dashboard' && <DashboardView onNavigate={setActiveTab} />}
        {activeTab === 'visualizer' && <AlgorithmVisualizer />}
        {activeTab === 'learn' && <LearnCatalogView onNavigate={setActiveTab} />}
        {activeTab === 'practice' && <PracticeArenaView />}
        {activeTab === 'companies' && <CompanyPrepView />}
        {activeTab === 'ai-tutor' && <AiTutorChatView />}
        {(activeTab === 'progress' || activeTab === 'profile') && <ProgressProfileView />}
      </main>

      <Footer />
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <ThemeProvider>
      <UserProvider>
        <VisualizerProvider>
          <AppContent />
        </VisualizerProvider>
      </UserProvider>
    </ThemeProvider>
  );
};

export default App;
