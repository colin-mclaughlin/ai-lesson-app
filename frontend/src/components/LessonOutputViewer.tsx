interface LessonOutputViewerProps {
  lessonText: string;
}

const LessonOutputViewer: React.FC<LessonOutputViewerProps> = ({ lessonText }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-3xl font-bold mb-6 text-gray-800 border-b-2 border-gray-200 pb-3">
        Lesson Worksheet
      </h2>
      <div className="prose max-w-none">
        {lessonText ? (
          <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
            {lessonText}
          </div>
        ) : (
          <div className="text-gray-500 italic text-center py-12">
            <p className="text-xl">Your lesson will appear here.</p>
            <p className="text-sm mt-2">Fill out the form above and click "Generate Lesson" to get started.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default LessonOutputViewer;