// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add animation class to elements when they come into view
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.animate-on-scroll');
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementBottom = element.getBoundingClientRect().bottom;
        const isVisible = (elementTop < window.innerHeight) && (elementBottom >= 0);
        
        if (isVisible) {
            element.classList.add('animate-fade-in');
        }
    });
};

window.addEventListener('scroll', animateOnScroll);
window.addEventListener('load', animateOnScroll);

// Product image gallery
const productGalleries = document.querySelectorAll('.product-gallery');
productGalleries.forEach(gallery => {
    const mainImage = gallery.querySelector('.main-image');
    const thumbnails = gallery.querySelectorAll('.thumbnail');
    
    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', () => {
            mainImage.src = thumb.src;
            thumbnails.forEach(t => t.classList.remove('active'));
            thumb.classList.add('active');
        });
    });
});

// Size selection
const sizeButtons = document.querySelectorAll('.size-button');
sizeButtons.forEach(button => {
    button.addEventListener('click', () => {
        sizeButtons.forEach(b => b.classList.remove('active'));
        button.classList.add('active');
    });
});

// Color selection
const colorButtons = document.querySelectorAll('.color-button');
colorButtons.forEach(button => {
    button.addEventListener('click', () => {
        colorButtons.forEach(b => b.classList.remove('active'));
        button.classList.add('active');
    });
});

// Quantity input
const quantityInputs = document.querySelectorAll('.quantity-input');
quantityInputs.forEach(input => {
    const minusBtn = input.parentElement.querySelector('.minus-btn');
    const plusBtn = input.parentElement.querySelector('.plus-btn');
    
    minusBtn.addEventListener('click', () => {
        const currentValue = parseInt(input.value);
        if (currentValue > 1) {
            input.value = currentValue - 1;
        }
    });
    
    plusBtn.addEventListener('click', () => {
        const currentValue = parseInt(input.value);
        input.value = currentValue + 1;
    });
});

// Add to cart animation
const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
addToCartButtons.forEach(button => {
    button.addEventListener('click', () => {
        button.classList.add('added');
        setTimeout(() => {
            button.classList.remove('added');
        }, 2000);
    });
});

// Newsletter form submission
const newsletterForm = document.querySelector('.newsletter-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = newsletterForm.querySelector('input[type="email"]').value;
        // Add your newsletter subscription logic here
        alert('Thank you for subscribing to our newsletter!');
        newsletterForm.reset();
    });
}

// Mobile menu toggle
const mobileMenuToggle = document.querySelector('.navbar-toggler');
const mobileMenu = document.querySelector('.navbar-collapse');

if (mobileMenuToggle && mobileMenu) {
    mobileMenuToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('show');
    });
}

// Search functionality
const searchForm = document.querySelector('.search-form');
if (searchForm) {
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const searchQuery = searchForm.querySelector('input[type="search"]').value;
        // Add your search logic here
        window.location.href = `/search/?q=${encodeURIComponent(searchQuery)}`;
    });
}

// Cart badge update
const updateCartBadge = (count) => {
    const cartBadge = document.querySelector('.cart-badge');
    if (cartBadge) {
        if (count > 0) {
            cartBadge.textContent = count;
            cartBadge.style.display = 'block';
        } else {
            cartBadge.style.display = 'none';
        }
    }
};

// Initialize tooltips
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
}); 