/* eslint-disable @typescript-eslint/no-explicit-any */
import axios, { AxiosError } from "axios";

// Configure base URL - Flask backend
const API_BASE_URL = import.meta.env.VITE_API_URL;

if (!API_BASE_URL) {
  throw new Error(
    "VITE_API_URL environment variable is not set. Please create a .env.local file with VITE_API_URL=http://localhost:5000"
  );
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add JWT token to all requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("authToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Helper to normalize document field names from backend to frontend
const normalizeDocument = (doc: any): Document => ({
  ...doc,
  filename: doc.original_name || doc.filename,
  createdAt: doc.created_at || doc.createdAt,
});

// Helper to normalize task field names
const normalizeTask = (task: any): Task => ({
  ...task,
  dueDate: task.due_date || task.dueDate,
  createdAt: task.created_at || task.createdAt,
  documentName: task.document?.original_name || task.documentName,
});

// Types
export interface Document {
  id: string;
  filename?: string; // For frontend compatibility
  original_name?: string; // Backend field name
  category: "Finance" | "HR" | "Procurement" | "Maintenance";
  tags: string[];
  createdAt?: string; // Frontend field
  created_at?: string; // Backend field
  summary?: string;
  text_preview?: string;
}

export interface DocumentDetails extends Document {
  extractedText?: string;
  linkedTasks?: Task[];
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: "pending" | "in_progress" | "completed";
  priority: "high" | "medium" | "low";
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
    throw new Error(
      `API Error: ${error.response.status} - ${error.response.statusText}`
    );
  } else if (error.request) {
    throw new Error("Network error: Unable to reach the server");
  } else {
    throw new Error(`Error: ${error.message}`);
  }
};

// Document APIs
export const documentsApi = {
  upload: async (file: File): Promise<Document> => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post<Document>("/api/documents", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      return normalizeDocument(response.data);
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },

  getAll: async (): Promise<Document[]> => {
    try {
      const response = await api.get<{
        documents: Document[];
        pagination: any;
      }>("/api/documents");
      return response.data.documents.map(normalizeDocument);
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },

  search: async (params: DocumentSearchParams): Promise<Document[]> => {
    try {
      const response = await api.get<{
        documents: Document[];
        pagination: any;
      }>("/api/documents", { params });
      return response.data.documents.map(normalizeDocument);
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
// REPORT REQUIREMENT: Task management endpoints for create, list, update, delete
export const tasksApi = {
  // Get all tasks with optional filtering
  // REPORT REQUIREMENT: Filter by status, due_from, due_to, and linked_document_id
  getAll: async (params?: {
    status?: string;
    document_id?: string;
  }): Promise<Task[]> => {
    try {
      const response = await api.get<{ tasks: Task[]; pagination: any }>(
        "/api/tasks",
        {
          params,
        }
      );
      return response.data.tasks.map(normalizeTask);
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },

  // Get upcoming tasks (next 2-3 days) - REPORT REQUIREMENT: deadline reminders
  getUpcoming: async (days: number = 3): Promise<Task[]> => {
    try {
      const response = await api.get<{
        tasks: Task[];
        count: number;
        period_days: number;
      }>("/api/tasks/upcoming", {
        params: { days },
      });
      return response.data.tasks.map(normalizeTask);
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },

  // Create a new task - REPORT REQUIREMENT: Users can create tasks linked to documents
  create: async (task: Omit<Task, "id" | "createdAt">): Promise<Task> => {
    try {
      // Map frontend field names to backend expectations
      const payload = {
        title: task.title,
        description: task.description || "",
        priority: task.priority || "medium",
        status: task.status || "pending",
        due_date: task.dueDate || null,
        document_id: task.documentId || null,
      };
      const response = await api.post<Task>("/api/tasks", payload);
      return normalizeTask(response.data);
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },

  // Update existing task - REPORT REQUIREMENT: Update status and details
  update: async (id: string, updates: Partial<Task>): Promise<Task> => {
    try {
      // Map frontend field names to backend expectations
      const payload: any = {};
      if (updates.title !== undefined) payload.title = updates.title;
      if (updates.description !== undefined)
        payload.description = updates.description;
      if (updates.priority !== undefined) payload.priority = updates.priority;
      if (updates.status !== undefined) payload.status = updates.status;
      if (updates.dueDate !== undefined) payload.due_date = updates.dueDate;
      if (updates.documentId !== undefined)
        payload.document_id = updates.documentId;

      const response = await api.patch<Task>(`/api/tasks/${id}`, payload);
      return normalizeTask(response.data);
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },

  // Delete a task
  delete: async (id: string): Promise<void> => {
    try {
      await api.delete(`/api/tasks/${id}`);
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },

  // Get tasks linked to a specific document - REPORT REQUIREMENT
  getByDocument: async (documentId: string): Promise<Task[]> => {
    try {
      const response = await api.get<{ tasks: Task[]; pagination: any }>(
        "/api/tasks",
        {
          params: { document_id: documentId },
        }
      );
      return response.data.tasks.map(normalizeTask);
    } catch (error) {
      return handleApiError(error as AxiosError);
    }
  },
};

// Mock data for demo when backend is not available
export const mockDocuments: Document[] = [
  {
    id: "1",
    filename: "Budget_Report_Q4_2024.pdf",
    category: "Finance",
    tags: ["budget", "quarterly"],
    createdAt: "2024-12-15T10:30:00Z",
  },
  {
    id: "2",
    filename: "Employee_Onboarding_Guide.docx",
    category: "HR",
    tags: ["onboarding", "policy"],
    createdAt: "2024-12-14T09:00:00Z",
  },
  {
    id: "3",
    filename: "Vendor_Contract_ABC.pdf",
    category: "Procurement",
    tags: ["contract", "vendor"],
    createdAt: "2024-12-13T14:20:00Z",
  },
  {
    id: "4",
    filename: "HVAC_Service_Schedule.xlsx",
    category: "Maintenance",
    tags: ["hvac", "schedule"],
    createdAt: "2024-12-12T11:45:00Z",
  },
  {
    id: "5",
    filename: "Payroll_December_2024.pdf",
    category: "Finance",
    tags: ["payroll", "salary"],
    createdAt: "2024-12-11T08:00:00Z",
  },
  {
    id: "6",
    filename: "Leave_Policy_2025.pdf",
    category: "HR",
    tags: ["leave", "policy"],
    createdAt: "2024-12-10T16:30:00Z",
  },
  {
    id: "7",
    filename: "Office_Supplies_Order.pdf",
    category: "Procurement",
    tags: ["supplies", "order"],
    createdAt: "2024-12-09T13:15:00Z",
  },
  {
    id: "8",
    filename: "Fire_Safety_Inspection.pdf",
    category: "Maintenance",
    tags: ["safety", "inspection"],
    createdAt: "2024-12-08T10:00:00Z",
  },
];

export const mockTasks: Task[] = [
  {
    id: "1",
    title: "Review Q4 Budget Report",
    description: "Analyze quarterly expenses and prepare summary",
    status: "pending",
    priority: "high",
    dueDate: "2024-12-22",
    documentId: "1",
    documentName: "Budget_Report_Q4_2024.pdf",
    createdAt: "2024-12-15T10:30:00Z",
  },
  {
    id: "2",
    title: "Update onboarding checklist",
    description: "Add new IT security training requirements",
    status: "in_progress",
    priority: "medium",
    dueDate: "2024-12-23",
    documentId: "2",
    documentName: "Employee_Onboarding_Guide.docx",
    createdAt: "2024-12-14T09:00:00Z",
  },
  {
    id: "3",
    title: "Vendor contract renewal",
    description: "Negotiate terms with ABC Corp",
    status: "pending",
    priority: "high",
    dueDate: "2024-12-25",
    documentId: "3",
    documentName: "Vendor_Contract_ABC.pdf",
    createdAt: "2024-12-13T14:20:00Z",
  },
  {
    id: "4",
    title: "Schedule HVAC maintenance",
    description: "Coordinate with maintenance team",
    status: "completed",
    priority: "low",
    dueDate: "2024-12-20",
    documentId: "4",
    documentName: "HVAC_Service_Schedule.xlsx",
    createdAt: "2024-12-12T11:45:00Z",
  },
  {
    id: "5",
    title: "Process payroll",
    description: "December salary processing",
    status: "pending",
    priority: "high",
    dueDate: "2024-12-24",
    documentId: "5",
    documentName: "Payroll_December_2024.pdf",
    createdAt: "2024-12-11T08:00:00Z",
  },
];

export default api;
