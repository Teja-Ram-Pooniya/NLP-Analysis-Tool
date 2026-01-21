import React, { useState } from 'react';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Upload, Download, Trash2, Copy, Check } from 'lucide-react';

export default function NLPApp() {
  const [text, setText] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState('analysis');

  // Simple NLP processing
  const processText = (inputText) => {
    // Preprocessing
    const cleaned = inputText.toLowerCase().replace(/[^\w\s]/g, '').trim();
    const tokens = cleaned.split(/\s+/).filter(t => t.length > 0);
    
    // Stopwords
    const stopwords = new Set([
      'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
      'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
      'i', 'you', 'he', 'she', 'it', 'we', 'they', 'this', 'that'
    ]);
    
    const filtered = tokens.filter(t => !stopwords.has(t) && t.length > 2);
    
    // Word frequency
    const freq = {};
    filtered.forEach(word => {
      freq[word] = (freq[word] || 0) + 1;
    });
    
    const topWords = Object.entries(freq)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .map(([word, count]) => ({ word, count }));
    
    // Keywords (same as top words for this version)
    const keywords = topWords.slice(0, 5).map(w => w.word);
    
    // Statistics
    const sentences = inputText.split(/[.!?]+/).filter(s => s.trim().length > 0).length;
    const avgWordLength = tokens.length > 0 
      ? (tokens.reduce((sum, w) => sum + w.length, 0) / tokens.length).toFixed(1)
      : 0;
    
    // Sentiment (simple heuristic)
    const positiveWords = new Set(['amazing', 'love', 'great', 'awesome', 'excellent', 'good', 'best', 'beautiful']);
    const negativeWords = new Set(['hate', 'bad', 'worst', 'terrible', 'horrible', 'poor', 'awful']);
    
    let sentiment = 'neutral';
    let score = 0;
    
    tokens.forEach(word => {
      if (positiveWords.has(word)) score++;
      if (negativeWords.has(word)) score--;
    });
    
    if (score > 2) sentiment = 'positive';
    else if (score < -2) sentiment = 'negative';
    
    // Entity extraction (simple - capitalized words)
    const entities = inputText.match(/\b[A-Z][a-z]*\b/g) || [];
    const uniqueEntities = [...new Set(entities)].slice(0, 5);
    
    return {
      cleaned,
      tokens,
      filtered,
      topWords,
      keywords,
      statistics: {
        characters: inputText.length,
        words: tokens.length,
        uniqueWords: new Set(tokens).size,
        sentences,
        avgWordLength
      },
      sentiment: {
        label: sentiment,
        score: score
      },
      entities: uniqueEntities
    };
  };

  const handleAnalyze = () => {
    if (!text.trim()) {
      alert('Please enter some text');
      return;
    }
    
    setLoading(true);
    setTimeout(() => {
      const processed = processText(text);
      setResults(processed);
      setLoading(false);
    }, 500);
  };

  const handleClear = () => {
    setText('');
    setResults(null);
  };

  const handleCopyResults = () => {
    const resultText = `NLP Analysis Results\n\n${JSON.stringify(results, null, 2)}`;
    navigator.clipboard.writeText(resultText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadJSON = () => {
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'nlp-analysis.json';
    link.click();
  };

  const sentimentColors = {
    positive: '#10b981',
    negative: '#ef4444',
    neutral: '#6b7280'
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-black p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">NLP Analysis Tool</h1>
          <p className="text-purple-300">Advanced text processing and analysis powered by AI</p>
        </div>

        {/* Main Container */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Input Section */}
          <div className="lg:col-span-1">
            <div className="bg-gray-900 rounded-lg p-6 shadow-xl border border-purple-500">
              <h2 className="text-xl font-bold text-white mb-4">Input Text</h2>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste your text here..."
                className="w-full h-64 bg-gray-800 text-white rounded p-3 border border-gray-700 focus:border-purple-500 focus:outline-none resize-none"
              />
              
              <div className="flex gap-2 mt-4">
                <button
                  onClick={handleAnalyze}
                  disabled={loading}
                  className="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded transition disabled:opacity-50"
                >
                  {loading ? 'Analyzing...' : 'Analyze'}
                </button>
                <button
                  onClick={handleClear}
                  className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition"
                >
                  <Trash2 size={20} />
                </button>
              </div>

              {text && (
                <p className="text-gray-400 text-sm mt-2">
                  Characters: {text.length} | Words: {text.split(/\s+/).filter(w => w).length}
                </p>
              )}
            </div>
          </div>

          {/* Results Section */}
          <div className="lg:col-span-2">
            {results ? (
              <div className="bg-gray-900 rounded-lg shadow-xl border border-purple-500 overflow-hidden">
                {/* Tabs */}
                <div className="flex border-b border-gray-700">
                  {['analysis', 'keywords', 'entities', 'export'].map(tab => (
                    <button
                      key={tab}
                      onClick={() => setActiveTab(tab)}
                      className={`flex-1 py-3 px-4 font-semibold transition capitalize ${
                        activeTab === tab
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-800 text-gray-300 hover:text-white'
                      }`}
                    >
                      {tab}
                    </button>
                  ))}
                </div>

                {/* Tab Content */}
                <div className="p-6">
                  {/* Analysis Tab */}
                  {activeTab === 'analysis' && (
                    <div className="space-y-6">
                      {/* Statistics */}
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        <div className="bg-gray-800 p-4 rounded border border-gray-700">
                          <p className="text-gray-400 text-sm">Characters</p>
                          <p className="text-2xl font-bold text-purple-400">{results.statistics.characters}</p>
                        </div>
                        <div className="bg-gray-800 p-4 rounded border border-gray-700">
                          <p className="text-gray-400 text-sm">Words</p>
                          <p className="text-2xl font-bold text-blue-400">{results.statistics.words}</p>
                        </div>
                        <div className="bg-gray-800 p-4 rounded border border-gray-700">
                          <p className="text-gray-400 text-sm">Unique Words</p>
                          <p className="text-2xl font-bold text-green-400">{results.statistics.uniqueWords}</p>
                        </div>
                        <div className="bg-gray-800 p-4 rounded border border-gray-700">
                          <p className="text-gray-400 text-sm">Sentences</p>
                          <p className="text-2xl font-bold text-yellow-400">{results.statistics.sentences}</p>
                        </div>
                        <div className="bg-gray-800 p-4 rounded border border-gray-700">
                          <p className="text-gray-400 text-sm">Avg Word Length</p>
                          <p className="text-2xl font-bold text-pink-400">{results.statistics.avgWordLength}</p>
                        </div>
                        <div className="bg-gray-800 p-4 rounded border border-gray-700">
                          <p className="text-gray-400 text-sm">Sentiment</p>
                          <p className="text-2xl font-bold capitalize" style={{color: sentimentColors[results.sentiment.label]}}>
                            {results.sentiment.label}
                          </p>
                        </div>
                      </div>

                      {/* Word Frequency Chart */}
                      <div className="bg-gray-800 p-4 rounded border border-gray-700">
                        <h3 className="text-white font-bold mb-4">Top Words</h3>
                        <ResponsiveContainer width="100%" height={250}>
                          <BarChart data={results.topWords}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                            <XAxis dataKey="word" stroke="#999" />
                            <YAxis stroke="#999" />
                            <Tooltip contentStyle={{backgroundColor: '#1f2937', border: '1px solid #444'}} />
                            <Bar dataKey="count" fill="#a855f7" />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>

                      {/* Cleaned Text */}
                      <div>
                        <h3 className="text-white font-bold mb-2">Cleaned Text</h3>
                        <p className="bg-gray-800 p-4 rounded text-gray-300 border border-gray-700 text-sm">
                          {results.cleaned}
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Keywords Tab */}
                  {activeTab === 'keywords' && (
                    <div className="space-y-4">
                      <h3 className="text-white font-bold">Extracted Keywords</h3>
                      <div className="flex flex-wrap gap-2">
                        {results.keywords.map((kw, i) => (
                          <span
                            key={i}
                            className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-full text-sm font-semibold transition"
                          >
                            {kw}
                          </span>
                        ))}
                      </div>

                      <div className="mt-6">
                        <h3 className="text-white font-bold mb-4">Word Frequency Distribution</h3>
                        <ResponsiveContainer width="100%" height={300}>
                          <PieChart>
                            <Pie
                              data={results.topWords.slice(0, 5)}
                              dataKey="count"
                              nameKey="word"
                              cx="50%"
                              cy="50%"
                              outerRadius={100}
                              label
                            >
                              {results.topWords.slice(0, 5).map((_, i) => (
                                <Cell key={i} fill={['#a855f7', '#3b82f6', '#10b981', '#f59e0b', '#ef4444'][i]} />
                              ))}
                            </Pie>
                            <Tooltip />
                          </PieChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  )}

                  {/* Entities Tab */}
                  {activeTab === 'entities' && (
                    <div>
                      <h3 className="text-white font-bold mb-4">Named Entities (Capitalized Terms)</h3>
                      {results.entities.length > 0 ? (
                        <div className="flex flex-wrap gap-2">
                          {results.entities.map((entity, i) => (
                            <span
                              key={i}
                              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded border border-blue-500 transition"
                            >
                              {entity}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <p className="text-gray-400">No named entities found</p>
                      )}
                    </div>
                  )}

                  {/* Export Tab */}
                  {activeTab === 'export' && (
                    <div className="space-y-4">
                      <button
                        onClick={downloadJSON}
                        className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded transition flex items-center justify-center gap-2"
                      >
                        <Download size={20} />
                        Download as JSON
                      </button>
                      <button
                        onClick={handleCopyResults}
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded transition flex items-center justify-center gap-2"
                      >
                        {copied ? <Check size={20} /> : <Copy size={20} />}
                        {copied ? 'Copied!' : 'Copy Results'}
                      </button>
                      <div className="bg-gray-800 p-4 rounded border border-gray-700">
                        <p className="text-gray-300 text-sm font-mono whitespace-pre-wrap max-h-64 overflow-y-auto">
                          {JSON.stringify(results, null, 2)}
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-gray-900 rounded-lg p-12 shadow-xl border border-purple-500 text-center">
                <p className="text-gray-400 text-lg">Enter text and click "Analyze" to see results</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
