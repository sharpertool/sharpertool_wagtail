/* Loading Script */
$(window).load(function() {
    "use strict";
    $(".loader").delay(500).fadeOut();
    $("#mask").delay(1000).fadeOut("slow");
});

/* Flexslider */
$(window).load(function() {
    "use strict";
    $('.flexslider').flexslider({
        animation: "fade",
        start: function(slider) {
            $('.np-controls a.next').click(function(event) {
                event.preventDefault();
                slider.flexAnimate(slider.getTarget("next"));
            });
            $('.np-controls a.previous').click(function(event) {
                event.preventDefault();
                slider.flexAnimate(slider.getTarget("previous"));
            });
        }
    });
});

/* Mixitup Portfolio */
jQuery(document).ready(function($) {
    "use strict";
    $('#portfolio').mixitup({
        targetSelector: '.item',
        transitionSpeed: 450
    });
});

/* Nivo - Lightbox */
jQuery(document).ready(function($) {
    "use strict";
    $('.nivo-lbox').nivoLightbox({effect: 'fade'});
});

/* Skills */
jQuery(document).ready(function($) {
    "use strict";
    $('.skills-info').appear(function() {
            $('.skill-bar', $(this)).each(function(index) {
                var barpct = $(this).data('pct');
                console.log(`Skill item ${index} has percent value of ${barpct}`)
                $(this).css('width', barpct);
            });
        }, {accX: 0, accY: -150}
    );
});


