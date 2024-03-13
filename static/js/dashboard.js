document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:8000/apis/monthly-total/')
        .then(response => response.json())
        .then(data => {
            console.log('Data from API:', data); // Log data for debugging

            // Extract keys (month abbreviations) and values (total bookings)
            const responseData = data[0]; // Access the first object in the array
            const labels = Object.keys(responseData);
            const dataValues = Object.values(responseData);

            console.log('Labels:', labels); // Log labels for debugging
            console.log('Data Values:', dataValues); // Log data values for debugging

            const dataBookings = {
                labels: labels,
                datasets: [{
                    label: 'Total Bookings',
                    data: dataValues,
                    borderWidth: 1,
                    backgroundColor: 'rgb(75, 192, 192)',
                }]
            };

            const configBookings = {
                type: 'bar',
                data: dataBookings,
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                },
            };

            const chartElement = document.getElementById('monthlyBookingsChart');
            if (chartElement) {
                new Chart(
                    chartElement,
                    configBookings
                );
            } else {
                console.error('Failed to find chart element.');
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});
