import { useState } from 'react'
import LessonGeneratorForm from './components/LessonGeneratorForm'
import LessonOutputViewer from './components/LessonOutputViewer'
import LessonHistory from './components/LessonHistory'
import './App.css'

interface LessonData {
  lessonText: string;
  regenerated?: boolean;
  warnings?: string[];
  lessonId?: number;
  grade?: string;
  topic?: string;
}

function App() {
  const [activeTab, setActiveTab] = useState<'generate' | 'history'>('generate')
  const [lessonData, setLessonData] = useState<LessonData>({ lessonText: '' })
  const [error, setError] = useState('')

  const handleGenerate = (data: LessonData) => {
    setLessonData(data)
    setError('') // Clear any previous errors
  }

  const handleError = (errorMessage: string) => {
    setError(errorMessage)
    setLessonData({ lessonText: '' }) // Clear any previous lesson
  }

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          Coding Cat Lesson Generator
        </h1>
        
        {/* Tab Navigation */}
        <div className="flex justify-center mb-8">
          <div className="inline-flex rounded-lg bg-gray-200 p-1">
            <button
              onClick={() => setActiveTab('generate')}
              className={`px-6 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'generate'
                  ? 'bg-white text-gray-900 shadow'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Generate Lesson
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`px-6 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'history'
                  ? 'bg-white text-gray-900 shadow'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Lesson History
            </button>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'generate' ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <LessonGeneratorForm onGenerate={handleGenerate} onError={handleError} />
              {error && (
                <div className="mt-4 bg-red-50 border border-red-200 rounded-md p-4">
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
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div>
              <LessonOutputViewer 
                lessonText={lessonData.lessonText} 
                lessonId={lessonData.lessonId}
                grade={lessonData.grade}
                topic={lessonData.topic}
              />
              {/* Content adjustment banner */}
              {(lessonData.regenerated || (lessonData.warnings && lessonData.warnings.length > 0)) && (
                <div className="mt-4 bg-blue-50 border border-blue-200 rounded-md p-3">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-4 w-4 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm text-blue-700">
                        Adjusted to meet constraints (no pictures, on-topic).
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        ) : (
          <LessonHistory />
        )}
      </div>
    </div>
  )
}

export default App
