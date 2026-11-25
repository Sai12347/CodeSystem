import React, { createContext, useContext, useState, useEffect, useRef } from 'react';
import { AlgorithmId, AlgorithmStep, AlgorithmMetadata } from '../types/algorithm';
import { AlgorithmEngine, ALGORITHM_REGISTRY } from '../engine/core/AlgorithmEngine';

interface VisualizerContextType {
  algorithmId: AlgorithmId;
  metadata: AlgorithmMetadata;
  currentStep: AlgorithmStep;
  currentStepIndex: number;
  totalSteps: number;
  isPlaying: boolean;
  speed: number;
  predictMode: boolean;
  isPredictModalOpen: boolean;
  predictionAnswered: boolean;
  predictionFeedback: {
    correct: boolean;
    explanation: string;
  } | null;
  liveAnnouncement: string;
  selectAlgorithm: (id: AlgorithmId, customInput?: any) => void;
  play: () => void;
  pause: () => void;
  togglePlay: () => void;
  nextStep: () => void;
  previousStep: () => void;
  jumpToStep: (index: number) => void;
  reset: () => void;
  setSpeed: (speed: number) => void;
  togglePredictMode: () => void;
  answerPrediction: (optionIndex: number) => void;
  closePredictModal: () => void;
  applyCustomInput: (input: any) => void;
  generateRandomInput: () => void;
}

const VisualizerContext = createContext<VisualizerContextType | undefined>(undefined);

