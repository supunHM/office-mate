import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileStack, Mail, Lock, Loader2 } from 'lucide-react';
import { useLanguage } from '@/context/LanguageContext';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';

const Login: React.FC = () => {
  const { t, language, setLanguage } = useLanguage();
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const success = await login(email, password);
    
    if (success) {
      toast({
        title: language === 'en' ? 'Welcome!' : 'සාදරයෙන් පිළිගනිමු!',
        description: language === 'en' ? 'Successfully logged in' : 'සාර්ථකව පිවිසුණා',
      });
      navigate('/');
    } else {
      toast({
        title: t('login.error'),
        description: language === 'en' ? 'Please check your credentials' : 'කරුණාකර ඔබගේ අක්තපත්‍ර පරීක්ෂා කරන්න',
        variant: 'destructive',
      });
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4">
      {/* Language Toggle */}
      <div className="absolute top-4 right-4">
        <div className="flex gap-2 bg-card rounded-lg p-1 border border-border">
          <button
            onClick={() => setLanguage('en')}
            className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
              language === 'en' 
                ? 'bg-primary text-primary-foreground' 
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            EN
          </button>
          <button
            onClick={() => setLanguage('si')}
            className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
              language === 'si' 
                ? 'bg-primary text-primary-foreground' 
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            සිං
          </button>
        </div>
      </div>

      {/* Logo & Title */}
      <div className="text-center mb-8 animate-fade-in">
        <div className="w-20 h-20 bg-primary rounded-2xl flex items-center justify-center mx-auto mb-4 card-shadow">
          <FileStack className="w-10 h-10 text-primary-foreground" />
        </div>
        <h1 className="text-3xl font-bold text-foreground mb-2">{t('login.title')}</h1>
        <p className="text-muted-foreground">{t('login.subtitle')}</p>
      </div>

      {/* Login Card */}
      <Card className="w-full max-w-md animate-slide-up card-shadow">
        <CardHeader className="text-center">
          <CardTitle className="text-xl">{t('login.button')}</CardTitle>
          <CardDescription>
            {language === 'en' 
              ? 'Enter your credentials to access your account' 
              : 'ඔබගේ ගිණුමට ප්‍රවේශ වීමට අක්තපත්‍ර ඇතුලත් කරන්න'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">{t('login.email')}</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <Input
                  id="email"
                  type="email"
                  placeholder="name@office.lk"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-10"
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">{t('login.password')}</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <Input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-10"
                  required
                  minLength={4}
                />
              </div>
            </div>

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  {t('common.loading')}
                </>
              ) : (
                t('login.button')
              )}
            </Button>
          </form>

          <p className="text-center text-xs text-muted-foreground mt-6">
            {language === 'en' 
              ? 'Demo: Use any email and password (min 4 chars)' 
              : 'Demo: ඕනෑම විද්‍යුත් තැපෑලක් සහ මුරපදයක් භාවිතා කරන්න (අවම අක්ෂර 4)'}
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default Login;
