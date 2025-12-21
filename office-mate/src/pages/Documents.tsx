import React, { useState, useCallback } from 'react';
import { 
  Upload, 
  Search, 
  Filter, 
  FileText, 
  Eye, 
  X, 
  Tag,
  Calendar,
  Loader2,
  CheckSquare
} from 'lucide-react';
import { useLanguage } from '@/context/LanguageContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
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
  DialogDescription,
} from '@/components/ui/dialog';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { mockDocuments, mockTasks, Document } from '@/services/api';
import { useToast } from '@/hooks/use-toast';
import { format, parseISO } from 'date-fns';

const Documents: React.FC = () => {
  const { t, language } = useLanguage();
  const { toast } = useToast();

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [isUploading, setIsUploading] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const categories = [
    { value: 'all', label: t('category.all') },
    { value: 'Finance', label: t('category.finance') },
    { value: 'HR', label: t('category.hr') },
    { value: 'Procurement', label: t('category.procurement') },
    { value: 'Maintenance', label: t('category.maintenance') },
  ];

  const categoryColors = {
    Finance: 'bg-finance text-finance-foreground',
    HR: 'bg-hr text-hr-foreground',
    Procurement: 'bg-procurement text-procurement-foreground',
    Maintenance: 'bg-maintenance text-maintenance-foreground',
  };

  const filteredDocs = mockDocuments.filter(doc => {
    const matchesSearch = doc.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || doc.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleFileUpload = useCallback(async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    
    setIsUploading(true);
    
    // Simulate upload
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    toast({
      title: t('docs.uploadSuccess'),
      description: `${files[0].name} - ${language === 'en' ? 'Classified as Finance' : 'මූල්‍ය ලෙස වර්ග කරන ලදී'}`,
    });
    
    setIsUploading(false);
  }, [toast, t, language]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    handleFileUpload(e.dataTransfer.files);
  }, [handleFileUpload]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const linkedTasks = selectedDoc 
    ? mockTasks.filter(task => task.documentId === selectedDoc.id)
    : [];

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl lg:text-3xl font-bold text-foreground">{t('docs.title')}</h1>
          <p className="text-muted-foreground mt-1">
            {filteredDocs.length} {language === 'en' ? 'documents found' : 'ලේඛන හමු විය'}
          </p>
        </div>
      </div>

      {/* Upload Area */}
      <Card 
        className={`card-shadow border-2 border-dashed transition-colors ${
          isDragging ? 'border-primary bg-primary/5' : 'border-border'
        }`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <CardContent className="p-8 text-center">
          <input
            type="file"
            id="file-upload"
            className="hidden"
            onChange={(e) => handleFileUpload(e.target.files)}
            accept=".pdf,.doc,.docx,.xls,.xlsx"
          />
          <label 
            htmlFor="file-upload" 
            className="cursor-pointer flex flex-col items-center"
          >
            {isUploading ? (
              <>
                <Loader2 className="w-12 h-12 text-primary animate-spin mb-4" />
                <p className="text-muted-foreground">{t('docs.uploading')}</p>
              </>
            ) : (
              <>
                <Upload className={`w-12 h-12 mb-4 ${isDragging ? 'text-primary' : 'text-muted-foreground'}`} />
                <p className="text-foreground font-medium mb-1">{t('docs.upload')}</p>
                <p className="text-sm text-muted-foreground">{t('docs.dropzone')}</p>
              </>
            )}
          </label>
        </CardContent>
      </Card>

      {/* Search and Filter */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <Input
            placeholder={t('docs.search')}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>
        <Select value={selectedCategory} onValueChange={setSelectedCategory}>
          <SelectTrigger className="w-full sm:w-48">
            <Filter className="w-4 h-4 mr-2" />
            <SelectValue placeholder={t('docs.filter')} />
          </SelectTrigger>
          <SelectContent>
            {categories.map((cat) => (
              <SelectItem key={cat.value} value={cat.value}>
                {cat.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Documents Table */}
      <Card className="card-shadow overflow-hidden">
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>{t('docs.name')}</TableHead>
                <TableHead className="hidden sm:table-cell">{t('docs.category')}</TableHead>
                <TableHead className="hidden md:table-cell">{t('docs.tags')}</TableHead>
                <TableHead className="hidden lg:table-cell">{t('docs.date')}</TableHead>
                <TableHead className="text-right">{t('docs.actions')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredDocs.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                    {t('docs.noResults')}
                  </TableCell>
                </TableRow>
              ) : (
                filteredDocs.map((doc) => (
                  <TableRow key={doc.id} className="group">
                    <TableCell>
                      <div className="flex items-center gap-3">
                        <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${categoryColors[doc.category]}`}>
                          <FileText className="w-4 h-4" />
                        </div>
                        <div className="min-w-0">
                          <p className="font-medium text-foreground truncate max-w-[200px] sm:max-w-none">
                            {doc.filename}
                          </p>
                          <p className="text-xs text-muted-foreground sm:hidden">
                            {doc.category}
                          </p>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="hidden sm:table-cell">
                      <Badge className={categoryColors[doc.category]}>
                        {doc.category}
                      </Badge>
                    </TableCell>
                    <TableCell className="hidden md:table-cell">
                      <div className="flex gap-1 flex-wrap">
                        {doc.tags.slice(0, 2).map((tag) => (
                          <Badge key={tag} variant="secondary" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                      </div>
                    </TableCell>
                    <TableCell className="hidden lg:table-cell text-muted-foreground">
                      {format(parseISO(doc.createdAt), 'MMM dd, yyyy')}
                    </TableCell>
                    <TableCell className="text-right">
                      <Button 
                        variant="ghost" 
                        size="sm"
                        onClick={() => setSelectedDoc(doc)}
                      >
                        <Eye className="w-4 h-4 mr-1" />
                        <span className="hidden sm:inline">{t('docs.view')}</span>
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </Card>

      {/* Document Details Dialog */}
      <Dialog open={!!selectedDoc} onOpenChange={() => setSelectedDoc(null)}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          {selectedDoc && (
            <>
              <DialogHeader>
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${categoryColors[selectedDoc.category]}`}>
                    <FileText className="w-6 h-6" />
                  </div>
                  <div>
                    <DialogTitle className="text-xl">{selectedDoc.filename}</DialogTitle>
                    <DialogDescription className="flex items-center gap-2 mt-1">
                      <Calendar className="w-4 h-4" />
                      {format(parseISO(selectedDoc.createdAt), 'MMMM dd, yyyy')}
                    </DialogDescription>
                  </div>
                </div>
              </DialogHeader>

              <div className="space-y-6 mt-4">
                {/* Category & Tags */}
                <div className="flex flex-wrap gap-2">
                  <Badge className={categoryColors[selectedDoc.category]}>
                    {selectedDoc.category}
                  </Badge>
                  {selectedDoc.tags.map((tag) => (
                    <Badge key={tag} variant="secondary">
                      <Tag className="w-3 h-3 mr-1" />
                      {tag}
                    </Badge>
                  ))}
                </div>

                {/* AI Summary */}
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                      {t('docs.summary')}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {language === 'en' 
                        ? `This ${selectedDoc.category.toLowerCase()} document contains important information related to ${selectedDoc.tags.join(' and ')}. The AI has analyzed the content and extracted key data points for quick reference. Review the linked tasks below for action items.`
                        : `මෙම ${selectedDoc.category} ලේඛනයේ ${selectedDoc.tags.join(' සහ ')} සම්බන්ධ වැදගත් තොරතුරු අඩංගු වේ. AI විසින් අන්තර්ගතය විශ්ලේෂණය කර ඉක්මන් යොමුව සඳහා ප්‍රධාන දත්ත කරුණු උපුටා ගෙන ඇත.`}
                    </p>
                  </CardContent>
                </Card>

                {/* Linked Tasks */}
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium flex items-center gap-2">
                      <CheckSquare className="w-4 h-4" />
                      {t('docs.linkedTasks')} ({linkedTasks.length})
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    {linkedTasks.length === 0 ? (
                      <p className="text-sm text-muted-foreground">
                        {language === 'en' ? 'No tasks linked to this document' : 'මෙම ලේඛනයට සම්බන්ධ කාර්යයන් නොමැත'}
                      </p>
                    ) : (
                      <div className="space-y-2">
                        {linkedTasks.map((task) => (
                          <div 
                            key={task.id} 
                            className="flex items-center justify-between p-3 rounded-lg bg-muted/50"
                          >
                            <div className="flex items-center gap-3">
                              <CheckSquare className={`w-4 h-4 ${
                                task.status === 'completed' ? 'text-success' : 'text-muted-foreground'
                              }`} />
                              <span className={`text-sm ${
                                task.status === 'completed' ? 'line-through text-muted-foreground' : 'text-foreground'
                              }`}>
                                {task.title}
                              </span>
                            </div>
                            <Badge variant={
                              task.status === 'completed' ? 'secondary' :
                              task.priority === 'high' ? 'destructive' : 'secondary'
                            }>
                              {task.status === 'completed' ? t('tasks.completed') : 
                               task.priority === 'high' ? t('tasks.high') : t('tasks.pending')}
                            </Badge>
                          </div>
                        ))}
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Documents;