export const VisualizerProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [algorithmId, setAlgorithmId] = useState<AlgorithmId>('binary-search');
  const engineRef = useRef<AlgorithmEngine>(new AlgorithmEngine('binary-search'));

  const [currentStep, setCurrentStep] = useState<AlgorithmStep>(() => engineRef.current.getCurrentStep());
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(0);
  const [totalSteps, setTotalSteps] = useState<number>(() => engineRef.current.getTotalSteps());
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [speed, setSpeed] = useState<number>(1);
  const [predictMode, setPredictMode] = useState<boolean>(false);
  const [isPredictModalOpen, setIsPredictModalOpen] = useState<boolean>(false);
  const [predictionAnswered, setPredictionAnswered] = useState<boolean>(false);
  const [predictionFeedback, setPredictionFeedback] = useState<{ correct: boolean; explanation: string } | null>(null);
  const [liveAnnouncement, setLiveAnnouncement] = useState<string>('Algorithm visualizer ready.');

  const timerRef = useRef<number | null>(null);

  // Sync state from engine
  const syncWithEngine = () => {
    const step = engineRef.current.getCurrentStep();
    setCurrentStep(step);
    setCurrentStepIndex(engineRef.current.getCurrentIndex());
    setTotalSteps(engineRef.current.getTotalSteps());
    setLiveAnnouncement(step.description);

    // If predict mode is ON and this step has a prediction challenge that hasn't been answered yet
    if (predictMode && step.prediction && !predictionAnswered) {
      setIsPlaying(false);
      setIsPredictModalOpen(true);
      setPredictionFeedback(null);
    }
  };

  const selectAlgorithm = (id: AlgorithmId, customInput?: any) => {
    pause();
    engineRef.current.loadAlgorithm(id, customInput);
    setAlgorithmId(id);
    setPredictionAnswered(false);
    setIsPredictModalOpen(false);
    setPredictionFeedback(null);
    syncWithEngine();
  };

  const play = () => {
    setIsPlaying(true);
  };

  const pause = () => {
    setIsPlaying(false);
    if (timerRef.current) {
      window.clearInterval(timerRef.current);
      timerRef.current = null;
    }
  };

  const togglePlay = () => {
    if (isPlaying) {
      pause();
    } else {
      // If at end, reset first
      if (currentStepIndex >= totalSteps - 1) {
        reset();
      }
      play();
    }
  };

  const nextStep = () => {
    const next = engineRef.current.nextStep();
    if (next) {
      setPredictionAnswered(false);
      syncWithEngine();
    } else {
      pause();
    }
  };

  const previousStep = () => {
    const prev = engineRef.current.previousStep();
    if (prev) {
      setPredictionAnswered(false);
      syncWithEngine();
    }
  };

  const jumpToStep = (index: number) => {
    pause();
    engineRef.current.jumpToStep(index);
    setPredictionAnswered(false);
    syncWithEngine();
  };

  const reset = () => {
    pause();
    engineRef.current.reset();
    setPredictionAnswered(false);
    setIsPredictModalOpen(false);
    setPredictionFeedback(null);
    syncWithEngine();
  };

  const togglePredictMode = () => {
    setPredictMode((prev) => !prev);
    setIsPredictModalOpen(false);
  };

  const answerPrediction = (optionIndex: number) => {
    const pred = currentStep.prediction;
    if (!pred) return;

    const isCorrect = optionIndex === pred.correctOptionIndex;
    setPredictionAnswered(true);
    setPredictionFeedback({
      correct: isCorrect,
      explanation: pred.explanation,
    });
  };

  const closePredictModal = () => {
    setIsPredictModalOpen(false);
  };

  const applyCustomInput = (input: any) => {
    selectAlgorithm(algorithmId, input);
  };

  const generateRandomInput = () => {
    const size = 7;
    const randomArray = Array.from({ length: size }, () => Math.floor(Math.random() * 90) + 10);
    if (algorithmId === 'binary-search') {
      randomArray.sort((a, b) => a - b);
      const target = randomArray[Math.floor(Math.random() * size)];
      applyCustomInput({ array: randomArray, target });
    } else if (algorithmId === 'linear-search') {
      const target = randomArray[Math.floor(Math.random() * size)];
      applyCustomInput({ array: randomArray, target });
    } else if (algorithmId === 'two-pointers') {
      randomArray.sort((a, b) => a - b);
      const target = randomArray[0] + randomArray[size - 1];
      applyCustomInput({ array: randomArray, target });
    } else if (algorithmId === 'sliding-window') {
      applyCustomInput({ array: randomArray, k: 3 });
    } else {
      applyCustomInput(randomArray);
    }
  };

  // Playback timer effect
  useEffect(() => {
    if (isPlaying) {
      const delay = Math.max(250, 1200 / speed);
      timerRef.current = window.setInterval(() => {
        if (engineRef.current.getCurrentIndex() < engineRef.current.getTotalSteps() - 1) {
          nextStep();
        } else {
          pause();
        }
      }, delay);
    } else if (timerRef.current) {
      window.clearInterval(timerRef.current);
      timerRef.current = null;
    }

    return () => {
      if (timerRef.current) window.clearInterval(timerRef.current);
    };
  }, [isPlaying, speed, currentStepIndex]);

  // Keyboard shortcut listener (Space, Left/Right arrow, R, P)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't intercept if user is typing in input or editor
      if (
        document.activeElement?.tagName === 'INPUT' ||
        document.activeElement?.tagName === 'TEXTAREA' ||
        (document.activeElement as HTMLElement)?.isContentEditable
      ) {
        return;
      }

      switch (e.key) {
        case ' ':
        case 'k':
          e.preventDefault();
          togglePlay();
          break;
        case 'ArrowRight':
        case 'l':
          e.preventDefault();
          nextStep();
          break;
        case 'ArrowLeft':
        case 'j':
          e.preventDefault();
          previousStep();
          break;
        case 'r':
        case 'R':
          e.preventDefault();
          reset();
          break;
        case 'p':
        case 'P':
          e.preventDefault();
          togglePredictMode();
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isPlaying, currentStepIndex, totalSteps]);

  const metadata = ALGORITHM_REGISTRY[algorithmId]?.metadata || ALGORITHM_REGISTRY['binary-search'].metadata;

  return (
    <VisualizerContext.Provider
      value={{
        algorithmId,
        metadata,
        currentStep,
        currentStepIndex,
        totalSteps,
        isPlaying,
        speed,
        predictMode,
        isPredictModalOpen,
        predictionAnswered,
        predictionFeedback,
        liveAnnouncement,
        selectAlgorithm,
        play,
        pause,
        togglePlay,
        nextStep,
        previousStep,
        jumpToStep,
        reset,
        setSpeed,
        togglePredictMode,
        answerPrediction,
        closePredictModal,
        applyCustomInput,
        generateRandomInput,
      }}
    >
      {children}
    </VisualizerContext.Provider>
  );
};

export const useVisualizer = () => {
  const context = useContext(VisualizerContext);
  if (!context) throw new Error('useVisualizer must be used within VisualizerProvider');
  return context;
};
