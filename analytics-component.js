import React, { useState, useEffect } from 'react';
import { 
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
    LineChart, Line, PieChart, Pie, Cell, ResponsiveContainer,
    AreaChart, Area
} from 'recharts';
import _ from 'lodash';

const TrendAnalytics = ({ videos = [] }) => {
    // Inizializza gli stati con array vuoti
    const [viewsDistribution, setViewsDistribution] = useState([]);
    const [categoryTrends, setCategoryTrends] = useState([]);
    const [keywordTrends, setKeywordTrends] = useState([]);
    const [timeAnalysis, setTimeAnalysis] = useState([]);
    const [engagementScores, setEngagementScores] = useState([]);

    const COLORS = ['#00F2EA', '#FF0050', '#8A2BE2', '#FF6B6B', '#4CAF50'];

    useEffect(() => {
        // Verifica che videos sia un array non vuoto
        if (Array.isArray(videos) && videos.length > 0) {
            analyzeData();
        }
    }, [videos]);

    const parseViews = (viewString) => {
        if (!viewString || viewString === 'N/A') return 0;
        return parseInt(viewString.replace(/\./g, '')) || 0;
    };

    const processViewsDistribution = () => {
        if (!Array.isArray(videos)) return [];
        
        const viewCounts = videos
            .filter(v => v && v.views && v.title)
            .map(v => ({
                views: parseViews(v.views),
                title: v.title
            }));

        return _.orderBy(viewCounts, ['views'], ['desc'])
            .slice(0, 10)
            .map(v => ({
                name: v.title.substring(0, 20) + '...',
                views: v.views
            }));
    };

    const processCategoryTrends = () => {
        if (!Array.isArray(videos)) return [];
        
        const categories = {};
        let totalViews = 0;

        videos.forEach(video => {
            if (!video) return;
            const views = parseViews(video.views);
            totalViews += views;

            // Assicurati che categories sia un array
            const videoCategories = Array.isArray(video.categories) ? video.categories : [];
            
            videoCategories.forEach(category => {
                if (!category) return;
                if (!categories[category]) {
                    categories[category] = { views: 0, count: 0 };
                }
                categories[category].views += views;
                categories[category].count++;
            });
        });

        return Object.entries(categories)
            .map(([name, data]) => ({
                name,
                views: data.views,
                percentage: totalViews ? ((data.views / totalViews) * 100).toFixed(1) : 0,
                count: data.count
            }))
            .sort((a, b) => b.views - a.views)
            .slice(0, 5);
    };

    const processKeywordTrends = () => {
        if (!Array.isArray(videos)) return [];
        
        const keywords = {};
        
        videos.forEach(video => {
            if (!video) return;
            const views = parseViews(video.views);
            
            // Assicurati che keywords sia un array
            const videoKeywords = Array.isArray(video.keywords) ? video.keywords : [];
            
            videoKeywords.forEach(keyword => {
                if (!keyword) return;
                if (!keywords[keyword]) {
                    keywords[keyword] = { views: 0, count: 0 };
                }
                keywords[keyword].views += views;
                keywords[keyword].count++;
            });
        });

        return Object.entries(keywords)
            .map(([name, data]) => ({
                name,
                views: data.views,
                count: data.count,
                avgViews: data.count ? Math.round(data.views / data.count) : 0
            }))
            .sort((a, b) => b.views - a.views)
            .slice(0, 5);
    };

    const processTimeAnalysis = () => {
        const categories = processCategoryTrends();
        return categories.map(cat => ({
            name: cat.name,
            trend: Math.round(cat.views / 1000),
            growth: cat.count
        }));
    };

    const calculateEngagementScores = () => {
        return processKeywordTrends().map(kw => ({
            name: kw.name,
            score: ((kw.views / kw.count) / 1000).toFixed(1),
            frequency: kw.count
        }));
    };

    const analyzeData = () => {
        const viewsData = processViewsDistribution();
        setViewsDistribution(viewsData);

        const categoryData = processCategoryTrends();
        setCategoryTrends(categoryData);

        const keywordData = processKeywordTrends();
        setKeywordTrends(keywordData);

        const timeData = processTimeAnalysis();
        setTimeAnalysis(timeData);

        const engagementData = calculateEngagementScores();
        setEngagementScores(engagementData);
    };

    // Se non ci sono dati, mostra un messaggio
    if (!Array.isArray(videos) || videos.length === 0) {
        return (
            <div className="w-full p-6 bg-gray-900 rounded-xl">
                <p className="text-white text-center">Caricamento dati in corso...</p>
            </div>
        );
    }

    return (
        <div className="w-full p-6 bg-gray-900 rounded-xl">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Top Video Performance */}
                <div className="bg-gray-800 p-6 rounded-xl">
                    <h3 className="text-xl font-bold mb-4 text-white">Top 10 Video per Visualizzazioni</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={viewsDistribution}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                            <YAxis />
                            <Tooltip />
                            <Bar dataKey="views" fill="#00F2EA" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Category Distribution */}
                <div className="bg-gray-800 p-6 rounded-xl">
                    <h3 className="text-xl font-bold mb-4 text-white">Distribuzione Categorie</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie
                                data={categoryTrends}
                                dataKey="views"
                                nameKey="name"
                                cx="50%"
                                cy="50%"
                                labelLine={false}
                                label={({ name, percentage }) => `${name} (${percentage}%)`}
                            >
                                {categoryTrends.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <Tooltip />
                        </PieChart>
                    </ResponsiveContainer>
                </div>

                {/* Keyword Performance */}
                <div className="bg-gray-800 p-6 rounded-xl">
                    <h3 className="text-xl font-bold mb-4 text-white">Performance Keywords</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <AreaChart data={keywordTrends}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Area type="monotone" dataKey="avgViews" stroke="#FF0050" fill="#FF0050" fillOpacity={0.3} />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>

                {/* Trend Analysis */}
                <div className="bg-gray-800 p-6 rounded-xl">
                    <h3 className="text-xl font-bold mb-4 text-white">Analisi Trend</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={timeAnalysis}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Line type="monotone" dataKey="trend" stroke="#00F2EA" />
                            <Line type="monotone" dataKey="growth" stroke="#FF0050" />
                        </LineChart>
                    </ResponsiveContainer>
                </div>

                {/* Engagement Stats Table */}
                <div className="bg-gray-800 p-6 rounded-xl col-span-2">
                    <h3 className="text-xl font-bold mb-4 text-white">Statistiche di Engagement</h3>
                    <div className="overflow-x-auto">
                        <table className="w-full text-white">
                            <thead>
                                <tr className="border-b border-gray-700">
                                    <th className="py-2 px-4 text-left">Keyword</th>
                                    <th className="py-2 px-4 text-left">Score Engagement</th>
                                    <th className="py-2 px-4 text-left">Frequenza</th>
                                </tr>
                            </thead>
                            <tbody>
                                {engagementScores.map((score, idx) => (
                                    <tr key={idx} className="border-b border-gray-700">
                                        <td className="py-2 px-4">{score.name}</td>
                                        <td className="py-2 px-4">{score.score}</td>
                                        <td className="py-2 px-4">{score.frequency}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TrendAnalytics;
