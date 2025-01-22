window.TrendAnalytics = ({ videos = [] }) => {
    const [showModal, setShowModal] = React.useState(true);
    const [wordCloudData, setWordCloudData] = React.useState([]);
    const [keywordPieData, setKeywordPieData] = React.useState([]);

    React.useEffect(() => {
        if (Array.isArray(videos) && videos.length > 0) {
            analyzeData();
        }
    }, [videos]);

    const analyzeData = () => {
        const wordCount = {};
        const keywordCount = {};

        videos.forEach(video => {
            const words = video.title.split(' ');
            words.forEach(word => {
                word = word.toLowerCase().replace(/[^\w\s]/gi, '');
                if (word) {
                    wordCount[word] = (wordCount[word] || 0) + parseInt(video.views.replace(/\./g, '')) || 0;
                }
            });

            video.keywords.forEach(keyword => {
                keyword = keyword.toLowerCase();
                keywordCount[keyword] = (keywordCount[keyword] || 0) + 1;
            });
        });

        const wordCloudData = Object.keys(wordCount).map(word => ({
            text: word,
            value: wordCount[word]
        }));
        setWordCloudData(wordCloudData);

        const keywordPieData = Object.keys(keywordCount).map(keyword => ({
            name: keyword,
            value: keywordCount[keyword]
        }));
        setKeywordPieData(keywordPieData);
    };

    return React.createElement('div', null, 
        showModal && [
            React.createElement('div', {
                key: 'overlay',
                style: {
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    backgroundColor: 'rgba(0, 0, 0, 0.75)',
                    zIndex: 999
                },
                onClick: () => setShowModal(false)
            }),
            React.createElement('div', {
                key: 'modal',
                style: {
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
                }
            },
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
                React.createElement('div', {
                    style: {
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))',
                        gap: '20px'
                    }
                },
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
                        }, 'Nuvola delle Parole'),
                        React.createElement(WordCloud, {
                            data: wordCloudData,
                            options: {
                                rotations: 2,
                                rotationAngles: [-90, 0],
                                fontSizes: [15, 60],
                                colors: ['#00F2EA', '#FF0050', '#8A2BE2', '#FF6B6B', '#4CAF50']
                            }
                        })
                    ),
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
                        }, 'Suddivisione delle Parole Chiave'),
                        React.createElement(Recharts.ResponsiveContainer, {
                            width: '100%',
                            height: 300
                        },
                            React.createElement(Recharts.PieChart, {},
                                React.createElement(Recharts.Pie, {
                                    data: keywordPieData,
                                    dataKey: 'value',
                                    nameKey: 'name',
                                    cx: '50%',
                                    cy: '50%',
                                    outerRadius: 80,
                                    fill: '#8884d8',
                                    label: true
                                },
                                    keywordPieData.map((entry, index) =>
                                        React.createElement(Recharts.Cell, {
                                            key: `cell-${index}`,
                                            fill: ['#00F2EA', '#FF0050', '#8A2BE2', '#FF6B6B', '#4CAF50'][index % 5]
                                        })
                                    )
                                ),
                                React.createElement(Recharts.Tooltip)
                            )
                        )
                    )
                )
            )
        ]
    );
};
