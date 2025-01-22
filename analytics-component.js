window.TrendAnalytics = ({ videos = [] }) => {
    const [showModal, setShowModal] = React.useState(true);
    const [viewsDistribution, setViewsDistribution] = React.useState([]);
    const [categoryTrends, setCategoryTrends] = React.useState([]);
    const [contentInsights, setContentInsights] = React.useState([]);
    const [keywordTrends, setKeywordTrends] = React.useState([]);

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

    const analyzeData = () => {
        // Analisi distribuzione visualizzazioni
        const viewsData = videos
            .filter(v => v && v.views && v.title)
            .map(v => ({
                name: v.title.substring(0, 30) + '...',
                views: parseViews(v.views)
            }))
            .sort((a, b) => b.views - a.views)
            .slice(0, 10);
        setViewsDistribution(viewsData);

        // Analisi categorie
        const categories = {};
        let totalViews = 0;

        videos.forEach(video => {
            const views = parseViews(video.views);
            totalViews += views;
            
            video.categories.forEach(category => {
                if (!categories[category]) {
                    categories[category] = { views: 0, count: 0 };
                }
                categories[category].views += views;
                categories[category].count++;
            });
        });

        const categoryData = Object.entries(categories)
            .map(([name, data]) => ({
                name,
                views: data.views,
                percentage: ((data.views / totalViews) * 100).toFixed(1),
                count: data.count
            }))
            .sort((a, b) => b.views - a.views)
            .slice(0, 5);

        setCategoryTrends(categoryData);

        // Analisi contenuti
        const patterns = videos.reduce((acc, video) => {
            const title = video.title.toLowerCase();
            const views = parseViews(video.views);
            const words = title.split(' ').length;

            // Identifica pattern nel titolo
            if (title.includes('come') || title.includes('tutorial')) {
                acc.howTo = (acc.howTo || 0) + views;
            }
            if (title.includes('?')) {
                acc.questions = (acc.questions || 0) + views;
            }
            if (title.includes('top') || title.includes('migliori')) {
                acc.rankings = (acc.rankings || 0) + views;
            }
            if (title.match(/\d+/)) {
                acc.numbers = (acc.numbers || 0) + views;
            }
            if (words < 5) {
                acc.shortTitles = (acc.shortTitles || 0) + views;
            }
            if (words > 10) {
                acc.longTitles = (acc.longTitles || 0) + views;
            }

            return acc;
        }, {});

        setContentInsights(Object.entries(patterns).map(([key, value]) => ({
            name: key,
            value: Math.round(value / 1000),
            fill: COLORS[Math.floor(Math.random() * COLORS.length)]
        })));
    };

    // Stile per il modal
    const modalStyle = {
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        backgroundColor: '#1e1e1e',
        padding: '20px',
        borderRadius: '16px',
        width: '90%',
        maxWidth: '1200px',
        maxHeight: '90vh',
        overflowY: 'auto',
        zIndex: 1000,
        border: '1px solid rgba(255, 255, 255, 0.1)',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
    };

    const overlayStyle = {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.75)',
        zIndex: 999
    };

    return React.createElement('div', null, 
        showModal && [
            // Overlay
            React.createElement('div', {
                key: 'overlay',
                style: overlayStyle,
                onClick: () => setShowModal(false)
            }),
            // Modal
            React.createElement('div', {
                key: 'modal',
                style: modalStyle
            },
                // Header
                React.createElement('div', {
                    style: {
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        marginBottom: '20px'
                    }
                },
                    React.createElement('h2', {
                        style: {
                            fontSize: '24px',
                            fontWeight: 'bold',
                            color: '#fff'
                        }
                    }, 'Analisi dei Trend'),
                    React.createElement('button', {
                        onClick: () => setShowModal(false),
                        style: {
                            background: 'none',
                            border: 'none',
                            color: '#fff',
                            fontSize: '24px',
                            cursor: 'pointer'
                        }
                    }, '×')
                ),

                // Content Grid
                React.createElement('div', {
                    style: {
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))',
                        gap: '20px'
                    }
                },
                    // Top Videos Chart
                    React.createElement('div', {
                        style: {
                            background: '#121212',
                            padding: '20px',
                            borderRadius: '12px'
                        }
                    },
                        React.createElement('h3', {
                            style: {
                                fontSize: '18px',
                                fontWeight: 'bold',
                                color: '#fff',
                                marginBottom: '15px'
                            }
                        }, 'Top 10 Video per Visualizzazioni'),
                        React.createElement(Recharts.ResponsiveContainer, {
                            width: '100%',
                            height: 300
                        },
                            React.createElement(Recharts.BarChart, {
                                data: viewsDistribution,
                                margin: { top: 20, right: 30, left: 20, bottom: 5 }
                            },
                                React.createElement(Recharts.CartesianGrid, { strokeDasharray: '3 3' }),
                                React.createElement(Recharts.XAxis, { dataKey: 'name' }),
                                React.createElement(Recharts.YAxis),
                                React.createElement(Recharts.Tooltip),
                                React.createElement(Recharts.Bar, {
                                    dataKey: 'views',
                                    fill: '#00F2EA'
                                })
                            )
                        )
                    ),

                    // Categories Chart
                    React.createElement('div', {
                        style: {
                            background: '#121212',
                            padding: '20px',
                            borderRadius: '12px'
                        }
                    },
                        React.createElement('h3', {
                            style: {
                                fontSize: '18px',
                                fontWeight: 'bold',
                                color: '#fff',
                                marginBottom: '15px'
                            }
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
                                    outerRadius: 80,
                                    fill: '#8884d8',
                                    label: true
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

                    // Content Analysis
                    React.createElement('div', {
                        style: {
                            background: '#121212',
                            padding: '20px',
                            borderRadius: '12px',
                            gridColumn: '1 / -1'
                        }
                    },
                        React.createElement('h3', {
                            style: {
                                fontSize: '18px',
                                fontWeight: 'bold',
                                color: '#fff',
                                marginBottom: '15px'
                            }
                        }, 'Analisi Contenuti'),
                        React.createElement(Recharts.ResponsiveContainer, {
                            width: '100%',
                            height: 300
                        },
                            React.createElement(Recharts.BarChart, {
                                data: contentInsights,
                                margin: { top: 20, right: 30, left: 20, bottom: 5 }
                            },
                                React.createElement(Recharts.CartesianGrid, { strokeDasharray: '3 3' }),
                                React.createElement(Recharts.XAxis, { dataKey: 'name' }),
                                React.createElement(Recharts.YAxis),
                                React.createElement(Recharts.Tooltip),
                                React.createElement(Recharts.Bar, {
                                    dataKey: 'value',
                                    fill: '#FF0050'
                                })
                            )
                        )
                    )
                )
            )
        ]
    );
};
