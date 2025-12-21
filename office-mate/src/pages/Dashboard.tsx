import React from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FileText, 
  CheckSquare, 
  Clock, 
  TrendingUp,
  ArrowRight,
  AlertCircle
} from 'lucide-react';
import { useLanguage } from '@/context/LanguageContext';
import { useAuth } from '@/context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { mockDocuments, mockTasks } from '@/services/api';
import { format, isAfter, parseISO, addDays } from 'date-fns';

const Dashboard: React.FC = () => {
  const { t } = useLanguage();
  const { user } = useAuth();
  const navigate = useNavigate();

  // Calculate stats
  const totalDocs = mockDocuments.length;
  const openTasks = mockTasks.filter(t => t.status !== 'completed').length;
  const upcomingDeadlines = mockTasks.filter(t => {
    if (!t.dueDate || t.status === 'completed') return false;
    const due = parseISO(t.dueDate);
    return isAfter(due, new Date()) && isAfter(addDays(new Date(), 7), due);
  }).length;

  // Category counts
  const categoryStats = {
    Finance: mockDocuments.filter(d => d.category === 'Finance').length,
    HR: mockDocuments.filter(d => d.category === 'HR').length,
    Procurement: mockDocuments.filter(d => d.category === 'Procurement').length,
    Maintenance: mockDocuments.filter(d => d.category === 'Maintenance').length,
  };

  const categoryColors = {
    Finance: 'bg-finance text-finance-foreground',
    HR: 'bg-hr text-hr-foreground',
    Procurement: 'bg-procurement text-procurement-foreground',
    Maintenance: 'bg-maintenance text-maintenance-foreground',
  };

  const categoryKeys = {
    Finance: 'category.finance',
    HR: 'category.hr',
    Procurement: 'category.procurement',
    Maintenance: 'category.maintenance',
  };

  const stats = [
    { 
      title: t('dashboard.totalDocs'), 
      value: totalDocs, 
      icon: FileText, 
      color: 'text-primary',
      bgColor: 'bg-primary/10'
    },
    { 
      title: t('dashboard.openTasks'), 
      value: openTasks, 
      icon: CheckSquare, 
      color: 'text-warning',
      bgColor: 'bg-warning/10'
    },
    { 
      title: t('dashboard.upcoming'), 
      value: upcomingDeadlines, 
      icon: Clock, 
      color: 'text-destructive',
      bgColor: 'bg-destructive/10'
    },
  ];

  const recentDocs = mockDocuments.slice(0, 5);
  const urgentTasks = mockTasks
    .filter(t => t.status !== 'completed' && t.priority === 'high')
    .slice(0, 3);

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-2xl lg:text-3xl font-bold text-foreground">
          {t('dashboard.welcome')}, {user?.name?.split(' ')[0]}! 👋
        </h1>
        <p className="text-muted-foreground mt-1">{t('dashboard.overview')}</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {stats.map((stat, index) => (
          <Card key={index} className="card-shadow hover:card-shadow-lg transition-shadow duration-300">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">{stat.title}</p>
                  <p className="text-3xl font-bold text-foreground mt-1">{stat.value}</p>
                </div>
                <div className={`w-12 h-12 rounded-xl ${stat.bgColor} flex items-center justify-center`}>
                  <stat.icon className={`w-6 h-6 ${stat.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Category Stats */}
      <Card className="card-shadow">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-lg">{t('dashboard.byCategory')}</CardTitle>
          <TrendingUp className="w-5 h-5 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {Object.entries(categoryStats).map(([category, count]) => (
              <div 
                key={category}
                className="p-4 rounded-xl bg-muted/50 hover:bg-muted transition-colors cursor-pointer"
                onClick={() => navigate(`/documents?category=${category}`)}
              >
                <div className="flex items-center gap-3 mb-2">
                  <div className={`w-3 h-3 rounded-full ${categoryColors[category as keyof typeof categoryColors].split(' ')[0]}`} />
                  <span className="text-sm font-medium text-foreground">
                    {t(categoryKeys[category as keyof typeof categoryKeys])}
                  </span>
                </div>
                <p className="text-2xl font-bold text-foreground">{count}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Two Column Layout */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Recent Documents */}
        <Card className="card-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-4">
            <CardTitle className="text-lg">{t('dashboard.recentDocs')}</CardTitle>
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={() => navigate('/documents')}
              className="text-primary"
            >
              {t('docs.view')}
              <ArrowRight className="w-4 h-4 ml-1" />
            </Button>
          </CardHeader>
          <CardContent className="space-y-3">
            {recentDocs.map((doc) => (
              <div 
                key={doc.id}
                className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted/50 transition-colors cursor-pointer"
                onClick={() => navigate(`/documents?id=${doc.id}`)}
              >
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${categoryColors[doc.category].split(' ')[0]}`}>
                  <FileText className="w-5 h-5 text-white" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-foreground truncate">{doc.filename}</p>
                  <p className="text-xs text-muted-foreground">
                    {format(parseISO(doc.createdAt), 'MMM dd, yyyy')}
                  </p>
                </div>
                <Badge variant="secondary" className="hidden sm:inline-flex">
                  {t(categoryKeys[doc.category])}
                </Badge>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Urgent Tasks */}
        <Card className="card-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-4">
            <CardTitle className="text-lg flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-destructive" />
              {t('tasks.high')} {t('tasks.priority')}
            </CardTitle>
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={() => navigate('/tasks')}
              className="text-primary"
            >
              {t('tasks.all')}
              <ArrowRight className="w-4 h-4 ml-1" />
            </Button>
          </CardHeader>
          <CardContent className="space-y-3">
            {urgentTasks.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-4">
                {t('tasks.noTasks')}
              </p>
            ) : (
              urgentTasks.map((task) => (
                <div 
                  key={task.id}
                  className="p-4 rounded-lg border border-destructive/20 bg-destructive/5 hover:bg-destructive/10 transition-colors cursor-pointer"
                  onClick={() => navigate('/tasks')}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-foreground">{task.title}</p>
                      {task.description && (
                        <p className="text-sm text-muted-foreground mt-1 line-clamp-1">
                          {task.description}
                        </p>
                      )}
                    </div>
                    {task.dueDate && (
                      <Badge variant="destructive" className="shrink-0">
                        {format(parseISO(task.dueDate), 'MMM dd')}
                      </Badge>
                    )}
                  </div>
                  {task.documentName && (
                    <p className="text-xs text-muted-foreground mt-2 flex items-center gap-1">
                      <FileText className="w-3 h-3" />
                      {task.documentName}
                    </p>
                  )}
                </div>
              ))
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
