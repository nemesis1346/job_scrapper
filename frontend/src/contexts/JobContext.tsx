/**
 * Job Context for Web3 Job Seeker Frontend
 * 
 * This context provides global state management for:
 * - Job data and filtering
 * - Search and filter state
 * - Loading and error states
 * - Pagination
 * 
 * @author Web3 Job Seeker Team
 * @version 1.0.0
 */

import React, { createContext, useContext, useReducer, useCallback, ReactNode } from 'react';

// Types
export interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  country: string;
  city?: string;
  description: string;
  description_text?: string;
  apply_url: string;
  salary_min?: number;
  salary_max?: number;
  salary_currency?: string;
  tags: string[];
  job_type?: string;
  experience_level?: string;
  date: string;
  date_epoch?: number;
  remote: boolean;
  featured: boolean;
}

export interface JobFilters {
  tags: string[];
  country?: string;
  company?: string;
  job_type?: string;
  experience_level?: string;
  remote_only?: boolean;
  salary_min?: number;
  salary_max?: number;
}

export interface JobState {
  jobs: Job[];
  filteredJobs: Job[];
  loading: boolean;
  error: string | null;
  filters: JobFilters;
  pagination: {
    currentPage: number;
    itemsPerPage: number;
    totalItems: number;
  };
  selectedJob: Job | null;
  availableTags: Array<{
    name: string;
    count: number;
    category?: string;
  }>;
  lastRefresh: Date | null;
}

// Action types
export type JobAction =
  | { type: 'SET_JOBS'; payload: Job[] }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_FILTERS'; payload: Partial<JobFilters> }
  | { type: 'CLEAR_FILTERS' }
  | { type: 'SET_PAGINATION'; payload: Partial<JobState['pagination']> }
  | { type: 'SET_SELECTED_JOB'; payload: Job | null }
  | { type: 'SET_AVAILABLE_TAGS'; payload: Array<{ name: string; count: number; category?: string }> }
  | { type: 'SET_LAST_REFRESH'; payload: Date }
  | { type: 'ADD_TAG_FILTER'; payload: string }
  | { type: 'REMOVE_TAG_FILTER'; payload: string }
  | { type: 'CLEAR_TAG_FILTERS' };

// Initial state
const initialState: JobState = {
  jobs: [],
  filteredJobs: [],
  loading: false,
  error: null,
  filters: {
    tags: [],
    country: undefined,
    company: undefined,
    job_type: undefined,
    experience_level: undefined,
    remote_only: undefined,
    salary_min: undefined,
    salary_max: undefined,
  },
  pagination: {
    currentPage: 1,
    itemsPerPage: 12,
    totalItems: 0,
  },
  selectedJob: null,
  availableTags: [],
  lastRefresh: null,
};

// Reducer function
function jobReducer(state: JobState, action: JobAction): JobState {
  switch (action.type) {
    case 'SET_JOBS':
      return {
        ...state,
        jobs: action.payload,
        filteredJobs: applyFilters(action.payload, state.filters),
        pagination: {
          ...state.pagination,
          totalItems: action.payload.length,
          currentPage: 1, // Reset to first page when new jobs are loaded
        },
      };

    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload,
      };

    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        loading: false,
      };

    case 'SET_FILTERS':
      const newFilters = { ...state.filters, ...action.payload };
      const filteredJobs = applyFilters(state.jobs, newFilters);
      return {
        ...state,
        filters: newFilters,
        filteredJobs,
        pagination: {
          ...state.pagination,
          currentPage: 1, // Reset to first page when filters change
          totalItems: filteredJobs.length,
        },
      };

    case 'CLEAR_FILTERS':
      return {
        ...state,
        filters: initialState.filters,
        filteredJobs: state.jobs,
        pagination: {
          ...state.pagination,
          currentPage: 1,
          totalItems: state.jobs.length,
        },
      };

    case 'SET_PAGINATION':
      return {
        ...state,
        pagination: { ...state.pagination, ...action.payload },
      };

    case 'SET_SELECTED_JOB':
      return {
        ...state,
        selectedJob: action.payload,
      };

    case 'SET_AVAILABLE_TAGS':
      return {
        ...state,
        availableTags: action.payload,
      };

    case 'SET_LAST_REFRESH':
      return {
        ...state,
        lastRefresh: action.payload,
      };

    case 'ADD_TAG_FILTER':
      if (!state.filters.tags.includes(action.payload)) {
        const newTags = [...state.filters.tags, action.payload];
        const newFilters = { ...state.filters, tags: newTags };
        const filteredJobs = applyFilters(state.jobs, newFilters);
        return {
          ...state,
          filters: newFilters,
          filteredJobs,
          pagination: {
            ...state.pagination,
            currentPage: 1,
            totalItems: filteredJobs.length,
          },
        };
      }
      return state;

    case 'REMOVE_TAG_FILTER':
      const updatedTags = state.filters.tags.filter(tag => tag !== action.payload);
      const updatedFilters = { ...state.filters, tags: updatedTags };
      const updatedFilteredJobs = applyFilters(state.jobs, updatedFilters);
      return {
        ...state,
        filters: updatedFilters,
        filteredJobs: updatedFilteredJobs,
        pagination: {
          ...state.pagination,
          currentPage: 1,
          totalItems: updatedFilteredJobs.length,
        },
      };

    case 'CLEAR_TAG_FILTERS':
      const clearedFilters = { ...state.filters, tags: [] };
      const clearedFilteredJobs = applyFilters(state.jobs, clearedFilters);
      return {
        ...state,
        filters: clearedFilters,
        filteredJobs: clearedFilteredJobs,
        pagination: {
          ...state.pagination,
          currentPage: 1,
          totalItems: clearedFilteredJobs.length,
        },
      };

    default:
      return state;
  }
}

