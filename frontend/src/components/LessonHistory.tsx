import React, { useState, useEffect } from 'react';
import LessonOutputViewer from './LessonOutputViewer';

interface LessonSummary {
  id: number;
  topics: string[];
  grade: number;
  age?: number;
  date_generated: string;
}

interface LessonDetail {
  id: number;
  topics: string[];
  grade: number;
  age?: number;
  date_generated: string;
  lesson_text: string;
  tags?: string[];
}

interface LessonsListResponse {
  lessons: LessonSummary[];
  total: number;
}

const LessonHistory: React.FC = () => {
  const [lessons, setLessons] = useState<LessonSummary[]>([]);
  const [selectedLesson, setSelectedLesson] = useState<LessonDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [loadingDetail, setLoadingDetail] = useState(false);

  // Fetch all lessons on component mount
  useEffect(() => {
    fetchLessons();
  }, []);

  const fetchLessons = async () => {
    try {
      setLoading(true);
      setError('');
      
      const response = await fetch('http://localhost:8000/api/lessons');
      if (!response.ok) {
        throw new Error(`Failed to fetch lessons: ${response.status}`);
      }
      
      const data: LessonsListResponse = await response.json();
      setLessons(data.lessons);
    } catch (err) {
      console.error('Error fetching lessons:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch lessons');
    } finally {
      setLoading(false);
    }
  };

  const fetchLessonDetail = async (lessonId: number) => {
    try {
      setLoadingDetail(true);
      setError('');
      
      const response = await fetch(`http://localhost:8000/api/lessons/${lessonId}`);
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Lesson not found');
        }
        throw new Error(`Failed to fetch lesson: ${response.status}`);
      }
      
      const lessonDetail: LessonDetail = await response.json();
      setSelectedLesson(lessonDetail);
    } catch (err) {
      console.error('Error fetching lesson detail:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch lesson details');
    } finally {
      setLoadingDetail(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleLessonClick = (lesson: LessonSummary) => {
    fetchLessonDetail(lesson.id);
  };

  const handleBackToList = () => {
    setSelectedLesson(null);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-gray-600">Loading lesson history...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Error</h3>
            <div className="mt-2 text-sm text-red-700">
              <p>{error}</p>
            </div>
            <div className="mt-4">
              <button
                onClick={fetchLessons}
                className="bg-red-100 px-4 py-2 rounded text-red-800 hover:bg-red-200 transition-colors"
              >
                Try Again
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Show lesson detail view
  if (selectedLesson) {
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <button
            onClick={handleBackToList}
            className="flex items-center text-blue-600 hover:text-blue-800 transition-colors"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Lesson History
          </button>
          <div className="text-sm text-gray-500">
            Lesson #{selectedLesson.id} • {formatDate(selectedLesson.date_generated)}
          </div>
        </div>
        
        {loadingDetail ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-gray-600">Loading lesson...</span>
          </div>
        ) : (
          <LessonOutputViewer lessonText={selectedLesson.lesson_text} />
        )}
      </div>
    );
  }

  // Show lessons list
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Lesson History</h2>
        <div className="text-sm text-gray-600">
          {lessons.length} lesson{lessons.length !== 1 ? 's' : ''} total
        </div>
      </div>

      {lessons.length === 0 ? (
        <div className="text-center py-12">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No lessons yet</h3>
          <p className="mt-1 text-sm text-gray-500">
            Generate your first lesson to see it appear here.
          </p>
        </div>
      ) : (
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <ul className="divide-y divide-gray-200">
            {lessons.map((lesson) => (
              <li key={lesson.id}>
                <button
                  onClick={() => handleLessonClick(lesson)}
                  className="w-full text-left px-6 py-4 hover:bg-gray-50 transition-colors focus:outline-none focus:bg-gray-50"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-3">
                        <div className="flex-shrink-0">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            Grade {lesson.grade}
                          </span>
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {lesson.topics.join(', ')}
                          </p>
                          <p className="text-sm text-gray-500">
                            ID: {lesson.id} • {formatDate(lesson.date_generated)}
                            {lesson.age && ` • Age: ${lesson.age}`}
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="flex-shrink-0">
                      <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default LessonHistory;