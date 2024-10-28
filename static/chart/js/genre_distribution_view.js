const labels = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'Fantasy', 'Documentary', 'Adventure'];

async function fetchGenreData() {
    const response = await fetch(popChartUrl);
    return response.json();
}

async function fetchCustGenreData() {
    const response = await fetch(custChartUrl);
    return response.json();
}

async function fetchSvdGenreData() {
    const response = await fetch(svdChartUrl);
    return response.json();
}

async function fetchNmfGenreData() {
    const response = await fetch(nmfChartUrl);
    return response.json();
}

async function fetchMfGenreData() {
    const response = await fetch(mfChartUrl);
    return response.json();
}

async function fetchLDAGenreData() {
    const response = await fetch(ldaChartUrl);
    return response.json();
}

function alignDataWithLabels(data) {
    return labels.map(label => data[label] || 0);
}

function drawChart(chartId, genreData, chartType = 'default') {
    const ctx = document.getElementById(chartId).getContext('2d');
    const alignedData = alignDataWithLabels(genreData);

    const colors = chartType === 'popular' ?
        ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)',
         'rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(100, 149, 237, 0.2)',
         'rgba(255, 159, 64, 0.2)', 'rgba(144, 238, 144, 0.2)', 'rgba(210, 105, 30, 0.2)',
         'rgba(70, 130, 180, 0.2)']
        :
        ['rgba(255, 99, 132, 0.8)', 'rgba(54, 162, 235, 0.8)', 'rgba(75, 192, 192, 0.8)',
         'rgba(255, 206, 86, 0.8)', 'rgba(153, 102, 255, 0.8)', 'rgba(100, 149, 237, 0.8)',
         'rgba(255, 159, 64, 0.8)', 'rgba(144, 238, 144, 0.8)', 'rgba(210, 105, 30, 0.8)',
         'rgba(70, 130, 180, 0.8)'];

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: alignedData,
                backgroundColor: colors,
                borderColor: colors.map(color => color.replace('0.2', '1').replace('0.8', '1')),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                datalabels: {
                    color: '#000',
                    formatter: (value, context) => context.chart.data.labels[context.dataIndex],
                    font: { size: 14, weight: 'bold' },
                    textAlign: 'center'
                }
            }
        },
        plugins: [ChartDataLabels]
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    const genreData = await fetchGenreData();
    drawChart('genreChart', genreData, 'popular');

    const custGenreData = await fetchCustGenreData();
    drawChart('custGenreChart', custGenreData);

    const svdGenreData = await fetchSvdGenreData();
    drawChart('svdGenreChart', svdGenreData, 'svd');

    const nmfGenreData = await fetchNmfGenreData();
    drawChart('nmfGenreChart', nmfGenreData, 'nmf');

    const mfGenreData = await fetchMfGenreData();
    drawChart('mfGenreChart', mfGenreData, 'mf');

    const ldaGenreData = await fetchLDAGenreData();
    drawChart('ldaGenreChart', ldaGenreData, 'lda');
});
