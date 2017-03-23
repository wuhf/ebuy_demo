/**
 * Created by allen on 16/8/26.
 */
require(["jquery", "bsAlert", "csrfToken"], function ($, bsAlert, csrfTokenHeader) {
    $('.item_add').click(function (e) {
        e.preventDefault();
        var product_id = parseInt($(this).attr('data_id'));
        $.ajax({
                beforeSend: csrfTokenHeader,
                url: "/add_to_cart/",
                data: {
                    product_id:product_id,
                },
                dataType: "json",
                method: "post",
                success: function (data) {
                    if (!data.code) {
                       bsAlert('成功添加进购物车!');
                    }
                    else {
                        bsAlert(data.data);
                    }
                },
                error: function(){
                    bsAlert("额 好像出错了，请刷新页面重试。如还有问题，请填写页面导航栏上的反馈。")
                }
            });
    })
});