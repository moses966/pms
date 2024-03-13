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
                    backgroundColor: ["#435ebe",]
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

document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM loaded');

    const currentYear = new Date().getFullYear();
    const year = currentYear;

    console.log('Fetching data for year:', year);

    fetch(`http://localhost:8000/apis/guests/gender/?year=${year}`)
        .then(response => response.json())
        .then(data => {
            console.log('Data from API:', data);

            const maleGuestsCount = data.male_guests_count;
            const femaleGuestsCount = data.female_guests_count;

            console.log('Male Guests Count:', maleGuestsCount);
            console.log('Female Guests Count:', femaleGuestsCount);

            // Get canvas element
            const canvas = document.getElementById('genderPieChart');
            const ctx = canvas.getContext('2d');

            // Create pie chart
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Male', 'Female'],
                    datasets: [{
                        data: [maleGuestsCount, femaleGuestsCount],
                        backgroundColor: ["#435ebe", "#55c6e8"]
                    }]
                },
                options: {
                    responsive: false,
                    maintainAspectRatio: false
                }
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});
