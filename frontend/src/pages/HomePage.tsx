/**
 * Home Page Component for Web3 Job Seeker
 * 
 * This is the main page that displays:
 * - Job listings in a grid layout
 * - Advanced filtering options
 * - Search functionality
 * - Pagination
 * - Statistics and featured jobs
 * 
 * @author Web3 Job Seeker Team
 * @version 1.0.0
 */

import React, { useEffect, useState, useCallback } from 'react';
import { Helmet } from 'react-helmet-async';
import { motion } from 'framer-motion';
import { useQuery } from 'react-query';
import toast from 'react-hot-toast';

// Import components
import JobCard from '../components/Jobs/JobCard';
import JobFilters from '../components/Jobs/JobFilters';
import SearchBar from '../components/UI/SearchBar';
import LoadingSpinner from '../components/UI/LoadingSpinner';
import Pagination from '../components/UI/Pagination';
import StatisticsCard from '../components/UI/StatisticsCard';
import FeaturedJobs from '../components/Jobs/FeaturedJobs';
import TagCloud from '../components/Jobs/TagCloud';

// Import hooks and services
import { useJobContext, useJobActions } from '../contexts/JobContext';
import { apiService } from '../services/api';
import { Job } from '../contexts/JobContext';

// Import icons
import { 
  Briefcase, 
  MapPin, 
  Clock, 
  TrendingUp, 
  Filter,
  RefreshCw,
  Search,
  X
} from 'lucide-react';

/**
 * HomePage Component
 * 
 * The main landing page that displays job listings with comprehensive
 * filtering, search, and pagination capabilities.
 */
