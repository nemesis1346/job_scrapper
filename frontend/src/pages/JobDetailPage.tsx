/**
 * Job Detail Page Component
 * 
 * Displays detailed information about a specific job
 */

import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { motion } from 'framer-motion';
import { useQuery } from 'react-query';
import { ArrowLeft, ExternalLink, MapPin, Clock, DollarSign, Briefcase } from 'lucide-react';

import { apiService } from '../services/api';
import LoadingSpinner from '../components/UI/LoadingSpinner';

const JobDetailPage: React.FC = () => {
  const { jobId } = useParams<{ jobId: string }>();

  const { data: job, isLoading, error } = useQuery(
    ['job', jobId],
    () => apiService.getJobById(Number(jobId)),
    {
      enabled: !!jobId,
    }
  );

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Job not found
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            The job you're looking for doesn't exist or has been removed.
          </p>
          <Link
            to="/"
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
          >
            Back to Jobs
          </Link>
        </div>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>{job.title} at {job.company} - Web3 Job Seeker</title>
        <meta name="description" content={job.description_text?.substring(0, 160) || job.title} />
      </Helmet>

      <div className="min-h-screen bg-gray-50 dark:bg-dark-900">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Back Button */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="mb-6"
          >
            <Link
              to="/"
              className="inline-flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to Jobs</span>
            </Link>
          </motion.div>

          {/* Job Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white dark:bg-dark-800 rounded-lg shadow-sm border border-gray-200 dark:border-dark-700 p-6 mb-6"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                  {job.title}
                </h1>
                <p className="text-xl text-gray-600 dark:text-gray-400 mb-4">
                  {job.company}
                </p>
              </div>
              <a
                href={job.apply_url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-2 bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
              >
                <span>Apply Now</span>
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>

            {/* Job Meta */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
                <MapPin className="w-5 h-5" />
                <span>{job.location}</span>
                {job.remote && (
                  <span className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 px-2 py-0.5 rounded-full text-xs">
                    Remote
                  </span>
                )}
              </div>
              <div className="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
                <Clock className="w-5 h-5" />
                <span>Posted {apiService.formatDate(job.date)}</span>
              </div>
              {(job.salary_min || job.salary_max) && (
                <div className="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
                  <DollarSign className="w-5 h-5" />
                  <span>{apiService.formatSalary(job.salary_min, job.salary_max, job.salary_currency)}</span>
                </div>
              )}
            </div>

            {/* Job Type and Experience */}
            <div className="flex items-center space-x-4 mb-6">
              {job.job_type && (
                <div className="flex items-center space-x-2">
                  <Briefcase className="w-4 h-4 text-gray-400" />
                  <span className={`px-3 py-1 rounded-full text-sm ${apiService.getJobTypeColor(job.job_type)}`}>
                    {job.job_type}
                  </span>
                </div>
              )}
              {job.experience_level && (
                <span className={`px-3 py-1 rounded-full text-sm ${apiService.getExperienceLevelColor(job.experience_level)}`}>
                  {job.experience_level}
                </span>
              )}
            </div>

            {/* Tags */}
            {job.tags.length > 0 && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Skills & Technologies</h3>
                <div className="flex flex-wrap gap-2">
                  {job.tags.map((tag) => (
                    <span
                      key={tag}
                      className={`px-3 py-1 rounded-full text-sm ${apiService.getTagCategoryColor()}`}
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </motion.div>

          {/* Job Description */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white dark:bg-dark-800 rounded-lg shadow-sm border border-gray-200 dark:border-dark-700 p-6"
          >
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              Job Description
            </h2>
            <div 
              className="prose prose-gray dark:prose-invert max-w-none"
              dangerouslySetInnerHTML={{ __html: job.description }}
            />
          </motion.div>
        </div>
      </div>
    </>
  );
};

export default JobDetailPage;
