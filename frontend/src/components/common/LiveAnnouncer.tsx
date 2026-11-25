import React from 'react';
import { useVisualizer } from '../../context/VisualizerContext';

export const LiveAnnouncer: React.FC = () => {
  const { liveAnnouncement } = useVisualizer();

  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {liveAnnouncement}
    </div>
  );
};
