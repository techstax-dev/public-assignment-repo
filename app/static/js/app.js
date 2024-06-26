async function fetchEvents() {
    const response = await fetch('/webhook/events');
    const events = await response.json();
    const container = document.getElementById('events-container');
    container.innerHTML = '';

    events.forEach(event => {
        const eventElement = document.createElement('div');
        eventElement.classList.add('event');
        eventElement.textContent = formatEvent(event);
        container.appendChild(eventElement);
    });
}

function formatEvent(event) {
    const timestamp = new Date(event.timestamp).toLocaleString();
    if (event.event === 'push') {
        return `${event.author} pushed to ${event.to_branch} on ${timestamp}`;
    } else if (event.event === 'pull_request') {
        return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${timestamp}`;
    } else if (event.event === 'merge') {
        return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${timestamp}`;
    }
}

setInterval(fetchEvents, 15000);
fetchEvents(); 
