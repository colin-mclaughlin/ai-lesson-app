import gradeTopicsData from './grade_topics.json';

type GradeTopicsData = {
  [key: string]: string[];
};

export function getTopicsForGrade(grade: number): string[] { 
  return ((gradeTopicsData as GradeTopicsData)[String(grade)] ?? []).map((t: string) => t.trim()); 
}

export default gradeTopicsData;
