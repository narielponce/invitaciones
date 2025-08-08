document.addEventListener('DOMContentLoaded', function () {
    // Font loading fallback
    function checkFontsLoaded() {
        const testElement = document.createElement('div');
        testElement.style.fontFamily = 'Comic Neue, Comic Sans MS, cursive';
        testElement.style.fontSize = '16px';
        testElement.style.position = 'absolute';
        testElement.style.visibility = 'hidden';
        testElement.innerHTML = 'Test';
        document.body.appendChild(testElement);
        
        // If fonts don't load properly, add fallback class
        setTimeout(() => {
            if (testElement.offsetWidth < 50) {
                document.body.classList.add('fonts-fallback');
            }
            document.body.removeChild(testElement);
        }, 100);
    }
    
    checkFontsLoaded();

    // Loading screen with fun animation
    const loadingScreen = document.getElementById('loading-screen');
    setTimeout(() => {
        loadingScreen.classList.add('fade-out');
        setTimeout(() => {
            loadingScreen.style.display = 'none';
        }, 500);
    }, 2000); // Longer loading for kids to enjoy the animation

    // Enhanced countdown functionality with fun animations
    const countdownElement = document.getElementById('countdown');
    const eventDateString = countdownElement.dataset.eventDate;

    if (eventDateString) {
        const eventDate = new Date(eventDateString);
        const daysEl = document.getElementById('days');
        const hoursEl = document.getElementById('hours');
        const minutesEl = document.getElementById('minutes');
        const secondsEl = document.getElementById('seconds');

        function updateCountdown() {
            const now = new Date();
            const distance = eventDate.getTime() - now.getTime();

            if (distance < 0) {
                clearInterval(countdownInterval);
                daysEl.innerHTML = '0';
                hoursEl.innerHTML = '0';
                minutesEl.innerHTML = '0';
                secondsEl.innerHTML = '0';
                
                // Show party time message
                const countdownContainer = document.querySelector('.countdown-container-kids');
                countdownContainer.innerHTML = '<div class="party-time-message"><h2>¡ES HORA DE LA FIESTA! 🎉</h2></div>';
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // Animate number changes with bounce effect
            animateNumberKids(daysEl, days);
            animateNumberKids(hoursEl, hours);
            animateNumberKids(minutesEl, minutes);
            animateNumberKids(secondsEl, seconds);
        }

        function animateNumberKids(element, newValue) {
            if (element.innerHTML !== newValue.toString()) {
                element.style.transform = 'scale(1.3) rotate(5deg)';
                element.style.color = '#ff69b4';
                setTimeout(() => {
                    element.innerHTML = newValue;
                    element.style.transform = 'scale(1) rotate(0deg)';
                    element.style.color = '';
                }, 200);
            }
        }

        updateCountdown();
        const countdownInterval = setInterval(updateCountdown, 1000);
    }

    // Enhanced smooth scroll with bounce effect
    const scrollBtn = document.getElementById("scroll-down-btn");
    const target = document.getElementById("cuenta-regresiva");

    if (scrollBtn && target) {
        scrollBtn.addEventListener("click", function () {
            // Add fun click animation
            scrollBtn.style.transform = 'translateX(-50%) scale(1.2)';
            setTimeout(() => {
                scrollBtn.style.transform = 'translateX(-50%) scale(1)';
            }, 200);
            
            target.scrollIntoView({ behavior: "smooth" });
        });
    }

    // Enhanced modal functionality with kids-friendly animations
    const modal = document.getElementById('gift-modal');
    const openBtn = document.getElementById('gift-modal-btn');
    const closeBtn = document.getElementById('close-gift-modal');
    const modalBg = modal ? modal.querySelector('.modal-background') : null;

    if (openBtn && modal) {
        openBtn.addEventListener('click', function () {
            modal.classList.add('is-active');
            document.body.style.overflow = 'hidden';
            
            // Add entrance animation
            const modalCard = modal.querySelector('.modal-card-kids');
            if (modalCard) {
                modalCard.style.transform = 'scale(0.5) rotate(10deg)';
                modalCard.style.opacity = '0';
                
                setTimeout(() => {
                    modalCard.style.transform = 'scale(1) rotate(0deg)';
                    modalCard.style.opacity = '1';
                    modalCard.style.transition = 'all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                }, 50);
            }
        });
    }

    function closeModal() {
        if (modal) {
            const modalCard = modal.querySelector('.modal-card-kids');
            if (modalCard) {
                modalCard.style.transform = 'scale(0.5) rotate(-10deg)';
                modalCard.style.opacity = '0';
                
                setTimeout(() => {
                    modal.classList.remove('is-active');
                    document.body.style.overflow = 'auto';
                }, 300);
            }
        }
    }

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (modalBg) modalBg.addEventListener('click', closeModal);

    // Enhanced gallery lightbox with kids animations
    const galleryImages = document.querySelectorAll('.gallery-item-kids');
    const lightboxModal = document.getElementById('lightbox-modal');
    const lightboxImage = document.getElementById('lightbox-image');
    const lightboxClose = document.getElementById('lightbox-close');
    const lightboxPrev = document.getElementById('lightbox-prev');
    const lightboxNext = document.getElementById('lightbox-next');
    const lightboxCurrent = document.getElementById('lightbox-current');
    const lightboxTotal = document.getElementById('lightbox-total');
    
    let currentImageIndex = 0;
    const imageUrls = Array.from(galleryImages).map(item => 
        item.querySelector('.gallery-image-kids').src
    );

    if (lightboxTotal) lightboxTotal.textContent = imageUrls.length;

    galleryImages.forEach((item, index) => {
        item.addEventListener('click', () => {
            currentImageIndex = index;
            showLightbox();
            
            // Add click animation
            item.style.transform = 'scale(0.95)';
            setTimeout(() => {
                item.style.transform = '';
            }, 150);
        });
    });

    function showLightbox() {
        if (lightboxImage && lightboxModal && lightboxCurrent) {
            lightboxImage.src = imageUrls[currentImageIndex];
            lightboxCurrent.textContent = currentImageIndex + 1;
            lightboxModal.classList.add('is-active');
            document.body.style.overflow = 'hidden';
            
            // Add entrance animation
            const lightboxContent = lightboxModal.querySelector('.lightbox-content-kids');
            if (lightboxContent) {
                lightboxContent.style.transform = 'scale(0.8)';
                lightboxContent.style.opacity = '0';
                
                setTimeout(() => {
                    lightboxContent.style.transform = 'scale(1)';
                    lightboxContent.style.opacity = '1';
                    lightboxContent.style.transition = 'all 0.3s ease-out';
                }, 50);
            }
        }
    }

    function closeLightbox() {
        if (lightboxModal) {
            const lightboxContent = lightboxModal.querySelector('.lightbox-content-kids');
            if (lightboxContent) {
                lightboxContent.style.transform = 'scale(0.8)';
                lightboxContent.style.opacity = '0';
                
                setTimeout(() => {
                    lightboxModal.classList.remove('is-active');
                    document.body.style.overflow = 'auto';
                }, 300);
            }
        }
    }

    if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
    if (lightboxModal) {
        const modalBg = lightboxModal.querySelector('.modal-background');
        if (modalBg) modalBg.addEventListener('click', closeLightbox);
    }

    if (lightboxPrev) {
        lightboxPrev.addEventListener('click', () => {
            currentImageIndex = (currentImageIndex - 1 + imageUrls.length) % imageUrls.length;
            showLightbox();
            
            // Add navigation animation
            lightboxPrev.style.transform = 'translateY(-50%) scale(1.2)';
            setTimeout(() => {
                lightboxPrev.style.transform = 'translateY(-50%) scale(1)';
            }, 150);
        });
    }

    if (lightboxNext) {
        lightboxNext.addEventListener('click', () => {
            currentImageIndex = (currentImageIndex + 1) % imageUrls.length;
            showLightbox();
            
            // Add navigation animation
            lightboxNext.style.transform = 'translateY(-50%) scale(1.2)';
            setTimeout(() => {
                lightboxNext.style.transform = 'translateY(-50%) scale(1)';
            }, 150);
        });
    }

    // Keyboard navigation for lightbox
    document.addEventListener('keydown', (e) => {
        if (lightboxModal && lightboxModal.classList.contains('is-active')) {
            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowLeft' && lightboxPrev) lightboxPrev.click();
            if (e.key === 'ArrowRight' && lightboxNext) lightboxNext.click();
        }
    });

    // Enhanced form interactions with kids-friendly feedback
    const inputs = document.querySelectorAll('.input-kids, .textarea-kids, .select-kids');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            if (this.parentElement) {
                this.parentElement.style.transform = 'translateY(-2px)';
            }
            this.style.borderColor = '#ff69b4';
            
            // Add sparkle effect
            createSparkles(this);
        });
        
        input.addEventListener('blur', function() {
            if (this.parentElement) {
                this.parentElement.style.transform = '';
            }
            this.style.borderColor = '';
        });
        
        // Add typing animation for inputs
        input.addEventListener('input', function() {
            this.style.transform = 'scale(1.02)';
            setTimeout(() => {
                this.style.transform = '';
            }, 100);
        });
    });

    // Fun sparkle effect for form interactions
    function createSparkles(element) {
        const rect = element.getBoundingClientRect();
        const sparkle = document.createElement('div');
        sparkle.innerHTML = '✨';
        sparkle.style.position = 'fixed';
        sparkle.style.left = rect.right - 20 + 'px';
        sparkle.style.top = rect.top + 10 + 'px';
        sparkle.style.fontSize = '1.5rem';
        sparkle.style.pointerEvents = 'none';
        sparkle.style.zIndex = '1000';
        sparkle.style.animation = 'sparkle 1s ease-out forwards';
        
        document.body.appendChild(sparkle);
        
        setTimeout(() => {
            if (sparkle.parentNode) {
                sparkle.remove();
            }
        }, 1000);
    }

    // Add sparkle animation to CSS dynamically
    const sparkleStyle = document.createElement('style');
    sparkleStyle.textContent = `
        @keyframes sparkle {
            0% { opacity: 1; transform: scale(0) rotate(0deg); }
            50% { opacity: 1; transform: scale(1) rotate(180deg); }
            100% { opacity: 0; transform: scale(0) rotate(360deg); }
        }
    `;
    document.head.appendChild(sparkleStyle);

    // Button click animations
    const buttons = document.querySelectorAll('.button-kids');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('div');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            ripple.style.pointerEvents = 'none';
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => {
                if (ripple.parentNode) {
                    ripple.remove();
                }
            }, 600);
        });
    });

    // Add ripple animation to CSS dynamically
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes ripple {
            to { transform: scale(4); opacity: 0; }
        }
    `;
    document.head.appendChild(rippleStyle);

    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                entry.target.style.transition = 'all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                
                // Add stagger effect for multiple elements
                const delay = Array.from(entry.target.parentElement.children).indexOf(entry.target) * 100;
                entry.target.style.transitionDelay = delay + 'ms';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.gallery-item-kids, .time-block-kids, .detail-row-kids, .info-card-kids').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        observer.observe(el);
    });

    // Fun hover effects for interactive elements
    const interactiveElements = document.querySelectorAll('.time-card-kids, .gallery-card-kids, .detail-row-kids');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.05)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });

    // Add confetti effect for special interactions
    function createConfetti() {
        const colors = ['#ff69b4', '#8a2be2', '#4169e1', '#32cd32', '#ffd700', '#ff8c00'];
        const confettiCount = 50;
        
        for (let i = 0; i < confettiCount; i++) {
            const confetti = document.createElement('div');
            confetti.style.position = 'fixed';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.top = '-10px';
            confetti.style.width = '10px';
            confetti.style.height = '10px';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.pointerEvents = 'none';
            confetti.style.zIndex = '1000';
            confetti.style.animation = `confetti-fall ${Math.random() * 3 + 2}s linear forwards`;
            
            document.body.appendChild(confetti);
            
            setTimeout(() => {
                if (confetti.parentNode) {
                    confetti.remove();
                }
            }, 5000);
        }
    }

    // Add confetti animation to CSS dynamically
    const confettiStyle = document.createElement('style');
    confettiStyle.textContent = `
        @keyframes confetti-fall {
            to {
                transform: translateY(100vh) rotate(720deg);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(confettiStyle);

    // Trigger confetti on form submission
    const forms = document.querySelectorAll('.form-kids');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            createConfetti();
        });
    });

    // Add party sound effects (optional - can be enabled)
    function playPartySound() {
        // This would play a fun sound effect
        // You can add actual audio files here
        console.log('🎉 Party sound effect!');
    }

    // Add sound to button clicks (optional)
    buttons.forEach(button => {
        button.addEventListener('click', playPartySound);
    });
});
