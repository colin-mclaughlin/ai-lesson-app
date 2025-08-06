import { useState } from 'react';

interface FormData {
  grade: string;
  subject: string;
  topic: string;
  questionsPerSection: number;
}

interface LessonGeneratorFormProps {
  onGenerate: (formData: FormData) => void;
}

const LessonGeneratorForm: React.FC<LessonGeneratorFormProps> = ({ onGenerate }) => {
  const [formData, setFormData] = useState<FormData>({
    grade: '2',
    subject: 'Grammar',
    topic: '',
    questionsPerSection: 6,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onGenerate(formData);
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
          className="w-full bg-blue-600 text-white py-3 px-6 rounded-md text-lg font-semibold hover:bg-blue-700 transition-colors duration-200 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Generate Lesson
        </button>
      </form>
    </div>
  );
};

export default LessonGeneratorForm;