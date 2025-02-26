document.addEventListener('DOMContentLoaded', function() {
    // Navbar
    function toggleNavbar() {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            if (window.innerWidth > 991) {
                if (window.scrollY >= 30) {
                    navbar.classList.add('navbar-scroll');
                } else {
                    navbar.classList.remove('navbar-scroll');
                }
            } else {
                navbar.classList.remove('navbar-scroll');
            }
        }
    }
    toggleNavbar({disable: 'mobile', disable: 'tablet'});
    window.addEventListener('scroll', toggleNavbar);
    window.addEventListener('resize', toggleNavbar);


    // AOS
    AOS.init({
        disable: function() {
            return window.innerWidth < 992;
        }
    });

    // GSAP
    gsap.registerPlugin(ScrollTrigger, TextPlugin);

    function animateTextElements(){
        const TextTitlesChartElements = document.querySelectorAll('.titles-header');
        const TextSubTitlesChartElements = document.querySelectorAll('.sub-titles-header');
        if (window.innerWidth > 991) {

            TextTitlesChartElements.forEach(element => {
                element.classList.add('animations-text-1');
            });
            
            TextSubTitlesChartElements.forEach(element => {
                element.classList.add('animations-text-2');
            });

        } else {

            TextTitlesChartElements.forEach(element => {
                element.classList.remove('animations-text-1');
            });
            
            TextSubTitlesChartElements.forEach(element => {
                element.classList.remove('animations-text-2');
            });
        }
    }
    animateTextElements();
    window.addEventListener('resize', animateTextElements);

    if (document.querySelector('.animations-text-1')) {
        let staggerAmount = 0.05,
            translateXValue = 20,
            delayValue = 0.5,
            easeType = "power2.out",
            animatedTextElements = document.querySelectorAll('.animations-text-1');

        animatedTextElements.forEach((element) => {
            element.style.opacity = '1';
            
            let animationSplitText = new SplitText(element, { 
                type: "chars, words"
            });

            gsap.from(animationSplitText.chars, {
                duration: 1,
                delay: delayValue,
                x: translateXValue,
                autoAlpha: 0,
                stagger: staggerAmount,
                ease: easeType,
                scrollTrigger: {
                    trigger: element,
                    start: "top 85%",
                    toggleActions: "play none none reverse",
                }
            });
        });
    }

    if (document.querySelector('.animations-text-2')) {
        const animatedTextElements = document.querySelectorAll('.animations-text-2');

        animatedTextElements.forEach((element) => {
            // Reset si es necesario
            if (element.animation) {
                element.animation.progress(1).kill();
                element.split.revert();
            }

            element.split = new SplitText(element, {
                type: "lines,words,chars",
                linesClass: "split-line"
            });

            gsap.set(element, { 
                perspective: 400 
            });

            gsap.set(element.split.chars, {
                opacity: 0,
                x: "50"
            });

            element.animation = gsap.to(element.split.chars, {
                scrollTrigger: { 
                    trigger: element,
                    start: "top 90%" 
                },
                x: "0",
                y: "0",
                rotateX: "0",
                opacity: 1,
                duration: 1,
                ease: "back.out",
                stagger: 0.02
            });
        });
    }
});