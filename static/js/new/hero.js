gsap.to('.overlay-svg',
{
    y: -100,
    opacity: 0,
    delay: 3.5,
    duration: 1
})

gsap.to('.overlay-theme',
{
    y: -100,
    opacity: 0,
    delay: 3.8,
    duration: 1.1
})

gsap.to('.overlay',
{
    height: 0,
    delay: 5,
    duration: .5
})

gsap.from('.left-hero-section-1',
{
    opacity: 0,
    height: 0,
    duration: 0.5,
    delay: 5
})

gsap.from('.right-hero .dates',
{
    x: 100,
    duration: 1
})

gsap.from('.left-hero ul li',
{
    opacity: 0,
    stagger: 0.5,
    duration: 1,
    delay: 5.5, 
    x: -50
})

gsap.from('.left-hero-bottom',
{
    y: 100,
    opacity: 0,
    duration: 1.5
})