// Hero button scroll
document.querySelector('.hero-button').addEventListener('click', () => {
    document.querySelector('#menu').scrollIntoView({ behavior: 'smooth' });
});

// Contact form submission
document.querySelector('#contact-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    if (formData.get('name') && formData.get('email') && formData.get('phone') && formData.get('message')) {
        // For demo purposes, just log the data
        console.log(Object.fromEntries(formData.entries()));
        alert('Form submitted successfully!');
        e.target.reset();
        document.querySelector('#error-message').innerText = '';
    } else {
        document.querySelector('#error-message').innerText = 'Please fill out all the fields.';
    }
});
