var typing=new Typed(".typingAnimation", {
    strings: ["", "Vigour", "",  "Victory", "",  "Valour"],
    typeSpeed: 50,
    backSpeed: 40,
    loop: true,
});


gsap.registerPlugin(ScrollTrigger);
gsap.from(
    '.bottom-left-section',
    {
        scrollTrigger: {
            trigger: '.bottom-left-section',
            start: 'top center',
            // markers: true
        },
        duration: 1,
        width: 0,

    }
)

gsap.from(
    '.bottom-right-section',
    {
        scrollTrigger: {
            trigger: '.bottom-right-section',
            start: 'top center',
            // markers: true
        },
 
        duration: 1,
        width: 0
    }
)

gsap.from(
    '.right-section-content',
    {
        scrollTrigger: {
            trigger: '.right-section-content',
            start: 'center center',
            // markers: true
        },
        stagger: true,
        opacity: 0,
        delay: 1,
        y: -30,
        duration: 1
    }
)
