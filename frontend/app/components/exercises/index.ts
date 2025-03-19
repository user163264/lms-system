// Base components
export { default as BaseExercise } from './base/BaseExercise';
export { default as SelectionExercise } from './base/SelectionExercise';
export { default as InputExercise } from './base/InputExercise';
export { default as InteractiveExercise } from './base/InteractiveExercise';

// Exercise type implementations
export { default as MultipleChoiceExercise } from './MultipleChoiceExercise';
export { default as TrueFalseExercise } from './TrueFalseExercise';
export { default as ShortAnswerExercise } from './ShortAnswerExercise';
export { default as FillBlanksExercise } from './FillBlanksExercise';
export { default as MatchingWordsExercise } from './MatchingWordsExercise';
export { default as WordScrambleExercise } from './WordScrambleExercise';
export { default as SentenceReorderingExercise } from './SentenceReorderingExercise';
export { default as ImageLabelingExercise } from './ImageLabelingExercise';
export { default as LongAnswerExercise } from './LongAnswerExercise';
export { default as ClozeTestExercise } from './ClozeTestExercise';

// Factory
export { default as ExerciseFactory } from './ExerciseFactory';

// Export types from components
export type { BaseExerciseProps } from './base/BaseExercise';
export type { SelectionOption, SelectionExerciseProps } from './base/SelectionExercise';
export type { InputExerciseProps } from './base/InputExercise';
export type { InteractiveExerciseProps } from './base/InteractiveExercise';
export type { MultipleChoiceExerciseProps } from './MultipleChoiceExercise';
export type { TrueFalseExerciseProps } from './TrueFalseExercise';
export type { ShortAnswerExerciseProps } from './ShortAnswerExercise';
export type { FillBlanksExerciseProps } from './FillBlanksExercise';
export type { MatchingWordsExerciseProps } from './MatchingWordsExercise';
export type { WordScrambleExerciseProps } from './WordScrambleExercise';
export type { SentenceReorderingExerciseProps } from './SentenceReorderingExercise';
export type { ImageLabelingExerciseProps, LabelPoint } from './ImageLabelingExercise';
export type { LongAnswerExerciseProps } from './LongAnswerExercise';
export type { ClozeTestExerciseProps } from './ClozeTestExercise';
export type { ExerciseFactoryProps } from './ExerciseFactory'; 