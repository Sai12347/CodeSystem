import React, { useState } from 'react';
import { Bot, Send, Sparkles, Code2, HelpCircle, Lightbulb, User } from 'lucide-react';

interface ChatMessage {
  id: string;
  sender: 'ai' | 'user';
  text: string;
  timestamp: string;
  codeSnippet?: string;
}

export const AiTutorChatView: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'msg_welcome',
      sender: 'ai',
      text: `Hello! I'm your DSA tutor. Ask me to explain an algorithm, walk through an example, or give you a hint.`,
      timestamp: 'Just now',
    },
  ]);

  const [inputQuery, setInputQuery] = useState('');
  const [isThinking, setIsThinking] = useState(false);

  const samplePrompts = [
    `Why do we use low + (high - low) / 2 instead of (low + high) / 2?`,
    `Explain how Merge Sort achieves O(n log n) guaranteed time.`,
    `Give me a hint for Two Sum sorted without revealing the solution.`,
    `Can you walk me through a dry run of Bubble Sort on [5, 1, 4]?`,
  ];

  const handleSendQuery = async (textToSend?: string) => {
    const query = textToSend || inputQuery;
    if (!query.trim() || isThinking) return;

    const userMsg: ChatMessage = {
      id: `usr_${Date.now()}`,
      sender: 'user',
      text: query,
      timestamp: 'Just now',
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setIsThinking(true);

    try {
      const response = await fetch('/api/ai-tutor/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, topic: 'Data Structures and Algorithms', userLevel: 'beginner' }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload?.error || `Tutor request failed (${response.status}).`);

      const modelText = payload?.data?.candidates?.[0]?.content?.parts
        ?.map((part: { text?: string }) => part.text || '')
        .filter(Boolean)
        .join('\n');
      const answer = payload?.explanation || modelText;
      if (!answer) throw new Error(payload?.error || 'Tutor returned an empty response.');

      setMessages((prev) => [...prev, {
        id: `ai_${Date.now()}`,
        sender: 'ai',
        text: answer,
        timestamp: 'Just now',
      }]);
    } catch (error) {
      setMessages((prev) => [...prev, {
        id: `ai_error_${Date.now()}`,
        sender: 'ai',
        text: error instanceof Error
          ? `${error.message} Make sure the backend is running on port 8080.`
          : 'Tutor request failed. Make sure the backend is running on port 8080.',
        timestamp: 'Just now',
      }]);
    } finally {
      setIsThinking(false);
    }
  };
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-7 h-7 rounded-lg bg-purple-600 text-white flex items-center justify-center">
            <Bot className="w-4 h-4" />
          </div>
          <span className="text-xs font-bold uppercase tracking-wider text-purple-600 dark:text-purple-400">
            AI Tutor â€¢ Backend-connected tutor
          </span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">
          Intelligent DSA Companion
        </h1>
        <p className="text-xs text-zinc-600 dark:text-zinc-400 mt-1 max-w-xl">
          Get intuitive, beginner-friendly explanations, line-by-line dry runs, and Socratic hints without full spoilers.
        </p>
      </div>

      {/* Suggested Quick Prompts */}
      <div className="flex items-center gap-2 overflow-x-auto no-scrollbar py-1">
        {samplePrompts.map((p, idx) => (
          <button
            key={idx}
            onClick={() => handleSendQuery(p)}
            className="px-3 py-1.5 rounded-full bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 dark:hover:bg-zinc-700 text-zinc-700 dark:text-zinc-300 text-xs whitespace-nowrap transition-colors border border-zinc-200 dark:border-zinc-700"
          >
            {p}
          </button>
        ))}
      </div>

      {/* Chat Messages Box */}
      <div className="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-3xl p-6 shadow-apple-sm min-h-[460px] max-h-[580px] overflow-y-auto space-y-4">
        {messages.map((msg) => {
          const isAi = msg.sender === 'ai';
          return (
            <div
              key={msg.id}
              className={`flex items-start gap-3 ${isAi ? 'justify-start' : 'justify-end'}`}
            >
              {isAi && (
                <div className="w-8 h-8 rounded-xl bg-purple-600 text-white flex items-center justify-center flex-shrink-0 mt-0.5">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div
                className={`max-w-[85%] rounded-2xl p-4 text-xs leading-relaxed ${
                  isAi
                    ? 'bg-zinc-50 dark:bg-zinc-800/70 border border-zinc-200/60 dark:border-zinc-700/60 text-zinc-800 dark:text-zinc-200'
                    : 'bg-blue-600 text-white shadow-sm'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.text}</div>

                {msg.codeSnippet && (
                  <div className="mt-3 p-3 rounded-xl bg-zinc-950 text-zinc-100 font-mono text-[11px] overflow-x-auto">
                    {msg.codeSnippet}
                  </div>
                )}

                <div
                  className={`mt-2 text-[10px] ${
                    isAi ? 'text-zinc-400' : 'text-blue-200'
                  }`}
                >
                  {msg.timestamp}
                </div>
              </div>

              {!isAi && (
                <div className="w-8 h-8 rounded-xl bg-blue-600 text-white flex items-center justify-center flex-shrink-0 mt-0.5">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          );
        })}

        {isThinking && (
          <div className="flex items-center gap-3 text-xs text-zinc-400">
            <div className="w-8 h-8 rounded-xl bg-purple-600 text-white flex items-center justify-center flex-shrink-0">
              <Bot className="w-4 h-4" />
            </div>
            <div className="p-3 rounded-2xl bg-zinc-100 dark:bg-zinc-800 flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-purple-500 animate-bounce" />
              <div className="w-2 h-2 rounded-full bg-purple-500 animate-bounce [animation-delay:0.2s]" />
              <div className="w-2 h-2 rounded-full bg-purple-500 animate-bounce [animation-delay:0.4s]" />
              <span className="text-[11px] font-medium text-zinc-500">Gemini is analyzing...</span>
            </div>
          </div>
        )}
      </div>

      {/* Input Field */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendQuery();
        }}
        className="flex items-center gap-3 bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-2 shadow-apple-sm"
      >
        <input
          type="text"
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          placeholder="Ask anything about algorithms, loops, variables, or time complexity..."
          className="flex-1 px-4 py-2 text-xs bg-transparent text-zinc-900 dark:text-white placeholder-zinc-400 focus:outline-none"
        />
        <button
          type="submit"
          disabled={!inputQuery.trim() || isThinking}
          className="p-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white transition-colors disabled:opacity-40"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
};

