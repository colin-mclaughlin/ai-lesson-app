import { useState, useEffect, useRef } from 'react';
import { getTopicsForGrade } from '../data/grade_topics';

interface TopicSelectorProps {
  grade: number | null;
  value: string;
  onChange: (v: string) => void;
  disabled?: boolean;
}

const TopicSelector: React.FC<TopicSelectorProps> = ({ 
  grade, 
  value, 
  onChange, 
  disabled = false 
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState(value);
  const [isCustomMode, setIsCustomMode] = useState(false);
  const [recentTopics, setRecentTopics] = useState<string[]>([]);
  const [isValid, setIsValid] = useState(true);
  const inputRef = useRef<HTMLInputElement>(null);
  const comboboxRef = useRef<HTMLDivElement>(null);

  // Load recent topics from localStorage
  useEffect(() => {
    if (grade) {
      const stored = localStorage.getItem(`recentTopics_${grade}`);
      if (stored) {
        setRecentTopics(JSON.parse(stored));
      }
    }
  }, [grade]);

  // Update input value when prop changes
  useEffect(() => {
    setInputValue(value);
  }, [value]);

  // Check if current topic is custom when grade changes
  useEffect(() => {
    if (grade && value) {
      const topicsForGrade = getTopicsForGrade(grade);
      const isCustom = !topicsForGrade.includes(value.trim());
      setIsCustomMode(isCustom);
    }
  }, [grade, value]);

  const handleInputChange = (newValue: string) => {
    setInputValue(newValue);
    // Clear validation error when user starts typing
    if (newValue.trim()) {
      setIsValid(true);
    }
    
    // Check if user typed something that matches a predefined topic
    if (grade) {
      const topicsForGrade = getTopicsForGrade(grade);
      const matchingTopic = topicsForGrade.find(topic => 
        topic.toLowerCase() === newValue.toLowerCase()
      );
      
      if (matchingTopic) {
        setIsCustomMode(false);
      } else if (newValue.trim()) {
        setIsCustomMode(true);
      }
    }
  };

  const handleOptionSelect = (selectedTopic: string) => {
    if (selectedTopic === 'Custom…') {
      setIsCustomMode(true);
      setIsOpen(false);
      inputRef.current?.focus();
    } else {
      const topicString = String(selectedTopic).trim();
      setInputValue(topicString);
      setIsCustomMode(false);
      setIsOpen(false);
      onChange(topicString);
      
      // Add to recent topics
      if (grade && topicString) {
        const updatedRecent = [topicString, ...recentTopics.filter(t => t !== topicString)].slice(0, 5);
        setRecentTopics(updatedRecent);
        localStorage.setItem(`recentTopics_${grade}`, JSON.stringify(updatedRecent));
      }
    }
  };

  const handleBlur = () => {
    const topicString = String(inputValue || '').trim();
    if (!topicString) {
      setIsValid(false);
      return;
    }
    
    setIsValid(true);
    onChange(topicString);
    
    // Add to recent topics if it's a custom topic
    if (grade && topicString && isCustomMode) {
      const updatedRecent = [topicString, ...recentTopics.filter(t => t !== topicString)].slice(0, 5);
      setRecentTopics(updatedRecent);
      localStorage.setItem(`recentTopics_${grade}`, JSON.stringify(updatedRecent));
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      const topicString = String(inputValue || '').trim();
      if (topicString) {
        onChange(topicString);
        setIsOpen(false);
      }
    } else if (e.key === 'Escape') {
      setIsOpen(false);
    }
  };

  // Get available options
  const getOptions = () => {
    if (!grade) return [];
    
    const topicsForGrade = getTopicsForGrade(grade);
    const recentForGrade = recentTopics.filter(topic => !topicsForGrade.includes(topic));
    
    return [
      ...recentForGrade,
      ...topicsForGrade,
      'Custom…'
    ];
  };

  const options = getOptions();

  if (!grade) {
    return (
      <div className="relative">
        <input
          type="text"
          disabled
          placeholder="Select a grade first"
          className="w-full p-3 border border-gray-300 rounded-md bg-gray-100 text-gray-500 cursor-not-allowed"
        />
      </div>
    );
  }

  return (
    <div className="relative" ref={comboboxRef}>
      <input
        ref={inputRef}
        type="text"
        value={inputValue}
        onChange={(e) => handleInputChange(e.target.value)}
        onFocus={() => setIsOpen(true)}
        onBlur={handleBlur}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        placeholder="e.g. Nouns"
        className={`w-full p-3 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
          !isValid ? 'border-red-500' : 'border-gray-300'
        } ${disabled ? 'bg-gray-100 cursor-not-allowed' : ''}`}
      />
      
      {!isValid && !inputValue.trim() && (
        <p className="text-red-500 text-sm mt-1">Topic cannot be empty</p>
      )}
      
      {isCustomMode && inputValue.trim() && (
        <p className="text-blue-600 text-sm mt-1">Custom topic</p>
      )}
      
      {isOpen && options.length > 0 && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
          {options.map((option, index) => (
            <button
              key={index}
              type="button"
              onClick={() => handleOptionSelect(option)}
              className={`w-full text-left px-3 py-2 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none ${
                option === 'Custom…' ? 'border-t border-gray-200 font-medium text-blue-600' : ''
              }`}
            >
              {option}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default TopicSelector;
