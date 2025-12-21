import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

type Language = 'en' | 'si';

interface Translations {
  [key: string]: {
    en: string;
    si: string;
  };
}

const translations: Translations = {
  // Navigation
  'nav.dashboard': { en: 'Dashboard', si: 'උපකරණ පුවරුව' },
  'nav.documents': { en: 'Documents', si: 'ලේඛන' },
  'nav.tasks': { en: 'Tasks', si: 'කාර්යයන්' },
  'nav.settings': { en: 'Settings', si: 'සැකසුම්' },
  'nav.logout': { en: 'Logout', si: 'පිටවීම' },

  // Login
  'login.title': { en: 'Document Organizer', si: 'ලේඛන සංවිධායක' },
  'login.subtitle': { en: 'AI-Powered Office Administration', si: 'AI බලයෙන් කාර්යාල පරිපාලනය' },
  'login.email': { en: 'Email', si: 'විද්‍යුත් තැපෑල' },
  'login.password': { en: 'Password', si: 'මුරපදය' },
  'login.button': { en: 'Sign In', si: 'පුරන්න' },
  'login.error': { en: 'Invalid credentials', si: 'වලංගු නොවන අක්තපත්‍ර' },

  // Dashboard
  'dashboard.welcome': { en: 'Welcome back', si: 'නැවත සාදරයෙන් පිළිගනිමු' },
  'dashboard.overview': { en: 'Overview', si: 'දළ විශ්ලේෂණය' },
  'dashboard.totalDocs': { en: 'Total Documents', si: 'මුළු ලේඛන' },
  'dashboard.openTasks': { en: 'Open Tasks', si: 'විවෘත කාර්යයන්' },
  'dashboard.upcoming': { en: 'Upcoming Deadlines', si: 'ළඟ එන නියමිත දින' },
  'dashboard.recentDocs': { en: 'Recent Documents', si: 'මෑත ලේඛන' },
  'dashboard.byCategory': { en: 'Documents by Category', si: 'ප්‍රවර්ගය අනුව ලේඛන' },

  // Categories
  'category.finance': { en: 'Finance', si: 'මූල්‍ය' },
  'category.hr': { en: 'HR', si: 'මානව සම්පත්' },
  'category.procurement': { en: 'Procurement', si: 'ප්‍රසම්පාදන' },
  'category.maintenance': { en: 'Maintenance', si: 'නඩත්තු' },
  'category.all': { en: 'All Categories', si: 'සියලු ප්‍රවර්ග' },

  // Documents
  'docs.title': { en: 'Documents', si: 'ලේඛන' },
  'docs.upload': { en: 'Upload Document', si: 'ලේඛනය උඩුගත කරන්න' },
  'docs.search': { en: 'Search documents...', si: 'ලේඛන සොයන්න...' },
  'docs.filter': { en: 'Filter by category', si: 'ප්‍රවර්ගය අනුව පෙරන්න' },
  'docs.name': { en: 'Document Name', si: 'ලේඛන නම' },
  'docs.category': { en: 'Category', si: 'ප්‍රවර්ගය' },
  'docs.date': { en: 'Date', si: 'දිනය' },
  'docs.tags': { en: 'Tags', si: 'ටැග්' },
  'docs.actions': { en: 'Actions', si: 'ක්‍රියාමාර්ග' },
  'docs.view': { en: 'View Details', si: 'විස්තර බලන්න' },
  'docs.summary': { en: 'AI Summary', si: 'AI සාරාංශය' },
  'docs.linkedTasks': { en: 'Linked Tasks', si: 'සම්බන්ධිත කාර්යයන්' },
  'docs.noResults': { en: 'No documents found', si: 'ලේඛන හමු නොවීය' },
  'docs.dropzone': { en: 'Drag & drop files here, or click to select', si: 'ගොනු මෙහි ඇද දමන්න, හෝ තේරීමට ක්ලික් කරන්න' },
  'docs.uploading': { en: 'Uploading...', si: 'උඩුගත කරමින්...' },
  'docs.uploadSuccess': { en: 'Document uploaded successfully', si: 'ලේඛනය සාර්ථකව උඩුගත කරන ලදී' },

  // Tasks
  'tasks.title': { en: 'Smart To-Do List', si: 'ස්මාර්ට් කාර්ය ලැයිස්තුව' },
  'tasks.add': { en: 'Add Task', si: 'කාර්යය එකතු කරන්න' },
  'tasks.edit': { en: 'Edit Task', si: 'කාර්යය සංස්කරණය' },
  'tasks.delete': { en: 'Delete', si: 'මකන්න' },
  'tasks.save': { en: 'Save', si: 'සුරකින්න' },
  'tasks.cancel': { en: 'Cancel', si: 'අවලංගු කරන්න' },
  'tasks.taskName': { en: 'Task Name', si: 'කාර්ය නම' },
  'tasks.description': { en: 'Description', si: 'විස්තරය' },
  'tasks.dueDate': { en: 'Due Date', si: 'නියමිත දිනය' },
  'tasks.priority': { en: 'Priority', si: 'ප්‍රමුඛතාවය' },
  'tasks.status': { en: 'Status', si: 'තත්ත්වය' },
  'tasks.linkedDoc': { en: 'Linked Document', si: 'සම්බන්ධිත ලේඛනය' },
  'tasks.pending': { en: 'Pending', si: 'අපේක්ෂිත' },
  'tasks.inProgress': { en: 'In Progress', si: 'සිදු වෙමින්' },
  'tasks.completed': { en: 'Completed', si: 'සම්පූර්ණයි' },
  'tasks.high': { en: 'High', si: 'ඉහළ' },
  'tasks.medium': { en: 'Medium', si: 'මධ්‍යම' },
  'tasks.low': { en: 'Low', si: 'අඩු' },
  'tasks.all': { en: 'All Tasks', si: 'සියලු කාර්යයන්' },
  'tasks.noTasks': { en: 'No tasks found', si: 'කාර්යයන් හමු නොවීය' },
  'tasks.reminder': { en: 'Set Reminder', si: 'මතක් කිරීම සකසන්න' },

  // Settings
  'settings.title': { en: 'Settings', si: 'සැකසුම්' },
  'settings.language': { en: 'Language', si: 'භාෂාව' },
  'settings.langEnglish': { en: 'English', si: 'English' },
  'settings.langSinhala': { en: 'සිංහල', si: 'සිංහල' },
  'settings.preferences': { en: 'Preferences', si: 'මනාපයන්' },
  'settings.notifications': { en: 'Enable Notifications', si: 'දැනුම්දීම් සක්‍රිය කරන්න' },
  'settings.saved': { en: 'Settings saved', si: 'සැකසුම් සුරකින ලදී' },

  // Common
  'common.loading': { en: 'Loading...', si: 'පූරණය වෙමින්...' },
  'common.error': { en: 'An error occurred', si: 'දෝෂයක් ඇති විය' },
  'common.retry': { en: 'Retry', si: 'නැවත උත්සාහ කරන්න' },
  'common.close': { en: 'Close', si: 'වසන්න' },
  'common.confirm': { en: 'Confirm', si: 'තහවුරු කරන්න' },
  'common.today': { en: 'Today', si: 'අද' },
  'common.tomorrow': { en: 'Tomorrow', si: 'හෙට' },
  'common.overdue': { en: 'Overdue', si: 'කල් ඉකුත්' },
};

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [language, setLanguageState] = useState<Language>(() => {
    const saved = localStorage.getItem('language');
    return (saved as Language) || 'en';
  });

  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
    localStorage.setItem('language', lang);
  };

  const t = (key: string): string => {
    const translation = translations[key];
    if (!translation) {
      console.warn(`Translation missing for key: ${key}`);
      return key;
    }
    return translation[language];
  };

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};
