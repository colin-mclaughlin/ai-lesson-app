import { useState } from 'react'
import LessonGeneratorForm from './components/LessonGeneratorForm'
import LessonOutputViewer from './components/LessonOutputViewer'
import './App.css'

interface FormData {
  grade: string;
  subject: string;
  topic: string;
  questionsPerSection: number;
}

function App() {
  const [lessonText, setLessonText] = useState('')

  const handleGenerate = (formData: FormData) => {
    // Dummy lesson text for now
    const dummyLesson = `
Grade ${formData.grade} ${formData.subject} Lesson: ${formData.topic}

Instructions: Complete the following exercises about ${formData.topic.toLowerCase()}.

Section 1: Identification
${Array.from({ length: formData.questionsPerSection }, (_, i) => `${i + 1}. [Question about ${formData.topic}]`).join('\n')}

Section 2: Practice
${Array.from({ length: formData.questionsPerSection }, (_, i) => `${i + 1}. [Practice exercise about ${formData.topic}]`).join('\n')}

Section 3: Application
${Array.from({ length: formData.questionsPerSection }, (_, i) => `${i + 1}. [Application question about ${formData.topic}]`).join('\n')}
    `.trim()
    
    setLessonText(dummyLesson)
  }

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          Coding Cat Lesson Generator
        </h1>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <LessonGeneratorForm onGenerate={handleGenerate} />
          </div>
          <div>
            <LessonOutputViewer lessonText={lessonText} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
