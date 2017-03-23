/**
 * Created by allen on 16/9/8.
 */
require(['jquery','swiper','commonobj','zone'],function($,swiper,commonObj,diqu){
    $(function(){
        if($("select[name='sheng']").length>0){
            new PCAS("sheng","shi","qu","","","");
        }
    })
})