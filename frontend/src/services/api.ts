/**
 * API Service for Web3 Job Seeker Frontend
 *
 * This service handles all communication with the backend API including:
 * - Job data fetching
 * - Filtering and search
 * - Tag management
 * - Statistics and health checks
 *
 * @author Web3 Job Seeker Team
 * @version 1.0.0
 */

import axios, { AxiosInstance, AxiosResponse } from "axios";
import { Job, JobFilters } from "../contexts/JobContext";

// API response types
export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

export interface JobResponse {
  jobs: Job[];
  total_count: number;
  limit: number;
  offset: number;
  filters: {
    tags?: string[];
    country?: string;
    company?: string;
  };
}

export interface TagInfo {
  name: string;
  count: number;
  category?: string;
}

export interface TagResponse {
  tags: TagInfo[];
  total_tags: number;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  job_count: number;
  last_refresh?: string;
}

export interface Statistics {
  total_jobs: number;
  remote_jobs: number;
  featured_jobs: number;
  total_companies: number;
  total_tags: number;
  jobs_by_country: Record<string, number>;
  top_tags: TagInfo[];
  top_companies: Array<{ name: string; job_count: number }>;
  salary_stats: {
    average?: number;
    median?: number;
    min?: number;
    max?: number;
  };
}

/**
 * API Service Class
 *
 * Handles all HTTP requests to the backend API with proper error handling,
 * request/response interceptors, and type safety.
 */
class ApiService {
  private api: AxiosInstance;
  private baseURL: string;