// Filter function
function applyFilters(jobs: Job[], filters: JobFilters): Job[] {
  return jobs.filter(job => {
    // Filter by tags
    if (filters.tags.length > 0) {
      const jobTags = job.tags.map(tag => tag.toLowerCase());
      const filterTags = filters.tags.map(tag => tag.toLowerCase());
      if (!filterTags.some(tag => jobTags.includes(tag))) {
        return false;
      }
    }

    // Filter by country
    if (filters.country && job.country.toLowerCase() !== filters.country.toLowerCase()) {
      return false;
    }

    // Filter by company
    if (filters.company && !job.company.toLowerCase().includes(filters.company.toLowerCase())) {
      return false;
    }

    // Filter by job type
    if (filters.job_type && job.job_type !== filters.job_type) {
      return false;
    }

    // Filter by experience level
    if (filters.experience_level && job.experience_level !== filters.experience_level) {
      return false;
    }

    // Filter by remote only
    if (filters.remote_only && !job.remote) {
      return false;
    }

    // Filter by salary range
    if (filters.salary_min && job.salary_max && job.salary_max < filters.salary_min) {
      return false;
    }
    if (filters.salary_max && job.salary_min && job.salary_min > filters.salary_max) {
      return false;
    }

    return true;
  });
}

// Context
const JobContext = createContext<{
  state: JobState;
  dispatch: React.Dispatch<JobAction>;
  actions: {
    setJobs: (jobs: Job[]) => void;
    setLoading: (loading: boolean) => void;
    setError: (error: string | null) => void;
    setFilters: (filters: Partial<JobFilters>) => void;
    clearFilters: () => void;
    addTagFilter: (tag: string) => void;
    removeTagFilter: (tag: string) => void;
    clearTagFilters: () => void;
    setSelectedJob: (job: Job | null) => void;
    setAvailableTags: (tags: Array<{ name: string; count: number; category?: string }>) => void;
    setLastRefresh: (date: Date) => void;
    goToPage: (page: number) => void;
    getPaginatedJobs: () => Job[];
  };
} | undefined>(undefined);

// Provider component
export const JobProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(jobReducer, initialState);

  // Action creators
  const setJobs = useCallback((jobs: Job[]) => {
    dispatch({ type: 'SET_JOBS', payload: jobs });
  }, []);

  const setLoading = useCallback((loading: boolean) => {
    dispatch({ type: 'SET_LOADING', payload: loading });
  }, []);

  const setError = useCallback((error: string | null) => {
    dispatch({ type: 'SET_ERROR', payload: error });
  }, []);

  const setFilters = useCallback((filters: Partial<JobFilters>) => {
    dispatch({ type: 'SET_FILTERS', payload: filters });
  }, []);

  const clearFilters = useCallback(() => {
    dispatch({ type: 'CLEAR_FILTERS' });
  }, []);

  const addTagFilter = useCallback((tag: string) => {
    dispatch({ type: 'ADD_TAG_FILTER', payload: tag });
  }, []);

  const removeTagFilter = useCallback((tag: string) => {
    dispatch({ type: 'REMOVE_TAG_FILTER', payload: tag });
  }, []);

  const clearTagFilters = useCallback(() => {
    dispatch({ type: 'CLEAR_TAG_FILTERS' });
  }, []);

  const setSelectedJob = useCallback((job: Job | null) => {
    dispatch({ type: 'SET_SELECTED_JOB', payload: job });
  }, []);

  const setAvailableTags = useCallback((tags: Array<{ name: string; count: number; category?: string }>) => {
    dispatch({ type: 'SET_AVAILABLE_TAGS', payload: tags });
  }, []);

  const setLastRefresh = useCallback((date: Date) => {
    dispatch({ type: 'SET_LAST_REFRESH', payload: date });
  }, []);

  const goToPage = useCallback((page: number) => {
    const maxPage = Math.ceil(state.pagination.totalItems / state.pagination.itemsPerPage);
    const validPage = Math.max(1, Math.min(page, maxPage));
    dispatch({ type: 'SET_PAGINATION', payload: { currentPage: validPage } });
  }, [state.pagination.totalItems, state.pagination.itemsPerPage]);

  const getPaginatedJobs = useCallback(() => {
    const startIndex = (state.pagination.currentPage - 1) * state.pagination.itemsPerPage;
    const endIndex = startIndex + state.pagination.itemsPerPage;
    return state.filteredJobs.slice(startIndex, endIndex);
  }, [state.filteredJobs, state.pagination.currentPage, state.pagination.itemsPerPage]);

  const value = {
    state,
    dispatch,
    actions: {
      setJobs,
      setLoading,
      setError,
      setFilters,
      clearFilters,
      addTagFilter,
      removeTagFilter,
      clearTagFilters,
      setSelectedJob,
      setAvailableTags,
      setLastRefresh,
      goToPage,
      getPaginatedJobs,
    },
  };

  return <JobContext.Provider value={value}>{children}</JobContext.Provider>;
};

// Hook to use the job context
export const useJobContext = () => {
  const context = useContext(JobContext);
  if (context === undefined) {
    throw new Error('useJobContext must be used within a JobProvider');
  }
  return context;
};

// Hook to get only the state
export const useJobState = () => {
  const context = useJobContext();
  return context.state;
};

// Hook to get only the actions
export const useJobActions = () => {
  const context = useJobContext();
  return context.actions;
};
