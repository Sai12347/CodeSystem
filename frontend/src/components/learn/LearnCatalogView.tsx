import React, { useState } from 'react';
import {
  BookOpen,
  PlayCircle,
  Clock,
  HardDrive,
  AlertTriangle,
  ChevronRight,
  Code2,
  CheckCircle2,
  Search,
  Sparkles,
  Layers,
} from 'lucide-react';
import { AlgorithmId } from '../../types/algorithm';
import { useVisualizer } from '../../context/VisualizerContext';
import { ActiveTab } from '../common/Navbar';
import { COMPLETE_30_DSA_TOPICS, DsaTopicMeta } from '../../data/dsaTopicsCatalog';
import { getAvailableQuestionTopicIds, getQuestionsForTopic, getTotalQuestionsCount } from '../../data/questionBank';

interface LearnCatalogViewProps {
  onNavigate: (tab: ActiveTab) => void;
  onOpenPractice: (topicId: string) => void;
}

export const LearnCatalogView: React.FC<LearnCatalogViewProps> = ({ onNavigate, onOpenPractice }) => {
  const { selectAlgorithm } = useVisualizer();
  const [selectedCategory, setSelectedCategory] = useState<'ALL' | 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED'>('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeModalTopic, setActiveModalTopic] = useState<DsaTopicMeta | null>(null);

  const availableTopicIds = getAvailableQuestionTopicIds();
  const availableTopics = COMPLETE_30_DSA_TOPICS.filter((topic) => availableTopicIds.includes(topic.id));
  const filteredTopics = availableTopics.filter((t) => {
    const matchCat = selectedCategory === 'ALL' || t.category === selectedCategory;
    const matchSearch =
      t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.keySubtopics.some((st) => st.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchCat && matchSearch;
  });

  const handleLaunchPracticeForTopic = (topic: DsaTopicMeta) => {
    onOpenPractice(topic.id);
  };

  const handleDirectVisualizer = (topicId: string) => {
    if (topicId === 'arrays' || topicId === 'two-pointers') {
      selectAlgorithm('two-pointers');
    } else if (topicId === 'sliding-window') {
      selectAlgorithm('sliding-window');
    } else if (topicId === 'binary-search') {
      selectAlgorithm('binary-search');
    } else if (topicId === 'sorting') {
      selectAlgorithm('bubble-sort');
    } else if (topicId === 'stacks') {
      selectAlgorithm('stack');
    } else if (topicId === 'queues-deques') {
      selectAlgorithm('queue');
      } else {
      return;
    }
    onNavigate('visualizer');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <BookOpen className="w-5 h-5 text-blue-600 dark:text-blue-400" />
          <span className="text-xs font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">
            Curated Practice Topics
          </span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">
          Practice {getTotalQuestionsCount()} DSA Problems
        </h1>
        <p className="text-sm text-zinc-600 dark:text-zinc-400 mt-1 max-w-3xl leading-relaxed">
          Browse reviewed problem statements with matching examples, constraints, hints, and reference solutions across {availableTopics.length} topics.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
        {/* Category Tabs */}
        <div className="flex items-center gap-1.5 bg-zinc-100 dark:bg-zinc-800/80 p-1 rounded-2xl overflow-x-auto no-scrollbar">
          {(['ALL', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED'] as const).map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-4 py-1.5 text-xs font-semibold rounded-xl whitespace-nowrap transition-all ${
                selectedCategory === cat
                  ? 'bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white shadow-sm'
                  : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white'
              }`}
            >
              {cat === 'ALL' ? `All ${availableTopics.length} Topics` : cat}
            </button>
          ))}
        </div>

        {/* Search Input */}
        <div className="relative min-w-[280px]">
          <Search className="w-4 h-4 text-zinc-400 absolute left-3 top-3 pointer-events-none" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={`Search ${availableTopics.length} DSA topics...`}
            className="w-full pl-9 pr-4 py-2 rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-xs text-zinc-900 dark:text-white placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-apple-sm"
          />
        </div>
      </div>

      {/* Topic Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredTopics.map((topic) => {
          return (
            <div
              key={topic.id}
              className="p-6 rounded-3xl bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 shadow-apple-sm hover:shadow-apple-md transition-all flex flex-col justify-between group"
            >
              <div>
                {/* Category & Badge */}
                <div className="flex items-center justify-between gap-2 mb-3">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded-md">
                    {topic.category}
                  </span>
                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-purple-500/10 text-purple-600 dark:text-purple-400">
                    {topic.badge}
                  </span>
                </div>

                <h3 className="text-base font-bold text-zinc-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                  {topic.name}
                </h3>
                <p className="text-xs text-zinc-600 dark:text-zinc-400 mt-1.5 line-clamp-2 leading-relaxed">
                  {topic.summary}
                </p>

                {/* Subtopics Pills */}
                <div className="flex flex-wrap gap-1.5 mt-3">
                  {topic.keySubtopics.map((st, i) => (
                    <span
                      key={i}
                      className="px-2 py-0.5 rounded-md text-[10px] font-medium bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400"
                    >
                      {st}
                    </span>
                  ))}
                </div>
              </div>

              {/* Card Footer: Question Count & Action Buttons */}
              <div className="mt-5 pt-4 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between gap-2">
                <span className="text-xs font-semibold text-zinc-700 dark:text-zinc-300">
                  {getQuestionsForTopic(topic.id).length} Questions
                </span>

                <div className="flex items-center gap-2">
                  {['arrays', 'two-pointers', 'sliding-window', 'binary-search', 'sorting', 'stacks', 'queues-deques'].includes(topic.id) && (
                    <button
                      onClick={() => handleDirectVisualizer(topic.id)}
                      className="p-1.5 rounded-xl bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 text-zinc-700 dark:text-zinc-300 text-xs font-semibold flex items-center gap-1 transition-colors"
                      title="Open a related algorithm visualizer"
                      aria-label={`Open visualizer for ${topic.name}`}
                    >
                      <PlayCircle className="w-3.5 h-3.5" />
                    </button>
                  )}
                  <button
                    onClick={() => handleLaunchPracticeForTopic(topic)}
                    className="px-3.5 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold flex items-center gap-1.5 shadow-sm transition-all active:scale-95"
                  >
                    <Code2 className="w-3.5 h-3.5" />
                    <span>Practice</span>
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