  constructor() {
    // Use proxy in development, direct URL in production
    this.baseURL =
      process.env.NODE_ENV === "production"
        ? process.env.REACT_APP_API_URL || "http://localhost:8000"
        : "";

    this.api = axios.create({
      baseURL: this.baseURL,
      timeout: 30000, // 30 seconds
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    // Request interceptor for logging and auth
    this.api.interceptors.request.use(
      (config) => {
        // Log requests in development
        if (process.env.NODE_ENV === "development") {
          console.log(
            `API Request: ${config.method?.toUpperCase()} ${config.url}`
          );
        }
        return config;
      },
      (error) => {
        console.error("API Request Error:", error);
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling
    this.api.interceptors.response.use(
      (response: AxiosResponse) => {
        // Log responses in development
        if (process.env.NODE_ENV === "development") {
          console.log(
            `API Response: ${response.status} ${response.config.url}`
          );
        }
        return response;
      },
      (error) => {
        console.error("API Response Error:", error);

        // Handle specific error cases
        if (error.response) {
          // Server responded with error status
          const { status, data } = error.response;

          switch (status) {
            case 404:
              throw new Error("Resource not found");
            case 429:
              throw new Error("Too many requests. Please try again later.");
            case 500:
              throw new Error("Server error. Please try again later.");
            default:
              throw new Error(
                data?.detail ||
                  `HTTP ${status}: ${data?.message || "Unknown error"}`
              );
          }
        } else if (error.request) {
          // Network error
          throw new Error("Network error. Please check your connection.");
        } else {
          // Other error
          throw new Error(error.message || "An unexpected error occurred.");
        }
      }
    );
  }

  /**
   * Get all jobs with optional filtering
   */
  async getJobs(
    filters?: Partial<JobFilters>,
    limit: number = 50,
    offset: number = 0
  ): Promise<JobResponse> {
    try {
      const params = new URLSearchParams();

      // Add filters to query parameters
      if (filters?.tags && filters.tags.length > 0) {
        params.append("tags", filters.tags.join(","));
      }
      if (filters?.country) {
        params.append("country", filters.country);
      }
      if (filters?.company) {
        params.append("company", filters.company);
      }
      if (limit) {
        params.append("limit", limit.toString());
      }
      if (offset) {
        params.append("offset", offset.toString());
      }

      const response = await this.api.get<JobResponse>(
        `/jobs?${params.toString()}`
      );
      return response.data;
    } catch (error) {
      console.error("Error fetching jobs:", error);
      throw error;
    }
  }

  /**
   * Get a specific job by ID
   */
  async getJobById(jobId: number): Promise<Job> {
    try {
      const response = await this.api.get<Job>(`/jobs/${jobId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching job ${jobId}:`, error);
      throw error;
    }
  }

  /**
   * Get all available tags
   */
  async getTags(): Promise<TagResponse> {
    try {
      const response = await this.api.get<TagResponse>("/tags");
      return response.data;
    } catch (error) {
      console.error("Error fetching tags:", error);
      throw error;
    }
  }

  /**
   * Get system statistics
   */
  async getStatistics(): Promise<Statistics> {
    try {
      const response = await this.api.get<Statistics>("/stats");
      return response.data;
    } catch (error) {
      console.error("Error fetching statistics:", error);
      throw error;
    }
  }

  /**
   * Get system health status
   */
  async getHealth(): Promise<HealthResponse> {
    try {
      const response = await this.api.get<HealthResponse>("/health");
      return response.data;
    } catch (error) {
      console.error("Error fetching health status:", error);
      throw error;
    }
  }

  /**
   * Manually refresh jobs
   */
  async refreshJobs(): Promise<{
    message: string;
    job_count: number;
    timestamp: string;
  }> {
    try {
      const response = await this.api.get("/jobs/refresh");
      return response.data;
    } catch (error) {
      console.error("Error refreshing jobs:", error);
      throw error;
    }
  }

  /**
   * Search jobs with text query
   * This is a client-side search implementation
   */
  searchJobs(jobs: Job[], query: string): Job[] {
    if (!query.trim()) return jobs;

    const searchTerm = query.toLowerCase();

    return jobs.filter((job) => {
      // Search in title
      if (job.title.toLowerCase().includes(searchTerm)) return true;

      // Search in company name
      if (job.company.toLowerCase().includes(searchTerm)) return true;

      // Search in description
      if (job.description_text?.toLowerCase().includes(searchTerm)) return true;

      // Search in tags
      if (job.tags.some((tag) => tag.toLowerCase().includes(searchTerm)))
        return true;

      // Search in location
      if (job.location.toLowerCase().includes(searchTerm)) return true;

      return false;
    });
  }

  /**
   * Get jobs by tag
   */
  async getJobsByTag(tag: string, limit: number = 50): Promise<JobResponse> {
    return this.getJobs({ tags: [tag] }, limit);
  }

  /**
   * Get remote jobs only
   */
  async getRemoteJobs(limit: number = 50): Promise<JobResponse> {
    return this.getJobs({ remote_only: true }, limit);
  }

  /**
   * Get featured jobs
   */
  getFeaturedJobs(jobs: Job[]): Job[] {
    return jobs.filter((job) => job.featured);
  }

  /**
   * Get recent jobs (last 7 days)
   */
  getRecentJobs(jobs: Job[], days: number = 7): Job[] {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);

    return jobs.filter((job) => {
      const jobDate = new Date(job.date);
      return jobDate >= cutoffDate;
    });
  }

  /**
   * Format salary range for display
   */
  formatSalary(min?: number, max?: number, currency: string = "USD"): string {
    if (!min && !max) return "Salary not specified";

    const formatter = new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: currency,
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    });

    if (min && max) {
      return `${formatter.format(min)} - ${formatter.format(max)}`;
    } else if (min) {
      return `${formatter.format(min)}+`;
    } else if (max) {
      return `Up to ${formatter.format(max)}`;
    }

    return "Salary not specified";
  }

  /**
   * Format date for display
   */
  formatDate(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
      return "Today";
    } else if (diffDays === 2) {
      return "Yesterday";
    } else if (diffDays <= 7) {
      return `${diffDays - 1} days ago`;
    } else {
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    }
  }

  /**
   * Get tag category color
   */
  getTagCategoryColor(category?: string): string {
    switch (category) {
      case "programming_language":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200";
      case "framework":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
      case "blockchain":
        return "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200";
      case "web3_sector":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200";
      case "blockchain_technology":
        return "bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200";
      case "role":
        return "bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200";
    }
  }

  /**
   * Get experience level color
   */
  getExperienceLevelColor(level?: string): string {
    switch (level?.toLowerCase()) {
      case "entry":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
      case "junior":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200";
      case "mid":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200";
      case "senior":
        return "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200";
      case "lead":
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200";
      case "executive":
        return "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200";
    }
  }

  /**
   * Get job type color
   */
  getJobTypeColor(type?: string): string {
    switch (type?.toLowerCase()) {
      case "full-time":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
      case "part-time":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200";
      case "contract":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200";
      case "internship":
        return "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200";
      case "freelance":
        return "bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200";
    }
  }
}

// Export singleton instance
export const apiService = new ApiService();

// Export the class for testing
export default ApiService;