const HomePage: React.FC = () => {
  // State
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // Context
  const { state } = useJobContext();
  const actions = useJobActions();

  // Fetch jobs data
  const {
    data: jobsData,
    isLoading,
    error,
    refetch
  } = useQuery(
    ['jobs', state.filters],
    () => apiService.getJobs(state.filters, 200, 0),
    {
      refetchInterval: 60000, // Refetch every minute
      staleTime: 30000, // Consider data stale after 30 seconds
      onSuccess: (data) => {
        actions.setJobs(data.jobs);
        actions.setLastRefresh(new Date());
      },
      onError: (error) => {
        actions.setError(error instanceof Error ? error.message : 'Failed to fetch jobs');
        toast.error('Failed to load jobs. Please try again.');
      }
    }
  );

  // Fetch tags data
  const { data: tagsData } = useQuery(
    ['tags'],
    () => apiService.getTags(),
    {
      staleTime: 300000, // 5 minutes
      onSuccess: (data) => {
        actions.setAvailableTags(data.tags);
      }
    }
  );

  // Fetch statistics
  const { data: statsData } = useQuery(
    ['statistics'],
    () => apiService.getStatistics(),
    {
      staleTime: 300000, // 5 minutes
    }
  );

  // Handle search
  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
  }, []);

  // Handle manual refresh
  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      await apiService.refreshJobs();
      await refetch();
      toast.success('Jobs refreshed successfully!');
    } catch (error) {
      toast.error('Failed to refresh jobs');
    } finally {
      setIsRefreshing(false);
    }
  };

  // Filter jobs based on search query
  const filteredJobs = searchQuery 
    ? apiService.searchJobs(state.filteredJobs, searchQuery)
    : state.filteredJobs;

  // Get paginated jobs
  const paginatedJobs = actions.getPaginatedJobs();

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.3
      }
    }
  };

  // Loading state
  if (isLoading && !state.jobs.length) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Error state
  if (error && !state.jobs.length) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Failed to load jobs
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            {error instanceof Error ? error.message : 'An error occurred'}
          </p>
          <button
            onClick={() => refetch()}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>Web3 Job Seeker - Find Your Next Web3 Career</title>
        <meta name="description" content="Discover the latest Web3 jobs from top companies. Filter by skills, location, and more. Find your next blockchain, DeFi, or crypto career opportunity." />
        <meta name="keywords" content="web3 jobs, blockchain jobs, crypto jobs, defi jobs, solidity developer, ethereum developer" />
      </Helmet>

      <div className="min-h-screen bg-gradient-to-br from-dark-50 to-dark-100 dark:from-dark-900 dark:to-dark-800">
        {/* Header Section */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white dark:bg-dark-800 shadow-sm border-b border-gray-200 dark:border-dark-700"
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
              {/* Title and Stats */}
              <div className="flex-1">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                  Web3 Job Seeker
                </h1>
                <p className="text-gray-600 dark:text-gray-400">
                  Discover {statsData?.total_jobs || state.jobs.length} Web3 opportunities
                  {state.lastRefresh && (
                    <span className="ml-2 text-sm">
                      • Last updated {apiService.formatDate(state.lastRefresh.toISOString())}
                    </span>
                  )}
                </p>
              </div>

              {/* Actions */}
              <div className="flex items-center gap-3">
                {/* Refresh Button */}
                <button
                  onClick={handleRefresh}
                  disabled={isRefreshing}
                  className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                  Refresh
                </button>

                {/* Filter Toggle */}
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="flex items-center gap-2 px-4 py-2 bg-gray-100 dark:bg-dark-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-dark-600 transition-colors"
                >
                  <Filter className="w-4 h-4" />
                  Filters
                </button>

                {/* View Mode Toggle */}
                <div className="flex bg-gray-100 dark:bg-dark-700 rounded-lg p-1">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                      viewMode === 'grid'
                        ? 'bg-white dark:bg-dark-600 text-gray-900 dark:text-white shadow-sm'
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                    }`}
                  >
                    Grid
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                      viewMode === 'list'
                        ? 'bg-white dark:bg-dark-600 text-gray-900 dark:text-white shadow-sm'
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                    }`}
                  >
                    List
                  </button>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Search Bar */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white dark:bg-dark-800 border-b border-gray-200 dark:border-dark-700"
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <SearchBar
              value={searchQuery}
              onChange={handleSearch}
              placeholder="Search jobs, companies, or skills..."
              className="max-w-2xl"
            />
          </div>
        </motion.div>

        {/* Filters Section */}
        {showFilters && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-white dark:bg-dark-800 border-b border-gray-200 dark:border-dark-700"
          >
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
              <JobFilters />
            </div>
          </motion.div>
        )}

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Sidebar */}
            <div className="lg:col-span-1 space-y-6">
              {/* Statistics */}
              {statsData && (
                <motion.div
                  variants={itemVariants}
                  initial="hidden"
                  animate="visible"
                >
                  <StatisticsCard stats={statsData} />
                </motion.div>
              )}

              {/* Tag Cloud */}
              {tagsData && (
                <motion.div
                  variants={itemVariants}
                  initial="hidden"
                  animate="visible"
                >
                  <TagCloud tags={tagsData.tags} />
                </motion.div>
              )}
            </div>

            {/* Main Content */}
            <div className="lg:col-span-3">
              {/* Results Header */}
              <motion.div
                variants={itemVariants}
                initial="hidden"
                animate="visible"
                className="flex items-center justify-between mb-6"
              >
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    {searchQuery ? `Search results for "${searchQuery}"` : 'All Jobs'}
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400">
                    Showing {paginatedJobs.length} of {filteredJobs.length} jobs
                  </p>
                </div>

                {/* Active Filters */}
                {state.filters.tags.length > 0 && (
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Active filters:</span>
                    {state.filters.tags.map(tag => (
                      <span
                        key={tag}
                        className="inline-flex items-center gap-1 px-2 py-1 bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 text-xs rounded-full"
                      >
                        {tag}
                        <button
                          onClick={() => actions.removeTagFilter(tag)}
                          className="hover:text-primary-600 dark:hover:text-primary-400"
                        >
                          <X className="w-3 h-3" />
                        </button>
                      </span>
                    ))}
                    <button
                      onClick={actions.clearTagFilters}
                      className="text-sm text-primary-600 dark:text-primary-400 hover:underline"
                    >
                      Clear all
                    </button>
                  </div>
                )}
              </motion.div>

              {/* Featured Jobs (if any) */}
              {!searchQuery && state.filters.tags.length === 0 && (
                <motion.div
                  variants={itemVariants}
                  initial="hidden"
                  animate="visible"
                  className="mb-8"
                >
                  <FeaturedJobs jobs={apiService.getFeaturedJobs(state.jobs)} />
                </motion.div>
              )}

              {/* Job Listings */}
              {paginatedJobs.length > 0 ? (
                <motion.div
                  variants={containerVariants}
                  initial="hidden"
                  animate="visible"
                  className={`grid gap-6 ${
                    viewMode === 'grid'
                      ? 'grid-cols-1 md:grid-cols-2 xl:grid-cols-3'
                      : 'grid-cols-1'
                  }`}
                >
                  {paginatedJobs.map((job) => (
                    <motion.div key={job.id} variants={itemVariants}>
                      <JobCard job={job} viewMode={viewMode} />
                    </motion.div>
                  ))}
                </motion.div>
              ) : (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center py-12"
                >
                  <div className="max-w-md mx-auto">
                    <Search className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                      No jobs found
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 mb-4">
                      {searchQuery
                        ? `No jobs match your search for "${searchQuery}"`
                        : 'No jobs match your current filters'}
                    </p>
                    <button
                      onClick={() => {
                        setSearchQuery('');
                        actions.clearFilters();
                      }}
                      className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
                    >
                      Clear filters
                    </button>
                  </div>
                </motion.div>
              )}

              {/* Pagination */}
              {filteredJobs.length > state.pagination.itemsPerPage && (
                <motion.div
                  variants={itemVariants}
                  initial="hidden"
                  animate="visible"
                  className="mt-8"
                >
                  <Pagination
                    currentPage={state.pagination.currentPage}
                    totalPages={Math.ceil(filteredJobs.length / state.pagination.itemsPerPage)}
                    onPageChange={actions.goToPage}
                  />
                </motion.div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default HomePage;
