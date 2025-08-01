document.addEventListener('DOMContentLoaded', () => {
    // --- Fonction pour récupérer un cookie ---
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // --- Affichage ou non du lien login ---
    function checkAuthentication() {
        const token = getCookie('token');
        const loginLink = document.getElementById('login-link');

        if (!token) {
            if (loginLink) loginLink.style.display = 'block';
        } else {
            if (loginLink) loginLink.style.display = 'none';
            fetchPlaces(token);
        }
    }

    // --- Récupération des places depuis l'API ---
    async function fetchPlaces(token) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const places = await response.json();
                displayPlaces(places);
            } else {
                console.error('Erreur lors de la récupération des places');
            }
        } catch (error) {
            console.error('Erreur réseau', error);
        }
    }

    // --- Affichage des places dans la page ---
    function displayPlaces(places) {
        const placesList = document.getElementById('places-list');
        if (!placesList) return;
        placesList.innerHTML = '';

        places.forEach(place => {
            const div = document.createElement('div');
            div.classList.add('place');
            div.dataset.price = place.price_by_night;

            div.innerHTML = `
                <h3>${place.name}</h3>
                <p>${place.description}</p>
                <p><strong>Price:</strong> $${place.price_by_night}</p>
                <p><strong>Location:</strong> ${place.city}, ${place.state}</p>
            `;
            placesList.appendChild(div);
        });
    }

    // --- Filtre sur le prix ---
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            const places = document.querySelectorAll('#places-list .place');

            places.forEach(place => {
                const price = Number(place.dataset.price);
                if (selectedPrice === 'All' || price <= Number(selectedPrice)) {
                    place.style.display = 'block';
                } else {
                    place.style.display = 'none';
                }
            });
        });
    }

    // --- Gestion du formulaire de login ---
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('http://localhost:5000/api/v1/users/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    const error = await response.json();
                    alert('Échec de la connexion : ' + (error.error || error.message || 'Identifiants invalides'));
                }
            } catch (err) {
                alert('Erreur réseau. Vérifie que ton serveur est lancé.');
                console.error(err);
            }
        });
    } else {
        // Si pas de formulaire login, on check l'auth et on affiche les places
        checkAuthentication();
    }

    // --- Détail d'une place (page détail) ---
    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('place_id');
    }

    function checkAuthenticationForDetails(placeId) {
        const token = getCookie('token');
        const addReviewSection = document.getElementById('add-review');

        if (addReviewSection) {
            if (!token) {
                addReviewSection.style.display = 'none';
                fetchPlaceDetails(null, placeId);
            } else {
                addReviewSection.style.display = 'block';
                fetchPlaceDetails(token, placeId);
            }
        } else {
            fetchPlaceDetails(token, placeId);
        }
    }

    async function fetchPlaceDetails(token, placeId) {
        try {
            const headers = {};
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
                method: 'GET',
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Impossible de récupérer les détails du lieu');
            }

            const place = await response.json();
            displayPlaceDetails(place);
        } catch (error) {
            alert(error.message);
            console.error(error);
        }
    }

    function displayPlaceDetails(place) {
        const placeDetails = document.getElementById('place-details');
        if (!placeDetails) return;
        placeDetails.innerHTML = '';  // vide le contenu avant de remplir

        // Création des éléments
        const title = document.createElement('h2');
        title.textContent = place.name;

        const description = document.createElement('p');
        description.textContent = place.description;

        const price = document.createElement('p');
        price.textContent = `Price: $${place.price_by_night}`;

        // Amenities
        const amenitiesTitle = document.createElement('h3');
        amenitiesTitle.textContent = 'Amenities:';
        const amenitiesList = document.createElement('ul');
        if (place.amenities) {
            place.amenities.forEach(am => {
                const li = document.createElement('li');
                li.textContent = am.name;
                amenitiesList.appendChild(li);
            });
        }

        // Reviews
        const reviewsTitle = document.createElement('h3');
        reviewsTitle.textContent = 'Reviews:';
        const reviewsList = document.createElement('ul');
        if (place.reviews) {
            place.reviews.forEach(rv => {
                const li = document.createElement('li');
                li.textContent = `${rv.user.first_name} ${rv.user.last_name}: ${rv.text}`;
                reviewsList.appendChild(li);
            });
        }

        // Ajout au DOM
        placeDetails.appendChild(title);
        placeDetails.appendChild(description);
        placeDetails.appendChild(price);
        placeDetails.appendChild(amenitiesTitle);
        placeDetails.appendChild(amenitiesList);
        placeDetails.appendChild(reviewsTitle);
        placeDetails.appendChild(reviewsList);
    }

    // Si on est sur la page détail, on initialise la récupération des détails
    if (document.getElementById('place-details')) {
        const placeId = getPlaceIdFromURL();
        if (!placeId) {
            alert('Aucun identifiant de lieu fourni dans l’URL');
        } else {
            checkAuthenticationForDetails(placeId);
        }
    }

    // --- Gestion du formulaire d'ajout de review (si présent) ---
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review-text').value.trim();
            if (!reviewText) {
                alert('Please enter a review.');
                return;
            }

            const token = getCookie('token');
            const placeId = getPlaceIdFromURL();
            if (!token) {
                alert('You must be logged in to submit a review.');
                return;
            }
            if (!placeId) {
                alert('Place ID not found in URL');
                return;
            }

            try {
                const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ text: reviewText })
                });

                if (response.ok) {
                    alert('Review submitted successfully!');
                    reviewForm.reset();
                } else {
                    const errorData = await response.json();
                    alert('Failed to submit review: ' + (errorData.error || 'Unknown error'));
                }
            } catch (err) {
                alert('Network error, please try again later.');
                console.error(err);
            }
        });
    }
});
