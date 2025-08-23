/**
 * Tag Cloud Component
 * 
 * Displays tags in a cloud format with clickable functionality
 */

import React from 'react';
import { useJobActions } from '../../contexts/JobContext';
import { apiService } from '../../services/api';

interface Tag {
  name: string;
  count: number;
  category?: string;
}

interface TagCloudProps {
  tags: Tag[];
}

const TagCloud: React.FC<TagCloudProps> = ({ tags }) => {
  const actions = useJobActions();

  const handleTagClick = (tagName: string) => {
    actions.addTagFilter(tagName);
  };

  // Sort tags by count and take top 20
  const sortedTags = tags
    .sort((a, b) => b.count - a.count)
    .slice(0, 20);

  const getTagSize = (count: number, maxCount: number) => {
    const ratio = count / maxCount;
    if (ratio > 0.8) return 'text-lg';
    if (ratio > 0.6) return 'text-base';
    if (ratio > 0.4) return 'text-sm';
    return 'text-xs';
  };

  const maxCount = Math.max(...sortedTags.map(tag => tag.count));

  return (
    <div className="bg-white dark:bg-dark-800 rounded-lg shadow-sm border border-gray-200 dark:border-dark-700 p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Popular Skills
      </h3>
      
      <div className="flex flex-wrap gap-2">
        {sortedTags.map((tag) => (
          <button
            key={tag.name}
            onClick={() => handleTagClick(tag.name)}
            className={`px-3 py-1 rounded-full font-medium transition-all hover:scale-105 ${getTagSize(tag.count, maxCount)} ${apiService.getTagCategoryColor(tag.category)}`}
            title={`${tag.count} jobs`}
          >
            {tag.name}
            <span className="ml-1 text-xs opacity-75">({tag.count})</span>
          </button>
        ))}
      </div>
      
      {tags.length > 20 && (
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-3">
          Showing top 20 of {tags.length} skills
        </p>
      )}
    </div>
  );
};

export default TagCloud;
