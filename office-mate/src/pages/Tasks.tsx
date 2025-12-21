import React, { useState } from 'react';
import { 
  Plus, 
  Filter, 
  CheckSquare, 
  Clock, 
  Edit2, 
  Trash2,
  FileText,
  Bell,
  AlertCircle,
  CheckCircle2,
  Circle
} from 'lucide-react';
import { useLanguage } from '@/context/LanguageContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Label } from '@/components/ui/label';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { mockTasks, mockDocuments, Task } from '@/services/api';
import { useToast } from '@/hooks/use-toast';
import { format, parseISO, isAfter, isBefore, addDays } from 'date-fns';

const Tasks: React.FC = () => {
  const { t, language } = useLanguage();
  const { toast } = useToast();

  const [tasks, setTasks] = useState<Task[]>(mockTasks);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deleteTask, setDeleteTask] = useState<Task | null>(null);

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: 'pending' as Task['status'],
    priority: 'medium' as Task['priority'],
    dueDate: '',
    documentId: '',
    reminder: '',
  });

  const statusOptions = [
    { value: 'all', label: t('tasks.all') },
    { value: 'pending', label: t('tasks.pending') },
    { value: 'in_progress', label: t('tasks.inProgress') },
    { value: 'completed', label: t('tasks.completed') },
  ];

  const priorityColors = {
    high: 'bg-destructive text-destructive-foreground',
    medium: 'bg-warning text-warning-foreground',
    low: 'bg-muted text-muted-foreground',
  };

  const statusIcons = {
    pending: Circle,
    in_progress: Clock,
    completed: CheckCircle2,
  };

  const filteredTasks = tasks.filter(task => 
    statusFilter === 'all' || task.status === statusFilter
  );

  const groupedTasks = {
    overdue: filteredTasks.filter(t => 
      t.dueDate && isBefore(parseISO(t.dueDate), new Date()) && t.status !== 'completed'
    ),
    today: filteredTasks.filter(t => {
      if (!t.dueDate || t.status === 'completed') return false;
      const due = parseISO(t.dueDate);
      return format(due, 'yyyy-MM-dd') === format(new Date(), 'yyyy-MM-dd');
    }),
    upcoming: filteredTasks.filter(t => {
      if (!t.dueDate || t.status === 'completed') return false;
      const due = parseISO(t.dueDate);
      return isAfter(due, new Date()) && format(due, 'yyyy-MM-dd') !== format(new Date(), 'yyyy-MM-dd');
    }),
    completed: filteredTasks.filter(t => t.status === 'completed'),
  };

  const openForm = (task?: Task) => {
    if (task) {
      setEditingTask(task);
      setFormData({
        title: task.title,
        description: task.description || '',
        status: task.status,
        priority: task.priority,
        dueDate: task.dueDate || '',
        documentId: task.documentId || '',
        reminder: task.reminder || '',
      });
    } else {
      setEditingTask(null);
      setFormData({
        title: '',
        description: '',
        status: 'pending',
        priority: 'medium',
        dueDate: '',
        documentId: '',
        reminder: '',
      });
    }
    setIsFormOpen(true);
  };

  const handleSave = () => {
    if (!formData.title.trim()) {
      toast({
        title: language === 'en' ? 'Error' : 'දෝෂය',
        description: language === 'en' ? 'Task title is required' : 'කාර්ය මාතෘකාව අවශ්‍යයි',
        variant: 'destructive',
      });
      return;
    }

    const linkedDoc = mockDocuments.find(d => d.id === formData.documentId);

    if (editingTask) {
      setTasks(prev => prev.map(t => 
        t.id === editingTask.id 
          ? { 
              ...t, 
              ...formData,
              documentName: linkedDoc?.filename,
            } 
          : t
      ));
      toast({
        title: language === 'en' ? 'Task updated' : 'කාර්යය යාවත්කාලීන කරන ලදී',
      });
    } else {
      const newTask: Task = {
        id: String(Date.now()),
        ...formData,
        documentName: linkedDoc?.filename,
        createdAt: new Date().toISOString(),
      };
      setTasks(prev => [newTask, ...prev]);
      toast({
        title: language === 'en' ? 'Task created' : 'කාර්යය නිර්මාණය කරන ලදී',
      });
    }

    setIsFormOpen(false);
  };

  const handleDelete = () => {
    if (deleteTask) {
      setTasks(prev => prev.filter(t => t.id !== deleteTask.id));
      toast({
        title: language === 'en' ? 'Task deleted' : 'කාර්යය මකා දමන ලදී',
      });
      setDeleteTask(null);
    }
  };

  const handleStatusChange = (taskId: string, newStatus: Task['status']) => {
    setTasks(prev => prev.map(t => 
      t.id === taskId ? { ...t, status: newStatus } : t
    ));
    toast({
      title: language === 'en' ? 'Status updated' : 'තත්ත්වය යාවත්කාලීන කරන ලදී',
    });
  };

  const TaskSection = ({ title, tasks, icon: Icon, variant }: { 
    title: string; 
    tasks: Task[]; 
    icon: React.ElementType;
    variant?: 'danger' | 'warning' | 'success' | 'default';
  }) => {
    if (tasks.length === 0) return null;

    const variantStyles = {
      danger: 'border-destructive/20 bg-destructive/5',
      warning: 'border-warning/20 bg-warning/5',
      success: 'border-success/20 bg-success/5',
      default: '',
    };

    return (
      <div className="space-y-3">
        <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground">
          <Icon className="w-4 h-4" />
          {title} ({tasks.length})
        </div>
        <div className="space-y-2">
          {tasks.map((task) => {
            const StatusIcon = statusIcons[task.status];
            return (
              <Card 
                key={task.id} 
                className={`card-shadow transition-all hover:card-shadow-lg ${variant ? variantStyles[variant] : ''}`}
              >
                <CardContent className="p-4">
                  <div className="flex items-start gap-3">
                    <button
                      onClick={() => handleStatusChange(
                        task.id, 
                        task.status === 'completed' ? 'pending' : 'completed'
                      )}
                      className="mt-0.5"
                    >
                      <StatusIcon className={`w-5 h-5 transition-colors ${
                        task.status === 'completed' 
                          ? 'text-success' 
                          : task.status === 'in_progress'
                            ? 'text-warning'
                            : 'text-muted-foreground hover:text-primary'
                      }`} />
                    </button>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2">
                        <p className={`font-medium ${
                          task.status === 'completed' ? 'line-through text-muted-foreground' : 'text-foreground'
                        }`}>
                          {task.title}
                        </p>
                        <div className="flex items-center gap-1 shrink-0">
                          <Button 
                            variant="ghost" 
                            size="icon" 
                            className="h-8 w-8"
                            onClick={() => openForm(task)}
                          >
                            <Edit2 className="w-4 h-4" />
                          </Button>
                          <Button 
                            variant="ghost" 
                            size="icon" 
                            className="h-8 w-8 text-destructive hover:text-destructive"
                            onClick={() => setDeleteTask(task)}
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                      
                      {task.description && (
                        <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
                          {task.description}
                        </p>
                      )}

                      <div className="flex flex-wrap items-center gap-2 mt-3">
                        <Badge className={priorityColors[task.priority]}>
                          {t(`tasks.${task.priority}`)}
                        </Badge>
                        
                        {task.dueDate && (
                          <Badge variant="outline" className="gap-1">
                            <Clock className="w-3 h-3" />
                            {format(parseISO(task.dueDate), 'MMM dd')}
                          </Badge>
                        )}
                        
                        {task.documentName && (
                          <Badge variant="secondary" className="gap-1">
                            <FileText className="w-3 h-3" />
                            <span className="max-w-[120px] truncate">{task.documentName}</span>
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl lg:text-3xl font-bold text-foreground">{t('tasks.title')}</h1>
          <p className="text-muted-foreground mt-1">
            {tasks.filter(t => t.status !== 'completed').length} {language === 'en' ? 'open tasks' : 'විවෘත කාර්යයන්'}
          </p>
        </div>
        <Button onClick={() => openForm()}>
          <Plus className="w-4 h-4 mr-2" />
          {t('tasks.add')}
        </Button>
      </div>

      {/* Filter */}
      <div className="flex gap-4">
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-full sm:w-48">
            <Filter className="w-4 h-4 mr-2" />
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {statusOptions.map((opt) => (
              <SelectItem key={opt.value} value={opt.value}>
                {opt.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Task Sections */}
      <div className="space-y-8">
        <TaskSection 
          title={t('common.overdue')} 
          tasks={groupedTasks.overdue} 
          icon={AlertCircle}
          variant="danger"
        />
        <TaskSection 
          title={t('common.today')} 
          tasks={groupedTasks.today} 
          icon={Clock}
          variant="warning"
        />
        <TaskSection 
          title={language === 'en' ? 'Upcoming' : 'ඉදිරි'} 
          tasks={groupedTasks.upcoming} 
          icon={CheckSquare}
        />
        <TaskSection 
          title={t('tasks.completed')} 
          tasks={groupedTasks.completed} 
          icon={CheckCircle2}
          variant="success"
        />

        {filteredTasks.length === 0 && (
          <Card className="card-shadow">
            <CardContent className="py-12 text-center">
              <CheckSquare className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
              <p className="text-muted-foreground">{t('tasks.noTasks')}</p>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Task Form Dialog */}
      <Dialog open={isFormOpen} onOpenChange={setIsFormOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>
              {editingTask ? t('tasks.edit') : t('tasks.add')}
            </DialogTitle>
          </DialogHeader>

          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="title">{t('tasks.taskName')}</Label>
              <Input
                id="title"
                value={formData.title}
                onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                placeholder={language === 'en' ? 'Enter task name...' : 'කාර්ය නම ඇතුලත් කරන්න...'}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">{t('tasks.description')}</Label>
              <Textarea
                id="description"
                value={formData.description}
                onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                placeholder={language === 'en' ? 'Add description...' : 'විස්තරය එක් කරන්න...'}
                rows={3}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>{t('tasks.priority')}</Label>
                <Select 
                  value={formData.priority} 
                  onValueChange={(v) => setFormData(prev => ({ ...prev, priority: v as Task['priority'] }))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="high">{t('tasks.high')}</SelectItem>
                    <SelectItem value="medium">{t('tasks.medium')}</SelectItem>
                    <SelectItem value="low">{t('tasks.low')}</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>{t('tasks.status')}</Label>
                <Select 
                  value={formData.status} 
                  onValueChange={(v) => setFormData(prev => ({ ...prev, status: v as Task['status'] }))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="pending">{t('tasks.pending')}</SelectItem>
                    <SelectItem value="in_progress">{t('tasks.inProgress')}</SelectItem>
                    <SelectItem value="completed">{t('tasks.completed')}</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="dueDate">{t('tasks.dueDate')}</Label>
              <Input
                id="dueDate"
                type="date"
                value={formData.dueDate}
                onChange={(e) => setFormData(prev => ({ ...prev, dueDate: e.target.value }))}
              />
            </div>

            <div className="space-y-2">
              <Label>{t('tasks.linkedDoc')}</Label>
              <Select 
                value={formData.documentId} 
                onValueChange={(v) => setFormData(prev => ({ ...prev, documentId: v }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder={language === 'en' ? 'Select a document...' : 'ලේඛනයක් තෝරන්න...'} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">
                    {language === 'en' ? 'No document' : 'ලේඛනයක් නොමැත'}
                  </SelectItem>
                  {mockDocuments.map((doc) => (
                    <SelectItem key={doc.id} value={doc.id}>
                      {doc.filename}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="reminder" className="flex items-center gap-2">
                <Bell className="w-4 h-4" />
                {t('tasks.reminder')}
              </Label>
              <Input
                id="reminder"
                type="datetime-local"
                value={formData.reminder}
                onChange={(e) => setFormData(prev => ({ ...prev, reminder: e.target.value }))}
              />
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setIsFormOpen(false)}>
              {t('tasks.cancel')}
            </Button>
            <Button onClick={handleSave}>
              {t('tasks.save')}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation */}
      <AlertDialog open={!!deleteTask} onOpenChange={() => setDeleteTask(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>
              {language === 'en' ? 'Delete Task?' : 'කාර්යය මකන්නද?'}
            </AlertDialogTitle>
            <AlertDialogDescription>
              {language === 'en' 
                ? 'This action cannot be undone. The task will be permanently deleted.'
                : 'මෙම ක්‍රියාව අහෝසි කළ නොහැක. කාර්යය ස්ථිරවම මකා දැමෙනු ඇත.'}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>{t('tasks.cancel')}</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
              {t('tasks.delete')}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default Tasks;
