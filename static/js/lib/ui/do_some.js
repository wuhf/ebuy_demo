/**
 * Created by allen on 16/8/26.
 */
    $("#slider").responsiveSlides({
        auto: true,
        speed: 500,
        namespace: "callbacks",
        pager: true
    });
    $(document).ready(function(){
        $(".memenu").memenu();
    });
    addEventListener("load", function() { setTimeout(hideURLbar, 0); }, false);
    function hideURLbar(){ window.scrollTo(0,1); }
