export type PromptSegment = {
  kind: string;
  text: string;
};

export type PracticeItemView = {
  mode: string;
  learning_unit_id: string;
  exercise_type: string;
  position: number;
  start: number;
  end: number;
  target_text: string;
  sentence: string;
  segments: PromptSegment[];
  chip_unit_ids: string[];
};

export type RendererFeedback = {
  attempt_id?: string;
  category: string;
  submitted: string;
  expected: string;
  explanation: string;
  chunks_used: string[];
  chunks_missed: string[];
  natural_alternative: string | null;
};

export type UnitLabel = {
  id: string;
  text: string;
};

export type RendererAnswer = {
  text: string;
  submittedUnitId: string | null;
};

export type RendererProps = {
  item: PracticeItemView;
  units: UnitLabel[];
  pending: boolean;
  submitError: string | null;
  feedback: RendererFeedback | null;
  revealed?: boolean;
  onSubmit: (answer: RendererAnswer) => void;
  onContinue: () => void;
  onTryAgain?: () => void;
  onShowAnswer?: () => void;
};
