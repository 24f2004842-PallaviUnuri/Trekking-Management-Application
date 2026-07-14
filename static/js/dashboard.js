// Bar Chart for monthly booking of current year : Admin Dashboard

const ch1 = document.getElementById("bookingChart");

new Chart(ch1, {
    type: "bar",

    data: {
        labels: months,

        datasets: [{
            label: "Bookings",
            data: monthlyBookings,

            backgroundColor: "#198754"
        }]
    },

    options: {
        responsive: true,

        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// chart to show booking status in admin dashboard

const ch2 = document.getElementById('statusChart');

new Chart(ch2, {
    type: "doughnut",
    data: {
        labels: statusLabels,

        datasets: [{
            data: statusCounts,
            backgroundColor: [
                "#0d6efd",
                "#dc3545",
                "#198754"

            ]
        }]
    },

    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

