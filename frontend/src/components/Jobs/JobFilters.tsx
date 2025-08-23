/**
 * Job Filters Component
 * 
 * Advanced filtering options for jobs
 */

import React from 'react';
import { useJobActions } from '../../contexts/JobContext';

const JobFilters: React.FC = () => {
  const actions = useJobActions();

  return (
    <div className="bg-white dark:bg-dark-800 rounded-lg p-4">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Advanced Filters
      </h3>
      <p className="text-gray-600 dark:text-gray-400 text-sm">
        Filter options will be implemented here.
      </p>
    </div>
  );
};

export default JobFilters;
