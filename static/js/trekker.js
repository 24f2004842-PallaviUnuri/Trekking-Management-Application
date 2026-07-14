const ch1 = document.getElementById("trekBookingChart");

if (ch1) {
    new Chart(ctx, {
        type: "bar",

        data: {
            labels: months,

            datasets: [{
                label: "Treks Booked",
                data: monthlyBookings,
                backgroundColor: "#198754",
                borderRadius: 8
            }]
        },

        options: {

            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },

            scales: {

                y: {
                beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}