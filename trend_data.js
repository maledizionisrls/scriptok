// trend_data.js
class TrendAnalyzer {
    constructor() {
        // Prende i dati direttamente dalla variabile videos definita nel template principale
        this.videos = window.videos || [];
        this.processedData = this.processData();
    }

    processData() {
        const wordWeights = {};
        const keywordCounts = {};
        const categoryStats = {};

        this.videos.forEach(video => {
            // Converte le visualizzazioni in numero
            const views = parseInt(video.views.replace(/\./g, '')) || 0;
            
            // Processa le keywords (già array dal template)
            video.keywords.forEach(keyword => {
                // Aggiorna pesi parole (peso = occorrenze * views)
                if (!wordWeights[keyword]) wordWeights[keyword] = 0;
                wordWeights[keyword] += views;
                
                // Aggiorna conteggio semplice keywords
                if (!keywordCounts[keyword]) keywordCounts[keyword] = 0;
                keywordCounts[keyword]++;
            });

            // Processa le categorie (già array dal template)
            video.categories.forEach(category => {
                if (!categoryStats[category]) {
                    categoryStats[category] = {
                        totalViews: 0,
                        count: 0
                    };
                }
                categoryStats[category].totalViews += views;
                categoryStats[category].count++;
            });
        });

        return {
            wordCloud: this.prepareWordCloudData(wordWeights),
            keywords: this.prepareKeywordsData(keywordCounts),
            categories: this.prepareCategoriesData(categoryStats)
        };
    }

    prepareWordCloudData(weights) {
        return Object.entries(weights)
            .map(([text, value]) => ({
                text,
                size: this.calculateFontSize(value),
                weight: value
            }))
            .sort((a, b) => b.weight - a.weight)
            .slice(0, 40);  // Limita a 40 parole
    }

    calculateFontSize(value) {
        // Calcola una dimensione del font tra 12 e 48px basata sul peso
        const max = Math.max(...Object.values(this.processedData?.wordCloud || []));
        const min = Math.min(...Object.values(this.processedData?.wordCloud || []));
        const normalized = (value - min) / (max - min);
        return Math.floor(12 + normalized * 36);
    }

    prepareKeywordsData(counts) {
        const total = Object.values(counts).reduce((sum, count) => sum + count, 0);
        
        return Object.entries(counts)
            .map(([keyword, count]) => ({
                keyword,
                count,
                percentage: ((count / total) * 100).toFixed(1)
            }))
            .sort((a, b) => b.count - a.count)
            .slice(0, 10);  // Top 10 keywords
    }

    prepareCategoriesData(stats) {
        return Object.entries(stats)
            .map(([category, data]) => ({
                category,
                avgViews: Math.round(data.totalViews / data.count),
                totalVideos: data.count
            }))
            .sort((a, b) => b.avgViews - a.avgViews)
            .slice(0, 8);  // Top 8 categorie
    }

    getData() {
        return this.processedData;
    }

    static formatNumber(num) {
        return new Intl.NumberFormat('it-IT').format(num);
    }
}

// Rendi disponibile globalmente
window.TrendAnalyzer = TrendAnalyzer;
