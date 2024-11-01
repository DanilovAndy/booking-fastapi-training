async function successfulBooking(roomId, dateFrom, dateTo) {
    const url = "/api/bookings";
    await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({room_id: {room_id: roomId}, booking_dates: {date_from: dateFrom, date_to: dateTo}}),
    }).then(response => {
        if (response.status === 201) {
            window.location.href = "/bookings"
        }
    });
}


async function deleteBooking(bookingId) {
    const url = "/api/bookings?booking_id=" + bookingId;
    await fetch(url, {
        method: 'DELETE',
    }).then(response => {
        if (response.status === 204) {
            window.location.href = "/bookings"
        }
    });
}