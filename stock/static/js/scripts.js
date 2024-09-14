// scripts.js
$(document).ready(function() {
    // Toggle Theme
    $('#theme-toggle').click(function() {
        $('body').toggleClass('dark-theme');
    });

    // Fetch and display live stock data
    function fetchLiveStocks() {
        $.ajax({
            url: '/api/live_stocks/', // Your API endpoint
            method: 'GET',
            success: function(data) {
                $('#live-stocks').html('');
                data.forEach(function(stock) {
                    $('#live-stocks').append(`
                        <div class="card mb-2">
                            <div class="card-body">
                                <h5 class="card-title">${stock.name}</h5>
                                <p class="card-text">Price: ${stock.price}</p>
                            </div>
                        </div>
                    `);
                });
            }
        });
    }

    // Fetch live stocks every 5 seconds
    setInterval(fetchLiveStocks, 5000);
    fetchLiveStocks();

    // Handle comparison form submission
    $('#compare-form').submit(function(e) {
        e.preventDefault();
        let stock1 = $('select[name="stock1"]').val();
        let stock2 = $('select[name="stock2"]').val();

        $.ajax({
            url: `/api/compare_stocks/?stock1=${stock1}&stock2=${stock2}`,
            method: 'GET',
            success: function(data) {
                renderComparisonChart(data);
            }
        });
    });

    // Render comparison chart
    function renderComparisonChart(data) {
        var ctx = document.getElementById('comparison-chart').getContext('2d');
        var chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.dates,
                datasets: [{
                    label: data.stock1.name,
                    data: data.stock1.prices,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                },
                {
                    label: data.stock2.name,
                    data: data.stock2.prices,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });
    }
});
