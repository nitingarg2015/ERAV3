let lossChart, accuracyChart;
let runHistory = [];
let currentRunId = 0;
const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']; // Different colors for each run

function initPlotly(divId, title, xaxis, yaxis) {
    const element = document.getElementById(divId);
    if (!element) {
        console.error(`Element with id ${divId} not found`);
        return null;
    }

    return {
        element: element,
        layout: {
            title: {
                text: title,
                font: { size: 14 }
            },
            xaxis: {
                title: xaxis,
                titlefont: { size: 12 }
            },
            yaxis: {
                title: yaxis,
                titlefont: { size: 12 }
            },
            margin: {l: 40, r: 20, t: 30, b: 30},
            showlegend: true,
            legend: {
                orientation: 'h',
                y: -0.2
            },
            font: { size: 10 },
            autosize: true
        }
    };
}

function updatePlot(chart, runs) {
    if (!chart || !chart.element) return;

    const traces = [];
    runs.forEach((run, index) => {
        const colorIndex = index % colors.length;
        // Add training loss trace
        if (run.trainLoss.length > 0) {
            traces.push({
                x: run.epochs,
                y: run.trainLoss,
                name: `Run ${run.id} - Training Loss`,
                mode: 'lines+markers',
                line: { color: colors[colorIndex] },
                showlegend: chart.element.id === 'loss-chart'
            });
        }
        // Add test loss/accuracy trace
        if (run.testLoss.length > 0) {
            traces.push({
                x: run.epochs,
                y: chart.element.id === 'loss-chart' ? run.testLoss : run.testAcc,
                name: `Run ${run.id} - ${chart.element.id === 'loss-chart' ? 'Test Loss' : 'Test Accuracy'}`,
                mode: 'lines+markers',
                line: { color: colors[colorIndex], dash: 'dashdot' },
                showlegend: true
            });
        }
    });

    Plotly.newPlot(chart.element, traces, chart.layout);
}

document.addEventListener('DOMContentLoaded', function() {
    var socket = io();
    
    // Initialize Plotly charts
    lossChart = initPlotly('loss-chart', 'Training Progress - Loss', 'Epoch', 'Loss');
    accuracyChart = initPlotly('accuracy-chart', 'Training Progress - Accuracy', 'Epoch', 'Accuracy (%)');
    
    // Initialize empty plots
    updatePlot(lossChart, []);
    updatePlot(accuracyChart, []);
    
    socket.on('training_update', function(data) {
        document.getElementById('training-status').innerHTML = `
            Run ${currentRunId} - Epoch ${data.epoch}: Batch ${data.batch}/${data.total_batches}<br>
            Loss: ${data.loss.toFixed(4)}<br>
            Accuracy: ${data.accuracy.toFixed(2)}%
        `;
    });
    
    socket.on('epoch_complete', function(data) {
        // Remove epoch-wise updates to results div
        // Just update the current run data
        let currentRun = runHistory.find(run => run.id === currentRunId);
        if (!currentRun) {
            currentRun = {
                id: currentRunId,
                epochs: [],
                trainLoss: [],
                testLoss: [],
                testAcc: [],
                hyperparameters: getCurrentHyperparameters()
            };
            runHistory.push(currentRun);
        }
        
        currentRun.epochs.push(data.epoch);
        currentRun.trainLoss.push(data.train_loss);
        currentRun.testLoss.push(data.test_loss);
        currentRun.testAcc.push(data.test_accuracy);
        
        // Update plots with all runs
        updatePlot(lossChart, runHistory);
        updatePlot(accuracyChart, runHistory);
        
        // Update run comparison table
        if (data.epoch === parseInt(currentRun.hyperparameters.epochs)) {
            updateRunComparisonTable();
        }
    });
    
    document.getElementById('training-form').onsubmit = async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        try {
            // Increment run counter for new run
            currentRunId++;
            
            document.getElementById('training-status').innerHTML = `Starting Run ${currentRunId}...`;
            
            const response = await fetch('/train', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('training-status').innerHTML = 'Error starting training: ' + error.message;
        }
    };
    
    // Add clear runs button handler
    document.getElementById('clear-runs').onclick = function() {
        runHistory = [];
        currentRunId = 0;
        document.getElementById('results').innerHTML = '';
        document.getElementById('run-comparison').innerHTML = '';
        updatePlot(lossChart, []);
        updatePlot(accuracyChart, []);
    };
});

function getCurrentHyperparameters() {
    return {
        epochs: document.getElementById('epochs').value,
        batchSize: document.getElementById('batch_size').value,
        learningRate: document.getElementById('learning_rate').value,
        optimizer: document.getElementById('optimizer').value,
        channels: [
            1,
            document.getElementById('channel_1').value,
            document.getElementById('channel_2').value,
            document.getElementById('channel_3').value
        ]
    };
}

function updateRunComparisonTable() {
    const table = document.getElementById('run-comparison');
    let html = `
        <h3>Run Comparison</h3>
        <table>
            <thead>
                <tr>
                    <th>Run</th>
                    <th>Best Accuracy</th>
                    <th>Learning Rate</th>
                    <th>Batch Size</th>
                    <th>Optimizer</th>
                    <th>Channels</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    runHistory.forEach(run => {
        const bestAcc = Math.max(...run.testAcc);
        html += `
            <tr style="border-left: 3px solid ${colors[run.id % colors.length]}">
                <td>${run.id}</td>
                <td>${bestAcc.toFixed(2)}%</td>
                <td>${run.hyperparameters.learningRate}</td>
                <td>${run.hyperparameters.batchSize}</td>
                <td>${run.hyperparameters.optimizer}</td>
                <td>${run.hyperparameters.channels.join(', ')}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    table.innerHTML = html;
}
