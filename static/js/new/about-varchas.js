var rule = CSSRulePlugin.getRule('.about-varchas .left-section h1::after')


gsap.from('.about-varchas .left-section',
{
    scrollTrigger:{
        target: '.about-varchas .left-section',
        start: "top center"
        
    },
    y: 50,
    opacity: 0,
    duration: 1.4
})

gsap.from('.about-varchas .right-section img',
{
    scrollTrigger:{
        target: '.about-varchas .right-section img',
        start: 'top center'
    },
    x: -100,
    opacity: 0,
    duration: 1.4
})

gsap.to(rule,

    {
        cssRule: {
            scaleY: 0
        },
        scrollTrigger:{
            target: '.about-varchas .left-section',
            start: "top center"
            
        },
        duration: 1.5
    })