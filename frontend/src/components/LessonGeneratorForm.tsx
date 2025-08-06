import { useState } from 'react';

interface FormData {
  grade: string;
  subject: string;
  topic: string;
  questionsPerSection: number;
}

interface LessonGeneratorFormProps {
  onGenerate: (lessonText: string) => void;
  onError: (error: string) => void;
}

const LessonGeneratorForm: React.FC<LessonGeneratorFormProps> = ({ onGenerate, onError }) => {
  const [formData, setFormData] = useState<FormData>({
    grade: '2',
    subject: 'Grammar',
    topic: '',
    questionsPerSection: 6,
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.topic.trim()) {
      onError('Please enter a topic');
      return;
    }

    setIsLoading(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/generate-lesson', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          grade: formData.grade,
          subject: formData.subject,
          topic: formData.topic,
          questions_per_section: formData.questionsPerSection,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate lesson');
      }

      const data = await response.json();
      onGenerate(data.lessonText);
    } catch (error) {
      console.error('Error generating lesson:', error);
      onError(error instanceof Error ? error.message : 'An unexpected error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (field: keyof FormData, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Generate Lesson</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="grade" className="block text-sm font-medium text-gray-700 mb-2">
            Grade
          </label>
          <select
            id="grade"
            value={formData.grade}
            onChange={(e) => handleInputChange('grade', e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="2">Grade 2</option>
            <option value="3">Grade 3</option>
            <option value="4">Grade 4</option>
            <option value="5">Grade 5</option>
            <option value="6">Grade 6</option>
          </select>
        </div>

        <div>
          <label htmlFor="subject" className="block text-sm font-medium text-gray-700 mb-2">
            Subject
          </label>
          <select
            id="subject"
            value={formData.subject}
            onChange={(e) => handleInputChange('subject', e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="Grammar">Grammar</option>
          </select>
        </div>

        <div>
          <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
            Topic
          </label>
          <input
            type="text"
            id="topic"
            value={formData.topic}
            onChange={(e) => handleInputChange('topic', e.target.value)}
            placeholder="e.g. Nouns"
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div>
          <label htmlFor="questionsPerSection" className="block text-sm font-medium text-gray-700 mb-2">
            Questions per Section
          </label>
          <input
            type="number"
            id="questionsPerSection"
            value={formData.questionsPerSection}
            onChange={(e) => handleInputChange('questionsPerSection', parseInt(e.target.value) || 6)}
            min="1"
            max="20"
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <button
          type="submit"
          disabled={isLoading || !formData.topic.trim()}
          className="w-full bg-blue-600 text-white py-3 px-6 rounded-md text-lg font-semibold hover:bg-blue-700 transition-colors duration-200 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
        >
          {isLoading ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Generating Lesson...
            </>
          ) : (
            'Generate Lesson'
          )}
        </button>
      </form>
    </div>
  );
};

export default LessonGeneratorForm;