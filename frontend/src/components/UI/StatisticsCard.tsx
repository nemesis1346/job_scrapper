/**
 * Statistics Card Component
 * 
 * Displays job statistics in a card format
 */

import React from 'react';
import { Briefcase, MapPin, Star, TrendingUp } from 'lucide-react';

interface Statistics {
  total_jobs: number;
  remote_jobs: number;
  featured_jobs: number;
  total_companies: number;
  total_tags: number;
  jobs_by_country: Record<string, number>;
  top_tags: Array<{ name: string; count: number; category?: string }>;
  top_companies: Array<{ name: string; job_count: number }>;
  salary_stats: {
    average?: number;
    median?: number;
    min?: number;
    max?: number;
  };
}

interface StatisticsCardProps {
  stats: Statistics;
}

const StatisticsCard: React.FC<StatisticsCardProps> = ({ stats }) => {
  const formatNumber = (num: number) => {
    return new Intl.NumberFormat().format(num);
  };

  const formatSalary = (salary?: number) => {
    if (!salary) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(salary);
  };

  return (
    <div className="bg-white dark:bg-dark-800 rounded-lg shadow-sm border border-gray-200 dark:border-dark-700 p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Job Statistics
      </h3>
      
      <div className="space-y-4">
        {/* Basic Stats */}
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center">
            <div className="flex items-center justify-center w-8 h-8 bg-primary-100 dark:bg-primary-900 rounded-lg mx-auto mb-2">
              <Briefcase className="w-4 h-4 text-primary-600 dark:text-primary-400" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              {formatNumber(stats.total_jobs)}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Total Jobs</div>
          </div>
          
          <div className="text-center">
            <div className="flex items-center justify-center w-8 h-8 bg-green-100 dark:bg-green-900 rounded-lg mx-auto mb-2">
              <MapPin className="w-4 h-4 text-green-600 dark:text-green-400" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              {formatNumber(stats.remote_jobs)}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Remote Jobs</div>
          </div>
        </div>

        {/* Featured Jobs */}
        {stats.featured_jobs > 0 && (
          <div className="text-center">
            <div className="flex items-center justify-center w-8 h-8 bg-yellow-100 dark:bg-yellow-900 rounded-lg mx-auto mb-2">
              <Star className="w-4 h-4 text-yellow-600 dark:text-yellow-400" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              {formatNumber(stats.featured_jobs)}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Featured Jobs</div>
          </div>
        )}

        {/* Companies */}
        <div className="text-center">
          <div className="flex items-center justify-center w-8 h-8 bg-purple-100 dark:bg-purple-900 rounded-lg mx-auto mb-2">
            <TrendingUp className="w-4 h-4 text-purple-600 dark:text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            {formatNumber(stats.total_companies)}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Companies</div>
        </div>

        {/* Salary Stats */}
        {stats.salary_stats.average && (
          <div className="pt-4 border-t border-gray-200 dark:border-dark-700">
            <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3">
              Salary Statistics
            </h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Average:</span>
                <span className="font-medium text-gray-900 dark:text-white">
                  {formatSalary(stats.salary_stats.average)}
                </span>
              </div>
              {stats.salary_stats.median && (
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Median:</span>
                  <span className="font-medium text-gray-900 dark:text-white">
                    {formatSalary(stats.salary_stats.median)}
                  </span>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StatisticsCard;
