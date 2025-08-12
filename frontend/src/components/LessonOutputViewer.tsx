import React, { useRef } from 'react';
import { useReactToPrint } from 'react-to-print';
import '../styles/print.css';

interface LessonOutputViewerProps {
  lessonText: string;
  lessonId?: number;
}

const LessonOutputViewer: React.FC<LessonOutputViewerProps> = ({ lessonText, lessonId }) => {
  const printRef = useRef<HTMLDivElement>(null);

  const handlePrint = useReactToPrint({
    contentRef: printRef,
    documentTitle: 'Lesson Worksheet',
    pageStyle: `
      @page {
        size: A4;
        margin: 20mm;
      }
      @media print {
        body {
          -webkit-print-color-adjust: exact;
          color-adjust: exact;
        }
        .no-print {
          display: none !important;
        }
        .print-content {
          font-family: 'Times New Roman', serif;
          font-size: 12pt;
          line-height: 1.6;
          color: black;
        }
        .print-title {
          font-size: 18pt;
          font-weight: bold;
          text-align: center;
          margin-bottom: 20pt;
          border-bottom: 2pt solid black;
          padding-bottom: 10pt;
        }
        .section-break {
          page-break-before: auto;
          margin-top: 20pt;
        }
        .avoid-break {
          page-break-inside: avoid;
        }
      }
    `,
  });

  const handleDownloadDocx = async () => {
    if (!lessonId) {
      alert('No lesson ID available for download');
      return;
    }

    try {
      // Download the DOCX using the lesson ID
      const docxResponse = await fetch(`http://localhost:8000/api/lessons/${lessonId}/docx`, {
        method: 'GET',
      });

      if (!docxResponse.ok) {
        if (docxResponse.status === 404) {
          throw new Error('Lesson not found. It may have been deleted.');
        }
        throw new Error('Failed to download DOCX');
      }

      // Create blob and download
      const blob = await docxResponse.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Lesson_${lessonId}.docx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading DOCX:', error);
      alert(error instanceof Error ? error.message : 'Failed to download DOCX file');
    }
  };

  // Format lesson text for better print layout
  const formatLessonForPrint = (text: string) => {
    return text.split('\n').map((line, index) => {
      // Add special handling for different types of content
      if (line.trim().startsWith('**') && line.trim().endsWith('**')) {
        // Bold headers
        return (
          <div key={index} className="font-bold text-lg mt-4 mb-2 avoid-break">
            {line.replace(/\*\*/g, '')}
          </div>
        );
      } else if (line.trim().startsWith('Activity') || line.trim().startsWith('Section')) {
        // Activity/Section headers
        return (
          <div key={index} className="font-bold text-base mt-6 mb-3 section-break">
            {line}
          </div>
        );
      } else if (line.match(/^\s*\d+\./)) {
        // Numbered questions - add space for answers
        return (
          <div key={index} className="question-item mb-4 avoid-break">
            <div className="mb-2">{line}</div>
            <div className="border-b border-gray-400 h-8 mb-2"></div>
          </div>
        );
      } else if (line.trim() === '') {
        // Empty lines
        return <div key={index} className="h-2"></div>;
      } else {
        // Regular content
        return (
          <div key={index} className="mb-2">
            {line}
          </div>
        );
      }
    });
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-6 no-print">
        <h2 className="text-3xl font-bold text-gray-800 border-b-2 border-gray-200 pb-3">
          Lesson Worksheet
        </h2>
        {lessonText && (
          <div className="flex gap-2">
            <button
              onClick={handlePrint}
              className="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-semibold hover:bg-green-700 transition-colors duration-200 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 flex items-center"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download as PDF
            </button>
            <button
              onClick={handleDownloadDocx}
              disabled={!lessonId}
              title={!lessonId ? "Generate a lesson first" : "Download as Word document"}
              className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-semibold hover:bg-blue-700 transition-colors duration-200 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 flex items-center disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download DOCX
            </button>
          </div>
        )}
        {lessonText && !lessonId && (
          <div className="mt-2 text-xs text-gray-500 italic">
            DOCX available after lesson is saved
          </div>
        )}
      </div>
      
      <div ref={printRef} className="print-content">
        <div className="prose max-w-none">
          {lessonText ? (
            <>
              <div className="print-title">
                Lesson Worksheet
              </div>
              <div className="print-lesson-content">
                {formatLessonForPrint(lessonText)}
              </div>
            </>
          ) : (
            <div className="text-gray-500 italic text-center py-12 no-print">
              <p className="text-xl">Your lesson will appear here.</p>
              <p className="text-sm mt-2">Fill out the form above and click "Generate Lesson" to get started.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LessonOutputViewer;