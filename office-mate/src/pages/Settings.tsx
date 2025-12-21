import React, { useState, useEffect } from 'react';
import { 
  Globe, 
  Bell, 
  Palette,
  Check,
  User,
  Shield
} from 'lucide-react';
import { useLanguage } from '@/context/LanguageContext';
import { useAuth } from '@/context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { useToast } from '@/hooks/use-toast';

const Settings: React.FC = () => {
  const { t, language, setLanguage } = useLanguage();
  const { user } = useAuth();
  const { toast } = useToast();

  const [notifications, setNotifications] = useState(() => {
    const saved = localStorage.getItem('notifications');
    return saved ? JSON.parse(saved) : true;
  });

  const [reminderSound, setReminderSound] = useState(() => {
    const saved = localStorage.getItem('reminderSound');
    return saved ? JSON.parse(saved) : true;
  });

  const [emailDigest, setEmailDigest] = useState(() => {
    const saved = localStorage.getItem('emailDigest');
    return saved ? JSON.parse(saved) : false;
  });

  useEffect(() => {
    localStorage.setItem('notifications', JSON.stringify(notifications));
  }, [notifications]);

  useEffect(() => {
    localStorage.setItem('reminderSound', JSON.stringify(reminderSound));
  }, [reminderSound]);

  useEffect(() => {
    localStorage.setItem('emailDigest', JSON.stringify(emailDigest));
  }, [emailDigest]);

  const handleLanguageChange = (lang: 'en' | 'si') => {
    setLanguage(lang);
    toast({
      title: t('settings.saved'),
      description: lang === 'en' ? 'Language changed to English' : 'භාෂාව සිංහල ලෙස වෙනස් කරන ලදී',
    });
  };

  return (
    <div className="space-y-6 max-w-2xl animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-2xl lg:text-3xl font-bold text-foreground">{t('settings.title')}</h1>
        <p className="text-muted-foreground mt-1">{t('settings.preferences')}</p>
      </div>

      {/* Profile Card */}
      <Card className="card-shadow">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <User className="w-5 h-5" />
            {language === 'en' ? 'Profile' : 'පැතිකඩ'}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
              <span className="text-2xl font-bold text-primary">
                {user?.name?.charAt(0)}
              </span>
            </div>
            <div>
              <p className="text-lg font-semibold text-foreground">{user?.name}</p>
              <p className="text-muted-foreground">{user?.email}</p>
              <p className="text-sm text-primary">{user?.role}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Language Settings */}
      <Card className="card-shadow">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Globe className="w-5 h-5" />
            {t('settings.language')}
          </CardTitle>
          <CardDescription>
            {language === 'en' 
              ? 'Choose your preferred language for the interface'
              : 'අතුරුමුහුණත සඳහා ඔබ කැමති භාෂාව තෝරන්න'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <button
              onClick={() => handleLanguageChange('en')}
              className={`relative p-4 rounded-xl border-2 transition-all ${
                language === 'en'
                  ? 'border-primary bg-primary/5'
                  : 'border-border hover:border-primary/50'
              }`}
            >
              {language === 'en' && (
                <div className="absolute top-2 right-2 w-6 h-6 bg-primary rounded-full flex items-center justify-center">
                  <Check className="w-4 h-4 text-primary-foreground" />
                </div>
              )}
              <div className="text-left">
                <p className="text-3xl mb-2">🇬🇧</p>
                <p className="font-medium text-foreground">{t('settings.langEnglish')}</p>
                <p className="text-sm text-muted-foreground">English</p>
              </div>
            </button>

            <button
              onClick={() => handleLanguageChange('si')}
              className={`relative p-4 rounded-xl border-2 transition-all ${
                language === 'si'
                  ? 'border-primary bg-primary/5'
                  : 'border-border hover:border-primary/50'
              }`}
            >
              {language === 'si' && (
                <div className="absolute top-2 right-2 w-6 h-6 bg-primary rounded-full flex items-center justify-center">
                  <Check className="w-4 h-4 text-primary-foreground" />
                </div>
              )}
              <div className="text-left">
                <p className="text-3xl mb-2">🇱🇰</p>
                <p className="font-medium text-foreground">{t('settings.langSinhala')}</p>
                <p className="text-sm text-muted-foreground">Sinhala</p>
              </div>
            </button>
          </div>
        </CardContent>
      </Card>

      {/* Notification Settings */}
      <Card className="card-shadow">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Bell className="w-5 h-5" />
            {language === 'en' ? 'Notifications' : 'දැනුම්දීම්'}
          </CardTitle>
          <CardDescription>
            {language === 'en' 
              ? 'Configure how you receive notifications'
              : 'ඔබට දැනුම්දීම් ලැබෙන ආකාරය වින්‍යාස කරන්න'}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label htmlFor="notifications" className="text-base">
                {t('settings.notifications')}
              </Label>
              <p className="text-sm text-muted-foreground">
                {language === 'en' 
                  ? 'Receive browser notifications for reminders'
                  : 'මතක් කිරීම් සඳහා බ්‍රවුසර දැනුම්දීම් ලබන්න'}
              </p>
            </div>
            <Switch
              id="notifications"
              checked={notifications}
              onCheckedChange={setNotifications}
            />
          </div>

          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label htmlFor="sound" className="text-base">
                {language === 'en' ? 'Reminder Sound' : 'මතක් කිරීමේ ශබ්දය'}
              </Label>
              <p className="text-sm text-muted-foreground">
                {language === 'en' 
                  ? 'Play sound when reminders are triggered'
                  : 'මතක් කිරීම් ක්‍රියාත්මක වන විට ශබ්දය වාදනය කරන්න'}
              </p>
            </div>
            <Switch
              id="sound"
              checked={reminderSound}
              onCheckedChange={setReminderSound}
            />
          </div>

          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label htmlFor="digest" className="text-base">
                {language === 'en' ? 'Daily Email Digest' : 'දෛනික විද්‍යුත් තැපැල් සාරාංශය'}
              </Label>
              <p className="text-sm text-muted-foreground">
                {language === 'en' 
                  ? 'Receive a daily summary of pending tasks'
                  : 'අපේක්ෂිත කාර්යයන්ගේ දෛනික සාරාංශයක් ලබන්න'}
              </p>
            </div>
            <Switch
              id="digest"
              checked={emailDigest}
              onCheckedChange={setEmailDigest}
            />
          </div>
        </CardContent>
      </Card>

      {/* About */}
      <Card className="card-shadow">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Shield className="w-5 h-5" />
            {language === 'en' ? 'About' : 'පිළිබඳව'}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 text-sm">
            <p className="text-foreground font-medium">
              AI-Powered Document Organizer v1.0.0
            </p>
            <p className="text-muted-foreground">
              {language === 'en' 
                ? 'Smart document management and task tracking for Sri Lankan offices'
                : 'ශ්‍රී ලංකාවේ කාර්යාල සඳහා ස්මාර්ට් ලේඛන කළමනාකරණය සහ කාර්ය නිරීක්ෂණය'}
            </p>
            <p className="text-muted-foreground">
              © 2024 Final Year Project
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Settings;
