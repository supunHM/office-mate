import axios, { AxiosError } from 'axios';

// Configure base URL - adjust this to your Python backend URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface Document {
  id: string;
  filename: string;
  category: 'Finance' | 'HR' | 'Procurement' | 'Maintenance';
  tags: string[];
  createdAt: string;
  summary?: string;
}

export interface DocumentDetails extends Document {
  extractedText?: string;
  linkedTasks?: Task[];
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'in_progress' | 'completed';
  priority: 'high' | 'medium' | 'low';
  dueDate?: string;
  documentId?: string;
  documentName?: string;
  createdAt: string;
  reminder?: string;
}

export interface DocumentSearchParams {
  query?: string;
  category?: string;
  from?: string;
  to?: string;
}

// API Error Handler
const handleApiError = (error: AxiosError): never => {
  if (error.response) {
    throw new Error(`API Error: ${error.response.status} - ${error.response.statusText}`);
  } else if (error.request) {
    throw new Error('Network error: Unable to reach the server');
  } else {
    throw new Error(`Error: ${error.message}`);
  }
};

// Document APIs
export const documentsApi = {
  upload: async (file: File): Promise<Document> => {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await api.post<Document>('/documents', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return response.data;
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },

  search: async (params: DocumentSearchParams): Promise<Document[]> => {
    try {
      const response = await api.get<Document[]>('/documents', { params });
      return response.data;
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },

  getById: async (id: string): Promise<DocumentDetails> => {
    try {
      const response = await api.get<DocumentDetails>(`/documents/${id}`);
      return response.data;
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },
};

// Task APIs
export const tasksApi = {
  getAll: async (status?: string): Promise<Task[]> => {
    try {
      const response = await api.get<Task[]>('/tasks', { 
        params: status ? { status } : undefined 
      });
      return response.data;
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },

  create: async (task: Omit<Task, 'id' | 'createdAt'>): Promise<Task> => {
    try {
      const response = await api.post<Task>('/tasks', task);
      return response.data;
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },

  update: async (id: string, updates: Partial<Task>): Promise<Task> => {
    try {
      const response = await api.patch<Task>(`/tasks/${id}`, updates);
      return response.data;
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },

  delete: async (id: string): Promise<void> => {
    try {
      await api.delete(`/tasks/${id}`);
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },
};

// Mock data for demo when backend is not available
export const mockDocuments: Document[] = [
  { id: '1', filename: 'Budget_Report_Q4_2024.pdf', category: 'Finance', tags: ['budget', 'quarterly'], createdAt: '2024-12-15T10:30:00Z' },
  { id: '2', filename: 'Employee_Onboarding_Guide.docx', category: 'HR', tags: ['onboarding', 'policy'], createdAt: '2024-12-14T09:00:00Z' },
  { id: '3', filename: 'Vendor_Contract_ABC.pdf', category: 'Procurement', tags: ['contract', 'vendor'], createdAt: '2024-12-13T14:20:00Z' },
  { id: '4', filename: 'HVAC_Service_Schedule.xlsx', category: 'Maintenance', tags: ['hvac', 'schedule'], createdAt: '2024-12-12T11:45:00Z' },
  { id: '5', filename: 'Payroll_December_2024.pdf', category: 'Finance', tags: ['payroll', 'salary'], createdAt: '2024-12-11T08:00:00Z' },
  { id: '6', filename: 'Leave_Policy_2025.pdf', category: 'HR', tags: ['leave', 'policy'], createdAt: '2024-12-10T16:30:00Z' },
  { id: '7', filename: 'Office_Supplies_Order.pdf', category: 'Procurement', tags: ['supplies', 'order'], createdAt: '2024-12-09T13:15:00Z' },
  { id: '8', filename: 'Fire_Safety_Inspection.pdf', category: 'Maintenance', tags: ['safety', 'inspection'], createdAt: '2024-12-08T10:00:00Z' },
];

export const mockTasks: Task[] = [
  { id: '1', title: 'Review Q4 Budget Report', description: 'Analyze quarterly expenses and prepare summary', status: 'pending', priority: 'high', dueDate: '2024-12-22', documentId: '1', documentName: 'Budget_Report_Q4_2024.pdf', createdAt: '2024-12-15T10:30:00Z' },
  { id: '2', title: 'Update onboarding checklist', description: 'Add new IT security training requirements', status: 'in_progress', priority: 'medium', dueDate: '2024-12-23', documentId: '2', documentName: 'Employee_Onboarding_Guide.docx', createdAt: '2024-12-14T09:00:00Z' },
  { id: '3', title: 'Vendor contract renewal', description: 'Negotiate terms with ABC Corp', status: 'pending', priority: 'high', dueDate: '2024-12-25', documentId: '3', documentName: 'Vendor_Contract_ABC.pdf', createdAt: '2024-12-13T14:20:00Z' },
  { id: '4', title: 'Schedule HVAC maintenance', description: 'Coordinate with maintenance team', status: 'completed', priority: 'low', dueDate: '2024-12-20', documentId: '4', documentName: 'HVAC_Service_Schedule.xlsx', createdAt: '2024-12-12T11:45:00Z' },
  { id: '5', title: 'Process payroll', description: 'December salary processing', status: 'pending', priority: 'high', dueDate: '2024-12-24', documentId: '5', documentName: 'Payroll_December_2024.pdf', createdAt: '2024-12-11T08:00:00Z' },
];

export default api;
