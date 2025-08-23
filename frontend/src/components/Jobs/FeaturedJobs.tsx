/**
 * Featured Jobs Component
 * 
 * Displays featured job opportunities
 */

import React from 'react';
import { Star } from 'lucide-react';
import { Job } from '../../contexts/JobContext';
import JobCard from './JobCard';

interface FeaturedJobsProps {
  jobs: Job[];
}

const FeaturedJobs: React.FC<FeaturedJobsProps> = ({ jobs }) => {
  if (jobs.length === 0) {
    return null;
  }

  return (
    <div className="bg-gradient-to-r from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 rounded-lg p-6 border border-yellow-200 dark:border-yellow-800">
      <div className="flex items-center space-x-2 mb-4">
        <Star className="w-5 h-5 text-yellow-600 dark:text-yellow-400 fill-current" />
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          Featured Opportunities
        </h3>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {jobs.slice(0, 3).map((job) => (
          <JobCard key={job.id} job={job} viewMode="grid" />
        ))}
      </div>
    </div>
  );
};

export default FeaturedJobs;
