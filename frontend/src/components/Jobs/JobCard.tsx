/**
 * Job Card Component for Web3 Job Seeker
 * 
 * This component displays individual job listings with:
 * - Job title and company
 * - Location and remote status
 * - Tags and skills
 * - Salary information
 * - Apply button
 * 
 * @author Web3 Job Seeker Team
 * @version 1.0.0
 */

import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  MapPin, 
  Clock, 
  ExternalLink, 
  Star,
  Briefcase,
  DollarSign
} from 'lucide-react';

import { Job } from '../../contexts/JobContext';
import { apiService } from '../../services/api';

interface JobCardProps {
  job: Job;
  viewMode: 'grid' | 'list';
}

/**
 * Job Card Component
 * 
 * Displays job information in either grid or list view mode
 * with hover effects and interactive elements.
 */
const JobCard: React.FC<JobCardProps> = ({ job, viewMode }) => {
  const isGrid = viewMode === 'grid';

  return (
    <motion.div
      whileHover={{ y: -2 }}
      className={`bg-white dark:bg-dark-800 rounded-lg border border-gray-200 dark:border-dark-700 shadow-sm hover:shadow-md transition-all duration-200 ${
        isGrid ? 'h-full' : ''
      }`}
    >
      <div className={`p-6 ${isGrid ? 'h-full flex flex-col' : ''}`}>
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2">
              {job.title}
            </h3>
            <p className="text-gray-600 dark:text-gray-400 font-medium">
              {job.company}
            </p>
          </div>
          {job.featured && (
            <div className="flex items-center text-accent-500 ml-2">
              <Star className="w-4 h-4 fill-current" />
            </div>
          )}
        </div>

        {/* Location and Date */}
        <div className="flex items-center justify-between mb-4 text-sm text-gray-500 dark:text-gray-400">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-1">
              <MapPin className="w-4 h-4" />
              <span>{job.location}</span>
              {job.remote && (
                <span className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 px-2 py-0.5 rounded-full text-xs">
                  Remote
                </span>
              )}
            </div>
          </div>
          <div className="flex items-center space-x-1">
            <Clock className="w-4 h-4" />
            <span>{apiService.formatDate(job.date)}</span>
          </div>
        </div>

        {/* Tags */}
        {job.tags.length > 0 && (
          <div className="mb-4">
            <div className="flex flex-wrap gap-2">
              {job.tags.slice(0, 5).map((tag) => (
                <span
                  key={tag}
                  className={`px-2 py-1 text-xs rounded-full ${apiService.getTagCategoryColor()}`}
                >
                  {tag}
                </span>
              ))}
              {job.tags.length > 5 && (
                <span className="px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300">
                  +{job.tags.length - 5} more
                </span>
              )}
            </div>
          </div>
        )}

        {/* Salary Information */}
        {(job.salary_min || job.salary_max) && (
          <div className="flex items-center space-x-1 mb-4 text-sm text-gray-600 dark:text-gray-400">
            <DollarSign className="w-4 h-4" />
            <span>{apiService.formatSalary(job.salary_min, job.salary_max, job.salary_currency)}</span>
          </div>
        )}

        {/* Job Type and Experience Level */}
        <div className="flex items-center space-x-4 mb-4 text-sm">
          {job.job_type && (
            <div className="flex items-center space-x-1">
              <Briefcase className="w-4 h-4 text-gray-400" />
              <span className={`px-2 py-1 rounded-full text-xs ${apiService.getJobTypeColor(job.job_type)}`}>
                {job.job_type}
              </span>
            </div>
          )}
          {job.experience_level && (
            <span className={`px-2 py-1 rounded-full text-xs ${apiService.getExperienceLevelColor(job.experience_level)}`}>
              {job.experience_level}
            </span>
          )}
        </div>

        {/* Description Preview */}
        {job.description_text && (
          <div className="mb-4">
            <p className="text-gray-600 dark:text-gray-400 text-sm line-clamp-3">
              {job.description_text.substring(0, 150)}
              {job.description_text.length > 150 && '...'}
            </p>
          </div>
        )}

        {/* Actions */}
        <div className={`flex items-center justify-between ${isGrid ? 'mt-auto' : ''}`}>
          <Link
            to={`/job/${job.id}`}
            className="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 text-sm font-medium transition-colors"
          >
            View Details
          </Link>
          <a
            href={job.apply_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-1 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            <span>Apply</span>
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      </div>
    </motion.div>
  );
};

export default JobCard;
