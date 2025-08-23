/**
 * Main App Component for Web3 Job Seeker
 * 
 * This component serves as the root of the application and provides:
 * - Routing configuration
 * - Global state management
 * - Theme and layout setup
 * - Error boundaries
 * - Global providers
 * 
 * @author Web3 Job Seeker Team
 * @version 1.0.0
 */

import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import { HelmetProvider } from 'react-helmet-async';

// Import components
import Layout from './components/Layout/Layout';
import LoadingSpinner from './components/UI/LoadingSpinner';
import ErrorBoundary from './components/UI/ErrorBoundary';
import { JobProvider } from './contexts/JobContext';

// Lazy load pages for better performance
const HomePage = lazy(() => import('./pages/HomePage'));
const JobDetailPage = lazy(() => import('./pages/JobDetailPage'));
const NotFoundPage = lazy(() => import('./pages/NotFoundPage'));

// Create a client for React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
      refetchOnReconnect: true,
    },
    mutations: {
      retry: 1,
    },
  },
});

/**
 * App Component
 * 
 * The main application component that sets up:
 * - React Query for data fetching
 * - React Router for navigation
 * - Global toast notifications
 * - Error boundaries
 * - Context providers
 */
const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <HelmetProvider>
        <QueryClientProvider client={queryClient}>
          <JobProvider>
            <Router>
              <div className="min-h-screen bg-gradient-to-br from-dark-50 to-dark-100 dark:from-dark-900 dark:to-dark-800">
                {/* Global toast notifications */}
                <Toaster
                  position="top-right"
                  toastOptions={{
                    duration: 4000,
                    style: {
                      background: '#1e293b',
                      color: '#f8fafc',
                      border: '1px solid #334155',
                    },
                    success: {
                      iconTheme: {
                        primary: '#22c55e',
                        secondary: '#f8fafc',
                      },
                    },
                    error: {
                      iconTheme: {
                        primary: '#ef4444',
                        secondary: '#f8fafc',
                      },
                    },
                  }}
                />

                {/* Main layout wrapper */}
                <Layout>
                  <Suspense
                    fallback={
                      <div className="flex items-center justify-center min-h-screen">
                        <LoadingSpinner size="lg" />
                      </div>
                    }
                  >
                    <Routes>
                      {/* Home page - Job listings with filters */}
                      <Route 
                        path="/" 
                        element={<HomePage />} 
                      />
                      
                      {/* Job detail page */}
                      <Route 
                        path="/job/:jobId" 
                        element={<JobDetailPage />} 
                      />
                      
                      {/* 404 page for unmatched routes */}
                      <Route 
                        path="*" 
                        element={<NotFoundPage />} 
                      />
                    </Routes>
                  </Suspense>
                </Layout>
              </div>
            </Router>
          </JobProvider>
        </QueryClientProvider>
      </HelmetProvider>
    </ErrorBoundary>
  );
};

export default App;
