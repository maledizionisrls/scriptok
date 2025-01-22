window.TrendAnalytics = ({ videos = [] }) => {
    const [viewsDistribution, setViewsDistribution] = React.useState([]);
    const [categoryTrends, setCategoryTrends] = React.useState([]);
    const [keywordTrends, setKeywordTrends] = React.useState([]);
    const [timeAnalysis, setTimeAnalysis] = React.useState([]);
    const [engagementScores, setEngagementScores] = React.useState([]);

    const COLORS = ['#00F2EA', '#FF0050', '#8A2BE2', '#FF6B6B', '#4CAF50'];

    React.useEffect(() => {
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

    return React.createElement('div', { 
        className: 'w-full p-6 bg-gray-900 rounded-xl' 
    }, 
        React.createElement('div', { 
            className: 'grid grid-cols-1 lg:grid-cols-2 gap-8' 
        },
            // Top Video Performance
            React.createElement('div', {
                className: 'bg-gray-800 p-6 rounded-xl'
            },
                React.createElement('h3', {
                    className: 'text-xl font-bold mb-4 text-white'
                }, 'Top 10 Video per Visualizzazioni'),
                React.createElement(Recharts.ResponsiveContainer, {
                    width: '100%',
                    height: 300
                },
                    React.createElement(Recharts.BarChart, {
                        data: viewsDistribution
                    },
                        React.createElement(Recharts.CartesianGrid, {
                            strokeDasharray: '3 3'
                        }),
                        React.createElement(Recharts.XAxis, {
                            dataKey: 'name',
                            angle: -45,
                            textAnchor: 'end',
                            height: 100
                        }),
                        React.createElement(Recharts.YAxis),
                        React.createElement(Recharts.Tooltip),
                        React.createElement(Recharts.Bar, {
                            dataKey: 'views',
                            fill: '#00F2EA'
                        })
                    )
                )
            ),

            // Category Distribution
            React.createElement('div', {
                className: 'bg-gray-800 p-6 rounded-xl'
            },
                React.createElement('h3', {
                    className: 'text-xl font-bold mb-4 text-white'
                }, 'Distribuzione Categorie'),
                React.createElement(Recharts.ResponsiveContainer, {
                    width: '100%',
                    height: 300
                },
                    React.createElement(Recharts.PieChart, {},
                        React.createElement(Recharts.Pie, {
                            data: categoryTrends,
                            dataKey: 'views',
                            nameKey: 'name',
                            cx: '50%',
                            cy: '50%',
                            labelLine: false,
                            label: ({ name, percentage }) => `${name} (${percentage}%)`
                        },
                            categoryTrends.map((entry, index) =>
                                React.createElement(Recharts.Cell, {
                                    key: `cell-${index}`,
                                    fill: COLORS[index % COLORS.length]
                                })
                            )
                        ),
                        React.createElement(Recharts.Tooltip)
                    )
                )
            ),

            // Keyword Performance
            React.createElement('div', {
                className: 'bg-gray-800 p-6 rounded-xl'
            },
                React.createElement('h3', {
                    className: 'text-xl font-bold mb-4 text-white'
                }, 'Performance Keywords'),
                React.createElement(Recharts.ResponsiveContainer, {
                    width: '100%',
                    height: 300
                },
                    React.createElement(Recharts.AreaChart, {
                        data: keywordTrends
                    },
                        React.createElement(Recharts.CartesianGrid, {
                            strokeDasharray: '3 3'
                        }),
                        React.createElement(Recharts.XAxis, {
                            dataKey: 'name'
                        }),
                        React.createElement(Recharts.YAxis),
                        React.createElement(Recharts.Tooltip),
                        React.createElement(Recharts.Area, {
                            type: 'monotone',
                            dataKey: 'avgViews',
                            stroke: '#FF0050',
                            fill: '#FF0050',
                            fillOpacity: 0.3
                        })
                    )
                )
            ),

            // Engagement Stats Table
            React.createElement('div', {
                className: 'bg-gray-800 p-6 rounded-xl col-span-2'
            },
                React.createElement('h3', {
                    className: 'text-xl font-bold mb-4 text-white'
                }, 'Statistiche di Engagement'),
                React.createElement('div', {
                    className: 'overflow-x-auto'
                },
                    React.createElement('table', {
                        className: 'w-full text-white'
                    },
                        React.createElement('thead', {},
                            React.createElement('tr', {
                                className: 'border-b border-gray-700'
                            },
                                React.createElement('th', {
                                    className: 'py-2 px-4 text-left'
                                }, 'Keyword'),
                                React.createElement('th', {
                                    className: 'py-2 px-4 text-left'
                                }, 'Score Engagement'),
                                React.createElement('th', {
                                    className: 'py-2 px-4 text-left'
                                }, 'Frequenza')
                            )
                        ),
                        React.createElement('tbody', {},
                            engagementScores.map((score, idx) =>
                                React.createElement('tr', {
                                    key: idx,
                                    className: 'border-b border-gray-700'
                                },
                                    React.createElement('td', {
                                        className: 'py-2 px-4'
                                    }, score.name),
                                    React.createElement('td', {
                                        className: 'py-2 px-4'
                                    }, score.score),
                                    React.createElement('td', {
                                        className: 'py-2 px-4'
                                    }, score.frequency)
                                )
                            )
                        )
                    )
                )
            )
        )
    );
};
